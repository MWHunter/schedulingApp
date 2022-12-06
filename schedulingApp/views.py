from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from schedulingApp.models import Profile, Course, LabSection
from schedulingApp.permissionTests import user_has_admin_permission


class Login(View):
    def get(self, request):
        # You are logged in already, you don't belong here
        if request.user.is_authenticated:
            return redirect("/")
        return render(request, "login.html", {})

    def post(self, request):
        # If you wish to create a user, the code is
        # user = User.objects.create_user('name', 'email', 'password')
        # user.save()
        user = authenticate(username=request.POST.get('loginID'), password=request.POST.get('loginPassword'))
        if user is not None:
            login(request, user)
            return redirect("/")
        return render(request, "login.html", {"error": "Invalid username or password"})


# if you would wish to restrict a page behind permissions, use the following code instead:
# @method_decorator(user_passes_test(user_has_admin_permission), name='dispatch')
@method_decorator(login_required, name='dispatch')
class Home(View):
    def get(self, request):
        return render(request, "home.html", {"profile": Profile.objects.get(user=request.user)})


class Users(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "users.html", {"profiles": Profile.objects.all(),
                                              "profile": Profile.objects.get(user=request.user)})


@method_decorator(user_passes_test(user_has_admin_permission), name='dispatch')
class AddUser(View):
    def get(self, request):
        return render(request, "addUser.html", {"profile": Profile.objects.get(user=request.user)})

    def post(self, request):
        try:
            user = User.objects.create_user(username=request.POST.get('email-address'),
                                            email=request.POST.get('email-address'),
                                            password=request.POST.get('password'),
                                            first_name=request.POST.get('first-name'),
                                            last_name=request.POST.get('last-name'))

            # We idiot-proofed profile creation so we must fetch it now
            profile = Profile.objects.get(user=user)
            profile.address = request.POST.get('home-address')
            profile.phoneNumber = request.POST.get("phone-number")
            profile.permission = request.POST.get("user-role").lower()

            user.full_clean()
            profile.full_clean()
            user.save()
            profile.save()
            return redirect("users.html")

        except (ValidationError, ValueError, IntegrityError) as e:
            error = str(e)
            return render(request, "addUser.html", {"error": error, "profile": Profile.objects.get(user=request.user)})


@method_decorator(user_passes_test(user_has_admin_permission), name='dispatch')
class AddCourse(View):
    def get(self, request):
        return render(request, "addCourse.html", {"semesters": Course.SEMESTER_CHOICES,
                                                  "profile": Profile.objects.get(user=request.user)})

    def post(self, request):
        newCourse = Course(title=request.POST.get('newCourseTitle'), semester=request.POST.get('newCourseSemester'))
        #Validates input and checks to see if there's already an object in the system.
        try:
            newCourse.full_clean()
            Course.objects.get(title=newCourse.title, semester=newCourse.semester)
            return render(request, "addCourse.html", {"message": "Course already exists",
                                                      "semesters": Course.SEMESTER_CHOICES})
        except (ValidationError, ValueError, IntegrityError) as e:
            error = str(e)
            return render(request, "addCourse.html", {"message": error, "semesters": Course.SEMESTER_CHOICES})
        #only if there's no object currently in the system and input is valid will the course be created
        except ObjectDoesNotExist:
            newCourse.save()
            return redirect("/courses.html")


@method_decorator(user_passes_test(user_has_admin_permission), name='dispatch')
class AddSection(View):
    def get(self, request):
        return render(request, "addSection.html", {"profile": Profile.objects.get(user=request.user)})


# We don't care if a user has logged in for this one
class LogOut(View):
    def get(self, request):
        logout(request)
        return redirect("login.html")


class Courses(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "courses.html", {"courses": Course.objects.all(),
                                                "profile": Profile.objects.get(user=request.user)})


class Sections(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "sections.html", {"sections": LabSection.objects.all(),
                                                 "profile": Profile.objects.get(user=request.user)})


class ViewUser(LoginRequiredMixin, View):
    def get(self, request, id):
        profile = Profile.objects.get(user=request.user)
        if profile.id != id and profile.permission != Profile.ADMIN:
            return redirect("/")
        return render(request, "viewUser.html", {"viewing": Profile.objects.get(id=id),
                                                 "profile": Profile.objects.get(user=request.user)})
