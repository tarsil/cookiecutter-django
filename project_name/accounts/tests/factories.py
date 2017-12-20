import factory
import uuid
import factory.django

from django.contrib.auth import get_user_model
import accounts.models


class ProfileFactory(factory.django.DjangoModelFactory):
    slug = factory.LazyAttribute(lambda u: "{{ project_name }}-%s" % str(uuid.uuid4())[0:12])

    class Meta:
        accounts.models.Profile


class ProfileTypeFactory(factory.django.DjangoModelFactory):
    profile = factory.SubFactory(ProfileFactory)
    profile_type = accounts.models.Choices.Profiles.USER

    class Meta:
        accounts.models.ProfileType


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda n: "{{ project_name }}-%s" % n)
    password = "{{ project_name }}"
    first_name = "Test"
    last_name = 'User'
    email = factory.LazyAttribute(lambda u: "%s@{{ project_name }}.example.com" % u.username)
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
