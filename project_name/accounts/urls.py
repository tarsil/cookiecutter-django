from django.urls import re_path

import accounts.views
from accounts.apps import AccountsConfig


app_name = AccountsConfig.name


accounts_urlpatterns = [
    re_path(r'^user/create/$', accounts.views.RegisterProfileView.as_view(), name='add-user'),
]
