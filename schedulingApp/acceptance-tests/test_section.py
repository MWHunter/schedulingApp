from django.test import TestCase

from schedulingApp.models import Course, Section


class DeleteSection(TestCase):
    title = "CS361-01"
    semester = "FA22"
    section = None

    def setUp(self) -> None:
        self.course = Course(title=self.title, semester=self.semester)
        self.course.save()
        self.section = Section(title=self.title, time="2:00", labType=Section.DISCUSSION, course=self.course)
        self.section.save()

    def test_validSection(self):
        self.section.delete()

        with self.assertRaises(Section.DoesNotExist):
            Section.objects.get(title=self.title)
