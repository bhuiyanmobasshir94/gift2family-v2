from django.conf.urls import include, url  # < Django-2.0
# from django.urls import include, path  # > Django-2.0
from django.contrib import admin
from oscar.app import application
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^admin/', admin.site.urls),
    url(r'', application.urls),
    url(r'^checkout/paypal/', include('paypal.express.urls')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)