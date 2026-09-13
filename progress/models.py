from django.conf import settings
from django.db import models


class CourseProgress(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="course_progress",
    )

    course = models.ForeignKey(
        "courses.Course",
        on_delete=models.CASCADE,
        related_name="progress_records",
    )

    completed_lessons = models.PositiveIntegerField(default=0)

    total_lessons = models.PositiveIntegerField(default=0)

    completed_assignments = models.PositiveIntegerField(default=0)

    total_assignments = models.PositiveIntegerField(default=0)

    completed_quizzes = models.PositiveIntegerField(default=0)

    total_quizzes = models.PositiveIntegerField(default=0)

    average_quiz_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
    )

    progress_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
    )

    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-last_updated"]

        constraints = [
            models.UniqueConstraint(
                fields=["student", "course"],
                name="unique_student_course_progress",
            )
        ]

    def __str__(self):
        return f"{self.student.username} - {self.course.title}"
    

    def calculate_progress(self):

    progress_values = []

    if self.total_lessons > 0:
        lesson_progress = (
            self.completed_lessons / self.total_lessons
        ) * 100

        progress_values.append(lesson_progress)

    if self.total_assignments > 0:
        assignment_progress = (
            self.completed_assignments / self.total_assignments
        ) * 100

        progress_values.append(assignment_progress)

    if self.total_quizzes > 0:
        quiz_progress = (
            self.completed_quizzes / self.total_quizzes
        ) * 100

        progress_values.append(quiz_progress)

    if progress_values:
        self.progress_percentage = round(
            sum(progress_values) / len(progress_values),
            2,
        )
    else:
        self.progress_percentage = 0

    return self.progress_percentage