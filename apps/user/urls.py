from django.conf.urls import include, url  # < Django-2.0
# from django.urls import include, path  # > Django-2.0
from django.contrib import admin
from oscar.app import application
from django.conf import settings
from django.conf.urls.static import static
from oscar_accounts.dashboard.app import application as accounts_app
from django.apps import apps

from oscar_accounts.dashboard.app import application as accounts_app
from oscar_accounts.views import AccountBalanceView
from oscar.core.loading import get_class
from apps.user.decorators import agent_login_required, non_agent_login_required

wallet_view = get_class(
    'apps.user.views', 'WalletView')
transaction_view = get_class(
    'apps.user.views', 'AgentTransactionView')
transfer_view = get_class(
    'apps.user.views', 'AgentTransferDetailView')
agent_profile_view = get_class(
    'apps.user.views', 'AgentProfileView')
agent_profile_update_view = get_class(
    'apps.user.views', 'AgentProfileUpdateView')
agent_profile_create_view = get_class(
    'apps.user.views', 'AgentRequestFormView')

urlpatterns = [
    url(r'^wallet/', agent_login_required(wallet_view.as_view()),
    name='account-view'),
    url(r'^transactions/', agent_login_required(transaction_view.as_view()),
        name='transaction-view'),
    url(r'^transfers/(?P<reference>[A-Z0-9]{32})/$', transfer_view.as_view(),
        name='agent-transfers-detail'),
    url(r'^agent-profile/', agent_login_required(agent_profile_view.as_view()),
        name='agent-profile-view'),
    url(r'^agent-profile-update/', agent_login_required(agent_profile_update_view.as_view()),
        name='agent-profile-update-view'),
    url(r'^agent-profile-create/', non_agent_login_required(agent_profile_create_view.as_view()),
        name='agent-profile-create-view'),

]
