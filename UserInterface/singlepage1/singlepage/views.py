from django.http import Http404, HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "singlepage/index.html")

texts= ["Text1", "Text2", "Text3"]

def section(request, num):
    if 1 <= num <= 3:
        return HttpResponse(texts[num-1])
    else:
        return Http404("No such section!")
