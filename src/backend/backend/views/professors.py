import django
from django.forms import model_to_dict
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import pysolr
from backend.utils import snake_to_camel_case

from backend.models import Degree, Professor

SOLR_SERVER = 'http://solr:8983/solr/'
SOLR_CORE = 'professor'


def searchProfessors(request, *args, **kwargs):
    search_query = request.GET.get('text', '')
    search_query = '*:*' if search_query == '' else f"name:{search_query}~ OR fieldsOfInterest:{search_query}~"
    status = request.GET.getlist('status')
    ranks = request.GET.getlist('rank')

    sortKey = request.GET.get('sortKey')
    sortOrder = request.GET.get('sortOrder')

    solr = pysolr.Solr(f'{SOLR_SERVER}{SOLR_CORE}', timeout=10)

    results = solr.search(search_query, **{
        'wt': 'json',
        'fq': getFilter(status, ranks),
        'sort': f'{sortKey} {sortOrder}' if sortKey != None and sortOrder != None else ''
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
    
def getFilter(statuses, ranks):
    fq = []
    if statuses != None and statuses != []:
        fq.append("(" + " OR ".join([f"status:\"{status}\"" for status in statuses]) + ")")
    if ranks != None and ranks != []:
        fq.append("(" + " OR ".join([f"rank:\"{rank}\"" for rank in ranks]) + ")")
    return " AND ".join(fq)


def getProfessor(request, *args, **kwargs):
    professor = get_object_or_404(Professor, id=kwargs['id'])
    professor_dict = model_to_dict(professor)
    professorDict = {}
    for key in professor_dict:
        professorDict[snake_to_camel_case(key)] = professor_dict[key]
    
    return JsonResponse(professorDict)