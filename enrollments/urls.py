from django.urls import path

from .views import enroll_course, my_courses


app_name = "enrollments"


urlpatterns = [
    path(
        "enroll/<int:course_id>/",
        enroll_course,
        name="enroll_course",
    ),

    path(
        "my-courses/",
        my_courses,
        name="my_courses",
    ),
]