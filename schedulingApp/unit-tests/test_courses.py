from django.core.exceptions import ValidationError
from django.test import TestCase
from schedulingApp.models import Course, Profile, User


# Fields: Title
class CreateCourse(TestCase):
    def test_noArgs(self):
        with self.assertRaises(ValidationError,
                               msg="Should raise ValidationError for no arguments, requires a title and semester"):
            a = Course()
            a.full_clean()

    def test_oneArg(self):
        with self.assertRaises(ValidationError,
                               msg="Should raise ValidationError for only one argument, requires a title and semester"):
            a = Course(title="CS361")
            a.full_clean()
    def test_validInfo(self):
        a = Course(title="CS361", semester="FA22")
        self.assertEqual(a.title, "CS361", msg="Course did not successfully create with a valid title.")
        self.assertEqual(a.semester, "FA22", msg="Course did not successfully create with a valid semester")

    def test_threeArgs(self):
        with self.assertRaises(ValidationError, msg="Should raise TypeError for three arguments, should only take two."):
            a = Course("CS361", "FA22", "Spring 2023")
            a.full_clean()

    def test_emptyTitle(self):
        with self.assertRaises(ValidationError,
                               msg="Should raise ValidationError for empty string title, should require a non-empty title"):
            a = Course(title="", semester="FA22")
            a.full_clean()

    def test_emptySemester(self):
        with self.assertRaises(ValidationError, msg="Should raise ValueError for empty string semester, should require a "
                                               "non-empty semester"):
            a = Course(title="CS361", semester="")
            a.full_clean()

    def test_conflictingCourse(self):
        a = Course("CS361", "FA22")
        with self.assertRaises(ValidationError, msg="Course with duplicate name and semester should not be allowed."):
            b = Course("CS361", "FA22")
            b.full_clean()


class EditCourse(TestCase):
    theCourse = Course(title="CS361", semester="FA22")

    # testing title changes
    def test_blankTitle(self):
        with self.assertRaises(TypeError, msg="Calling setTitle with no argument should throw TypeError"):
            self.theCourse.setTitle()

    def test_invalidTitle(self):
        with self.assertRaises(ValidationError,msg="Changing semester name to a blank string should throw ValidationError"):
                self.theCourse.setTitle("")
                self.theCourse.full_clean()

    def test_titleChange(self):
        print(self.theCourse.getTitle)
        self.theCourse.setTitle("CS423")
        self.assertEqual(self.theCourse.getTitle(), "CS423", msg="Changing to a valid new title not successful")

    def test_titleNoChange(self):
        self.theCourse.setTitle("CS361")
        self.assertEqual(self.theCourse.getTitle(), "CS361",
                         msg="Changing title to the currently set title should cause no change to the course")

    # testing semester changes
    def test_blankSemester(self):
        with self.assertRaises(TypeError, msg="Calling setSemester with no argument should throw TypeError"):
            self.theCourse.setSemester()

    def test_invalidSemester(self):
        with self.assertRaises(ValidationError, msg="Changing semester name to a blank string should throw ValidationError"):
            self.theCourse.setSemester("")
            self.theCourse.full_clean()


    def test_semesterChange(self):
        self.theCourse.setSemester("Spring 2023")
        self.assertEqual(self.theCourse.getSemester(), "Spring 2023",
                         msg="Changing to a valid new semester not successful")

    def test_semesterNoChange(self):
        self.theCourse.setSemester("Fall 2022")
        self.assertEqual(self.theCourse.getSemester(), "Fall 2022",
                         msg="Changing semester to the currently set semester should cause no change to the course")

    # general course change tests
    def test_conflictingCourse(self):
        self.setUp()
        a = Course("CS423", "Fall 2022")
        a.title = "CS423"
        a.semester = "Fall 2022"
        a.setTitle("CS361")
        self.assertFalse(a.title == "CS361",
                         msg="Should not allow multiple courses with the same semester and title")

    def test_sameNameDifferentSemester(self):
        self.setUp()
        a = Course("CS423", "Spring 2023")
        a.title = "CS423"
        a.semester = "Spring 2023"
        a.setTitle("CS361")
        self.assertEqual(a.title, "CS361",
                         msg="Should update to the same name as a different course as long as semesters are different.")


class DeleteCourse(TestCase):
    theCourse = Course(title="CS361", semester="FA22")

    def test_courseNotFound(self):
        with self.assertRaises(NameError, msg="Trying to delete nonexistent course should throw NameError"):
            del self.myCourse

    def test_validAndExistingCourse(self):
        del self.theCourse
        with self.assertRaises(NameError, msg="Title for deleted course should no longer exist."):
            self.theCourse.getTitle()
        with self.assertRaises(NameError, msg="Semester for deleted course should no longer exist."):
            self.theCourse.getSemester()


class AssignUsers(TestCase):
    course = None
    title = "CS361"
    semester = "FA22"
    profile = None
    profile2 = None

    def setUp(self) -> None:
        self.course = Course(title=self.title, semester=self.semester)
        user = User()
        self.profile = Profile(user=user, phoneNumber="123456789", homeAddress="Here", permission=Profile.PROFESSOR)
        user2 = User()
        self.profile2 = Profile(user=user2, phoneNumber="987654321", homeAddress="There", permission=Profile.TA)

    def test_validAdd(self):
        pass

    def test_addContainedProfile(self):
        pass

    def test_addAdmin(self):
        pass

    def test_validDelete(self):
        pass

    def test_deleteNotContainedProfile(self):
        pass
