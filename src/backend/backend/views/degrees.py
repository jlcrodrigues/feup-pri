from urllib.parse import urlencode
import django
from django.forms import model_to_dict
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import pysolr
from backend.utils import text_to_embedding

from backend.models import Degree, Degreecourseunit

SOLR_SERVER = "http://solr:8983/solr/"
SOLR_CORE = "degree"

def searchDegrees(request, *args, **kwargs):
    search_text = request.GET.get("text", "")
    search_query = "*:*"
    if search_text != "":
        search_query = f"(name:{search_text})^10"
        search_query += f"OR (description:{search_text})^4"
        search_query += f"OR (outings:{search_text})^3"

        # Semantic Search
        semantic_search = ""
        embedding = text_to_embedding(search_text)
        semantic_search = "{!knn f=vector topK=100}" + embedding
        search_query = search_query + " OR " + semantic_search


    typeOfCourse = request.GET.getlist("typeOfCourse")

    sortKey = request.GET.get("sortKey")
    sortOrder = request.GET.get("sortOrder")

    solr = pysolr.Solr(f"{SOLR_SERVER}{SOLR_CORE}", timeout=10)

    results = solr.search(
        **{
            "q": search_query,
            "wt": "json",
            "fq": getFilter(typeOfCourse),
            "sort": f"{sortKey} {sortOrder}"
            if sortKey != None and sortOrder != None
            else "",
        },
    )

    found_objects = [
        {
            "id": result["id"],
            "url": result["url"],
            "name": result.get("name", ""),
            "description": result.get("description", ""),
            "outings": result.get("outings", ""),
            "typeOfCourse": result.get("typeOfCourse", ""),
            "duration": result.get("duration", ""),
        }
        for result in results
    ]

    return JsonResponse({"results": found_objects})


def getFilter(typeOfCourse):
    fq = ""
    if typeOfCourse != None:
        fq += " OR ".join(
            [f'typeOfCourse:"{typeOfCourse}"' for typeOfCourse in typeOfCourse]
        )
    return fq


def getDegree(request, *args, **kwargs):
    degree = get_object_or_404(Degree, id=kwargs["id"])
    degree_dict = model_to_dict(degree)
    degree_dict["courses"] = getDegreeCourses(degree)
    return JsonResponse(degree_dict)


def getDegreeCourses(degree: Degree):
    degree_courses = Degreecourseunit.objects.filter(degree=degree)
    courses_for_degree = [
        model_to_dict(degree_course.course_unit) for degree_course in degree_courses
    ]
    return courses_for_degree


def getRelatedDegrees(request, *args, **kwargs):
    degree_id = kwargs["id"]

    solr = pysolr.Solr(f"{SOLR_SERVER}{SOLR_CORE}", timeout=10)

    mlt_query = {
        "q": f"id:{degree_id}",
        "rows": 10,
        "mltfl": "name,outings,description",
    }

    results = solr.more_like_this(**mlt_query)

    found_objects = [
        {
            "id": result["id"],
            "url": result["url"],
            "name": result.get("name", ""),
            "description": result.get("description", ""),
            "outings": result.get("outings", ""),
            "typeOfCourse": result.get("typeOfCourse", ""),
            "duration": result.get("duration", ""),
        }
        for result in results
    ]

    return JsonResponse({'results': found_objects})

def getDegreeEntities(request, *args, **kwargs):
    degree_id = kwargs['id']

    solr = pysolr.Solr(f'{SOLR_SERVER}{SOLR_CORE}', timeout=10)

    results = solr.search(f"id:{degree_id}", **{
        'wt': 'json',
        'fl': 'entities',
    })


    for result in results:
        entities = result.get('entities', ''),

    return JsonResponse(entities, safe=False)
