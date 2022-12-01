from django.db import models
from django.core.validators import MaxValueValidator


class User(models.Model):
    PermissionLevel = (
        ('ta', 'TA'),
        ('professor', 'Professor'),
        ('admin', 'Admin')
    )

    firstName = models.CharField(max_length=32)
    lastName = models.CharField(max_length=32)
    emailAddress = models.CharField(max_length=32)
    homeAddress = models.CharField(max_length=64)
    phoneNumber = models.PositiveIntegerField(primary_key=True, validators=[MaxValueValidator(9999999999)])
    permission = models.CharField(max_length=16,
                                  choices=PermissionLevel,
                                  default=PermissionLevel[0])

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


class CourseToAssignedTAEntry(models.Model):
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, null=False)
    assignedTA = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False)
    numAllowedLabs = models.IntegerField


class CourseToProfessorEntry(models.Model):
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, null=False)
    assignedProfessor = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False)


class LabSection(models.Model):
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, null=False)
    title = models.CharField(max_length=32)
    assignedTA = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False)
