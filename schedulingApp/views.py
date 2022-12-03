from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin


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
        # TODO: Say invalid username or password?
        return render(request, "login.html", {})


class Home(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "home.html", {})


class CreateUser(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "createUser.html", {})
