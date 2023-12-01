import django
from django.forms import model_to_dict
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import pysolr

from backend.models import Degree

def index(request):
    return HttpResponse("Hello, world. Welcome to the index.")
