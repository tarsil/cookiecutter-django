from django.http import HttpResponseForbidden, HttpResponseRedirect
from lib.common.utils import reverse
from django.contrib.auth.mixins import LoginRequiredMixin


class StaffOnlyMixin(object):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)


class UserAuthMixin(object):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        return super().dispatch(request, *args, **kwargs)


class BaseTemplateMixin(LoginRequiredMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'active': False
        })
        return context

