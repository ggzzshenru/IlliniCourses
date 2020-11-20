from django.shortcuts import render

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
    # parse request data
    subject_list = request.GET.getlist("subject", [])           # string list
    gened_list = request.GET.getlist("gened", [])               # string list
    avg_rating_lo = int(request.GET.get('avgratinglo', 0))      # int
    avg_rating_hi = int(request.GET.get('avgratinghi', 10))     # int
    avg_workload_lo = int(request.GET.get('avgworkloadlo', 0))  # int
    avg_workload_hi = int(request.GET.get('avgworkloadhi', 10)) # int
    rating_order = request.GET.get('ratingorder', "ASC")      # string DESC OR ASC
    workload_order = request.GET.get('workloadorder', "ASC")    # string DESC OR ASC
    lo = request.GET.get('lo', 0)
    hi = request.GET.get('hi', 20)
    # parse

    return render(request, "ranking.html", {});

def error(request):
    return render(request, "error.html", {});
