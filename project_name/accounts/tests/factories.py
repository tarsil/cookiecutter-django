import factory
import uuid
import factory.django

from django.contrib.auth import get_user_model
import accounts.models


class ProfileFactory(factory.django.DjangoModelFactory):
    slug = factory.LazyAttribute(lambda u: "testes-%s" % str(uuid.uuid4())[0:12])

    class Meta:
        model = accounts.models.Profile


class ProfileTypeFactory(factory.django.DjangoModelFactory):
    profile = factory.SubFactory(ProfileFactory)
    profile_type = accounts.models.Choices.Profiles.USER

    class Meta:
        model = accounts.models.ProfileType


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda n: "testes-%s" % n)
    password = "testes"
    first_name = "Test"
    last_name = 'User'
    email = factory.LazyAttribute(lambda u: "%s@testes.example.com" % u.username)
    profile = factory.RelatedFactory(ProfileFactory, name='user')

    class Meta:
        model = get_user_model()

    @classmethod
    def _prepare(cls, create, **kwargs):
        user = super()._prepare(create, **kwargs)
        password = kwargs.pop('password', None)
        if password:
            user.set_password(password)
            if create:
                user.save()
        return user
