from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

UserModel = get_user_model()


class EmailBackend(ModelBackend):
    """
    Enables the login backend through email.
    By Default django only login with username. This overrides that default and adds a new backend possibility,
    allowing also to login using emails.
    """

    def authenticate(self, request, email=None, password=None, **kwargs):
        if email is None:
            email = kwargs.get(UserModel.EMAIL_FIELD)
        if email is None or password is None:
            return
        breakpoint()
        try:
            user = UserModel.objects.get(email__iexact=email)
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
