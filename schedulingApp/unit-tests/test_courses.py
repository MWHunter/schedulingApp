from django.test import TestCase
from models import Course

# Fields: Title
class CreateCourse(TestCase):
    def test_noArgs(self):
        a = Course()
        self.assertRaises(TypeError, msg="Should raise TypeError for no arguments, requires a title and semester")

    def test_oneArg(self):
        a = Course("CS361")
        self.assertRaises(TypeError, msg="Should raise TypeError for only one argument, requires a title and semester")

    def test_validInfo(self):
        a = Course("CS361", "Fall 2022")
        self.assertEqual(a.title, "CS361", msg="Course did not successfully create with a valid title.")
        self.assertEqual(a.semester, "Fall 2022", msg="Course did not successfully create with a valid semester")

    def test_threeArgs(self):
        a = Course("CS361", "Fall 2022", "Spring 2023")
        self.assertRaises(TypeError, msg="Should raise TypeError for three arguments, should only take two.")

    def test_emptyTitle(self):
        a = Course("", "Fall 2022")
        self.assertRaises(ValueError,
                          msg="Should raise ValueError for empty string title, should require a non-empty title")

    def test_emptySemester(self):
        a = Course("CS361", "")
        self.assertRaises(ValueError,
                          msg="Should raise ValueError for empty string semester, should require a non-empty semester")

    def test_conflictingCourse(self):
        a = Course("CS361", "Fall 2022")
        self.assertRaises(ValueError, Course("CS361", "Fall 2022"),
                          msg="Course with duplicate name and semester should not be allowed.")


class EditCourse(TestCase):
    theCourse = None
    def setUp(self):
        theCourse = Course("CS361", "Fall 2022")
        theCourse.title = "CS361"
        theCourse.semester = "Fall 2022"
    #testing title changes
    def test_blankTitle(self):
        self.setUp()
        self.assertRaises(TypeError, self.theCourse.setTitle(),
                          msg="Calling setTitle with no argument should throw TypeError")

    def test_invalidTitle(self):
        self.setUp()
        self.assertRaises(ValueError, self.theCourse.setTitle(""),
                          msg="Changing course name to a blank string should throw ValueError")

    def test_titleChange(self):
        self.setUp()
        self.theCourse.setTitle("CS423")
        self.assertEqual(self.theCourse.getTitle(), "CS423", msg="Changing to a valid new title not successful")

    def test_titleNoChange(self):
        self.setUp()
        self.theCourse.setTitle("CS361")
        self.assertEqual(self.theCourse.getTitle(), "CS361",
                         msg="Changing title to the currently set title should cause no change to the course")
    #testing semester changes
    def test_blankSemester(self):
        self.setUp()
        self.assertRaises(TypeError, self.theCourse.setSemester(),
                          msg="Calling setSemester with no argument should throw TypeError")

    def test_invalidSemester(self):
        self.setUp()
        self.assertRaises(ValueError, self.theCourse.setSemester(""),
                          msg="Changing semester name to a blank string should throw ValueError")

    def test_semesterChange(self):
        self.setUp()
        self.theCourse.setSemester("Spring 2023")
        self.assertEqual(self.theCourse.getSemester(), "Spring 2023",
                         msg="Changing to a valid new semester not successful")

    def test_semesterNoChange(self):
        self.setUp()
        self.theCourse.setSemester("Fall 2022")
        self.assertEqual(self.theCourse.getSemester(), "Fall 2022",
                         msg="Changing semester to the currently set semester should cause no change to the course")
    #general course change tests
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
    theCourse = None
    def setUp(self):
        theCourse = Course("CS361", "Fall 2022")
        theCourse.title = "CS361"
        theCourse.semester = "Fall 2022"

    def test_courseNotFound(self):
        self.setUp()
        self.assertRaises(NameError, self.myCourse.__del__(),
                          msg="Trying to delete nonexistent course should throw NameError")

    def test_validAndExistingCourse(self):
        self.setUp()
        self.theCourse.__del__()
        self.assertFalse(self.theCourse.getTitle() == "CS361", msg="Title for deleted course should no longer exist.")
        self.assertFalse(self.theCourse.getSemester() == "Fall 2022",
                         msg="Semester for deleted course should no longer exist.")
