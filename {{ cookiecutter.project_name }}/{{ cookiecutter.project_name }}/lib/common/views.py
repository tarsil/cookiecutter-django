from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from lib.common.utils import reverse


class BaseView:
    """Base of the Base for the pages"""
    page_name = None
    company_name = None

    def get_url(self):
        """ """
        try:
            return self.get_success_url()
        except AttributeError:
            return reverse('homepage')

    def get_context_data(self, **kwargs):
        """

        Args:
          **kwargs:

        Returns:

        """
        context = super().get_context_data(**kwargs)
        context.update({
            'active': False,
            'page_name': self.page_name,
            'edit': False,
            'nav_name': ''
        })
        return context


class AuthMixin(LoginRequiredMixin, BaseView):
    """Class common to every view in the system, for instance, the user should be always logged in"""
    redirect_field_name = 'next'

    def get_host_url(self):
        """Returns the host url (localhost, staging, preview, live)"""
        return self.request.get_host()

    def get_context_data(self, **kwargs):
        """Updates the list of employers of a hub_user
        """
        context = super().get_context_data(**kwargs)
        context.update(
            {
                'edit': False,
            },
        )
        return context


class NotLoginMixin(BaseView):
    """Applied for non logged in pages"""

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_url())
        return super().get(request, *args, **kwargs)
