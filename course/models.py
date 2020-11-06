from django.db import models

# Create your models here.
class Course(models.Model):
    subject_number = models.CharField(max_length = 64, primary_key = True)
    title = models.CharField(max_length = 64)
    # comma seperated subject_number prerequsite list for the current course
    prerequsite = models.CharField(max_length = 512)
    introduction = models.CharField(max_length = 512)

class GeneralEducation(models.Model):
    type = models.CharField(max_length = 64, primary_key = True)

class GenedSatisfaction(models.Model):
    subject_number = models.ForeignKey(Course, on_delete = models.CASCADE)
    type = models.ForeignKey(GeneralEducation, on_delete = models.CASCADE)
    # can not set two field as primary key, use unique constraints to bypass it
    class Meta:
        constraints = [
            models.UniqueConstraint(fields = ['subject_number', 'type'], name='genedsatisfaction_unique_constraint')
        ]

class Semester(models.Model):
    year_term = models.CharField(max_length = 64)

class Instructor(models.Model):
    email = models.CharField(max_length = 64, primary_key = True)
    department = models.CharField(max_length = 64)
    first_name = models.CharField(max_length = 64)
    middle_name = models.CharField(max_length = 64)
    last_name =  models.CharField(max_length = 64)

class Grade(models.Model):
    subject_number = models.ForeignKey(Course, on_delete = models.CASCADE)
    email = models.ForeignKey(Instructor, on_delete = models.DO_NOTHING)
    year_term = models.ForeignKey(Semester, on_delete = models.CASCADE)

    a_plus = models.IntegerField()
    a = models.IntegerField()
    a_minus = models.IntegerField()
    b_plus = models.IntegerField()
    b = models.IntegerField()
    b_minus = models.IntegerField()
    c_plus = models.IntegerField()
    c = models.IntegerField()
    c_minus = models.IntegerField()
    d_plus = models.IntegerField()
    d = models.IntegerField()
    d_minus = models.IntegerField()
    w = models.IntegerField()
    f = models.IntegerField()
