from datetime import datetime
from select import select
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import  HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from auctions.utils import get_categories, submit_bid, submit_comment, update_watchlist
from .models import Listing
from django.contrib.auth.decorators import login_required

from .models import User
from auctions import models


def index(request):
    return render(request, "auctions/index.html", {
        "Listings": Listing.objects.filter(is_active = True),
    })

@login_required
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
            creator = creator,
            # is_active = True,
            current_bidder = request.user,
        )
        list.save()
        return HttpResponseRedirect(reverse("index"))

    return render(request, "auctions/create.html", {
        "categories": get_categories()
    })

# show listing page
@login_required
def listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)

    # check if the listing is already in the watchlist of this user
    user = request.user
    is_watched = user.wishlistings.filter(id=listing.id)
    is_creator = (listing.creator == user)
    # is_watched = listing.watchers.filter(wishlistings = listing.id)
    if request.method == "POST": 

        if "update_watchlist" in request.POST: 
            update_watchlist(is_watched, user, listing)
            
        elif "submit_bid" in request.POST: 
            submit_bid(request, listing, user)

        elif "submit_comment" in request.POST:
            submit_comment(request, listing, user)
        
        elif "close_auction" in request.POST:
            listing.is_active = False
            listing.save()
            return HttpResponseRedirect(reverse("index"))

        return HttpResponseRedirect(reverse("listing", args=(listing.id,)))

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "is_watched": is_watched,
        "is_creator" : is_creator,
        "comments": listing.comments.all()
    })

# show watchlist page
def watchlist(request):
    user = request.user
    return render(request, "auctions/watchlist.html", {
        "Listings": user.wishlistings.all(),
    })

# show closed listings if user owns the auction
@login_required
def closed_listings(request):
    owned_auctions = Listing.objects.filter(
        is_active = False,
        current_bidder = request.user,
        )
    return render(request, "auctions/closed_listings.html", {
        "listings" : owned_auctions,
    })

# show listings based on categories
def categories(request):
    if request.method == "POST":
        selected_category = request.POST["selected_category"]
        return render(request, "auctions/categories.html", {
            "categories": get_categories(),
            "selected_category": selected_category,
            "Listings": Listing.objects.filter(category=selected_category)
        })
    return render(request, "auctions/categories.html", {
            "categories": get_categories(),
            "Listings": Listing.objects.filter(is_active = True),
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
