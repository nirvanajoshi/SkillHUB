from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),

    path(
        "accounts/",
        include("accounts.urls"),
    ),

    path(
        "courses/",
        include("courses.urls"),
    ),

    path(
        "enrollments/",
        include("enrollments.urls"),
    ),

    path(
        "learning/",
        include("learning.urls"),
    ),

    path("assignments/", include("assignments.urls")),
    path("quizzes/", include("quizzes.urls")),
    path("notifications/", include("notifications.urls")),

    path(
        "",
        include("dashboard.urls"),
    ),
]