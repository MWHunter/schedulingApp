from django.core.exceptions import ValidationError, PermissionDenied
from django.test import TestCase
from schedulingApp.models import Section, Course, Profile, User
from unittest import mock


# Fields: course, title, assignedTA
class TestInit(TestCase):
    course = None
    title = "CS361-01"
    profile = None

    def setUp(self) -> None:
        self.course = Course(title="CS361", semester="FA22")
        user = User()
        self.profile = Profile(user=user, phoneNumber="123456789", homeAddress="Here", permission=Profile.TA)

    def test_validArgs(self):
        s = LabSection(course=self.course, title=self.title, assignedTA=self.profile)
        self.assertEqual(s.course, self.course, msg="Course not properly set in constructor")
        self.assertEqual(s.title, self.title, msg="Title not properly set in constructor")

    def test_invalidCourse(self):
        with self.assertRaises(ValueError, msg="Invalid Course fails to raise ValueError"):
            s = LabSection(course="course", title=self.title, assignedTA=self.profile)

    def test_blankTitle(self):
        with self.assertRaises(ValidationError, msg="Invalid Title fails to raise ValidationError"):
            s = LabSection(course=self.course, title="", assignedTA=self.profile)
            s.full_clean()  # Note: is for validation

    def test_invalidTA(self):
        with self.assertRaises(ValueError, msg="Invalid Title fails to raise ValueError"):
            s = LabSection(course=self.course, title=self.title, assignedTA="TA")


class TestDelete(TestCase):
    course = None
    title = "CS361-01"
    profile = None
    section = None

    def setUp(self) -> None:
        self.course = Course(title="CS361", semester="FA22")
        user = User()
        self.profile = Profile(user=user, phoneNumber="123456789", homeAddress="Here", permission=Profile.TA)
        self.section = LabSection(course=self.course, title=self.title, assignedTA=self.profile)

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
    profile = None
    section = None

    def setUp(self) -> None:
        self.course = Course(title="CS361", semester="FA22")
        user = User()
        self.profile = Profile(user=user, phoneNumber="123456789", homeAddress="Here", permission=Profile.TA)
        self.section = LabSection(course=self.course, title=self.title, assignedTA=self.profile)

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

    def test_getTAValid(self):
        self.assertEqual(self.section.getTA(), self.profile, msg="getTA does not return proper TA")


class TestSetters(TestCase):
    course = None
    title = "CS361-01"
    profile = None
    section = None
    course2 = None
    title2 = "CS431-01"
    profile2 = None

    def setUp(self) -> None:
        self.course = Course(title="CS361", semester="FA22")
        user = User()
        self.profile = Profile(user=user, phoneNumber="123456789", homeAddress="Here", permission=Profile.TA)
        self.section = LabSection(course=self.course, title=self.title, assignedTA=self.profile)

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

    def test_setTAInvalid(self):
        with self.assertRaises(ValueError, msg="Setting TA to invalid value should raise ValueError"):
            self.section.setTA(None)

            
class TestUserAssignmentInstructor(TestCase):
    course = None
    title = "CS361-01"
    profile = None
    profProfile = None
    section = None
    course2 = None
    title2 = "CS431-01"
    profile2 = None

    def setUp(self) -> None:
        theProf = User()
        self.profProfile = Profile(user=theProf, phoneNumber="2345678900", homeAddress="Easy st", permission=Profile.PROFESSOR)
        self.course = Course(title="CS361", semester="FA22")

        user = User()
        self.profile = Profile(user=user, phoneNumber="123456789", homeAddress="Here", permission=Profile.TA)
        self.section = Section(course=self.course, title=self.title, assignedTA=self.profile)

        self.course2 = Course(title="CS431", semester="SP23")
        user2 = User()
        self.profile2 = Profile(user=user2, phoneNumber="987654321", homeAddress="There", permission=Profile.TA)

    def test_assignTAValid(self):
        self.assertEqual(Profile.PROFESSOR, self.profProfile.PermissionLevel,
                         msg="Professor does not have correct permissions level")
        self.section.setTA(self.profile2)
        self.assertEqual(self.section.assignedTA, self.profile2, msg="setTA does not set the TA properly")

    def test_setTAInvalidPermission(self):
        self.profProfile.PermissionLevel = Profile.TA
        self.assertEquals(self.profProfile.permission, Profile.TA,
                          msg="Professor profile needs to have TA permissions for failing test")
        with self.assertRaises(PermissionDenied, msg="Assigned user with TA permissions shouldn't be able to add users"):
            self.section.setTA(self.profile2)

    def test_setTANotAssignedToCourse(self):
        self.assertFalse(self.profProfile in self.course.getAllProfiles(),
                        msg="Professor should not be assigned to course for non-assigned test")
        self.assertEqual(Profile.PROFESSOR, self.profProfile.PermissionLevel,
                         msg="Professor does not have correct permissions level")
        with self.assertRaises(PermissionDenied,
                               msg="User with correct permissions but not assigned to course should not be able to assign TA"):
            self.section.setTA(self.profile2)

    def test_setTANotAssignedInvalidPermissions(self):
        self.profProfile.PermissionLevel = Profile.TA
        self.assertEquals(self.profProfile.permission, Profile.TA,
                          msg="Professor profile needs to have TA permissions for failing test")
        self.assertFalse(self.profProfile in self.course.getAllProfiles(),
                        msg="Professor should not assigned to course for non-assigned test")
        with self.assertRaises(PermissionDenied,
                               msg="User with TA permissions and not assigned to course should not be able to assign TA"):
            self.section.setTA(self.profile2)

    def test_setTAAlreadyAssigned(self):
        self.section.setTA(self.profile)
        self.assertEquals(self.profile, self.section.assignedTA,
                        msg="TA needs to be assigned to section before testing adding duplicate")
        self.assertRaises(ValidationError, self.section.setTA(self.profile),
                          msg="Allows assignment of same TA twice to one section")

