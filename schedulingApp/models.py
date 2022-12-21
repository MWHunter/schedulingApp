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
    skills = models.CharField(max_length=4096, blank=True)
    permission = models.CharField(max_length=16,
                                  choices=PermissionLevel,
                                  default=TA)

    def setSkills(self, skills):
        self.skills = skills

    def getSkills(self):
        return self.skills


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
    FALL22 = "FA22"
    WINTERIM22 = "WI22"
    SPRING23 = "SP23"
    SUMMER23 = "SU23"
    SEMESTER_CHOICES = [
        (FALL22, "Fall 2022"),
        (WINTERIM22, "Winterim 2022"),
        (SPRING23, "Spring 2023"),
        (SUMMER23, "Summer 2023"),
    ]
    title = models.CharField(max_length=32)
    semester = models.CharField(max_length=4, choices=SEMESTER_CHOICES, default=FALL22)

    def getUsersAssignedToCourse(self):
        users = []
        for entry in CourseToAssignedUserEntry.objects.filter(course=self):
            users.append(entry.assignedUser)
        return users

    def addUserToCourse(self, user):
        entry = CourseToAssignedUserEntry(course=self, assignedUser=user)
        entry.full_clean()
        entry.save()

    def removeUserFromCourse(self, user):
        entry = CourseToAssignedUserEntry.objects.get(course=self, assignedUser=user)
        entry.delete()

    def setTitle(self, newtitle):
        self.title = newtitle

    def setSemester(self, newsemester):
        self.semester = newsemester

    def getTitle(self):
        return self.title

    def getSemester(self):
        return self.semester

    def addProfile(self, newprofile):
        pass

    def removeProfile(self, remprofile):
        pass

    def getAllProfiles(self):
        pass


class Assignment(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=65536)


class Section(models.Model):
    LAB = "lab"
    LECTURE = "lecture"
    DISCUSSION = "discussion"
    LAB_TYPE = [
        (LAB, "LAB"),
        (LECTURE, "LECTURE"),
        (DISCUSSION, "DISCUSSION")
    ]

    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, null=False)
    time = models.CharField(max_length=16)
    title = models.CharField(max_length=32)
    labType = models.CharField(max_length=10, choices=LAB_TYPE, default=LAB)

    def getUsersAssignedToCourse(self):
        users = []
        for entry in SectionToAssignedUserEntry.objects.filter(section=self):
            users.append(entry.assignedUser)
        return users

    def addUserToSection(self, user):
        entry = SectionToAssignedUserEntry(course=self, assignedUser=user)
        entry.full_clean()
        entry.save()

    def removeUserFromSection(self, user):
        entry = SectionToAssignedUserEntry.objects.get(course=self, assignedUser=user)
        entry.delete()


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


class CourseToAssignmentEntry(models.Model):
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, null=False)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, null=False)

class CourseToAssignedUserEntry(models.Model):
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, null=False)
    assignedUser = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, null=False)


class SectionToAssignmentEntry(models.Model):
    section = models.ForeignKey(Section, on_delete=models.DO_NOTHING, null=False)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, null=False)


class SectionToAssignedUserEntry(models.Model):
    section = models.ForeignKey(Section, on_delete=models.DO_NOTHING, null=False)
    assignedUser = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, null=False)
