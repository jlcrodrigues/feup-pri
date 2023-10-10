import argparse
from fetchers.degrees import *
from fetchers.teachers import *
from fetchers.course_plan import *
from fetchers.course_unit import *
from db.database import *

from db import database
import psycopg2
import re


def arguments():
    parser = argparse.ArgumentParser(
        description="Script to fetch data from the web and insert it into a relational database."
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
    parser.add_argument(
        "--url",
        nargs="+",
        default=[
            "https://www.up.pt//portal/pt/estudar/licenciaturas-e-mestrados-integrados/oferta-formativa",
            # "https://www.up.pt/portal/pt/estudar/mestrados/oferta-formativa",
        ],
        help="Entry point links. Provide one or more URLs separated by spaces. These URLs will be used as the starting points for the web crawler. If no URLs are provided, the default URLs will be used.",
    )
    parser.add_argument(
        "--university_name",
        default="Universidade do Porto",
        help="The name of the university. Default is 'Universidade do Porto'.",
    )
    parser.add_argument(
        "--university_url",
        default="https://www.up.pt",
        help="The URL of the university. Default is 'https://www.up.pt'.",
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="If this flag is provided, the database will be reset before inserting the data.",
        default=True,
    )
    parser.add_argument(
        "--schema",
        help="The path to the SQL schema file. Default is 'db/schema.sql'.",
        default="db/schema.sql",
    )
    return parser.parse_args()


def terminate(db, message=""):
    print("An error occurred. Terminating...")
    print(message)
    db.disconnect()
    exit(1)


def insert_university(db, name, url):
    try:
        db.execute(
            "INSERT INTO University (name, url) VALUES (%s, %s)", (name, url), "none"
        )
    except psycopg2.errors.UniqueViolation:
        pass
    except Exception as e:
        terminate(db, e)

    try:
        university_id = db.execute(
            "SELECT id FROM University WHERE name = %s", (name,), "one"
        )[0]
    except Exception as e:
        terminate(db, e)

    return university_id


def insert_degree(db, university_id, degree):
    try:
        db.execute(
            "INSERT INTO Degree (url, name, description, outings, academic_degree, type_of_course, duration) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (degree.url, degree.title, degree.description, degree.exits, "", "", 1),
            "none",
        )
    except psycopg2.errors.UniqueViolation:
        pass
    except Exception as e:
        terminate(db, e)

    try:
        degree_id = db.execute(
            "SELECT id FROM Degree WHERE url = %s", (degree.url,), fetch="one"
        )[0]
        db.execute(
            "INSERT INTO UniversityDegree (university_id, degree_id) VALUES (%s, %s)",
            (university_id, degree_id),
            "none",
        )
    except Exception as e:
        terminate(db, e)

    return degree_id


def get_urls_courses(degree_url):
    match = re.search(r"pv_curso_id=(\d+)", degree_url)
    if match:
        id_degree = match.group(1)
    else:
        return []

    start_pos = degree_url.find("sigarra.up.pt/") + len("sigarra.up.pt/")
    end_pos = degree_url.find("/pt/cur_geral")
    faculty = degree_url[start_pos:end_pos]
    return get_course_list(id_degree, faculty)


def insert_courses(db, degree_id, degree_url):
    urls_courses = get_urls_courses(degree_url)
    for url_course in urls_courses:
        id_course = db.execute(
            "SELECT id FROM CourseUnit WHERE url = %s", (url_course,), fetch="one"
        )
        if id_course != None:
            try:
                db.execute(
                    "INSERT INTO DegreeCourse (degree_id, course_id) VALUES (%s, %s)",
                    (degree_id, id_course[0]),
                    "none",
                )
            finally:
                print("Course already exists")
                pass
        else:
            course = parse_unit_page(url_course)
            try:
                db.execute(
                    "INSERT INTO CourseUnit (name, url, code, language, ects, objectives, results, working_method, pre_requirements, program, evaluation_type, passing_requirements) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (
                        course.name,
                        url_course,
                        course.code,
                        course.language,
                        course.credits,
                        course.objectives,
                        course.results,
                        course.working_method,
                        course.pre_requirements,
                        course.program,
                        course.evaluation_type,
                        course.passing_requirements,
                    ),
                    "none",
                )
            except Exception as e:
                print(e)
                print("Error adding course! URL: " + url_course)
                pass


def main(args):
    db = database.Database(args.host, args.port, args.user, args.pwd, args.db)
    db.connect()
    if args.reset:
        db.exec_file(args.schema)

    university_id = insert_university(db, args.university_name, args.university_url)
    for degree in fetch_degrees(args.url, args.university_url):
        degree_id = insert_degree(db, university_id, degree)
        insert_courses(db, degree_id, degree.url)


if __name__ == "__main__":
    args = arguments()
    main(args)
