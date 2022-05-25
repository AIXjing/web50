from django import http
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# render the whole url to seperate python and html logicals
def index(request):
    return render(request, "hello/index.html")

def world(request):
    return HttpResponse("Hello, world!")

def jean(request):
    return HttpResponse("Hello, Jean!")

def fuyang(request):
    return HttpResponse("Hello, Fuyang!")

# to parameterize url
# def greet(request, name):
    # in the curly bracket, we can make changes to the variable
    # return HttpResponse(f"Hello, {name.capitalize()}!")

def greet(request, name):
    return render(request, "hello/greet.html", {
        "name" : name.capitalize()
    })