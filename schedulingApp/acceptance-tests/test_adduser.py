from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.test import TestCase, Client

from schedulingApp.models import Profile


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

        self.resp = self.monkey.post("/addUser.html", {"email-address": "test@uwm.edu",
                                                      "password": "password",
                                                      "first-name": "firstname",
                                                      "last-name": "lastname",
                                                      "home-address": "some address",
                                                      "phone-number": "555 867-5309",
                                                      "user-role": Profile.ADMIN})

        self.userCreated = User.objects.get(email="test@uwm.edu")
        self.profileCreated = Profile.objects.get(user=self.userCreated)

    def testEmailEquals(self):
        self.assertEqual(self.userCreated.username, "test@uwm.edu")

    def testLogin(self):
        testAuth = authenticate(username="test@uwm.edu", password="password")
        self.assertNotEqual(testAuth, None)

    def testFirstName(self):
        self.assertEqual(self.userCreated.first_name, "firstname")

    def testLastName(self):
        self.assertEqual(self.userCreated.last_name, "lastname")

    def testAddress(self):
        self.assertEqual(self.profileCreated.homeAddress, "some address")

    def testPhoneNumber(self):
        self.assertEqual(self.profileCreated.phoneNumber, "555 867-5309")

    def testPermission(self):
        self.assertEqual(self.profileCreated.permission, Profile.ADMIN)
