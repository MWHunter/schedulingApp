from django.contrib.auth.models import User
from django.test import TestCase, Client
from schedulingApp.models import Course, Profile, CourseToAssignedUserEntry

class TestAssignUserToCourse(TestCase):
    monkey = None

    def setUp(self):
        self.monkey = Client()
        testUser = User.objects.create_user(username="user", password="pass")
        testUser.save()
        profile = Profile.objects.get(user=testUser)
        profile.permission = Profile.ADMIN
        profile.save()
        self.monkey.force_login(testUser)

        self.course = Course(title='CS361', semester='FA22')
        self.course.save()
        self.taUser = User.objects.create_user(username="test", password="TA", email="testTA@uwm.edu")
        self.taUser.save()
        self.profileTA = Profile.objects.get(user=self.taUser)
        self.profileTA.permission = Profile.TA
        self.profileTA.save()

    def test_userAdded(self):
        self.resp = self.monkey.post("/assignCourseUser.html", {"course": self.course.title,
                                                                  "user": self.taUser.email})
        courseToUser = CourseToAssignedUserEntry.objects.get(course=self.course)
        self.assertEqual(courseToUser.course, self.course, msg="Course does not match in course to assigned user entry")
        self.assertEqual(courseToUser.assignedUser, self.profileTA, msg="Profile does not match in course to assigned user entry")
        self.assertEqual(len(CourseToAssignedUserEntry.objects.filter(course=self.course)), 1, msg="Too many course to assigned user entries are being made")

    def test_invalidCourse(self):
        self.resp = self.monkey.post("/assignUserToCourse.html", {"course": "",
                                                                  "user": self.taUser.email})
        with self.assertRaises(CourseToAssignedUserEntry.DoesNotExist, msg="Course to assigned user entry made upon invalid course name"):
            CourseToAssignedUserEntry.objects.get(profile=self.profileTA)

    def test_invalidUser(self):
        self.resp = self.monkey.post("/assignUserToCourse.html", {"course": self.course.title,
                                                                  "user": ""})
        with self.assertRaises(CourseToAssignedUserEntry.DoesNotExist, msg="Course to assigned user entry made upon invalid user email"):
            CourseToAssignedUserEntry.objects.get(course=self.course)
