from django.test import SimpleTestCase

from .models import CourseProgress


class CourseProgressTests(SimpleTestCase):
    def test_calculate_progress_averages_available_activity_types(self):
        progress = CourseProgress(
            completed_lessons=3,
            total_lessons=4,
            completed_quizzes=1,
            total_quizzes=2,
        )

        self.assertEqual(progress.calculate_progress(), 62.5)

    def test_calculate_progress_does_not_exceed_one_hundred(self):
        progress = CourseProgress(completed_lessons=8, total_lessons=4)

        self.assertEqual(progress.calculate_progress(), 100)
