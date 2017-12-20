from django.conf.urls import url

import accounts.views

accounts_urlpatterns = [
    url(r'^add-user/$', accounts.views.RegisterProfileView.as_view(), name='add-user'),
    url(r'^view/(?P<slug>[a-zA-Z0-9-_]+)/', accounts.views.ProfileView.as_view(), name="view-profile"),
    url(r'^edit/(?P<slug>[a-zA-Z0-9-_]+)/', accounts.views.ProfileEditView.as_view(), name="edit-profile"),
    url(r'^(?P<slug>[a-zA-Z0-9-_]+)/change-password/', accounts.views.ChangePasswordView.as_view(), name="change-password"),
    url(r'^list-users/$', accounts.views.ListUsersView.as_view(), name='list-users'),
    url(r'^settings/(?P<slug>[a-zA-Z0-9-_]+)/$', accounts.views.SettingsView.as_view(), name='settings'),
]
