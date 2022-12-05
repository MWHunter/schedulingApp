from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


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

    # email, first_name, last_name, group see django object
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Examples of valid formats
    # +1 (555) 555-5555, (555) 555-5555, 555-555-5555, 555 555-5555,
    # 555 555 5555, 555 555 5555 55
    phoneNumber = models.CharField(max_length=24, validators=[RegexValidator(phoneRegex)])
    homeAddress = models.CharField(max_length=64)
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


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # This is the first user and is therefore the admin user.
        if len(Profile.objects.all()) == 0:
            instance.first_name = "admin"
            instance.last_name = "user"
            profile = Profile.objects.create(user=instance, phoneNumber="(555) 555-5555", homeAddress="UWM Admins",
                                             permission=Profile.ADMIN)
        else:
            profile = Profile.objects.create(user=instance, phoneNumber="(555) 555-5555", homeAddress="USER",
                                             permission=Profile.TA)
        profile.save()
        instance.save()


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Course(models.Model):
    title = models.CharField(max_length=32)
    semester = models.CharField(max_length=16)


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
