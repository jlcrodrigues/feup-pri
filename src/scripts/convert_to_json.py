import argparse
from db import database
import json


def arguments():
    parser = argparse.ArgumentParser(
        description="Script to fetch json from the relation database and convert to json."
    )
    parser.add_argument(
        "--host",
        default="localhost",
        help="The hostname or IP address of the database server. Default is 'localhost'.",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=5432,
        help="The port number of the database server. Default is 5432.",
    )
    parser.add_argument(
        "--user",
        default="pri",
        help="The username to use when connecting to the database server. Default is 'pri'.",
    )
    parser.add_argument(
        "--pwd",
        default="pri",
        help="The password to use when connecting to the database server. Default is 'pri'.",
    )
    parser.add_argument(
        "--db",
        default="pri23",
        help="The name of the PostgreSQL database to use. Default is 'pri23'.",
    )
    return parser.parse_args()


def get_degree_course_units(degree, degree_courses):
    degree_courses_filtered = filter(lambda x: x[0] == degree[0], degree_courses)
    degree_courses_json = []
    for degree_course in degree_courses_filtered:
        degree_courses_json.append({
            "id_course": degree_course[1],
            "year": degree_course[2]
        })
    return degree_courses_json


def get_professor_course_units(professor, professor_courses):
    professor_courses_filtered = filter(lambda x: x[0] == professor[0], professor_courses)
    professor_courses_json = []
    for professor_course in professor_courses_filtered:
        professor_courses_json.append({
            "id_course": professor_course[1],
            "type": professor_course[2]
        })
    return professor_courses_json


def get_course_unit_degrees(course_unit, degree_courses):
    degree_courses_filtered = filter(lambda x: x[1] == course_unit[0], degree_courses)
    degree_courses_json = []
    for degree_course in degree_courses_filtered:
        degree_courses_json.append({
            "id_degree": degree_course[0],
            "year": degree_course[2]
        })
    return degree_courses_json


def get_course_unit_professors(course_unit, professor_courses):
    professor_courses_filtered = filter(lambda x: x[1] == course_unit[0], professor_courses)
    professor_courses_json = []
    for professor_course in professor_courses_filtered:
        professor_courses_json.append({
            "id_professor": professor_course[0],
            "type": professor_course[2]
        })
    return professor_courses_json


def degrees_to_json(db):
    degrees_json = []
    degrees = db.execute("SELECT * FROM pri_g81.degree")
    degrees_course = db.execute("SELECT * FROM pri_g81.degreecourseunit")
    for degree in degrees:
        degrees_json.append({
            "id": degree[0],
            "url": degree[1],
            "name": degree[2],
            "description": degree[3],
            "outings": degree[4],
            "typeOfCourse": degree[5],
            "duration": degree[6],
        })
    return degrees_json


def course_units_to_json(db):
    courses_units_json = []
    courses_units = db.execute("SELECT * FROM pri_g81.courseunit")
    course_degrees = db.execute("SELECT * FROM pri_g81.degreecourseunit")
    course_professors = db.execute("SELECT * FROM pri_g81.professorcourseunit")

    for course_unit in courses_units:
        courses_units_json.append({
            "id": course_unit[0],
            "name": course_unit[1],
            "url": course_unit[2],
            "code": course_unit[3],
            "language": course_unit[4],
            "ects": course_unit[5],
            "objective": course_unit[6],
            "results": course_unit[7],
            "workingMethod": course_unit[8],
            "preRequirements": course_unit[9],
            "program": course_unit[10],
            "evaluationType": course_unit[11],
            "passingRequirements": course_unit[12],
            })

    return courses_units_json


def professors_to_json(db):
    professors_json = []
    professors = db.execute("SELECT * FROM pri_g81.professor")
    professor_courses = db.execute("SELECT * FROM pri_g81.professorcourseunit")

    for professor in professors:
        professors_json.append({
            "id": professor[0],
            "name": professor[1],
            "personalWebsite": professor[2],
            "institutionalWebsite": professor[3],
            "abbreviation": professor[4],
            "status": professor[5],
            "code": professor[6],
            "institutionEmail": professor[7],
            "phone": professor[8],
            "rank": professor[9],
            "personalPresentation": professor[10],
            "fieldsOfInterest": professor[11],
        })

    return professors_json


def main(args):
    db = database.Database(args.host, args.port, args.user, args.pwd, args.db)
    db.connect()
    degrees_json = degrees_to_json(db)
    course_units_json = course_units_to_json(db)
    professors_json = professors_to_json(db)
    db.disconnect()

    with open("../json/degrees.json", "w") as outfile:
        outfile.write(json.dumps(degrees_json))
    with open("../json/course_units.json", "w") as outfile:
        outfile.write(json.dumps(course_units_json))
    with open("../json/professors.json", "w") as outfile:
        outfile.write(json.dumps(professors_json))
    print("JSON files created. Exiting...")
    exit(0)


if __name__ == "__main__":
    args = arguments()
    main(args)
