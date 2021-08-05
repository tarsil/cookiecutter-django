"""django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import os
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin
from accounts.views import LoginView, LogoutView, HomepageView

from accounts.apis.v1.views import EmailTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)

admin.autodiscover()


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomepageView.as_view(), name='homepage'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('u/', include('accounts.urls'), name='user'),

    # API
    path("api/", include(("core.apis.urls", "api"))),

    # JWT
    path('auth/api/token', EmailTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/api/token/verify', TokenVerifyView.as_view(), name='token_verify'),
]


if settings.DEBUG and (os.getenv("ENVIRONMENT") not in ["live", "staging"]):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    import debug_toolbar
    import django.views.defaults

    def custom_page_not_found(request):
        return django.views.defaults.page_not_found(request, None)

    def server_error(request):
        return django.views.defaults.server_error(request)

    def permission_denied(request):
        return django.views.defaults.permission_denied(request, None)

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
        path("403/", permission_denied),
        path("404/", custom_page_not_found),
        path("500/", server_error),
    ]
