from django.shortcuts import render
from course import models
from django.db import connection

# Create your views here.
def search(request):
    return render(request, 'search.html', {})

def course(request, subject_number):
    # query database
    # handler
    # context(handler)
    context = {
        "subject_number": subject_number
    }
    return render(request, "course.html", context)

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
    FROM Course JOIN GenedSatisfaction \
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
    def dictfetchall(cursor):
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]
    cursor = connection.cursor()
    cursor.execute(sql)
    dic = dictfetchall(cursor)
    dic = {i:dic[0] for i in range(len(dic))}

    # send back the data
    if(True if is_data_only == "True" else False):
        return JsonResponse(dic)
    else:
        dic["default_subject_list"] = default_subject_list
        dic["default_gened_list"] = default_gened_list
        return render(request, "ranking.html", dic);


def error(request):
    return render(request, "error.html", {});
