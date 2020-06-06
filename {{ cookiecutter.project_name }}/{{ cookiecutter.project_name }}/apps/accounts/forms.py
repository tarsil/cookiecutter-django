from django import forms
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _


def check_email_domain_is_valid(email):
    if email.split("@")[-1].strip() in settings.BLACKLISTED_DOMAINS:
        raise forms.ValidationError(_("This email address is invalid."))
    return True


class LoginForm(forms.Form):
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(attrs={'autofocus': 'autofocus', 'id': 'login_email', 'Placeholder': 'Email'}))
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={'id': 'login_password', 'placeholder': 'Password'}))

    def clean(self):
        try:
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']

            user = get_user_model().objects.get(email__iexact=email, is_active=True)
            try:
                self.authed_user = authenticate(
                    username=user.username,
                    password=password,
                )
            except ValueError:
                self.authed_user = None

            if self.authed_user:
                return self.cleaned_data

        except (get_user_model().DoesNotExist, KeyError):
            pass

        raise forms.ValidationError("Your login details were incorrect. Please try again.")

    def get_user(self):
        return self.authed_user
