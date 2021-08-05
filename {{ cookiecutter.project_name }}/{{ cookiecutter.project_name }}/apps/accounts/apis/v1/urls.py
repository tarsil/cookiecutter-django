from django.urls import path
from accounts.apis.v1.views import (
    LoginApiView,
    RegisterApiView,
    UpdatePasswordView,
    UpdateEmailView,
    DeleteUserAccountApiView,
)

urlpatterns = [
    path("auth/login", LoginApiView.as_view(), name="login"),
    path("auth/signup", RegisterApiView.as_view(), name="register"),
    path("auth/password", UpdatePasswordView.as_view(), name="update-password"),
    path("auth/email", UpdateEmailView.as_view(), name="update-email"),
    path("auth/account/delete", DeleteUserAccountApiView.as_view(), name="delete-account"),
]
