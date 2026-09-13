from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from courses.models import Lesson
from enrollments.models import Enrollment
from progress.models import CourseProgress

from .models import LessonProgress


@login_required
def lesson_detail(request, lesson_id):

    lesson = get_object_or_404(
        Lesson.objects.select_related(
            "chapter",
            "chapter__course",
        ),
        id=lesson_id,
    )

    course = lesson.chapter.course

    is_enrolled = Enrollment.objects.filter(
        student=request.user,
        course=course,
        status=Enrollment.Status.ACTIVE,
    ).exists()

    if not is_enrolled:
        messages.error(
            request,
            "You must be enrolled in this course to access this lesson.",
        )

        return redirect(
            "courses:course_detail",
            slug=course.slug,
        )

    lesson_progress, created = LessonProgress.objects.get_or_create(
        student=request.user,
        lesson=lesson,
    )

    return render(
        request,
        "learning/lesson_detail.html",
        {
            "lesson": lesson,
            "course": course,
            "progress": lesson_progress,
        },
    )


@login_required
def complete_lesson(request, lesson_id):

    lesson = get_object_or_404(
        Lesson.objects.select_related(
            "chapter",
            "chapter__course",
        ),
        id=lesson_id,
    )

    course = lesson.chapter.course

    is_enrolled = Enrollment.objects.filter(
        student=request.user,
        course=course,
        status=Enrollment.Status.ACTIVE,
    ).exists()

    if not is_enrolled:
        messages.error(
            request,
            "You must be enrolled in this course.",
        )

        return redirect(
            "courses:course_detail",
            slug=course.slug,
        )

    if request.method == "POST":

        lesson_progress, created = LessonProgress.objects.get_or_create(
            student=request.user,
            lesson=lesson,
        )

        lesson_progress.is_completed = True
        lesson_progress.completed_at = timezone.now()
        lesson_progress.save()

        # Count all lessons in the course
        total_lessons = Lesson.objects.filter(
            chapter__course=course,
        ).count()

        # Count completed lessons by this student
        completed_lessons = LessonProgress.objects.filter(
            student=request.user,
            lesson__chapter__course=course,
            is_completed=True,
        ).count()

        # Create or update course progress
        course_progress, created = CourseProgress.objects.get_or_create(
            student=request.user,
            course=course,
        )

        course_progress.total_lessons = total_lessons
        course_progress.completed_lessons = completed_lessons

        course_progress.calculate_progress()
        course_progress.save()

        messages.success(
            request,
            "Lesson marked as completed. Your course progress has been updated.",
        )

    return redirect(
        "learning:lesson_detail",
        lesson_id=lesson.id,
    )