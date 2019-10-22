from django.urls import re_path

import accounts.django_views
from accounts.apps import AccountsConfig


app_name = AccountsConfig.name


accounts_urlpatterns = [
    re_path(r'^user/create/$', accounts.views.RegisterProfileView.as_view(), name='add-user'),
]


accounts_api_urlpatterns = [

]
