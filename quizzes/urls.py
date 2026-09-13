from django.urls import path

from .views import quiz_detail

app_name = "quizzes"

urlpatterns = [
    path("<int:quiz_id>/", quiz_detail, name="quiz_detail"),
]
