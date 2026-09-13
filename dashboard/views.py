from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from courses.models import Course
from enrollments.models import Enrollment
from notifications.models import Notification
from progress.models import CourseProgress


def home(request):
    featured_courses = Course.objects.filter(
        is_published=True,
    ).select_related("category", "instructor")[:6]

    context = {
        "featured_courses": featured_courses,
        "unread_count": 0,
    }

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
            unread_count=Notification.objects.filter(
                recipient=request.user,
                is_read=False,
            ).count(),
        )

    return render(request, "home.html", context)


@login_required
def dashboard_home(request):
    """Personalized dashboard for authenticated users."""
    active_enrollments = Enrollment.objects.filter(
        student=request.user,
        status=Enrollment.Status.ACTIVE,
    ).select_related("course", "course__instructor").prefetch_related(
        "course__progress_records"
    )

    recent_activity = CourseProgress.objects.filter(
        student=request.user,
    ).select_related("course").order_by("-last_updated")[:5]

    unread_notifications = Notification.objects.filter(
        recipient=request.user,
        is_read=False,
    ).select_related("recipient")[:5]

    context = {
        "active_enrollments": active_enrollments,
        "recent_activity": recent_activity,
        "unread_notifications": unread_notifications,
        "unread_count": Notification.objects.filter(
            recipient=request.user,
            is_read=False,
        ).count(),
        "enrolled_count": active_enrollments.count(),
        "completed_count": CourseProgress.objects.filter(
            student=request.user,
            progress_percentage=100,
        ).count(),
    }

    return render(request, "dashboard/home.html", context)