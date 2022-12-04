from django.contrib.auth.models import User
from django.test import TestCase, Client


class TestLogin(TestCase):
    monkey = None
    logins = {'user1': '123', 'user2': '456', 'user3': r'98ufe0/a\;q09124*)($!@)*%&)_*(@%!``~'}

    def setUp(self):
        self.monkey = Client()

        for login in self.logins.keys():
            user = User.objects.create_user(login, password=self.logins[login])
            user.save()

    def testCorrectLogin(self):
        for login in self.logins.keys():
            resp = self.monkey.post("/login.html", {"loginID": login, "loginPassword": self.logins[login]}, follow=True)
            self.assertEqual(resp.request['PATH_INFO'], "/", "login was not successful with correct password")

    def testIncorrectLogin(self):
        for login in self.logins.keys():
            resp = self.monkey.post("/login.html", {"loginID": login, "loginPassword": r"0]er[]\o"}, follow=True)
            self.assertEqual(resp.request['PATH_INFO'], '/login.html', "login successful with incorrect password")

    def testNoLoginRedirect(self):
        resp = self.monkey.get("/", follow=True)
        self.assertEqual(resp.request['PATH_INFO'], '/login.html', "Not logged in user allowed to view restricted page")
