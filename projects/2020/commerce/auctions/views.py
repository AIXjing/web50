from datetime import datetime
from unicodedata import category
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Listing

from .models import User


def index(request):
    return render(request, "auctions/index.html", {
        "Listings": Listing.objects.all(),
    })

def create(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        category = request.POST["category"]
        created_date = datetime.now
        creator = request.user
        
        # create an object with above parameters
        list = Listing(
            title = title,
            description = description,
            starting_bid = starting_bid,
            current_bid = starting_bid,
            category = category,
            created_date = created_date,
            creator = creator
        )
        list.save()

        # once a new list is created, return to the home page.
        return HttpResponseRedirect(reverse("index"))

    return render(request, "auctions/create.html", {
        "categories": {'Fashion', 'Toys', 'Home', 'Electronics'},
    })

# show listing page
def listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)

    # check if the listing is alreayding in the watchlist
    user = request.user
    # check if user is logged in
    if user:
        is_watched = listing.watchers.filter(wishlistings = listing.id)

        if request.method == "POST": 
            if not is_watched: # add the listing to watchlist
                listing.watchers.add(user)
                return HttpResponseRedirect(reverse("listing", args=(listing.id,)))
            else: # remove from the listing to watchlist
                listing.watchers.remove(user)
                return HttpResponseRedirect(reverse("listing", args=(listing.id,)))
    else: 
        return login_view(request)

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "is_watched": is_watched
    })

# show watchlist page
def watchlist(request):
    user = request.user
    return render(request, "auctions/watchlist.html", {
        "wishlistings": user.wishlistings.all(),
    })

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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
