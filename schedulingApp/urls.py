"""schedulingApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from schedulingApp.views import Login, Home, Users, LogOut, AddUser, AddCourse, AddSection

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users.html', Users.as_view()),
    path('login.html', Login.as_view()),
    path('logout.html', LogOut.as_view()),
    path('addUser.html', AddUser.as_view()),
    path('addCourse.html', AddCourse.as_view()),
    path('addSection.html', AddSection.as_view()),
    path('', Home.as_view())
]
