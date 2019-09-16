import datetime
from decimal import Decimal as D
from oscar_accounts.dashboard import forms, reports
from oscar_accounts import exceptions, facade, names
from oscar.templatetags.currency_filters import currency
from itertools import chain
from django.contrib import messages
from .forms import AgentForm,AgentRequestForm
from oscar_accounts import security
from django.shortcuts import get_object_or_404, redirect, HttpResponseRedirect,render
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic
from oscar.core.compat import get_user_model
from oscar.core.loading import (get_class, get_classes, get_model, get_profile_class)
from django.contrib.sites.shortcuts import get_current_site
from oscar.apps.customer.utils import get_password_reset_url
from django.core.files.storage import FileSystemStorage
from django.conf import settings
Dispatcher = get_class('customer.utils', 'Dispatcher')
CommunicationEventType = get_model('customer', 'CommunicationEventType')

AccountType = get_model('oscar_accounts', 'AccountType')
Wallet = get_model('oscar_accounts', 'Account')
country = get_model('address', 'Country')
Account = get_model('oscar_accounts', 'Account')
Transfer = get_model('oscar_accounts', 'Transfer')
Transaction = get_model('oscar_accounts', 'Transaction')

User = get_user_model()
from .models import AgentProfile

# ------------
# Wallet
# ------------


class AgentTransactionView(generic.ListView):
    """Agent transactions"""
    template_name = 'agents/transaction/transactions.html'
    active_tab = 'agent-transaction'
    page_title = _('Transactions')
    form_class = forms.TransferSearchForm
    description = _("Transactions")
    context_object_name = 'transactions'
    paginate_by = getattr(settings, 'OSCAR_ACCOUNTS_DASHBOARD_ITEMS_PER_PAGE', 20)

    def get_queryset(self):
        """ Return Transactions """
        try:
            self.account = Account.objects.filter(
                primary_user=self.request.user)
        except Account.DoesNotExist:
            self.account = None
        if self.account:
            transactions = []
            for a in self.account:
                # transactions.append(a.transactions.all().order_by('-date_created'))
                queryset = a.transactions.all().order_by('-date_created')
            # queryset = list(chain(*transactions))

                if 'reference' not in self.request.GET:
                    # Form not submitted
                    self.form = self.form_class()
                    return queryset
                
                self.form = self.form_class(self.request.GET)
                if not self.form.is_valid():
                    # Form submitted but invalid
                    return queryset
                
                data = self.form.cleaned_data
                desc_template = _(
                    "Transfers %(reference)s %(date)s")
                desc_ctx = {
                    'reference': "",
                    'date': "",
                }

                # if data['reference']:

                #     queryset = queryset.filter(reference=data['reference'])
                #     desc_ctx['reference'] = _(
                #         " with reference '%s'") % data['reference']

                if data['start_date'] and data['end_date']:
                        # Add 24 hours to make search inclusive
                    date_from = data['start_date']
                    date_to = data['end_date'] + datetime.timedelta(days=1)
                    queryset = queryset.filter(date_created__gte=date_from).filter(
                        date_created__lt=date_to)
                    desc_ctx['date'] = _(" created between %(start_date)s and %(end_date)s") % {
                        'start_date': data['start_date'],
                        'end_date': data['end_date']}
                elif data['start_date']:
                    queryset = queryset.filter(date_created__gte=data['start_date'])
                    desc_ctx['date'] = _(" created since %s") % data['start_date']
                elif data['end_date']:
                    date_to = data['end_date'] + datetime.timedelta(days=1)
                    queryset = queryset.filter(date_created__lt=date_to)
                    desc_ctx['date'] = _(" created before %s") % data['end_date']
                transactions.append(queryset)
            queryset = list(chain(*transactions))
            self.description = desc_template % desc_ctx
            return queryset
        else:
            return None

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = self.form
        ctx['queryset_description'] = self.description
        ctx['is_blocked'] = security.is_blocked(self.request)
        ctx['active_tab'] = 'agent-transaction'
        ctx['page_title'] = _('Transactions')
        return ctx

class AgentTransferDetailView(generic.DetailView):
    model = Transfer
    context_object_name = 'transfer'
    page_title = _('Transfers')
    template_name = 'agents/transaction/transfer_detail.html'

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        return queryset.get(reference=self.kwargs['reference'])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['is_blocked'] = security.is_blocked(self.request)
        ctx['active_tab'] = 'agent-transaction'
        ctx['page_title'] = _('Transfers')
        return ctx

class WalletView(generic.ListView):
    """Wallet"""
    template_name = 'customer/wallet/balance-list.html'
    active_tab = 'wallet'
    page_title = _('Wallet')
    context_object_name = 'accounts'

    def get_queryset(self):
        """Return customer's addresses"""
        wallets = Wallet.objects.filter(primary_user=self.request.user)
        if wallets:
            return wallets
        else:
            return wallets

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['is_blocked'] = security.is_blocked(self.request)
        ctx['active_tab'] = 'wallet'
        ctx['page_title'] = _('Wallet')
        return ctx

# ------------
# Agent Profile
# ------------


class AgentProfileView(generic.TemplateView):
    template_name = 'agents/profile/profile.html'
    page_title = _('Agent Profile')
    active_tab = 'agent-profile'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['profile_fields'] = self.get_profile_fields(self.request.user)
        ctx['active_tab'] = self.active_tab
        ctx['page_title'] = self.page_title
        return ctx

    def get_profile_fields(self, user):
        field_data = []

        # Check for profile class
        profile_class = AgentProfile
        if profile_class:
            try:
                profile = profile_class.objects.get(user=user)
            except profile_class.DoesNotExist:
                profile = None

            field_names = [f.name for f in profile._meta.local_fields]
            for field_name in field_names:
                if field_name in ('user', 'id'):
                    continue
                field_data.append(
                    self.get_model_field_data(profile, field_name))

        return field_data

    def get_model_field_data(self, model_class, field_name):
        """
        Extract the verbose name and value for a model's field value
        """
        field = model_class._meta.get_field(field_name)
        if field.choices:
            value = getattr(model_class, 'get_%s_display' % field_name)()
        else:
            value = getattr(model_class, field_name)
        return {
            'name': getattr(field, 'verbose_name'),
            'value': value,
        }


class AgentProfileUpdateView(generic.FormView):
    form_class = AgentForm
    template_name = 'agents/profile/profile_form.html'
    page_title = _('Edit Agent Profile')
    active_tab = 'agent-profile'
    success_url = reverse_lazy('agent-profile-view')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['active_tab'] = self.active_tab
        ctx['page_title'] = self.page_title
        ctx['includes_files'] = True
        return ctx

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        try:
            agentprofile = AgentProfile.objects.get(user=self.request.user)
            kwargs['user'] = agentprofile
        except AgentProfile.DoesNotExist:
            agentprofile = AgentProfile.objects.create(
                user=self.request.user, country=country.objects.get(printable_name="Bangladesh"))
            kwargs['user'] = agentprofile
        return kwargs

    def form_valid(self, form):
        form.save(commit=True)
        messages.success(self.request, _("Agent Profile Updated"))
        return redirect(self.get_success_url())


class AgentRequestFormView(generic.FormView):
    form_class = AgentRequestForm
    template_name = 'agents/profile/profile_form.html'
    page_title = _('Agent Request Form')
    active_tab = 'agent-request-form'
    success_url = reverse_lazy('customer:profile-view')
        
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['active_tab'] = self.active_tab
        ctx['page_title'] = self.page_title
        ctx['includes_files'] = True
        return ctx

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        try:
            agentprofile = AgentProfile.objects.get(
                user=self.request.user)
            kwargs['user'] = agentprofile
        except AgentProfile.DoesNotExist:
            agentprofile = AgentProfile.objects.create(
                user=self.request.user, country=country.objects.get(printable_name="Bangladesh"))
            kwargs['user'] = agentprofile
        return kwargs

    def form_valid(self, form):
        form.save(commit=True)
        messages.success(self.request, _("Agent Profile Created"))
        return redirect(self.get_success_url())


