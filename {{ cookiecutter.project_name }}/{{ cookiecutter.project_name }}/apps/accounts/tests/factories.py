from uuid import uuid4
import factory
import factory.django

from django.contrib.auth import get_user_model

import accounts.models


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda n: "testes-%s" % n)
    password = factory.PostGenerationMethodCall("set_password", "testes")
    first_name = "Test"
    last_name = "User"
    email = factory.LazyAttribute(lambda u: "%s@testes.example.com" % u.username)

    class Meta:
        model = get_user_model()


class HubUserFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    uuid = factory.Sequence(lambda n: "%s" % str(uuid4()))

    class Meta:
        model = accounts.models.HubUser
