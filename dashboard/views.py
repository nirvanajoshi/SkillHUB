from django.shortcuts import render

from courses.models import Course
from enrollments.models import Enrollment
from progress.models import CourseProgress


def home(request):
    featured_courses = Course.objects.filter(
        is_published=True,
    ).select_related("category", "instructor")[:6]

    context = {"featured_courses": featured_courses}

    if request.user.is_authenticated:
        context.update(
            enrolled_count=Enrollment.objects.filter(
                student=request.user,
                status=Enrollment.Status.ACTIVE,
            ).count(),
            completed_count=CourseProgress.objects.filter(
                student=request.user,
                progress_percentage=100,
            ).count(),
        )

    return render(request, "home.html", context)