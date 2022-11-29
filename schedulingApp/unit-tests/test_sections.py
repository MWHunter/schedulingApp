from django.test import TestCase
from schedulingApp.models import Section


# Fields: course, title, assignedTA
class TestInit(TestCase):
    def setUp(self) -> None:
        pass  # TODO set up model course for valid foreign key
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
        pass  # TODO


class TestDelete(TestCase): # TODO not entirely sure on del
    s = None
    def setUp(self): # TODO
        self.s = Section("CS361", "Fall 2022")
        # self.s.course = "CS361"   # TODO make this a course foreign key
        self.s.title = "361-01"
    def test_sectionNotFound(self):
        with self.assertRaises(NameError, msg="Trying to delete nonexistent Section should throw NameError"):
            self.s2.delete()

    def test_validAndExistingSection(self):
        self.s.delete()
        with self.assertRaises(AttributeError, msg="Field course Still exists after deletion"):
            self.assertNotEqual(self.s.course, "CS361", msg="No Change to course field after deletion")
        with self.assertRaises(AttributeError, msg="Field title Still exists after deletion"):
            self.assertNotEqual(self.s.title, "361-01", msg="No Change to title field after deletion")


class TestGetters(TestCase):
    s = None
    c = "CS361"
    t = "361-01"
    def setUp(self): # TODO
        self.s = Section(self.course, self.title)
        # self.s.course = "CS361"   # TODO make this a course foreign key
        self.s.title = "361-01"

    def test_getCourseArgs(self):
        with self.assertRaises(TypeError, msg="Too many arguments (1) fails to raise TypeError"):
            self.s.getCourse("arg")

    def test_getCourseValid(self):
        self.assertEqual(self.s.getCourse(), "CS361", msg="getCourse does not return proper course")

    def test_getTitleArgs(self):
        with self.assertRaises(TypeError, msg="Too many arguments (1) fails to raise TypeError"):
            self.s.getTitle("arg")

    def test_getTitleValid(self):
        self.assertEqual(self.s.getTitle(), "CS361", msg="getTitle does not return proper course")

    def test_getTAsArgs(self):
        pass  # TODO outside the scope of current sprint

    def test_getTAsValid(self):
        pass  # TODO outside the scope of current sprint


class TestSetters(TestCase):
    s = None
    c = "CS361"
    t = "361-01"

    def setUp(self):  # TODO
        self.s = Section(self.course, self.title)
        # self.s.course = "CS361"   # TODO make this a course foreign key
        self.s.title = "361-01"

    def test_setCourseNoArgs(self):
        with self.assertRaises(TypeError, msg="Too few arguments (0) fails to raise TypeError"):
            self.s.setCourse()

    def test_setCourseTwoArgs(self):
        with self.assertRaises(TypeError, msg="Too many arguments (2) fails to raise TypeError"):
            self.s.setCourse("newCourse", "arg2")

    def test_setCourseValid(self):
        self.s.setCourse("newCourse")
        self.assertEqual(self.s.course, "newCourse", msg="setCourse does not set the course properly")

    def test_setTitleNoArgs(self):
        with self.assertRaises(TypeError, msg="Too few arguments (0) fails to raise TypeError"):
            self.s.setTitle()

    def test_setTitleTwoArgs(self):
        with self.assertRaises(TypeError, msg="Too many arguments (2) fails to raise TypeError"):
            self.s.setTitle("newTitle", "arg2")

    def test_setTitleValid(self):
        self.s.setTitle("newTitle")
        self.assertEqual(self.s.course, "newTitle", msg="setTitle does not set the title properly")

    # TODO Following methods are outside the scope of the current sprint
    def test_addTANoArgs(self):
        pass

    def test_addTATwoArgs(self):
        pass

    def test_addTAValid(self):
        pass

    def test_removeTANoArgs(self):
        pass

    def test_removeTATwoArgs(self):
        pass

    def test_removeTAValid(self):
        pass
