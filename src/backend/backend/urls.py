"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from .views import views
from .views.degrees import *
from .views.courses import *
from .views.professors import *

urlpatterns = [
    path("", views.index, name="index"),
    path("search/degrees", searchDegrees, name="searchDegrees"),
    path("search/courses", searchCourses, name="searchCourses"),
    path("search/professors", searchProfessors, name="searchProfessors"),
    path("degree/<int:id>", getDegree, name="getDegree"),
    path("degree/related/<int:id>", getRelatedDegrees, name="getRelatedDegrees"),
    path("course/<int:id>", getCourse, name="getCourse"),
    path("professor/<int:id>", getProfessor, name="getProfessor"),
]
