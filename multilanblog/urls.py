from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path,include
from django.views.i18n import JavaScriptCatalog

urlpatterns = [
    path('admin/', admin.site.urls),
]+i18n_patterns(
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('',include('news.urls',namespace='news')),
    prefix_default_language=False
)

