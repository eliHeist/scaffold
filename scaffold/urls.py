from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from scaffold.appsConfig import getAppUrls
from scaffold.registrar import registrar

from accounts.views import accounts_router

registrar.include_many(
    accounts_router,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path("mfa/", include("allauth.mfa.urls")),
    path("", include(registrar.get_patterns())),
]

urlpatterns += getAppUrls()
urlpatterns += debug_toolbar_urls()

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
