from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.test import TestCase, Client

import schedulingApp
from schedulingApp.models import Profile, Section, Course, SectionToAssignedUserEntry


class TestAddSection(TestCase):
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

        self.resp = self.monkey.post("/addSection.html", {"sectionType": Section.LAB,
                                                          "newSectionNumber": "001",
                                                          "newSectionTime": "9:30AM",
                                                          "newSectionAssignedCourse": course.title,
                                                          "newSectionInstructor": taUser.email})

        self.sectionCreated = Section.objects.get(title="001")


    def testTitle(self):
        self.assertEqual(self.sectionCreated.title, "001")

    def testSectionType(self):
        self.assertEqual(self.sectionCreated.labType, Section.LAB, "section type not set properly")

    def tesSectionTime(self):
        self.assertEqual(self.sectionCreated.time, "9:30AM", "time not set properly")

    def testCourse(self):
        self.assertEqual(self.sectionCreated.course, Course.objects.get(title="CS361"), "course not set properly")

    def testInstructor(self):
        self.assertEqual(SectionToAssignedUserEntry.objects.get(section=self.sectionCreated).assignedUser, Profile.objects.get(user__email="testTA@uwm.edu"), "instructor not set properly")

    def testIncorrect(self):
        self.resp = self.monkey.post("/addSection.html", {"sectionType": Section.LAB,
                                                          "newSectionNumber": "IncorrectSection",
                                                          "newSectionTime": "Never",
                                                          "newSectionAssignedCourse": "NoCourse",
                                                          "newSectionInstructor": "NoEmail"})

        self.sectionCreated = Section.objects.filter(title="IncorrectSection")
        self.assertTrue(len(self.sectionCreated) == 0, "Section created for invalid request")


class TestAddDiscussion(TestCase):
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

        self.resp = self.monkey.post("/addSection.html", {"sectionType": Section.DISCUSSION,
                                                          "newSectionNumber": "001",
                                                          "newSectionTime": "9:30AM",
                                                          "newSectionAssignedCourse": course.title,
                                                          "newSectionInstructor": taUser.email})

        self.sectionCreated = Section.objects.get(title="001")


    def testTitle(self):
        self.assertEqual(self.sectionCreated.title, "001")

    def testSectionType(self):
        self.assertEqual(self.sectionCreated.labType, Section.DISCUSSION, "section type not set properly")

    def tesSectionTime(self):
        self.assertEqual(self.sectionCreated.time, "9:30AM", "time not set properly")

    def testCourse(self):
        self.assertEqual(self.sectionCreated.course, Course.objects.get(title="CS361"), "course not set properly")

    def testInstructor(self):
        self.assertEqual(SectionToAssignedUserEntry.objects.get(section=self.sectionCreated).assignedUser, Profile.objects.get(user__email="testTA@uwm.edu"), "instructor not set properly")


class TestAddSectionNoUser(TestCase):
    monkey = None

    def setUp(self):
        self.monkey = Client()
        testUser = User.objects.create_user(username="user", password="pass", email="u@uwm.edu")
        testUser.save()
        profile = Profile.objects.get(user=testUser)
        profile.permission = Profile.ADMIN
        profile.save()
        self.monkey.force_login(testUser)

        course = Course(title='CS361', semester='FA22')
        course.save()

        self.resp = self.monkey.post("/addSection.html", {"sectionType": Section.LECTURE,
                                                          "newSectionNumber": "001",
                                                          "newSectionTime": "9:30AM",
                                                          "newSectionAssignedCourse": course.title,
                                                          "newSectionInstructor": ""})

        self.sectionCreated = Section.objects.get(title="001")


    def testTitle(self):
        self.assertEqual(self.sectionCreated.title, "001")

    def testSectionType(self):
        self.assertEqual(self.sectionCreated.labType, Section.LECTURE, "section type not set properly")

    def tesSectionTime(self):
        self.assertEqual(self.sectionCreated.time, "9:30AM", "time not set properly")

    def testCourse(self):
        self.assertEqual(self.sectionCreated.course, Course.objects.get(title="CS361"), "course not set properly")

    def testInstructor(self):
        with self.assertRaises(schedulingApp.models.SectionToAssignedUserEntry.DoesNotExist, msg="instructor should not exist"):
            SectionToAssignedUserEntry.objects.get(section=self.sectionCreated)
