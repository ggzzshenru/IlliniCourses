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
