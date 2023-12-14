import django
from django.forms import model_to_dict
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import pysolr
from backend.utils import snake_to_camel_case

from backend.models import Courseunit

SOLR_SERVER = "http://solr:8983/solr/"
SOLR_CORE = "course_unit"


def searchCourses(request, *args, **kwargs):
    search_query = request.GET.get("text", "")
    search_query = "*:*" if search_query == "" else f"name:{search_query}~"
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
        "rows": 5,
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

    return JsonResponse({"results": found_objects})
