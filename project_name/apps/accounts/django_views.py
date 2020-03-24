import accounts.forms
import accounts.models
import accounts.models
import accounts.utils
from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView, View, TemplateView
from lib.common.views import BaseTemplateMixin


class BaseUserSystemView(BaseTemplateMixin):
    """
    Base class inheriting from the main settings object where common validations are placed
    """

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
        login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.add_message(
            self.request, messages.ERROR, _("The credentials that you've entered don't match any account")
        )
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
