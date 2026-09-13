from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from courses.models import Course
from enrollments.models import Enrollment
from progress.models import CourseProgress

from .models import Answer, Attempt, Quiz


@login_required
def quiz_detail(request, quiz_id):
	quiz = get_object_or_404(
		Quiz.objects.prefetch_related("questions__options").select_related(
			"lesson__chapter__course"
		),
		id=quiz_id,
		is_published=True,
	)
	course = quiz.lesson.chapter.course
	if not Enrollment.objects.filter(
		student=request.user,
		course=course,
		status=Enrollment.Status.ACTIVE,
	).exists():
		messages.error(request, "Enroll in this course to take the quiz.")
		return redirect("courses:course_detail", slug=course.slug)

	if request.method == "POST":
		attempt = Attempt.objects.create(student=request.user, quiz=quiz)
		total_marks = sum(question.marks for question in quiz.questions.all())
		score = 0
		for question in quiz.questions.all():
			selected_id = request.POST.get(f"question_{question.id}")
			selected = question.options.filter(id=selected_id).first() if selected_id else None
			is_correct = bool(selected and selected.is_correct)
			marks = question.marks if is_correct else 0
			score += marks
			Answer.objects.create(
				attempt=attempt,
				question=question,
				selected_option=selected,
				is_correct=is_correct,
				marks_awarded=marks,
			)
		percentage = round((score / total_marks) * 100, 2) if total_marks else 0
		attempt.score = score
		attempt.percentage = percentage
		attempt.passed = percentage >= quiz.passing_score
		attempt.completed_at = timezone.now()
		attempt.save()
		total_quizzes = Quiz.objects.filter(
			lesson__chapter__course=course,
			is_published=True,
		).count()
		passed_quizzes = Attempt.objects.filter(
			student=request.user,
			quiz__lesson__chapter__course=course,
			passed=True,
		).values("quiz_id").distinct().count()
		progress, _ = CourseProgress.objects.get_or_create(
			student=request.user,
			course=course,
		)
		progress.total_quizzes = total_quizzes
		progress.completed_quizzes = passed_quizzes
		progress.calculate_progress()
		progress.save()
		return render(request, "quizzes/result.html", {"quiz": quiz, "attempt": attempt, "course": course})

	return render(request, "quizzes/quiz_detail.html", {"quiz": quiz, "course": course})
