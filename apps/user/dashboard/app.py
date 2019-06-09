    
from django.conf.urls import url
from oscar.core.application import Application

from apps.user.dashboard import views


class AgentsDashboardApplication(Application):
    name = 'agents_dashboard'
    default_permissions = ['is_staff',]

    agents_view = views.IndexView
    agent_detail_view = views.AgentDetailView

    def get_urls(self):
        urls = [
            url(r'^$',
                self.agents_view.as_view(),
                name='agents-list'),
            url(r'^(?P<pk>-?\d+)/$',
                self.agent_detail_view.as_view(), name='agent-detail'),
        ]
        return self.post_process_urls(urls)


application = AgentsDashboardApplication()