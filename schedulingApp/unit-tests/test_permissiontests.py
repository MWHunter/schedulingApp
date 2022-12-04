from django.contrib.auth.models import User, AnonymousUser
from django.test import TestCase

from schedulingApp.permissionTests import *


class TestPermissionTest(TestCase):
    user = None

    def setUp(self):
        self.user = User.objects.create_user("username", "password")
        self.user.save()

    def testPositiveTaPermission(self):
        for i in (Profile.TA, Profile.PROFESSOR, Profile.ADMIN):
            self.setPermissionLevel(i)
            self.assertTrue(user_has_ta_permission(self.user))

    def testAnonymousUser(self):
        self.user = AnonymousUser()
        for method in [user_has_ta_permission, user_has_professor_permission, user_has_ta_permission]:
            self.assertFalse(method(self.user), "Anonymous user doesn't have TA permission")

    def testProfessorPermission(self):
        for i in (Profile.PROFESSOR, Profile.ADMIN):
            self.setPermissionLevel(i)
            self.assertTrue(user_has_ta_permission(self.user))

    def testNegativeProfessorPermission(self):
        self.setPermissionLevel(permission=Profile.TA)
        self.assertFalse(user_has_professor_permission(self.user))

    def testAdminPermission(self):
        self.setPermissionLevel(Profile.ADMIN)
        self.assertTrue(user_has_admin_permission(self.user))

    def testNegativeAdminPermission(self):
        for i in (Profile.TA, Profile.PROFESSOR):
            self.setPermissionLevel(i)
            self.assertFalse(user_has_admin_permission(self.user))

    def setPermissionLevel(self, permission):
        profile = Profile.objects.get(user=self.user)
        profile.permission = permission
        profile.save()
