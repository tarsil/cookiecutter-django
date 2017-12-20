import re

from rest_framework.generics import ListAPIView

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin

class BaseAuthView(ListAPIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication,)
    permission_classes = (IsAuthenticated,)


class BaseEndpointRetrieveView(RetrieveModelMixin, GenericViewSet):
    pass
