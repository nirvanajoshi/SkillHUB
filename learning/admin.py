from django.contrib import admin

from .models import LessonProgress


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "lesson",
        "is_completed",
        "watched_seconds",
        "last_accessed_at",
    )

    list_filter = (
        "is_completed",
        "last_accessed_at",
    )

    search_fields = (
        "student__username",
        "student__email",
        "lesson__title",
        "lesson__chapter__course__title",
    )

    readonly_fields = (
        "last_accessed_at",
    )