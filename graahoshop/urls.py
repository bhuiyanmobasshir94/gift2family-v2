from django.conf.urls import include, url  # < Django-2.0
# from django.urls import include, path  # > Django-2.0
from django.contrib import admin
from oscar.app import application
from django.conf import settings
from django.conf.urls.static import static
from oscar_accounts.dashboard.app import application as accounts_app
from apps.user.dashboard.app import application as agents_app
from django.apps import apps
from apps.user import urls as agent_url

urlpatterns = [
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^admin/', admin.site.urls),
    url(r'', application.urls),
    url(r'^checkout/paypal/', include('paypal.express.urls')),
    url(r'^dashboard/accounts/', accounts_app.urls),
    url(r'^dashboard/agents/', agents_app.urls),
    url(r'^agents/', include(agent_url)),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
