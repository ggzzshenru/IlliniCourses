from django.shortcuts import render
from course import models
from django.db import connection
from course import utility

# Create your views here.
def search(request):
    return render(request, 'search.html', {})

def course(request, subject_number):
    # format subject_number from e.g. CS411 to CS_411
    subject = []
    number = []
    for i, c in enumerate(subject_number):
        if(c.isalpha()):
            subject.append(c)
            continue
        number.extend(subject_number[i:])
        break
    subject = ''.join(subject)
    number = ''.join(number)
    subject_number = subject + "_" + number

    # query database
    GPA_Mapping = {"a_plus": 4.0, "a": 4.00, "a_minus": 3.67,   \
                    "b_plus": 3.33, "b": 3, "b_minus": 2.67,    \
                    "c_plus": 2.33, "c": 2.00, "c_minus": 1.67, \
                    "d_plus": 1.33, "d": 1.00, "d_minus": 0.67, \
                    "f": 0.00, "abs": 0.00, "w": 0.00}
    sql = "SELECT subject_number_id AS subject_number, year_term_id AS year_term, \
            first_name, middle_name, last_name, \
            sum(a_plus) AS a_plus, sum(a) AS a, sum(a_minus) AS a_minus, \
            sum(b_plus) AS b_plus, sum(b) AS b, sum(b_minus) AS b_minus, \
            sum(c_plus) AS c_plus, sum(c) AS c, sum(c_minus) AS c_minus, \
            sum(d_plus) AS d_plus, sum(d) AS d, sum(d_minus) AS d_minus, \
            sum(w) AS w, sum(f) AS f\
            FROM Grade \
            WHERE subject_number_id = \"{subject_number}\" \
            GROUP BY year_term_id, first_name, middle_name, last_name" \
            .format(subject_number = subject_number)

    # handle queried data
    cursor = connection.cursor()
    cursor.execute(sql)
    data = utility.dictfetchall(cursor)
    GPA_semester = {}
    GPA_instructor = {}
    all_semester = []
    all_instructor = []
    for semester in data:
        current_semester = semester["year_term"]
        instructor_name = ' '.join([semester["first_name"], semester["middle_name"], semester["last_name"]]) \
                            if semester["middle_name"] else ' '.join([semester["first_name"], semester["last_name"]])
        if(instructor_name not in GPA_instructor):
            GPA_instructor[instructor_name] = {"total_count": 0, "total_GPA": 0}
            all_instructor.append(instructor_name)
        if(current_semester not in GPA_semester):
            GPA_semester[current_semester] = {"total_count": 0, "total_GPA": 0}
            all_semester.append(current_semester)

        for k, v in GPA_Mapping.items():
            if(k in semester):
                GPA_semester[current_semester]["total_count"] += int(semester[k])
                GPA_semester[current_semester]["total_GPA"] += (int(semester[k]) * v)
                GPA_instructor[instructor_name]["total_count"] += int(semester[k])
                GPA_instructor[instructor_name]["total_GPA"] += (int(semester[k]) * v)

    all_semester = sorted(all_semester)
    all_instructor = sorted(all_instructor)

    # returned data
    ret_dic = {"GPA_semester" : GPA_semester, "all_semester": all_semester, \
                "GPA_instructor": GPA_instructor, "all_instructor": all_instructor}
    return render(request, "course.html", ret_dic)

def ranking(request):
    # query default subject list and gened list
    sql = "SELECT subject, subject_number FROM Course GROUP BY subject"
    default_subject_list = [i.subject for i in models.Course.objects.raw(sql)]
    sql = "SELECT type FROM GeneralEducation"
    default_gened_list = [i.type for i in models.GeneralEducation.objects.raw(sql)]
    default_record_size = "20"
    # parse request data
    is_data_only = request.GET.get("isdataonly", "False")
    subject_list = request.GET.getlist("subject", default_subject_list)
    gened_list = request.GET.getlist("gened", default_gened_list)
    avg_rating_lo = int(request.GET.get("avgratinglo", "-1"))
    avg_rating_hi = int(request.GET.get("avgratinghi", "10"))
    avg_workload_lo = int(request.GET.get("avgworkloadlo", "-1"))
    avg_workload_hi = int(request.GET.get("avgworkloadhi", "10"))
    rating_order = request.GET.get("ratingorder", "ASC")
    workload_order = request.GET.get("workloadorder", "ASC")
    lo = request.GET.get("lo", "0")
    hi = request.GET.get("hi", default_record_size)
    record_size = str((int(hi) - int(lo)) + 1)

    # do the query
    sql = "SELECT * \
    FROM Course JOIN GenedSatisfaction ON Course.subject_number = GenedSatisfaction.subject_number_id\
    WHERE average_rating >= {avg_rating_lo} AND average_rating <= {avg_rating_hi} \
    AND average_workload >= {avg_workload_lo} AND average_workload <= {avg_workload_hi} \
    AND subject IN ({subject_list}) AND type_id IN ({gened_list}) \
    ORDER BY average_rating {rating_order}, average_workload {workload_order} \
    LIMIT {record_size} \
    OFFSET {lo}" \
    .format(avg_rating_lo = avg_rating_lo, avg_rating_hi = avg_rating_hi,\
    avg_workload_lo = avg_workload_lo, avg_workload_hi = avg_workload_hi, \
    subject_list = ','.join(["\"" + s + "\"" for s in subject_list]), \
    gened_list = ','.join(["\"" + s + "\"" for s in gened_list]), \
    rating_order = rating_order, workload_order = workload_order, record_size = record_size, lo = lo)

    # handle the result
    cursor = connection.cursor()
    cursor.execute(sql)
    all_rows = utility.dictfetchall(cursor)
    dic = {i:all_rows[i] for i in range(len(all_rows))}

    # send back the data
    if(True if is_data_only == "True" else False):
        return JsonResponse(dic)
    else:
        dic["default_subject_list"] = default_subject_list
        dic["default_gened_list"] = default_gened_list
        return render(request, "ranking.html", dic);


def error(request):
    return render(request, "error.html", {});
