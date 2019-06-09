from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from django.views import generic

from oscar.core.application import OscarConfig
from oscar.core.loading import get_class

from oscar.core.loading import get_class
from apps.user.decorators import agent_login_required



class AgentConfig(OscarConfig):
    label = 'user'
    name = 'apps.user'
    verbose_name = _('User')

    namespace = 'user'

    def ready(self):
        from oscar.apps.customer import receivers  
        from oscar.apps.customer.alerts import receivers 

        self.wallet_view = get_class('apps.user.views', 'WalletView')

    def get_urls(self):
        urls = [url(r'^accounts/wallet/', agent_login_required(self.wallet_view.as_view()),
        name='account-view'),]
        return self.post_process_urls(urls)

application = AgentConfig()