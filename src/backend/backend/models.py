# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Courseunit(models.Model):
    name = models.CharField()
    url = models.CharField(unique=True)
    code = models.CharField(blank=True, null=True)
    language = models.CharField(blank=True, null=True)
    ects = models.IntegerField(blank=True, null=True)
    objectives = models.TextField(blank=True, null=True)
    results = models.TextField(blank=True, null=True)
    working_method = models.TextField(blank=True, null=True)
    pre_requirements = models.TextField(blank=True, null=True)
    program = models.TextField(blank=True, null=True)
    evaluation_type = models.TextField(blank=True, null=True)
    passing_requirements = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'courseunit'


class Degree(models.Model):
    url = models.CharField(unique=True)
    name = models.CharField()
    description = models.TextField(blank=True, null=True)
    outings = models.TextField(blank=True, null=True)
    academic_degree = models.CharField(blank=True, null=True)
    type_of_course = models.CharField()
    duration = models.CharField()

    class Meta:
        managed = False
        db_table = 'degree'


class Degreecourseunit(models.Model):
    degree = models.OneToOneField(Degree, models.DO_NOTHING, primary_key=True)  # The composite primary key (degree_id, course_unit_id) found, that is not supported. The first column is selected.
    course_unit = models.ForeignKey(Courseunit, models.DO_NOTHING)
    year = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'degreecourseunit'
        unique_together = (('degree', 'course_unit'),)


class Professor(models.Model):
    name = models.CharField()
    personal_website = models.CharField(blank=True, null=True)
    institutional_website = models.CharField(unique=True)
    abbreviation = models.CharField(blank=True, null=True)
    status = models.CharField(blank=True, null=True)
    code = models.IntegerField(unique=True)
    institutional_email = models.CharField(unique=True, max_length=150, blank=True, null=True)
    phone = models.CharField(blank=True, null=True)
    rank = models.CharField(blank=True, null=True)
    personal_presentation = models.TextField(blank=True, null=True)
    fields_of_interest = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'professor'


class Professorcourseunit(models.Model):
    professor = models.OneToOneField(Professor, models.DO_NOTHING, primary_key=True)  # The composite primary key (professor_id, course_unit_id, type) found, that is not supported. The first column is selected.
    course_unit = models.ForeignKey(Courseunit, models.DO_NOTHING)
    type = models.CharField()

    class Meta:
        managed = False
        db_table = 'professorcourseunit'
        unique_together = (('professor', 'course_unit', 'type'),)


class University(models.Model):
    url = models.CharField(unique=True)
    name = models.CharField(unique=True)

    class Meta:
        managed = False
        db_table = 'university'


class Universitydegree(models.Model):
    university = models.OneToOneField(University, models.DO_NOTHING, primary_key=True)  # The composite primary key (university_id, degree_id) found, that is not supported. The first column is selected.
    degree = models.ForeignKey(Degree, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'universitydegree'
        unique_together = (('university', 'degree'),)
