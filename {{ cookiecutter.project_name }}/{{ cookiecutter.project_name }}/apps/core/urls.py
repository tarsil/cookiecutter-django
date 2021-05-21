from django.urls import path
from core.views import DashboardView


urlpatterns = [path("dashboard/", DashboardView.as_view(), name="dashboard")]
