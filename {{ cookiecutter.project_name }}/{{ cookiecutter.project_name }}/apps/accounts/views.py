import accounts.forms
import accounts.models
import accounts.utils
from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView, View


class LoginView(FormView):
    template_name = 'saturn/auth/login.html'
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


class HomepageView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Homepage")
