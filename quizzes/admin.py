from django.contrib import admin

from .models import Quiz, Question, Option, Attempt, Answer


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "lesson",
        "time_limit",
        "passing_score",
        "is_published",
        "created_at",
    )

    list_filter = (
        "is_published",
        "passing_score",
    )

    search_fields = (
        "title",
        "description",
        "lesson__title",
        "lesson__chapter__course__title",
    )


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        "quiz",
        "question_number",
        "marks",
    )

    list_filter = ("quiz",)

    search_fields = (
        "question_text",
        "quiz__title",
    )


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = (
        "question",
        "option_number",
        "option_text",
        "is_correct",
    )

    list_filter = (
        "is_correct",
    )

    search_fields = (
        "option_text",
        "question__question_text",
    )


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "quiz",
        "score",
        "percentage",
        "passed",
        "started_at",
        "completed_at",
    )

    list_filter = (
        "passed",
        "started_at",
        "completed_at",
    )

    search_fields = (
        "student__username",
        "student__email",
        "quiz__title",
    )

    readonly_fields = (
        "started_at",
    )


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = (
        "attempt",
        "question",
        "selected_option",
        "is_correct",
        "marks_awarded",
    )

    list_filter = (
        "is_correct",
    )

    search_fields = (
        "attempt__student__username",
        "question__question_text",
    )