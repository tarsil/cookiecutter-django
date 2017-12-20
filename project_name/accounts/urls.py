from django.urls import re_path

import accounts.views
from accounts.apps import AccountsConfig


app_name = AccountsConfig.name


accounts_urlpatterns = [
    re_path(r'^add-user/$', accounts.views.RegisterProfileView.as_view(), name='add-user'),
    re_path(r'^view/(?P<slug>[a-zA-Z0-9-_]+)/$', accounts.views.ProfileView.as_view(), name="view-profile"),
    re_path(r'^edit/(?P<slug>[a-zA-Z0-9-_]+)/$', accounts.views.ProfileEditView.as_view(), name="edit-profile"),
    re_path(r'^(?P<slug>[a-zA-Z0-9-_]+)/change-password/$', accounts.views.ChangePasswordView.as_view(), name="change-password"),
    re_path(r'^list-users/$', accounts.views.ListUsersView.as_view(), name='list-users'),
    re_path(r'^settings/(?P<slug>[a-zA-Z0-9-_]+)/$', accounts.views.SettingsView.as_view(), name='settings'),
]
