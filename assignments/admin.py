from django.contrib import admin

from .models import Assignment, Submission


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "lesson",
        "due_date",
        "max_marks",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "due_date",
    )

    search_fields = (
        "title",
        "description",
        "lesson__title",
        "lesson__chapter__course__title",
    )


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "assignment",
        "status",
        "marks",
        "submitted_at",
        "graded_at",
    )

    list_filter = (
        "status",
        "submitted_at",
        "graded_at",
    )

    search_fields = (
        "student__username",
        "student__email",
        "assignment__title",
    )

    readonly_fields = (
        "submitted_at",
    )