from django.contrib.auth.models import User
from django.test import TestCase
from ..models import Profile, Course


class TestDatabase(TestCase):
    def test_profile_creation_on_user_creation(self):
        user = User.objects.create_user("name", "email@example.com", "password")
        profile = Profile.objects.get(user=user)
        assert(profile is not None)

    def test_course(self):
        course = Course.objects.create(title="course test")
        course.save()
        course.title = "123"
        course = Course.objects.get(title="course test")
        assert(course is not None)
