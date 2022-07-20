from django.db.models import Count
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

from .models import Post, User


def index(request):

    # Authenticated users view their inbox
    if request.user.is_authenticated:
        return render(request, "network/index.html")

    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse("login"))

@csrf_exempt
@login_required
def compose(request):
     # Composing a new email must be via POST
    if request.method != "POST":
       return JsonResponse({"error": "POST request required."}, status=400)

    # Get Post data using json    
    data = json.loads(request.body)
    print("body: ", data.get("subject", ""))
    if data.get("subject", "") == "":
        return JsonResponse({
            "error": "Cannot post an empty message"
        }, status=400)
    else:
        poster = request.user
        post_subject = data.get("subject")
        timestamp = datetime.now

        # Save it to Post Class
        post = Post(
            poster = poster,
            subject = post_subject, 
            timestamp = timestamp)
        print("post: ", post)
        post.save()
        
        #return HttpResponseRedirect(reverse("index"))
    return JsonResponse({"message": "Post successfully."})


def show_posts(request):
    posts = Post.objects.all()
    print(posts)

    # Return emails in reverse chronologial order
    posts = posts.order_by("-timestamp").all()
    return JsonResponse([post.serialize() for post in posts], safe=False)

def post(request, post_id):
    pass

def page(request, pagename):
    pass


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
