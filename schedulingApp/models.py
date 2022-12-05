from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import re


# Confused about OneToOneFields and how to use them?
# The code was borrowed from this URL
# https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
class Profile(models.Model):
    TA = 'ta'
    PROFESSOR = 'professor'
    ADMIN = 'admin'

    PermissionLevel = (
        (TA, 'TA'),
        (PROFESSOR, 'Professor'),
        (ADMIN, 'Admin')
    )

    homeAddress = models.CharField(max_length=64)
    
    # email, firstName, lastName, group see django object
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phoneNumber = models.CharField(max_length=16, validators=[RegexValidator(r"^(\+[0-9]{1,3}[\s-])?(\([0-9]{3}\)|["
                                                                             r"0-9]{3}[\s-])?[0-9]{3}[\s-]?[0-9]{4}("
                                                                             r"x[0-9]+)?$")])

    permission = models.CharField(max_length=16,
                                  choices=PermissionLevel,
                                  default=TA)


def validatePhoneNumber(number):
    if not re.match(r"^(\+[0-9]{1,3}[\s-])?(\([0-9]{3}\)|[0-9]{3}[\s-])?[0-9]{3}[\s-]?[0-9]{4}(x[0-9]+)?$", number):
        raise ValidationError("Invalid phone number")


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

    # constructor/destructor
    def __init__(self, firstName, lastName, password, emailAddress, homeAddress, phoneNumber, permission):
        pass

    def __del__(self):
        pass

    # getters/setters
    def getFirstName(self):
        pass

    def getLastName(self):
        pass

    def getPassword(self):
        pass

    def getEmailAddress(self):
        pass

    def getHomeAddress(self):
        pass

    def getPhoneNumber(self):
        pass

    def getPermission(self):
        pass

    def setFirstName(self, firstName):
        pass

    def setLastName(self, lastName):
        pass

    def setPassword(self, password):
        pass

    def setEmailAddress(self, emailAddress):
        pass

    def setHomeAddress(self, homeAddress):
        pass

    def setPhoneNumber(self, phoneNumber):
        pass

    def setPermission(self, permission):
        pass

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
        return self.course

    def getTitle(self):
        return self.title

    def getTA(self):
        return self.assignedTA

    def setCourse(self, newCourse):
        if newCourse is None:
            raise ValueError("Cannot set newCourse to None")
        self.course = newCourse

    def setTitle(self, newTitle):
        if newTitle == "":
            raise ValueError("Cannot set title to empty string")
        self.title = newTitle

    def setTA(self, newTA):
        if newTA is None:
            raise ValueError("Cannot set assignedTA to None")
        self.assignedTA = newTA
