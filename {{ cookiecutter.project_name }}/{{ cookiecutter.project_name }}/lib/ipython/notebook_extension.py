def load_ipython_extension(ipython):
    """

    Args:
      ipython:

    Returns:

    """
    from django.core.management.color import color_style
    from django_extensions.management.shells import import_objects

    imported_objects = import_objects(options={"dont_load": []}, style=color_style())
    ipython.push(imported_objects)
