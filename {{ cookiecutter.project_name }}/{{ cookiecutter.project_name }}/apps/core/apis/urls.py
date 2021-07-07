from core.apis import imports
from django.conf import settings
from django.conf.urls import include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

URLPATTERNS = "urlpatterns"

api = []
if settings.DEBUG:
    schema_view = get_schema_view(
        openapi.Info(title="{{ cookiecutter.project_name }} API", default_version="v1"),
        public=True,
        permission_classes=(permissions.IsAuthenticated,),
    )
    api = [
        re_path(r"^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),
        re_path(r"^swagger/$", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
        re_path(r"^swagger/redoc$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    ]


def get_urls(version, importer):
    version_urls = []
    for app, module in importer.execute().items():
        app_urls = getattr(module, URLPATTERNS, None)
        if app_urls:
            app_path = r"^%s/%s/" % (version, app)  # noqa
            version_clean = version.replace(".", "_").replace("\\", "")  # noqa
            namespace = f"{app}_{version_clean}"  # noqa
            version_urls += [re_path(app_path, include((app_urls, app), namespace=namespace))]
    return version_urls


for version, _import in imports.items():
    api += get_urls(version, _import)


urlpatterns = [re_path(r"^", include(api))]
