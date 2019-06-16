from django.contrib import messages
from .forms import AgentForm
from oscar_accounts import security
from django.shortcuts import get_object_or_404, redirect, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic
from oscar.core.compat import get_user_model
from oscar.core.loading import (
    get_class, get_classes, get_model, get_profile_class)
from django.contrib.sites.shortcuts import get_current_site
from oscar.apps.customer.utils import get_password_reset_url
from django.core.files.storage import FileSystemStorage
Dispatcher = get_class('customer.utils', 'Dispatcher')
CommunicationEventType = get_model('customer', 'CommunicationEventType')


Wallet = get_model('oscar_accounts', 'Account')

User = get_user_model()
from .models import AgentProfile

# ------------
# Wallet
# ------------


class WalletView(generic.ListView):
    """Wallet"""
    template_name = 'customer/wallet/balance-list.html'
    active_tab = 'wallet'
    page_title = _('Wallet')
    context_object_name = 'account'

    def get_queryset(self):
        """Return customer's addresses"""
        wallets = Wallet.objects.filter(primary_user=self.request.user)
        if wallets:
            return wallets[0]
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
                profile = profile_class(user=user)

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
        kwargs['user'] = self.request.user.agentprofile
        return kwargs

    def form_valid(self, form):

        form.save(commit=True)
        messages.success(self.request, _("Agent Profile updated"))
        return redirect(self.get_success_url())


