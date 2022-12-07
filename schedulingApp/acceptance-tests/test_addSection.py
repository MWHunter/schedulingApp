from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.test import TestCase, Client

from schedulingApp.models import Profile, LabSection, Course


class TestAddUser(TestCase):
    monkey = None

    def setUp(self):
        self.monkey = Client()
        testUser = User.objects.create_user(username="user", password="pass")
        testUser.save()
        profile = Profile.objects.get(user=testUser)
        profile.permission = Profile.ADMIN
        profile.save()
        self.monkey.force_login(testUser)

        course = Course(title='CS361', semester='FA22')
        course.save()
        taUser = User.objects.create_user(username="test", password="TA", email="testTA@uwm.edu")
        taUser.save()
        profileTA = Profile.objects.get(user=taUser)
        profileTA.permission = Profile.TA
        profileTA.save()

        self.resp = self.monkey.post("/addSection.html", {"sectionType": LabSection.LAB,
                                                          "newSectionNumber": "001",
                                                          "newSectionTime": "9:30AM",
                                                          "newSectionAssignedCourse": course.title,
                                                          "newSectionInstructor": taUser.email})

        self.sectionCreated = LabSection.objects.get(title="001")


    def testTitle(self):
        self.assertEqual(self.sectionCreated.title, "001")

    def testSectionType(self):
        self.assertEqual(self.sectionCreated.labType, LabSection.LAB, "section type not set properly")

    def tesSectionTime(self):
        self.assertEqual(self.sectionCreated.time, "9:30AM", "time not set properly")

    def testCourse(self):
        self.assertEqual(self.sectionCreated.course, Course.objects.get(title="CS361"), "course not set properly")

    def testInstructor(self):
        self.assertEqual(self.sectionCreated.assignedTA, Profile.objects.get(user__email="testTA@uwm.edu"), "instructor not set properly")

    def testIncorrect(self):
        self.resp = self.monkey.post("/addSection.html", {"sectionType": LabSection.LAB,
                                                          "newSectionNumber": "IncorrectSection",
                                                          "newSectionTime": "Never",
                                                          "newSectionAssignedCourse": "NoCourse",
                                                          "newSectionInstructor": "NoEmail"})

        self.sectionCreated = LabSection.objects.filter(title="IncorrectSection")
        self.assertTrue(len(self.sectionCreated) == 0, "Section created for invalid request")