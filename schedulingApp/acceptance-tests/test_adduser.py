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
        self.assertNotEqual(testAuth, None, "unable to login as new user")

    def testFirstName(self):
        self.assertEqual(self.userCreated.first_name, "firstname", "first name not retained")

    def testLastName(self):
        self.assertEqual(self.userCreated.last_name, "lastname", "last name not retained")

    def testAddress(self):
        self.assertEqual(self.profileCreated.homeAddress, "some address", "Address not retained")

    def testPhoneNumber(self):
        self.assertEqual(self.profileCreated.phoneNumber, "555 867-5309", "Phone number not retained")

    def testIncorrect(self):
        self.assertEqual(self.profileCreated.permission, Profile.ADMIN)

        self.resp = self.monkey.post("/addUser.html", {"email-address": "testIncorrect@uwm.edu",
                                                      "password": "password",
                                                      "first-name": "firstname",
                                                      "last-name": "lastname",
                                                      "home-address": "some address",
                                                      "phone-number": "not a valid phone number",
                                                      "user-role": Profile.ADMIN})

        self.userCreated = User.objects.filter(email="testIncorrect@uwm.edu")
        self.assertTrue(len(self.userCreated) == 0, "User created for invalid request")

    def testNoLogin(self):
        self.monkey.logout()
        self.resp = self.monkey.post("/addUser.html", {"email-address": "test@uwm.edu",
                                                      "password": "password",
                                                      "first-name": "firstname",
                                                      "last-name": "lastname",
                                                      "home-address": "some address",
                                                      "phone-number": "555 867-5309",
                                                      "user-role": Profile.ADMIN})
        self.assertEqual(self.resp.status_code, 302, "Can create user when not logged in")
