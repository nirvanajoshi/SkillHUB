from django.urls import path

from .views import assignment_detail

app_name = "assignments"

urlpatterns = [
    path("<int:assignment_id>/", assignment_detail, name="assignment_detail"),
]
