from django.http import HttpResponse

# Create your views here.
def index(request):
    # return doc page
    return HttpResponse("Welcome to the home automation heating page")
