from django.contrib import admin

from .models import Category, Course, Chapter, Lesson


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "instructor",
        "category",
        "level",
        "is_published",
        "created_at",
    )

    list_filter = (
        "level",
        "is_published",
        "category",
    )

    search_fields = (
        "title",
        "description",
        "instructor__username",
    )

    prepopulated_fields = {
        "slug": ("title",)
    }


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "course",
        "chapter_number",
    )

    list_filter = ("course",)

    search_fields = (
        "title",
        "course__title",
    )


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "chapter",
        "lesson_number",
        "is_preview",
    )

    list_filter = (
        "is_preview",
        "chapter__course",
    )

    search_fields = (
        "title",
        "chapter__title",
    )