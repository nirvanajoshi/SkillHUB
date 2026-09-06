from django.conf import settings
from django.db import models


class Assignment(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"
        CLOSED = "closed", "Closed"

    lesson = models.ForeignKey(
        "courses.Lesson",
        on_delete=models.CASCADE,
        related_name="assignments",
    )

    title = models.CharField(max_length=200)

    description = models.TextField()

    instructions = models.TextField(blank=True)

    due_date = models.DateTimeField(
        null=True,
        blank=True,
    )

    max_marks = models.PositiveIntegerField(default=100)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Submission(models.Model):
    class Status(models.TextChoices):
        SUBMITTED = "submitted", "Submitted"
        GRADED = "graded", "Graded"
        LATE = "late", "Late"

    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name="submissions",
    )

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="assignment_submissions",
    )

    answer = models.TextField(blank=True)

    file = models.FileField(
        upload_to="assignment_submissions/",
        blank=True,
        null=True,
    )

    marks = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    feedback = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SUBMITTED,
    )

    submitted_at = models.DateTimeField(
        auto_now_add=True,
    )

    graded_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["-submitted_at"]

        constraints = [
            models.UniqueConstraint(
                fields=["assignment", "student"],
                name="unique_assignment_submission_per_student",
            )
        ]

    def __str__(self):
        return f"{self.student.username} - {self.assignment.title}"