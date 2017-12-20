from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.forms.models import modelformset_factory, inlineformset_factory
from slugify import slugify

import accounts.models
import accounts.utils


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


class RegistrationForm(forms.Form):

    first_name = forms.CharField(label=_('First name'), required=True, widget=forms.TextInput(
        attrs={
            'id': 'register_first_name',
            'class': 'validate black-text'
        }))

    last_name = forms.CharField(label=_('Last name'), required=True, widget=forms.TextInput(
        attrs={
            'id': 'register_first_name',
            'class': 'validate black-text'
        }))

    email = forms.EmailField(label=_("Email"), required=True, widget=forms.EmailInput(
        attrs={
            'class': 'validate black-text',
            'id': 'register_email',
        }))

    password = forms.CharField(label=_("Password"), required=True, widget=forms.PasswordInput(
        attrs={
            'id': 'register_password',
            'class': 'validate black-text',
        }))

    retype_password = forms.CharField(label=_("Repeat Password"), required=True, widget=forms.PasswordInput(
        attrs={
            'id': 'repeat_password',
            'class': 'validate black-text',
        }))

    profile_type = forms.ChoiceField(choices=accounts.models.Choices.Profiles.PROFILE_CHOICES)

    def clean(self):
        cleaned_data = super().clean()
        self._validate_password()
        return cleaned_data

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']

        if first_name.strip() == "" or first_name.strip() is None:
            raise forms.ValidationError(_("First name cannot be empty."))
        return first_name

    def clean_last_name(self):
        first_name = self.cleaned_data['last_name']

        if first_name.strip() == "" or first_name.strip() is None:
            raise forms.ValidationError(_("Last name cannot be empty."))
        return first_name

    def clean_email(self, raise_on_duplicate=True):
        email = self.cleaned_data['email'].lower().strip().rstrip(".")
        try:
            self.user = get_user_model().objects.get(email__iexact=email)
        except get_user_model().DoesNotExist:
            pass
        except get_user_model().MultipleObjectsReturned:
            raise forms.ValidationError(_("There is already an account with that email address."))
        else:
            if raise_on_duplicate or self.user.has_usable_password():
                raise forms.ValidationError(_("There is already an account with that email address."))

        check_email_domain_is_valid(email)
        return email

    def clean_password(self):
        password = self.cleaned_data['password'].strip()

        if not password:
            self.add_error('password', _("The password cannot be empty"))
        return password

    def clean_retype_password(self):
        retype_password = self.cleaned_data['retype_password'].strip()

        if not retype_password:
            self.add_error('retype_password', _("The password cannot be empty"))

        self._validate_password()
        return retype_password

    def _validate_password(self):
        password = self.cleaned_data.get('password')
        retype_password = self.cleaned_data.get('retype_password')

        if password != retype_password:
            self.add_error('password', _("The passwords do not match"))


class ProfileEditForm(forms.ModelForm):

    class Meta:
        model = accounts.models.User
        fields = ['first_name', 'last_name', 'username', 'email', 'is_active']

    def clean_email(self, raise_on_duplicate=True):
        email = self.cleaned_data['email'].lower().strip().rstrip(".")
        try:
            self.user = get_user_model().objects.get(email__iexact=email)
        except get_user_model().DoesNotExist:
            pass
        except get_user_model().MultipleObjectsReturned:
            raise forms.ValidationError(_("There is already an account with that email address."))

        check_email_domain_is_valid(email)
        return email

    def clean_username(self, raise_on_duplicate=True):
        username = self.cleaned_data['username']
        username = slugify(username)

        try:
            self.user = get_user_model().objects.get(username__iexact=username)
        except get_user_model().DoesNotExist:
            pass
        except get_user_model().MultipleObjectsReturned:
            raise forms.ValidationError(_("There is already an account with that username"))
        return username


class ProfileRequestUserForm(ProfileEditForm):

    class Meta:
        model = accounts.models.User
        fields = ['first_name', 'last_name', 'username', 'email']


class ChangePasswordForm(forms.Form):
    original_password = forms.CharField(label=_("Old password"), required=True, widget=forms.PasswordInput(
        attrs={'placeholder': 'Old password'}
    ))
    new_password = forms.CharField(label=_("New password"), required=True, widget=forms.PasswordInput(
        attrs={'placeholder': 'New password'}
    ))
    retype_password = forms.CharField(label=_("Retype password"), required=True, widget=forms.PasswordInput(
        attrs={'placeholder': 'Retype password'}
    ))

    def clean_original_password(self):
        password = self.cleaned_data['original_password'].strip()

        if not password:
            raise forms.ValidationError(_("The password cannot be empty"))
        return password

    def clean_new_password(self):
        password = self.cleaned_data['new_password'].strip()
        if not password:
            raise forms.ValidationError(_("The password cannot be empty"))
        return password

    def clean_retype_password(self):
        retype_password = self.cleaned_data['retype_password'].strip()
        if not retype_password:
            raise forms.ValidationError( _("The password cannot be empty"))
        return retype_password

    def clean(self):
        cleaned_data = super().clean()
        self._validate_password()
        return cleaned_data

    def _validate_password(self):
        old_password = self.cleaned_data.get('original_password')
        password = self.cleaned_data.get('new_password')
        retype_password = self.cleaned_data.get('retype_password')

        if password != retype_password:
            raise forms.ValidationError(_("The passwords do not match"))
        if password == retype_password == old_password:
            raise forms.ValidationError(_("The password is the same as the original, please choose another password"))
