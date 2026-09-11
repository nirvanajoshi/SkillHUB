from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from courses.models import Lesson
from enrollments.models import Enrollment

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

    # Check whether the student is enrolled
    enrollment = Enrollment.objects.filter(
        student=request.user,
        course=course,
        status=Enrollment.Status.ACTIVE,
    ).first()

    if not enrollment:
        messages.error(
            request,
            "You must be enrolled in this course to access this lesson.",
        )

        return redirect(
            "courses:course_detail",
            slug=course.slug,
        )

    progress, created = LessonProgress.objects.get_or_create(
        student=request.user,
        lesson=lesson,
    )

    return render(
        request,
        "learning/lesson_detail.html",
        {
            "lesson": lesson,
            "course": course,
            "progress": progress,
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

    # Check enrollment
    enrollment = Enrollment.objects.filter(
        student=request.user,
        course=course,
        status=Enrollment.Status.ACTIVE,
    ).first()

    if not enrollment:
        messages.error(
            request,
            "You must be enrolled in this course.",
        )

        return redirect(
            "courses:course_detail",
            slug=course.slug,
        )

    if request.method == "POST":

        progress, created = LessonProgress.objects.get_or_create(
            student=request.user,
            lesson=lesson,
        )

        progress.is_completed = True
        progress.completed_at = timezone.now()
        progress.save()

        messages.success(
            request,
            "Lesson marked as completed.",
        )

    return redirect(
        "learning:lesson_detail",
        lesson_id=lesson.id,
    )