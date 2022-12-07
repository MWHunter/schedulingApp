from django.contrib.auth.models import User
from django.test import TestCase, Client
from schedulingApp.models import Course, Profile


def createSetUp(self):
    self.cl = Client()
    testUser = User.objects.create_user(username="user", password="pass")
    testUser.save()
    profile = Profile.objects.get(user=testUser)
    profile.permission = Profile.ADMIN
    profile.save()
    self.cl.force_login(testUser)

    for course in self.courses.keys():
        newCourse = Course(title=course, semester=self.courses[course])
        newCourse.save()


class TestAddCourseSuccessful(TestCase):
    cl = None
    courses = {'CS361': 'FA22', 'CS423': 'WI22', 'CS535': "SP23"}

    def setUp(self):
        createSetUp(self)

    def testCreateCourseSuccessful(self):
            resp = self.cl.post("/addCourse.html", {"newCourseTitle": "CS600", "newCourseSemester": Course.FALL22}, follow=True)
            #Confirms correct landing page
            self.assertEqual(resp.request['PATH_INFO'], "/courses.html", "Course creation not successful")
            #confirms this course now exists in the database.
            self.assertEqual("CS600", Course.objects.get(title="CS600", semester=Course.FALL22).getTitle(),
                             "Newly created course is not in database")
            self.assertEqual(Course.FALL22, Course.objects.get(title="CS600", semester=Course.FALL22).getSemester(),
                             "Newly created course is not in database")


class TestAddCourseUnsuccessful(TestCase):
    cl = None
    courses = {'CS361': 'FA22', 'CS423': 'WI22', 'CS535': "SP23"}

    def setUp(self):
        createSetUp(self)

    def testCreateCourseInvalidTitle(self):
        resp = self.cl.post("/addCourse.html", {"newCourseTitle": "", "newCourseSemester": Course.FALL22}, follow=True)
        self.assertEqual(resp.request['PATH_INFO'], "/addCourse.html", "Course creation proceeded to courses page with incorrect information")
        self.assertEqual(resp.context['message'], "{'title': ['This field cannot be blank.']}", "incorrect message thrown")

    def testCreateDuplicateCourse(self):
        resp = self.cl.post("/addCourse.html", {"newCourseTitle": "CS361", "newCourseSemester": "FA22"}, follow=True)
        self.assertEqual("Course already exists", resp.context['message'],
                          msg="Should not allow creation of duplicate course")

    def testTACreationAttempt(self):
        #creates TA user
        testTA = User.objects.create_user(username="theta", password="theta")
        testTA.save()
        profile = Profile.objects.get(user=testTA)
        profile.permission = Profile.TA
        profile.save()
        self.cl.force_login(testTA)

        resp = self.cl.post("/addCourse.html", {"newCourseTitle": "CS500", "newCourseSemester": Course.FALL22}, follow=True)
        self.assertEqual(resp.request['PATH_INFO'], "/", "Allows TA to create a course, should bounce user to homepage")

    def testProfessorCreationAttempt(self):
        #creates Professor user.
        testProf = User.objects.create_user(username="theprof", password="theprof")
        testProf.save()
        profile = Profile.objects.get(user=testProf)
        profile.permission = Profile.PROFESSOR
        profile.save()
        self.cl.force_login(testProf)

        resp = self.cl.post("/addCourse.html", {"newCourseTitle": "CS500", "newCourseSemester": Course.FALL22}, follow=True)
        self.assertEqual(resp.request['PATH_INFO'], "/", "Allows Instructor to create a course, should bounce user to homepage")
