from django.db import models


class User(models.Model):
    class PermissionLevel(models.TextChoices):
        TA = 'TA'
        PROFESSOR = 'PROFESSOR'
        ADMIN = 'ADMIN'

    emailAddress = models.CharField(max_length=32)
    phoneNumber = models.CharField(max_length=16)
    homeAddress = models.CharField(max_length=64)
    firstName = models.CharField(max_length=32)
    lastName = models.CharField(max_length=32)
    permission = models.CharField(max_length=16,
                                  choices=PermissionLevel,
                                  default=PermissionLevel.TA)


class Course(models.Model):
    title = models.CharField(max_length=32)


class Assignment(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=65536)


# Many TA's can be assigned to a single course
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
