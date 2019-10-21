import uuid

from slugify import slugify

import accounts.models


def generate_username(first_name):
    uuid_user = str(uuid.uuid4())
    username = first_name.lower() + "-{id}".format(id=uuid_user[:12])
    return username


def generate_profile_type(profile):
    profile_type = accounts.models.ProfileType.objects.create(
        profile=profile, profile_type=accounts.models.Choices.Profiles.ADMIN
    )
    return profile_type


def update_profile_slug(profile, user):
    try:
        slug = slugify(user.username)
        profile.slug = slug
        profile.save()
        return profile
    except accounts.models.Profile.DoesNotExist:
        pass
