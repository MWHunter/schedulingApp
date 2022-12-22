from django.contrib.auth.models import User
from django.test import TestCase, Client
from schedulingApp.models import Profile


class TestTASkillInfo(TestCase):
    monkey = None

    def setUp(self):
        self.taUser = User.objects.create_user(username="test", password="TA", email="testTA@uwm.edu")
        self.taUser.save()
        self.profileTA = Profile.objects.get(user=self.taUser)
        self.profileTA.permission = Profile.TA
        self.profileTA.save()

        self.monkeyTA = Client()
        self.monkeyTA.force_login(self.taUser)

    def test_skillsChanged(self):

        self.resp = self.monkeyTA.post("/editUser/" + str(self.profileTA.id), {'new-email-address': "",
                                                          'new-password': "",
                                                          'new-first-name': "",
                                                          'new-last-name': "",
                                                          'new-home-address': "",
                                                          'new-phone-number': "",
                                                          'new-skills': "These are skills"})

        self.assertEqual("These are skills", Profile.objects.get(user=self.taUser).skills, msg="Skills have not been altered")

