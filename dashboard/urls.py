from django.urls import path

from .views import dashboard_home, home


app_name = "dashboard"


urlpatterns = [
    path("", home, name="home"),
    path("dashboard/", dashboard_home, name="dashboard_home"),
]