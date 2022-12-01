from django.test import TestCase
from schedulingApp.models import LabSection, Course, User
from unittest import mock


# Fields: course, title, assignedTA
class TestInit(TestCase):
    c = None

    def setUp(self) -> None:
        self.c = Course.objects.create("CS361")

    def test_noArgs(self):
        with self.assertRaises(TypeError, msg="Too few arguments (0) fails to raise TypeError"):
            s = LabSection()

    def test_oneArgs(self):
        with self.assertRaises(TypeError, msg="Too few arguments (1) fails to raise TypeError"):
            s = LabSection("Course")

    def test_validArgs(self):
        s = LabSection(self.c, "Title")
        self.assertEqual(s.course, self.c, msg="Course not properly set in constructor")
        self.assertEqual(s.title, "Title", msg="Title not properly set in constructor")

    def test_threeArgs(self):
        with self.assertRaises(TypeError, msg="Too many arguments (3) fails to raise TypeError"):
            s = LabSection("Course", "Title", "Arg3")

    def test_blankCourse(self):
        with self.assertRaises(ValueError, msg="Invalid Course fails to raise ValueError"):
            s = LabSection("\0", "Title")

    def test_blankTitle(self):
        with self.assertRaises(ValueError, msg="Invalid Title fails to raise ValueError"):
            s = LabSection("Course", "\0")


class TestDelete(TestCase):
    c = None
    s = None

    def setUp(self): # TODO
        self.c = Course.objects.create("CS361")
        self.s = LabSection("CS361", "Fall 2022")
        self.s.course = self.c
        self.s.title = "361-01"

    def test_sectionNotFound(self):
        with self.assertRaises(NameError, msg="Trying to delete nonexistent Section should throw NameError"):
            self.s2.delete()

    def test_validAndExistingSection(self):
        self.s.delete()
        with self.assertRaises(AttributeError, msg="Field course Still exists after deletion"):
            self.assertNotEqual(self.s.course, self.c, msg="No Change to course field after deletion")
        with self.assertRaises(AttributeError, msg="Field title Still exists after deletion"):
            self.assertNotEqual(self.s.title, "361-01", msg="No Change to title field after deletion")


class TestGetters(TestCase):
    s, c, ta = None
    t = "361-01"

    def setUp(self): # TODO
        self.c = Course.objects.create("CS361")
        self.ta = User.objects.create("firstName", "lastName", "password", "emailAddress", "homeAddress", "phoneNumber", User.PermissionLevel[0])
        self.s = LabSection(self.c, self.title)
        self.s.course = self.c
        self.s.title = "361-01"

    def test_getCourseArgs(self):
        with self.assertRaises(TypeError, msg="Too many arguments (1) fails to raise TypeError"):
            self.s.getCourse("arg")

    def test_getCourseValid(self):
        self.assertEqual(self.s.getCourse(), self.c, msg="getCourse does not return proper course")

    def test_getTitleArgs(self):
        with self.assertRaises(TypeError, msg="Too many arguments (1) fails to raise TypeError"):
            self.s.getTitle("arg")

    def test_getTitleValid(self):
        self.assertEqual(self.s.getTitle(), "361-01", msg="getTitle does not return proper course")

    def test_getTAArgs(self):
        with self.assertRaises(TypeError, msg="Too many arguments (1) fails to raise TypeError"):
            self.s.getTA("arg")

    def test_getTAValid(self):
        self.assertEqual(self.s.getTA(), self.ta, msg="getTA does not return proper TA")


class TestSetters(TestCase):
    s, c, c2, ta, ta2 = None
    t = "361-01"

    def setUp(self):
        self.c = Course.objects.create("CS361")
        self.c2 = Course.objects.create("CS431")
        self.ta = User.objects.create("firstName", "lastName", "password", "emailAddress", "homeAddress", "phoneNumber", User.PermissionLevel[0])
        self.ta2 = User.objects.create("firstName2", "lastName2", "password2", "emailAddress2", "homeAddress2", "phoneNumber2", User.PermissionLevel[0])
        self.s = LabSection(self.c, self.title)
        self.s.course = self.c
        self.s.assignedTA = self.ta
        self.s.title = "361-01"

    def test_setCourseNoArgs(self):
        with self.assertRaises(TypeError, msg="Too few arguments (0) fails to raise TypeError"):
            self.s.setCourse()

    def test_setCourseTwoArgs(self):
        with self.assertRaises(TypeError, msg="Too many arguments (2) fails to raise TypeError"):
            self.s.setCourse(self.c2, "arg2")

    def test_setCourseValid(self):
        self.s.setCourse(self.c2)
        self.assertEqual(self.s.course, self.c2, msg="setCourse does not set the course properly")

    def test_setTitleNoArgs(self):
        with self.assertRaises(TypeError, msg="Too few arguments (0) fails to raise TypeError"):
            self.s.setTitle()

    def test_setTitleTwoArgs(self):
        with self.assertRaises(TypeError, msg="Too many arguments (2) fails to raise TypeError"):
            self.s.setTitle("newTitle", "arg2")

    def test_setTitleValid(self):
        self.s.setTitle("newTitle")
        self.assertEqual(self.s.course, "newTitle", msg="setTitle does not set the title properly")

    def test_setTANoArgs(self):
        with self.assertRaises(TypeError, msg="Too few arguments (0) fails to raise TypeError"):
            self.s.setTA()

    def test_setTATwoArgs(self):
        with self.assertRaises(TypeError, msg="Too many arguments (2) fails to raise TypeError"):
            self.s.setTA(self.ta2, "arg2")

    def test_setTAValid(self):
        self.s.setTA(self.c2)
        self.assertEqual(self.s.course, self.ta2, msg="setTA does not set the TA properly")
