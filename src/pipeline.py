import argparse
from fetchers.degrees import *
from fetchers.teachers import *
from fetchers.course_plan import *
from fetchers.course_unit import *
from db.database import *

from db import database
import psycopg2

def arguments():
    parser = argparse.ArgumentParser(description="Script to fetch data from the web and insert it into a relational database.")
    parser.add_argument("--host", default="localhost", help="The hostname or IP address of the database server. Default is 'localhost'.")
    parser.add_argument("--port", type=int, default=5432, help="The port number of the database server. Default is 5432.")
    parser.add_argument("--user", default="pri", help="The username to use when connecting to the database server. Default is 'pri'.")
    parser.add_argument("--pwd", default="pri", help="The password to use when connecting to the database server. Default is 'pri'.")
    parser.add_argument("--db", default="pri23", help="The name of the PostgreSQL database to use. Default is 'pri23'.")
    parser.add_argument("--url", nargs='+', default=["https://www.up.pt//portal/pt/estudar/licenciaturas-e-mestrados-integrados/oferta-formativa", "https://www.up.pt/portal/pt/estudar/mestrados/oferta-formativa"], help="Entry point links. Provide one or more URLs separated by spaces. These URLs will be used as the starting points for the web crawler. If no URLs are provided, the default URLs will be used.")
    parser.add_argument("--university_name", default="Universidade do Porto", help="The name of the university. Default is 'Universidade do Porto'.")
    parser.add_argument("--university_url", default="https://www.up.pt", help="The URL of the university. Default is 'https://www.up.pt'.")
    parser.add_argument("--reset", action="store_true", help="If this flag is provided, the database will be reset before inserting the data.", default=True)    
    parser.add_argument("--schema", help="The path to the SQL schema file. Default is 'db/schema.sql'.", default="db/schema.sql")
    return parser.parse_args()

def terminate(db, message = "An error occurred. Terminating..."):
    print("An error occurred. Terminating...")
    print(message)
    db.disconnect()
    exit(1)

def insert_university(db, name, url):
    try:
        db.execute("INSERT INTO University (name, url) VALUES (%s, %s)", (name, url))
    except psycopg2.errors.UniqueViolation:
        pass
    except Exception as e:
        terminate(db, e)

    try:
        university_id = db.execute("SELECT id FROM University WHERE name = %s", (name,), fetch="one")[0]
    except Exception as e:
        terminate(db, e)

    return university_id

def insert_degree(db, university_id, degree):
    try:
        db.execute("INSERT INTO Degree (url, name, description, outings, academic_degree, type_of_course, duration) VALUES (%s, %s, %s, %s, %s, %s, %s)", (degree.url, degree.title, degree.description, degree.exits, "", "", 1))
    except psycopg2.errors.UniqueViolation:
        pass
    except Exception as e:
        terminate(db, e)

    try:
        degree_id = db.execute("SELECT id FROM Degree WHERE url = %s", (degree.url,), fetch="one")[0]
        db.execute("INSERT INTO UniversityDegree (university_id, degree_id) VALUES (%s, %s)", (university_id, degree_id))
    except Exception as e:
        terminate(db, e)

    return degree_id

def main(args):
    
    db = database.Database(args.host, args.port, args.user, args.pwd, args.db)
    db.connect()
    if args.reset:
        db.exec_file(args.schema)

    university_id = insert_university(db, args.university_name, args.university_url)
    for degree in fetch_degrees(args.url):
        degree_id = insert_degree(db, university_id, degree)
        break

    
if __name__ == '__main__':
    args = arguments()
    main(args)