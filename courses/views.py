from django.shortcuts import get_object_or_404, render

from .models import Course


def course_list(request):
    courses = Course.objects.filter(
        is_published=True
    ).select_related(
        "category",
        "instructor",
    )

    return render(
        request,
        "courses/course_list.html",
        {"courses": courses},
    )


def course_detail(request, slug):
    course = get_object_or_404(
        Course.objects.select_related(
            "category",
            "instructor",
        ).prefetch_related(
            "chapters__lessons"
        ),
        slug=slug,
        is_published=True,
    )

    return render(
        request,
        "courses/course_detail.html",
        {"course": course},
    )