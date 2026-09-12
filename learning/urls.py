from django.urls import path

from . import views

app_name = "learning"

urlpatterns = [
    path(
        "lesson/<int:lesson_id>/",
        views.lesson_detail,
        name="lesson_detail",
    ),
    path(
        "lesson/<int:lesson_id>/complete/",
        views.complete_lesson,
        name="complete_lesson",
    ),
]
