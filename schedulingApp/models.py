from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import re


# Confused about OneToOneFields and how to use them?
# The code was borrowed from this URL
# https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
class Profile(models.Model):
    phoneRegex = r"^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}(?:[\s.-]?\d{2,5})?$"

    TA = 'ta'
    PROFESSOR = 'professor'
    ADMIN = 'admin'

    PermissionLevel = (
        (TA, 'TA'),
        (PROFESSOR, 'Professor'),
        (ADMIN, 'Admin')
    )

    # email, firstName, lastName, group see django object
    user = models.OneToOneField(User, on_delete=models.CASCADE, )
    # Examples of valid formats
    # +1 (555) 555-5555, (555) 555-5555, 555-555-5555, 555 555-5555,
    # 555 555 5555, 555 555 5555 x555, 555 555 5555 ext555
    phoneNumber = models.CharField(max_length=16, validators=[RegexValidator(phoneRegex)])
    address = models.CharField(max_length=128)
    permission = models.CharField(max_length=16,
                                  choices=PermissionLevel,
                                  default=TA)

    def get_user(self):
        return self.user

    def get_phone_number(self):
        return self.phoneNumber

    def set_phone_number(self, number):
        return self.phoneNumber

    def get_permission_level(self):
        return self.permission

    def set_permission_level(self, permission):
        self.permission = permission


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        instance.first_name = "admin"
        instance.last_name = "user"
        Profile.objects.create(user=instance, phoneNumber="(555) 555-5555", address="UWM Admins",
                               permission=Profile.ADMIN)
        instance.save()


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Course(models.Model):
    title = models.CharField(max_length=32)


class Assignment(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=65536)
    isTaAssignment = models.BooleanField


class CourseToAssignmentEntry(models.Model):
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, null=False)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, null=False)


class CourseToAssignedTAEntry(models.Model):
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, null=False)
    assignedTA = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, null=False)
    numAllowedLabs = models.IntegerField


class CourseToProfessorEntry(models.Model):
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, null=False)
    assignedProfessor = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, null=False)


class LabSection(models.Model):
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, null=False)
    title = models.CharField(max_length=32)
    assignedTA = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, null=False)

    # getters/setters
    def getCourse(self):
        pass

    def getTitle(self):
        pass

    def getTA(self):
        pass

    def setCourse(self, newCourse):
        pass

    def setTitle(self, newTitle):
        pass

    def setTA(self, newTA):
        pass
