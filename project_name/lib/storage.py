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


class DatabaseRouter(object):
    """
    Determine how to route database calls for an app's modelos (in this case, for an app named Example).
    All other modelos will be routed to the next router in the DATABASE_ROUTERS setting if applicable,
    or otherwise to the default database.
    """

    def db_for_read(self, model, **hints):
        """Send all read operations on Example app modelos to `example_db`."""
        if model._meta.app_label == 'example':
            return 'example_db'
        return None

    def db_for_write(self, model, **hints):
        """Send all write operations on Example app modelos to `example_db`."""
        if model._meta.app_label == 'example':
            return 'example_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """Determine if relationship is allowed between two objects."""

        # Allow any relation between two modelos that are both in the Example app.
        if obj1._meta.app_label == 'example' and obj2._meta.app_label == 'example':
            return True
        # No opinion if neither object is in the Example app (defer to default or other routers).
        elif 'example' not in [obj1._meta.app_label, obj2._meta.app_label]:
            return None

        # Block relationship if one object is in the Example app and the other isn't.
            return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Ensure that the Example app's modelos get created on the right database."""
        if app_label == 'example':
            # The Example app should be migrated only on the example_db database.
            return db == 'example_db'
        elif db == 'example_db':
            # Ensure that all other apps don't get migrated on the example_db database.
            return False

        # No opinion for all other scenarios
        return None
