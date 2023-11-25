from django.http import HttpResponse
from django.http import JsonResponse
import pysolr

def index(request):
    return HttpResponse("Hello, world. Welcome to the index.")

SOLR_SERVER = 'http://solr:8983/solr/'
SOLR_CORE = 'degree' 

def search(request, *args, **kwargs):
    search_query = request.GET.get('text', '')

    solr = pysolr.Solr(f'{SOLR_SERVER}{SOLR_CORE}', timeout=10)

    results = solr.search('name:'+search_query, **{
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
