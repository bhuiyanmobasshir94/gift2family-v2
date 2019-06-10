from oscar_accounts import security
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic
from oscar.core.compat import get_user_model
from oscar.core.loading import (
    get_class, get_classes, get_model, get_profile_class)

Wallet = get_model('oscar_accounts', 'Account')

User = get_user_model()

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