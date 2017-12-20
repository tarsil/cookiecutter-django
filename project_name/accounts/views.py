from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import login, logout, update_session_auth_hash
from django.urls import reverse
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic import View, TemplateView, FormView, UpdateView, ListView, CreateView
from lib.common.views import BaseTemplateMixin

import accounts.forms
import accounts.models
import accounts.utils
import accounts.models


def login_and_handle_data_stored_in_session(user, request):
    session_key = request.session.session_key
    login(request, user)


class BaseUserSystemView(BaseTemplateMixin):

    def get_object(self):
        user = accounts.models.User.objects.get(
            profile__slug=self.kwargs.get('slug', self.request.user.profile.slug)
        )
        if self.request.user.email == user.email:
            return self.request.user
        return user

    def get_back_url(self):
        return self.request.META.get("HTTP_REFERER", reverse('homepage'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'user': self.get_object(),
            'active': False
        })
        return context


class LoginView(FormView):
    template_name = '{{ project_name }}/auth/login.html'
    form_class = accounts.forms.LoginForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.get_user()
        login_and_handle_data_stored_in_session(user, self.request)
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.add_message(
            self.request, messages.ERROR, _("The credentials that you've entered don't match any account")
        )
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('homepage')


class RegisterProfileView(FormView):
    template_name = '{{ project_name }}/application/configurations/add-user.html'
    form_class = accounts.forms.RegistrationForm

    def form_valid(self, form):
        first_name = form.data['first_name']
        last_name = form.data['last_name']
        email = form.data['email']
        password = form.data['password']
        profile_type = form.data['profile_type']
        username = accounts.utils.generate_username(first_name)

        try:
            user = get_user_model().objects.create_user(
                username=username, email=email, password=password,
                is_staff=False, is_superuser=False, first_name=first_name, last_name=last_name
            )

        except IntegrityError:
            msg = _("There was a problem processing your information, please try again")
            messages.add_message(self.request, messages.ERROR, _(msg))
            return super().form_valid(form)

        user.save()
        user.get_or_create_profile(first_name=first_name, last_name=last_name)
        profile = user.get_or_create_profile(first_name=first_name, last_name=last_name)
        profile.profile_type = profile_type
        profile.save()

        msg = _("The profile for {email} has been created").format(
            email=user.email
        )
        messages.add_message(self.request, messages.SUCCESS, _(msg))
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        for errors in form.errors.items():
            key, msg = errors
            messages.add_message(self.request, messages.ERROR, _(msg[0]))
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('homepage')


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(self.request)
        return HttpResponseRedirect(reverse('login'))


class HomepageView(TemplateView):
    template_name = '{{ project_name }}/application/homepage/homepage.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().get(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('login'))


class ProfileView(BaseUserSystemView, TemplateView):
    template_name = '{{ project_name }}/application/profiles/view-form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'back_url': self.get_back_url(),
            'profile': self.get_object().profile,
            'active': 'profile-view'
        })
        return context


class SettingsView(BaseUserSystemView, TemplateView):
    template_name = '{{ project_name }}/application/configurations/settings.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'active': 'profile-settings'
        })
        return context


class ProfileEditView(BaseUserSystemView, UpdateView):
    template_name = '{{ project_name }}/application/profiles/edit-form.html'

    def get_form_class(self):
        if self.request.user.email == self.get_object().email:
            return accounts.forms.ProfileRequestUserForm
        return accounts.forms.ProfileEditForm

    def get_profile_form(self):
        return accounts.forms.ProfileSuperUserFormSet(
            prefix='edit-profile',
            queryset=accounts.models.Profile.objects.filter(user=self.get_object())
        )

    def form_valid(self, form):
        profile = accounts.forms.ProfileSuperUserFormSet(self.request.POST)
        user = form.save()
        profile.save()
        accounts.utils.update_profile_slug(self.get_object().profile, user)

        msg = _("Your profile has been updated")
        messages.add_message(self.request, messages.SUCCESS, msg)
        return HttpResponseRedirect(self.get_success_url(user.username))

    def get_success_url(self, username):
        return reverse('profiles:view-profile', kwargs={
            'slug': username
        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'profile': self.get_object().profile,
            'formset': self.get_profile_form()
        })
        return context


class ChangePasswordView(BaseUserSystemView, FormView):
    template_name = '{{ project_name }}/application/profiles/set-password.html'
    form_class = accounts.forms.ChangePasswordForm

    def form_valid(self, form):
        user = self.get_object()
        is_valid_old_password = user.check_password(form.cleaned_data.get('original_password'))
        if is_valid_old_password:
            user.set_password(form.cleaned_data.get('new_password'))
            user.save()
            update_session_auth_hash(self.request, user)
        else:
            msg = u'Your password does not match with any of our records, please put the correct password and try again'
            messages.add_message(self.request, messages.ERROR, _(msg))
            return super().form_invalid(form)

        msg = _("Your password has been updated")
        messages.add_message(self.request, messages.SUCCESS, msg)
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        for errors in form.errors.items():
            key, msg = errors
            messages.add_message(self.request, messages.ERROR, _(msg[0]))
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'active': "change-password"
        })
        return context

    def get_success_url(self):
        return reverse('profiles:view-profile', kwargs={
            'slug': self.get_object().profile.slug
        })


class ListUsersView(BaseUserSystemView, ListView):
    template_name = '{{ project_name }}/application/configurations/list-users.html'
    paginate_by = 20

    def get_queryset(self):
        queryset = accounts.models.User.objects.all().order_by('profile__created_at').exclude(email=self.request.user.email)

        if self.request.GET.get('name'):
            queryset = queryset.filter(Q(first_name__icontains=self.request.GET.get('name')) |
                                       Q(last_name__icontains=self.request.GET.get('name')))

        if self.request.GET.get('slug'):
            queryset = queryset.filter(profile__slug=self.request.GET.get('slug'))

        if self.request.GET.get('email'):
            queryset = queryset.filter(email=self.request.GET.get('email'))

        if self.request.GET.get('status'):
            queryset = queryset.filter(profile__profile_type=self.request.GET.get('status'))

        if self.request.GET.get('job_level'):
            queryset = queryset.filter(profile__job_level=self.request.GET.get('job_level'))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = accounts.forms.ListUsersSearchForm(
            data=self.request.GET, initial=self.request.GET
        )
        return context
