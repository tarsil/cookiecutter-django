import django.contrib.staticfiles.storage


class CachedStaticFilesStorage(
    django.contrib.staticfiles.storage.CachedStaticFilesStorage):

    def hashed_name(self, name, content=None):
        try:
            return super().hashed_name(
                name, content=content)
        except ValueError:
            # If there is a static asset that refers to another asset
            # that doesn't exist, don't fall over, just ignore it.
            return name
