    
from .forms import AgentInterestRateForm
from django.conf import settings
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    DeleteView, DetailView, FormView, ListView, UpdateView)
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin
from django_tables2 import SingleTableView

from oscar.core.compat import get_user_model
from oscar.core.loading import get_class, get_classes, get_model
from oscar.views.generic import BulkEditMixin
from django.urls import reverse, reverse_lazy

from django.shortcuts import get_object_or_404

UserSearchForm, ProductAlertSearchForm, ProductAlertUpdateForm = get_classes(
    'dashboard.users.forms', ('UserSearchForm', 'ProductAlertSearchForm',
                              'ProductAlertUpdateForm'))
PasswordResetForm = get_class('customer.forms', 'PasswordResetForm')
UserTable = get_class('apps.user.dashboard.tables', 'UserTable')
ProductAlert = get_model('customer', 'ProductAlert')
User = get_user_model()

Account = get_model('oscar_accounts', 'Account')
Transfer = get_model('oscar_accounts', 'Transfer')
Transaction = get_model('oscar_accounts', 'Transaction')
Agents = get_model('user', 'AgentProfile')
InterestRate = get_model('user', 'AgentInterestRate')


class IndexView(BulkEditMixin, FormMixin, SingleTableView):
    template_name = 'agents/dashboard/index.html'
    table_pagination = True
    model = User
    actions = ('make_active', 'make_inactive', )
    form_class = UserSearchForm
    table_class = UserTable
    context_table_name = 'users'
    desc_template = _('%(main_filter)s %(email_filter)s %(name_filter)s')
    description = ''

    def dispatch(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        self.form = self.get_form(form_class)
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        """
        Only bind search form if it was submitted.
        """
        kwargs = super().get_form_kwargs()

        if 'search' in self.request.GET:
            kwargs.update({
                'data': self.request.GET,
            })

        return kwargs

    def get_queryset(self):
        queryset = self.model.objects.filter(is_agent=True).order_by('-date_joined')
        return self.apply_search(queryset)

    def apply_search(self, queryset):
        # Set initial queryset description, used for template context
        self.desc_ctx = {
            'main_filter': _('All agents'),
            'email_filter': '',
            'name_filter': '',
        }
        if self.form.is_valid():
            return self.apply_search_filters(queryset, self.form.cleaned_data)
        else:
            return queryset

    def apply_search_filters(self, queryset, data):
        """
        Function is split out to allow customisation with little boilerplate.
        """
        if data['email']:
            email = data['email']
            queryset = queryset.filter(email__istartswith=email)
            self.desc_ctx['email_filter'] \
                = _(" with email matching '%s'") % email
        if data['name']:
            # If the value is two words, then assume they are first name and
            # last name
            parts = data['name'].split()
            # always true filter
            condition = Q()
            for part in parts:
                condition &= Q(first_name__icontains=part) \
                    | Q(last_name__icontains=part)
            queryset = queryset.filter(condition).distinct()
            self.desc_ctx['name_filter'] \
                = _(" with name matching '%s'") % data['name']

        return queryset

    def get_table(self, **kwargs):
        table = super().get_table(**kwargs)
        table.caption = self.desc_template % self.desc_ctx
        return table

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        return context

    def make_inactive(self, request, users):
        return self._change_users_active_status(users, False)

    def make_active(self, request, users):
        return self._change_users_active_status(users, True)

    def _change_users_active_status(self, users, value):
        for user in users:
            if not user.is_superuser:
                user.is_agent = value
                user.save()
        messages.info(self.request, _("Agent's status successfully changed"))
        return redirect('agents_dashboard:agents-list')


class AgentDetailView(DetailView):
    template_name = 'agents/dashboard/detail.html'
    model = User
    context_object_name = 'customer'

    def get(self, request, *args, **kwargs):
        try:
            from apps.user.models import User
            self.requested_user = User.objects.get(id=kwargs['pk'])
            self.account = Account.objects.get(primary_user=self.requested_user) 
        except Account.DoesNotExist:
            self.account = None
        return super(AgentDetailView, self).get(
            request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(AgentDetailView, self).get_context_data(**kwargs)
        try:
            self.agent_profile = Agents.objects.get(user=self.requested_user)
        except Agents.DoesNotExist:
            self.agent_profile = None

        if self.agent_profile != None and self.agent_profile.name and self.agent_profile.email:
            ctx['agents'] = self.agent_profile

        if self.account != None:
            ctx['account'] = self.account
            ctx['transactions'] = self.account.transactions.all().order_by('-date_created')
        return ctx


def change_agent_status(self, request, *args, **kwargs):
    try:
        from apps.user.models import User
        requested_user = User.objects.get(id=kwargs['pk'])
        old_status = requested_user.is_agent
        requested_user.is_agent = not requested_user.is_agent
        requested_user.save()
    except User.DoesNotExist:
            requested_user = None

    if requested_user and old_status != requested_user.is_agent:
        messages.info(request, _("Agent's status successfully changed"))
        return redirect('agents_dashboard:agents-list')
    else:
        messages.info(self.request._request, _(
            "Agent's status couldn't change. Please try again."))
        return reverse(
            'agents_dashboard:agent-detail', kwargs={'pk': kwargs['pk']}
        )
        # return redirect('agents_dashboard:agent-detail')


class AgentRequestView(BulkEditMixin, FormMixin, SingleTableView):
    template_name = 'agents/dashboard/request_index.html'
    table_pagination = True
    model = User
    actions = ('make_active', 'make_inactive', )
    form_class = UserSearchForm
    table_class = UserTable
    context_table_name = 'users'
    desc_template = _('%(main_filter)s %(email_filter)s %(name_filter)s')
    description = ''

    def dispatch(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        self.form = self.get_form(form_class)
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        """
        Only bind search form if it was submitted.
        """
        kwargs = super().get_form_kwargs()

        if 'search' in self.request.GET:
            kwargs.update({
                'data': self.request.GET,
            })

        return kwargs

    def get_queryset(self):
        queryset = self.model.objects.filter(
            is_agent=False).order_by('-date_joined')
        return self.apply_search(queryset)

    def apply_search(self, queryset):
        # Set initial queryset description, used for template context
        self.desc_ctx = {
            'main_filter': _('All agent requests'),
            'email_filter': '',
            'name_filter': '',
        }
        if self.form.is_valid():
            return self.apply_search_filters(queryset, self.form.cleaned_data)
        else:
            return queryset

    def apply_search_filters(self, queryset, data):
        """
        Function is split out to allow customisation with little boilerplate.
        """
        if data['email']:
            email = data['email']
            queryset = queryset.filter(email__istartswith=email)
            self.desc_ctx['email_filter'] \
                = _(" with email matching '%s'") % email
        if data['name']:
            # If the value is two words, then assume they are first name and
            # last name
            parts = data['name'].split()
            # always true filter
            condition = Q()
            for part in parts:
                condition &= Q(first_name__icontains=part) \
                    | Q(last_name__icontains=part)
            queryset = queryset.filter(condition).distinct()
            self.desc_ctx['name_filter'] \
                = _(" with name matching '%s'") % data['name']

        return queryset

    def get_table(self, **kwargs):
        table = super().get_table(**kwargs)
        table.caption = self.desc_template % self.desc_ctx
        return table

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        return context

    def make_inactive(self, request, users):
        return self._change_users_active_status(users, False)

    def make_active(self, request, users):
        return self._change_users_active_status(users, True)

    def _change_users_active_status(self, users, value):
        for user in users:
            if not user.is_superuser:
                user.is_agent = value
                user.save()
        messages.info(self.request, _("Agent's status successfully changed"))
        return redirect('agents_dashboard:agents-list')


class AgentInterestRateView(BulkEditMixin, FormMixin, SingleTableView):
    template_name = 'agents/dashboard/interest.html'
    model = InterestRate
    form_class = AgentInterestRateForm
    success_url = reverse_lazy('agent-interest-rate')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form(self.get_form_class())
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        try:
            interest_rate = InterestRate.objects.get(name='ALL_AGENTS_APPLICABLE')
            kwargs['ir'] = interest_rate
        except InterestRate.DoesNotExist:
            interest_rate = InterestRate.objects.create(
                name='ALL_AGENTS_APPLICABLE')
            kwargs['ir'] = interest_rate
        return kwargs

    def form_valid(self, form):
        form.save(commit=True)
        messages.success(self.request, _("Agent Interest Rate Updated"))
        return redirect(self.get_success_url())


