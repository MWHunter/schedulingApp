from django.test import TestCase
from schedulingApp.models import Section


# Fields: course, title, assignedTA
class CreateSection(TestCase):
    def setUp(self) -> None:
        pass #TODO set up model course for valid foreign key
    def test_noArgs(self):
        with self.assertRaises(TypeError, msg="Too few arguments (0) fails to raise TypeError"):
            s = Section()

    def test_oneArgs(self):
        with self.assertRaises(TypeError, msg="Too few arguments (1) fails to raise TypeError"):
            s = Section("Course")

    # TODO dont know how to test foreign keys
    def test_validArgs(self):
        s = Section("Course", "Title")
        self.assertEqual(s.course, "Course", msg="Course")
        self.assertEqual(s.title, "Title")

    def test_threeArgs(self):
        with self.assertRaises(TypeError, msg="Too many arguments (3) fails to raise TypeError"):
            s = Section("Course", "Title", "Arg3")

    def test_blankCourse(self):
        with self.assertRaises(ValueError, msg="Invalid Course fails to raise ValueError"):
            s = Section("\0", "Title")

    def test_blankTitle(self):
        with self.assertRaises(ValueError, msg="Invalid Title fails to raise ValueError"):
            s = Section("Course", "\0")

    def test_nonExistantCourse(self):
        pass #TODO


class EditSection(TestCase):
    def test_blankFields(self):
        pass

    def test_invalidCourse(self):
        pass

    def test_invalidTitle(self):
        pass

    def test_invalidTA(self):
        pass

    def test_toConflictingName(self):
        pass

    def test_toTAWithConflictingTime(self):
        pass

    def test_noChange(self):
        pass

    def test_validEditAllFields(self):
        pass


class DeleteSection(TestCase):
    def test_sectionNotFound(self):
        pass

    def test_validAndExistingSection(self):
        pass
