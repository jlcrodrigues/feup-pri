import django
from django.forms import model_to_dict
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import pysolr

from backend.models import Degree

SOLR_SERVER = 'http://solr:8983/solr/'
SOLR_CORE = 'degree' 

def searchDegrees(request, *args, **kwargs):
    search_query = request.GET.get('text', '')

    solr = pysolr.Solr(f'{SOLR_SERVER}{SOLR_CORE}', timeout=10)

    results = solr.search(f"name:{search_query}~", **{
        'wt': 'json',  
    })

    found_objects = [
        {
            'id': result['id'],
            'url': result['url'],
            'name': result.get('name', ''),
            'description': result.get('description', ''),
            'outings': result.get('outings', ''),
            'typeOfCourse': result.get('typeOfCourse', ''),
            'duration': result.get('duration', ''),
        }
        for result in results
    ]

    return JsonResponse({'results': found_objects})

def getDegree(request, *args, **kwargs):
    degree = get_object_or_404(Degree, id=kwargs['id'])
    return JsonResponse(model_to_dict(degree))