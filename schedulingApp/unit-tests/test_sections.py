from django.core.exceptions import ValidationError
from django.test import TestCase
from schedulingApp.models import Section, Course, User, Profile
from unittest import mock


# Fields: course, title, assignedTA
class TestInit(TestCase):
    course = None
    title = "CS361-01"
    time = "5:30PM"
    profile = None

    def setUp(self) -> None:
        self.course = Course(title="CS361", semester="FA22")

    def test_validArgs(self):
        s = Section(course=self.course, title=self.title, time=self.time)
        self.assertEqual(s.course, self.course, msg="Course not properly set in constructor")
        self.assertEqual(s.title, self.title, msg="Title not properly set in constructor")
        self.assertEqual(s.time, self.time, msg="Title not properly set in constructor")

    def test_invalidCourse(self):
        with self.assertRaises(ValueError, msg="Invalid Course fails to raise ValueError"):
            s = Section(course="course", title=self.title, time=self.time)

    def test_blankTitle(self):
        with self.assertRaises(ValidationError, msg="Invalid Title fails to raise ValidationError"):
            s = Section(course=self.course, title="", time=self.time)
            s.full_clean()  # Note: is for validation

    def test_invalidTime(self):
        with self.assertRaises(ValueError, msg="Invalid TA fails to raise ValueError"):
            s = Section(course=self.course, title=self.title, time=5.30)


class TestDelete(TestCase):
    course = None
    title = "CS361-01"
    time = "5:30"
    section = None

    def setUp(self) -> None:
        self.course = Course(title="CS361", semester="FA22")
        self.section = Section(course=self.course, title=self.title, time=self.time)

    def test_sectionNotFound(self):
        with self.assertRaises(NameError, msg="Trying to delete nonexistent Section should throw NameError"):
            del section2

    def test_validAndExistingSection(self):
        del self.section
        with self.assertRaises(AttributeError, msg="Field course Still exists after deletion"):
            self.assertNotEqual(self.section.course, self.c, msg="No Change to course field after deletion")
        with self.assertRaises(AttributeError, msg="Field title Still exists after deletion"):
            self.assertNotEqual(self.section.title, "361-01", msg="No Change to title field after deletion")


class TestGetters(TestCase):
    course = None
    title = "CS361-01"
    time = "5:30"
    profile = None
    section = None

    def setUp(self) -> None:
        self.course = Course(title="CS361", semester="FA22")
        self.section = Section(course=self.course, title=self.title, time=self.time)

    def test_getCourseArgs(self):
        with self.assertRaises(TypeError, msg="Too many arguments (1) fails to raise TypeError"):
            self.section.getCourse("arg")

    def test_getCourseValid(self):
        self.assertEqual(self.section.getCourse(), self.course, msg="getCourse does not return proper course")

    def test_getTitleArgs(self):
        with self.assertRaises(TypeError, msg="Too many arguments (1) fails to raise TypeError"):
            self.section.getTitle("arg")

    def test_getTitleValid(self):
        self.assertEqual(self.section.getTitle(), self.title, msg="getTitle does not return proper course")

    def test_getTAArgs(self):
        with self.assertRaises(TypeError, msg="Too many arguments (1) fails to raise TypeError"):
            self.section.getTA("arg")

    #def test_getTAValid(self):
    #    self.assertEqual(self.section.getTA(), self.profile, msg="getTA does not return proper TA")
    
    def test_addDiscussionSection(self):
        s = Section(course=self.course, title=self.title, time=self.time, labType=Section.DISCUSSION)
        self.assertEqual(s.course, self.course, msg="Course not properly set in constructor")
        self.assertEqual(s.title, self.title, msg="Title not properly set in constructor")
        self.assertEqual(s.labType, Section.DISCUSSION, msg="Section not created with Discussion type")

class TestSetters(TestCase):
    course = None
    title = "CS361-01"
    time = "5:30"
    profile = None
    section = None
    course2 = None
    title2 = "CS431-01"
    profile2 = None

    def setUp(self) -> None:
        self.course = Course(title="CS361", semester="FA22")
        user = User()
        self.profile = Profile(user=user, phoneNumber="123456789", homeAddress="Here", permission=Profile.TA)
        self.section = Section(course=self.course, title=self.title, time=self.time)

        self.course2 = Course(title="CS431", semester="SP23")
        user2 = User()
        self.profile2 = Profile(user=user2, phoneNumber="987654321", homeAddress="There", permission=Profile.TA)

    def test_setCourseNoArgs(self):
        with self.assertRaises(TypeError, msg="Too few arguments (0) fails to raise TypeError"):
            self.section.setCourse()

    def test_setCourseTwoArgs(self):
        with self.assertRaises(TypeError, msg="Too many arguments (2) fails to raise TypeError"):
            self.section.setCourse(self.course2, "arg2")

    def test_setCourseValid(self):
        self.section.setCourse(self.course2)
        self.assertEqual(self.section.course, self.course2, msg="setCourse does not set the course properly")

    def test_setCourseInvalid(self):
        with self.assertRaises(ValueError, msg="Setting course to invalid value should raise ValueError"):
            self.section.setCourse(None)

    def test_setTitleNoArgs(self):
        with self.assertRaises(TypeError, msg="Too few arguments (0) fails to raise TypeError"):
            self.section.setTitle()

    def test_setTitleTwoArgs(self):
        with self.assertRaises(TypeError, msg="Too many arguments (2) fails to raise TypeError"):
            self.section.setTitle(self.title2, "arg2")

    def test_setTitleValid(self):
        self.section.setTitle(self.title2)
        self.assertEqual(self.section.title, self.title2, msg="setTitle does not set the title properly")

    def test_setTitleInvalid(self):
        with self.assertRaises(ValueError, msg="Setting title to invalid value should raise ValueError"):
            self.section.setTitle("")

    def test_setTANoArgs(self):
        with self.assertRaises(TypeError, msg="Too few arguments (0) fails to raise TypeError"):
            self.section.setTA()

    def test_setTATwoArgs(self):
        with self.assertRaises(TypeError, msg="Too many arguments (2) fails to raise TypeError"):
            self.section.setTA(self.profile2, "arg2")

    def test_setTAValid(self):
        self.section.setTA(self.profile2)
        self.assertEqual(self.section.assignedTA, self.profile2, msg="setTA does not set the TA properly")

    # def test_setTAInvalid(self):
    #     with self.assertRaises(ValueError, msg="Setting TA to invalid value should raise ValueError"):
    #         self.section.setTA(None)
