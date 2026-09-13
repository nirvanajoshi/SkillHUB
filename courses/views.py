from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Category, Course


def course_list(request):
    courses = Course.objects.filter(
        is_published=True
    ).select_related(
        "category",
        "instructor",
    )

    # Search functionality
    search_query = request.GET.get("q", "").strip()
    if search_query:
        courses = courses.filter(
            Q(title__icontains=search_query)
            | Q(description__icontains=search_query)
            | Q(instructor__username__icontains=search_query)
            | Q(category__name__icontains=search_query)
        )

    # Filter by level
    level = request.GET.get("level", "")
    if level:
        courses = courses.filter(level=level)

    # Filter by category
    category_id = request.GET.get("category", "")
    if category_id:
        courses = courses.filter(category_id=category_id)

    # Get all categories for filter dropdown
    categories = Category.objects.all()

    # Get unique levels for filter
    levels = Course.Level.choices

    context = {
        "courses": courses,
        "categories": categories,
        "levels": levels,
        "current_search": search_query,
        "current_level": level,
        "current_category": category_id,
    }

    return render(
        request,
        "courses/course_list.html",
        context,
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

    is_enrolled = request.user.is_authenticated and course.enrollments.filter(
        student=request.user,
        status="active",
    ).exists()

    return render(
        request,
        "courses/course_detail.html",
        {
            "course": course,
            "is_enrolled": is_enrolled,
        },
    )