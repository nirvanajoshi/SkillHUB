from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from courses.models import Course
from .models import Enrollment


@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(
        Course,
        id=course_id,
        is_published=True,
    )

    if request.method == "POST":

        enrollment, created = Enrollment.objects.get_or_create(
            student=request.user,
            course=course,
        )

        if created:
            messages.success(
                request,
                f"You have successfully enrolled in {course.title}.",
            )
        else:
            messages.info(
                request,
                "You are already enrolled in this course.",
            )

        return redirect(
            "courses:course_detail",
            slug=course.slug,
        )

    return redirect(
        "courses:course_detail",
        slug=course.slug,
    )


@login_required
def my_courses(request):
    enrollments = Enrollment.objects.filter(
        student=request.user,
        status=Enrollment.Status.ACTIVE,
    ).select_related(
        "course",
        "course__instructor",
    )

    return render(
        request,
        "enrollments/my_courses.html",
        {"enrollments": enrollments},
    )