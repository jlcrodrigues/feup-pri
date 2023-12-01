import django
from django.forms import model_to_dict
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import pysolr

from backend.models import Courseunit, Degree

SOLR_SERVER = 'http://solr:8983/solr/'
SOLR_CORE = 'course_unit' 

def searchCourses(request, *args, **kwargs):
    search_query = request.GET.get('text', '')

    solr = pysolr.Solr(f'{SOLR_SERVER}{SOLR_CORE}', timeout=10)

    results = solr.search(f"name:{search_query}~", **{
        'wt': 'json',  
    })

    found_objects = [
        {
            'id': result['id'],
            'name': result.get('name', ''),
            'url': result['url'],
            'code': result['code'],
            'language': result.get('language', ''),
            'ects': result.get('ects', ''),
            'objective': result.get('objective', ''),
            'results': result.get('results', ''),
            'workingMethod': result.get('workingMethod', ''),
            'preRequirements': result.get('preRequirements', ''),
            'program': result.get('program', ''),
            'evaluationType': result.get('evaluationType', ''),
            'passingRequirements': result.get('passingRequirements', '')
        }
        for result in results
    ]

    return JsonResponse({'results': found_objects})

def getCourse(request, *args, **kwargs):
    course_id = request.GET.get('id', '')
    degree = get_object_or_404(Courseunit, id=course_id)
    return JsonResponse(model_to_dict(degree))