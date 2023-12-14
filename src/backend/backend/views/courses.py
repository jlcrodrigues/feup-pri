import django
from django.forms import model_to_dict
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import pysolr
from backend.utils import snake_to_camel_case
from backend.utils import text_to_embedding

from backend.models import Courseunit

SOLR_SERVER = "http://solr:8983/solr/"
SOLR_CORE = "course_unit"


def searchCourses(request, *args, **kwargs):
    search_text = request.GET.get("text", "")
    search_query = "*:*"
    if search_text != "":
        search_query = f"(name:{search_text})^10"
        search_query += f"OR (objectives:{search_text})^5"
        search_query += f"OR (program:{search_text})^5"
        search_query += f"OR (results:{search_text})^4"
        search_query += f"OR (preRequirements:{search_text})^3"
        search_query += f"OR (evaluationType:{search_text})^3"
        search_query += f"OR (passingRequirements:{search_text})^3"

    language = request.GET.getlist("language")

    sortKey = request.GET.get("sortKey")
    sortOrder = request.GET.get("sortOrder")

    solr = pysolr.Solr(f"{SOLR_SERVER}{SOLR_CORE}", timeout=10)

    results = solr.search(
        search_query,
        **{
            "wt": "json",
            "fq": getFilter(language),
            "sort": f"{sortKey} {sortOrder}"
            if sortKey != None and sortOrder != None
            else "",
        },
    )

    found_objects = [
        {
            "id": result["id"],
            "name": result.get("name", ""),
            "url": result["url"],
            "code": result["code"],
            "language": result.get("language", ""),
            "ects": result.get("ects", ""),
            "objectives": result.get("objectives", ""),
            "results": result.get("results", ""),
            "workingMethod": result.get("workingMethod", ""),
            "preRequirements": result.get("preRequirements", ""),
            "program": result.get("program", ""),
            "evaluationType": result.get("evaluationType", ""),
            "passingRequirements": result.get("passingRequirements", ""),
        }
        for result in results
    ]

    return JsonResponse({"results": found_objects})


def getFilter(languages):
    fq = ""
    if languages != None:
        fq += " OR ".join([f'language:"{language}"' for language in languages])
    return fq


def getCourse(request, *args, **kwargs):
    course = get_object_or_404(Courseunit, id=kwargs["id"])
    course_dict = model_to_dict(course)

    courseDict = {}
    for key in course_dict:
        courseDict[snake_to_camel_case(key)] = course_dict[key]

    return JsonResponse(courseDict)


def getRelatedCourses(request, *args, **kwargs):
    course_id = kwargs["id"]

    solr = pysolr.Solr(f"{SOLR_SERVER}{SOLR_CORE}", timeout=10)

    mlt_query = {
        "q": f"id:{course_id}",
        "rows": 10,
        "mltfl": "name,objectives,results,program",
    }

    results = solr.more_like_this(**mlt_query)

    found_objects = [
        {
            "id": result["id"],
            "name": result.get("name", ""),
            "url": result["url"],
            "code": result["code"],
            "language": result.get("language", ""),
            "ects": result.get("ects", ""),
            "objectives": result.get("objectives", ""),
            "results": result.get("results", ""),
            "workingMethod": result.get("workingMethod", ""),
            "preRequirements": result.get("preRequirements", ""),
            "program": result.get("program", ""),
            "evaluationType": result.get("evaluationType", ""),
            "passingRequirements": result.get("passingRequirements", ""),
        }
        for result in results
    ]

    return JsonResponse({'results': found_objects})

def getCourseEntities(request, *args, **kwargs):
    course_id = kwargs['id']

    solr = pysolr.Solr(f'{SOLR_SERVER}{SOLR_CORE}', timeout=10)

    results = solr.search(f"id:{course_id}", **{
        'wt': 'json',
        'fl': 'entities',
    })


    for result in results:
        entities = result.get('entities', ''),

    return JsonResponse(entities, safe=False)
