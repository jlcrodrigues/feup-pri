DROP SCHEMA IF EXISTS pri_g81 CASCADE;
CREATE SCHEMA pri_g81;
SET SCHEMA 'pri_g81';

DROP TABLE IF EXISTS University CASCADE;
DROP TABLE IF EXISTS Degree CASCADE;
DROP TABLE IF EXISTS UniversityDegree CASCADE;
DROP TABLE IF EXISTS Professor CASCADE;
DROP TABLE IF EXISTS ProfessorDegree CASCADE;
DROP TABLE IF EXISTS CourseUnit CASCADE;
DROP TABLE IF EXISTS ProfessorCourseUnit CASCADE;
DROP TABLE IF EXISTS DegreeCourseUnit CASCADE;

CREATE TABLE University (
    id SERIAL PRIMARY KEY,
    url VARCHAR NOT NULL UNIQUE,
    name VARCHAR NOT NULL UNIQUE
);

CREATE TABLE Degree (
    id SERIAL PRIMARY KEY,
    url VARCHAR NOT NULL UNIQUE,
    name VARCHAR NOT NULL,
    description TEXT,
    outings TEXT,
    academic_degree VARCHAR,
    type_of_course VARCHAR NOT NULL,
    duration INT CHECK (duration > 0)
);

CREATE TABLE UniversityDegree (
    university_id INT NOT NULL REFERENCES University(id),
    degree_id INT NOT NULL REFERENCES Degree(id),
    PRIMARY KEY (university_id, degree_id)
);

CREATE TABLE Professor (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    personal_website VARCHAR,
    institutional_website VARCHAR NOT NULL UNIQUE,
    abbreviation VARCHAR,
    status VARCHAR,
    code INT NOT NULL UNIQUE,
    institutional_email VARCHAR(150) UNIQUE,
    phone VARCHAR,
    rank VARCHAR,
    personal_presentation TEXT,
    fields_of_interest TEXT
);

CREATE TABLE ProfessorDegree (
    professor_id INT NOT NULL REFERENCES Professor(id),
    degree_id INT NOT NULL REFERENCES Degree(id),
    role VARCHAR NOT NULL,
    PRIMARY KEY (professor_id, degree_id)
);

CREATE TABLE CourseUnit (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    url VARCHAR NOT NULL UNIQUE,
    code VARCHAR,
    language VARCHAR,
    ects INT CHECK (ects > 0),
    objectives TEXT,
    results TEXT,
    working_method TEXT,
    pre_requirements TEXT,
    program TEXT,
    evaluation_type TEXT,
    passing_requirements TEXT
);

CREATE TABLE ProfessorCourseUnit (
    professor_id INT NOT NULL REFERENCES Professor(id),
    course_unit_id INT NOT NULL REFERENCES CourseUnit(id),
    type VARCHAR NOT NULL,
    PRIMARY KEY (professor_id, course_unit_id, type)
);

CREATE TABLE DegreeCourseUnit (
    degree_id INT NOT NULL REFERENCES Degree(id),
    course_unit_id INT NOT NULL REFERENCES CourseUnit(id),
    year INT CHECK (year > 0), --NOT NULL,
    semester INT,-- CHECK (semester > 0 AND semester < 3) NOT NULL,
    PRIMARY KEY (degree_id, course_unit_id)
);
