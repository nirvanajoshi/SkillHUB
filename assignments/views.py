from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from enrollments.models import Enrollment

from .models import Assignment, Submission


@login_required
def assignment_detail(request, assignment_id):
	assignment = get_object_or_404(
		Assignment.objects.select_related("lesson__chapter__course"),
		id=assignment_id,
		status=Assignment.Status.PUBLISHED,
	)
	course = assignment.lesson.chapter.course
	if not Enrollment.objects.filter(
		student=request.user,
		course=course,
		status=Enrollment.Status.ACTIVE,
	).exists():
		messages.error(request, "Enroll in this course to submit the assignment.")
		return redirect("courses:course_detail", slug=course.slug)

	submission, _ = Submission.objects.get_or_create(
		assignment=assignment,
		student=request.user,
	)
	if request.method == "POST":
		submission.answer = request.POST.get("answer", "")
		if request.FILES.get("file"):
			submission.file = request.FILES["file"]
		submission.status = (
			Submission.Status.LATE
			if assignment.due_date and assignment.due_date < timezone.now()
			else Submission.Status.SUBMITTED
		)
		submission.save()
		messages.success(request, "Your assignment has been submitted.")
		return redirect("assignments:assignment_detail", assignment_id=assignment.id)

	return render(request, "assignments/assignment_detail.html", {
		"assignment": assignment,
		"submission": submission,
		"course": course,
	})
