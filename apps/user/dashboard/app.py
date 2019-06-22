    
from django.conf.urls import url
from oscar.core.application import Application
from django.urls import path

from apps.user.dashboard import views


class AgentsDashboardApplication(Application):
    name = 'agents_dashboard'
    default_permissions = ['is_staff',]

    agents_view = views.IndexView
    agent_detail_view = views.AgentDetailView
    change_agent_status = views.change_agent_status
    agent_request_view = views.AgentRequestView

    def get_urls(self):
        urls = [
            url(r'^$',
                self.agents_view.as_view(),
                name='agents-list'),
            url(r'^requests/$',
                self.agent_request_view.as_view(),
                name='agent-request-view'),
            url(r'^(?P<pk>-?\d+)/$',
                self.agent_detail_view.as_view(), name='agent-detail'),
            url(r'^(?P<pk>-?\d+)/change-agent-status/$',
                self.change_agent_status, name='change-agent-status'),
        ]
        return self.post_process_urls(urls)


application = AgentsDashboardApplication()
