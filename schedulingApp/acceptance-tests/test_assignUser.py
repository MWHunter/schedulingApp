from django.contrib.auth.models import User
from django.test import TestCase, Client
from schedulingApp.models import Course, Section, Profile, CourseToAssignedUserEntry, SectionToAssignedUserEntry


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
        self.resp = self.monkey.post("/add_user_to_course/" + str(self.course.id) +"/"+str(self.profileTA.id), HTTP_REFERER='http://foo/bar')
        courseToUser = CourseToAssignedUserEntry.objects.get(course=self.course)
        self.assertEqual(courseToUser.course, self.course, msg="Course does not match in course to assigned user entry")
        self.assertEqual(courseToUser.assignedUser, self.profileTA, msg="Profile does not match in course to assigned user entry")
        self.assertEqual(len(CourseToAssignedUserEntry.objects.filter(course=self.course)), 1, msg="Too many course to assigned user entries are being made")

    def test_invalidCourse(self):
        with self.assertRaises(Course.DoesNotExist, msg="Course to assigned user entry made upon invalid course name"):
            self.resp = self.monkey.post("/add_user_to_course/" + str(0) +"/"+str(self.profileTA.id), HTTP_REFERER='http://foo/bar')

    def test_invalidUser(self):
        with self.assertRaises(Profile.DoesNotExist, msg="Course to assigned user entry made upon invalid user email"):
            self.resp = self.monkey.post("/add_user_to_course/" + str(self.course.id) +"/"+str(0), HTTP_REFERER='http://foo/bar')


class TestAssignUserToSection(TestCase):

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

        self.section = Section(course=self.course, title="CS361-01", time="5:30")
        self.section.save()

        self.taUser = User.objects.create_user(username="test", password="TA")
        self.taUser.save()
        self.profileTA = Profile.objects.get(user=self.taUser)
        self.profileTA.permission = Profile.TA
        self.profileTA.save()

        self.profUser = User.objects.create_user(username="testProf", password="Prof")
        self.profUser.save()
        self.profileProf = Profile.objects.get(user=self.profUser)
        self.profileProf.permission = Profile.PROFESSOR
        self.profileProf.save()

        self.profMonkey = Client()
        self.profMonkey.force_login(self.profUser)

    def test_addTAtoSection(self):
        # Assign TA and Prof to course as Admin
        self.resp = self.monkey.post("/add_user_to_course/" + str(self.course.id) +"/"+str(self.profileTA.id), HTTP_REFERER='http://foo/bar')
        self.assertEqual(CourseToAssignedUserEntry.objects.get(assignedUser=self.profileTA).assignedUser, self.profileTA, msg="Profile does not match in course to assigned user entry")
        self.assertEqual(len(CourseToAssignedUserEntry.objects.filter(course=self.course)), 1, msg="Too many course to assigned user entries are being made")

        self.resp = self.monkey.post("/add_user_to_course/" + str(self.course.id) +"/"+str(self.profileProf.id), HTTP_REFERER='http://foo/bar')
        self.assertEqual(CourseToAssignedUserEntry.objects.get(assignedUser=self.profileProf).assignedUser, self.profileProf, msg="Profile does not match in course to assigned user entry")
        self.assertEqual(len(CourseToAssignedUserEntry.objects.filter(course=self.course)), 2, msg="Too many course to assigned user entries are being made")

        self.resp = self.monkey.post("/add_user_to_section/" + str(self.section.id) +"/"+str(self.profileTA.id), HTTP_REFERER='http://foo/bar')
        self.assertEqual(SectionToAssignedUserEntry.objects.get(assignedUser=self.profileTA).assignedUser, self.profileTA, msg="Profile does not match in course to assigned user entry")
        self.assertEqual(len(SectionToAssignedUserEntry.objects.filter(section=self.section)), 1, msg="Too many course to assigned user entries are being made")

    def test_profNotInCourse(self):
        # Assign TA to course as Admin
        self.resp = self.monkey.post("/add_user_to_course/" + str(self.course.id) +"/"+str(self.profileTA.id), HTTP_REFERER='http://foo/bar')
        self.assertEqual(CourseToAssignedUserEntry.objects.get(assignedUser=self.profileTA).assignedUser, self.profileTA, msg="Profile does not match in course to assigned user entry")
        self.assertEqual(len(CourseToAssignedUserEntry.objects.filter(course=self.course)), 1, msg="Too many course to assigned user entries are being made")

        # Assign TA and to section as Prof
        self.resp = self.profMonkey.post("/add_user_to_section/" + str(self.section.id) +"/"+str(self.profileTA.id), HTTP_REFERER='http://foo/bar')
        self.assertEqual(len(SectionToAssignedUserEntry.objects.filter(section=self.section)), 0, msg="Section to User being made when Prof is not in course")

    def test_TAnotInCourse(self):
        # Assign Prof to course as Admin
        self.resp = self.monkey.post("/add_user_to_course/" + str(self.course.id) +"/"+str(self.profileProf.id), HTTP_REFERER='http://foo/bar')
        self.assertEqual(CourseToAssignedUserEntry.objects.get(assignedUser=self.profileProf).assignedUser, self.profileProf, msg="Profile does not match in course to assigned user entry")
        self.assertEqual(len(CourseToAssignedUserEntry.objects.filter(course=self.course)), 1, msg="Too many course to assigned user entries are being made")

        # Assign TA and to section as Prof
        self.resp = self.profMonkey.post("/add_user_to_section/" + str(self.section.id) +"/"+str(self.profileTA.id), HTTP_REFERER='http://foo/bar')
        self.assertEqual(len(SectionToAssignedUserEntry.objects.filter(section=self.section)), 0, msg="Section to User being made when TA is not in course")
