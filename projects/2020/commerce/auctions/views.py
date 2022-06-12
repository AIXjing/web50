from datetime import datetime
from unicodedata import category
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Listing
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import User


def index(request):
    return render(request, "auctions/index.html", {
        "Listings": Listing.objects.all(),
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
        "categories": {'Fashion', 'Toys', 'Home', 'Electronics'},
    })

# show listing page
@login_required
def listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)

    # check if the listing is already in the watchlist of this user
    user = request.user
    is_watched = user.wishlistings.filter(id=listing.id)
    # is_watched = listing.watchers.filter(wishlistings = listing.id)
    if request.method == "POST": 
        # check if it is the post for watchlist
        if "update_watchlist" in request.POST: 
            if not is_watched: # add the listing to watchlist
                listing.watchers.add(user)
            else: # remove from the listing to watchlist
                listing.watchers.remove(user)
            return HttpResponseRedirect(reverse("listing", args=(listing.id,)))

            # if the post is to submit a bit
        elif "submit_bid" in request.POST: 
            bid = float(request.POST["bid"])
            # set restrictions for new bid
            previous_bid = listing.current_bid
            if bid > previous_bid:
                listing.current_bid = bid
                listing.current_bidder = user
                listing.save()
                messages.success(request, 'Successfully bid.')
            else:
                messages.warning(request, 'Invalid bid.')
            return HttpResponseRedirect(reverse("listing", args=(listing.id,)))

    # user as the creator is able to close the auction
    m = ""
    if request.method == "POST" and "close_auction" in request.POST:
        if user == listing.creator:
            listing.is_active = False
            listing.save()
            m = "The bid is closed."
            return HttpResponseRedirect(reverse("index"))
        else:
            m = "You are not the creator!"

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "is_watched": is_watched,
        "m" : m
    })

# show watchlist page
def watchlist(request):
    user = request.user
    return render(request, "auctions/watchlist.html", {
        "wishlistings": user.wishlistings.all(),
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
