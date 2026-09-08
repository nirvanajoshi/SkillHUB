from django.contrib import admin

from .models import CourseProgress


@admin.register(CourseProgress)
class CourseProgressAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "course",
        "completed_lessons",
        "total_lessons",
        "completed_assignments",
        "total_assignments",
        "completed_quizzes",
        "total_quizzes",
        "average_quiz_score",
        "progress_percentage",
        "last_updated",
    )

    list_filter = (
        "course",
        "last_updated",
    )

    search_fields = (
        "student__username",
        "student__email",
        "course__title",
    )

    readonly_fields = (
        "last_updated",
    )