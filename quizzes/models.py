from django.conf import settings
from django.db import models


class Quiz(models.Model):
    lesson = models.ForeignKey(
        "courses.Lesson",
        on_delete=models.CASCADE,
        related_name="quizzes",
    )

    title = models.CharField(max_length=200)

    description = models.TextField(blank=True)

    time_limit = models.PositiveIntegerField(
        default=30,
        help_text="Time limit in minutes.",
    )

    passing_score = models.PositiveIntegerField(
        default=50,
        help_text="Minimum percentage required to pass.",
    )

    is_published = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name="questions",
    )

    question_text = models.TextField()

    marks = models.PositiveIntegerField(default=1)

    question_number = models.PositiveIntegerField()

    class Meta:
        ordering = ["question_number"]

        constraints = [
            models.UniqueConstraint(
                fields=["quiz", "question_number"],
                name="unique_question_number_per_quiz",
            )
        ]

    def __str__(self):
        return f"{self.quiz.title} - Question {self.question_number}"


class Option(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="options",
    )

    option_text = models.CharField(max_length=500)

    is_correct = models.BooleanField(default=False)

    option_number = models.PositiveIntegerField()

    class Meta:
        ordering = ["option_number"]

        constraints = [
            models.UniqueConstraint(
                fields=["question", "option_number"],
                name="unique_option_number_per_question",
            )
        ]

    def __str__(self):
        return self.option_text


class Attempt(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="quiz_attempts",
    )

    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name="attempts",
    )

    score = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
    )

    passed = models.BooleanField(default=False)

    started_at = models.DateTimeField(
        auto_now_add=True,
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["-started_at"]

    def __str__(self):
        return f"{self.student.username} - {self.quiz.title}"


class Answer(models.Model):
    attempt = models.ForeignKey(
        Attempt,
        on_delete=models.CASCADE,
        related_name="answers",
    )

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="answers",
    )

    selected_option = models.ForeignKey(
        Option,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="selected_answers",
    )

    is_correct = models.BooleanField(default=False)

    marks_awarded = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["attempt", "question"],
                name="unique_question_answer_per_attempt",
            )
        ]

    def __str__(self):
        return f"{self.attempt} - {self.question}"