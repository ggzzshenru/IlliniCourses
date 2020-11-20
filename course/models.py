from django.db import models
# Create your models here.
class Course(models.Model):
    subject_number = models.CharField(max_length = 64, primary_key = True)
    title = models.CharField(max_length = 64)
    # redundency here.
    subject = models.CharField(max_length = 64)
    number = models.CharField(max_length = 64)
    prerequsite = models.CharField(max_length = 512)
    introduction = models.CharField(max_length = 512)
    average_workload = models.IntegerField()
    average_rating = models.IntegerField()
    class Meta:
        constraints = [
            models.CheckConstraint(check = models.Q(average_workload__gte = '0'), name = "course_averge_workload_gte_zero_constraint"),
            models.CheckConstraint(check = models.Q(average_rating__gte = '0'), name = "course_averge_rating_gte_zero_constraint"),
            models.CheckConstraint(check = ~models.Q(subject_number = ""), name = "course_subject_number_not_null_constraint"),
            models.CheckConstraint(check = ~models.Q(subject = ""), name = "course_subject_not_null_constraint"),
            models.CheckConstraint(check = ~models.Q(number = ""), name = "course_number_not_null_constraint"),
            models.CheckConstraint(check = ~models.Q(title = ""), name = "course_title_not_null_constraint"),
            models.UniqueConstraint(fields = ["subject", "number"], name = "course_title_unique_constraint")
        ]


class GeneralEducation(models.Model):
    type = models.CharField(max_length = 64, primary_key = True)
    class Meta:
        constraints = [
            models.CheckConstraint(check = ~models.Q(type = ""), name = "general_education_not_null_constraint")
        ]

class GenedSatisfaction(models.Model):
    subject_number_type = models.CharField(max_length = 64, primary_key = True)
    subject_number = models.ForeignKey(Course, on_delete = models.CASCADE)
    type = models.ForeignKey(GeneralEducation, on_delete = models.CASCADE)
    # can not set two field as primary key, use unique constraints to bypass it
    class Meta:
        constraints = [
            models.CheckConstraint(check = ~models.Q(subject_number_type = ""), name = "gened_satisfication_subject_number_type_not_null_constraint"),
            models.CheckConstraint(check = ~models.Q(subject_number = ""), name = "gened_satisfication_subject_numbe_not_null_constraint"),
            models.CheckConstraint(check = ~models.Q(type = ""), name = "gened_satisfication_type_not_null_constraint")
        ]

class Semester(models.Model):
    year_term = models.CharField(max_length = 64, primary_key = True)
    year = models.CharField(max_length = 64)
    term = models.CharField(max_length = 64)
    class Meta:
        constraints = [
            models.CheckConstraint(check = ~models.Q(year_term = ""), name = "semester_year_term_not_null_constraint"),
            models.CheckConstraint(check = ~models.Q(year = ""), name = "semester_year_not_null_constraint"),
            models.CheckConstraint(check = ~models.Q(term = ""), name = "semester_term_not_null_constraint")
        ]

class Grade(models.Model):
    subject_number = models.ForeignKey(Course, on_delete = models.CASCADE)
    year_term = models.ForeignKey(Semester, on_delete = models.CASCADE)

    first_name = models.CharField(max_length = 64)
    middle_name = models.CharField(max_length = 64)
    last_name =  models.CharField(max_length = 64)

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
    class Meta:
        constraints = [
            models.CheckConstraint(check = ~models.Q(first_name = ""), name = "grade_first_name_not_null_constraint"),
            models.CheckConstraint(check = ~models.Q(last_name = ""), name = "grade_last_name_not_null_constraint")
        ]
