from django.test import TestCase
from models import Course

# Fields: Title
class CreateCourse(TestCase):
    def test_noArgs(self):
        with self.assertRaises(TypeError, msg="Should raise TypeError for no arguments, requires a title and semester"):
            a = Course()

    def test_oneArg(self):
        with self.assertRaises(TypeError, msg="Should raise TypeError for only one argument, requires a title and semester"):
            a = Course("CS361")

    def test_validInfo(self):
        a = Course("CS361", "Fall 2022")
        self.assertEqual(a.title, "CS361", msg="Course did not successfully create with a valid title.")
        self.assertEqual(a.semester, "Fall 2022", msg="Course did not successfully create with a valid semester")

    def test_threeArgs(self):
        with self.assertRaises(TypeError, msg="Should raise TypeError for three arguments, should only take two."):
            a = Course("CS361", "Fall 2022", "Spring 2023")

    def test_emptyTitle(self):
        with self.assertRaises(ValueError, msg="Should raise ValueError for empty string title, should require a non-empty title"):
            a = Course("", "Fall 2022")

    def test_emptySemester(self):
        with self.assertRaises(ValueError, msg="Should raise ValueError for empty string semester, should require a "
                                               "non-empty semester"):
            a = Course("CS361", "")

    def test_conflictingCourse(self):
        a = Course("CS361", "Fall 2022")
        with self.assertRaises(ValueError, msg="Course with duplicate name and semester should not be allowed."):
            b = Course("CS361", "Fall 2022")


class EditCourse(TestCase):
    theCourse = None

    def setUp(self):
        theCourse = Course("CS361", "Fall 2022")
        theCourse.title = "CS361"
        theCourse.semester = "Fall 2022"

    #testing title changes
    def test_blankTitle(self):
        with self.assertRaises(TypeError, msg="Calling setTitle with no argument should throw TypeError"):
            self.theCourse.setTitle()

    def test_invalidTitle(self):
        with self.assertRaises(ValueError, msg="Changing course name to a blank string should throw ValueError"):
            self.theCourse.setTitle("")

    def test_titleChange(self):
        self.theCourse.setTitle("CS423")
        self.assertEqual(self.theCourse.getTitle(), "CS423", msg="Changing to a valid new title not successful")

    def test_titleNoChange(self):
        self.theCourse.setTitle("CS361")
        self.assertEqual(self.theCourse.getTitle(), "CS361",
                         msg="Changing title to the currently set title should cause no change to the course")

    #testing semester changes
    def test_blankSemester(self):
        with self.assertRaises(TypeError, msg="Calling setSemester with no argument should throw TypeError"):
            self.theCourse.setSemester()

    def test_invalidSemester(self):
        with self.assertRaises(ValueError, msg="Changing semester name to a blank string should throw ValueError"):
            self.theCourse.setSemester("")

    def test_semesterChange(self):
        self.theCourse.setSemester("Spring 2023")
        self.assertEqual(self.theCourse.getSemester(), "Spring 2023",
                         msg="Changing to a valid new semester not successful")

    def test_semesterNoChange(self):
        self.theCourse.setSemester("Fall 2022")
        self.assertEqual(self.theCourse.getSemester(), "Fall 2022",
                         msg="Changing semester to the currently set semester should cause no change to the course")

    #general course change tests
    def test_conflictingCourse(self):
        a = Course("CS423", "Fall 2022")
        a.title = "CS423"
        a.semester = "Fall 2022"
        a.setTitle("CS361")
        self.assertFalse(a.title == "CS361",
                         msg="Should not allow multiple courses with the same semester and title")

    def test_sameNameDifferentSemester(self):
        a = Course("CS423", "Spring 2023")
        a.title = "CS423"
        a.semester = "Spring 2023"
        a.setTitle("CS361")
        self.assertEqual(a.title, "CS361",
                         msg="Should update to the same name as a different course as long as semesters are different.")



class DeleteCourse(TestCase):
    theCourse = None
    def setUp(self):
        theCourse = Course("CS361", "Fall 2022")
        theCourse.title = "CS361"
        theCourse.semester = "Fall 2022"

    def test_courseNotFound(self):
        with self.assertRaises(NameError, msg="Trying to delete nonexistent course should throw NameError"):
            del self.myCourse

    def test_validAndExistingCourse(self):
        del self.theCourse
        with self.assertRaises(NameError, msg="Title for deleted course should no longer exist."):
            self.theCourse.getTitle()
        with self.assertRaises(NameError, msg="Semester for deleted course should no longer exist."):
            self.theCourse.getSemester()

