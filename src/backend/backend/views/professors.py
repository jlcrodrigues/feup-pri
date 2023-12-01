import django
from django.forms import model_to_dict
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import pysolr

from backend.models import Degree, Professor

SOLR_SERVER = 'http://solr:8983/solr/'
SOLR_CORE = 'professor'


def searchProfessors(request, *args, **kwargs):
    search_query = request.GET.get('text', '')

    solr = pysolr.Solr(f'{SOLR_SERVER}{SOLR_CORE}', timeout=10)

    results = solr.search(f"name:{search_query}~ OR fieldsOfInterest:{search_query}~", **{
        'wt': 'json',
    })

    found_objects = [
        {
            'id': result['id'],
            'name': result.get('name', ''),
            'institutionalWebsite': result.get('institutionalWebsite', ''),
            'abbrevitaion': result.get('abbrevitaion', ''),
            'status': result.get('status', ''),
            'code': result.get('code', ''),
            'institutionalEmail': result.get('institutionalEmail', ''),
            'phone': result.get('phone', ''),
            'rank': result.get('rank', ''),
            'personalPresentation': result.get('personalPresentation', ''),
            'fieldsOfInterest': result.get('fieldsOfInterest', ''),
        }
        for result in results
    ]

    return JsonResponse({'results': found_objects})


def getProfessor(request, *args, **kwargs):
    professor = get_object_or_404(Professor, id=kwargs['id'])
    return JsonResponse(model_to_dict(professor))
