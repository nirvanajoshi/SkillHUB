from django.conf import settings
from django.db import models


class LessonProgress(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="lesson_progress",
    )

    lesson = models.ForeignKey(
        "courses.Lesson",
        on_delete=models.CASCADE,
        related_name="progress_records",
    )

    is_completed = models.BooleanField(default=False)

    watched_seconds = models.PositiveIntegerField(
        default=0,
        help_text="Number of seconds of video/content completed.",
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    last_accessed_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-last_accessed_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["student", "lesson"],
                name="unique_student_lesson_progress",
            )
        ]

    def __str__(self):
        return f"{self.student.username} - {self.lesson.title}"