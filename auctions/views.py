from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid, Comments
from .forms import NewListing, NewBid


def index(request):
    listings = Listing.objects.all()

    return render(request, "auctions/index.html", {
        "listings": listings,
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

@login_required
def new_listing(request):
    if request.method == "POST":
        # request.POST handles regular form data while request.FILES handles images
        listing_form = NewListing(request.POST, request.FILES)
        bid_form = NewBid(request.POST)
        # Checks if data submited is valid and if user has signed in
        if listing_form.is_valid() and bid_form.is_valid() and request.user.is_authenticated:

            # Creates a new listing from posted listing form
            title = listing_form.cleaned_data["title"]
            descr = listing_form.cleaned_data["descr"]
            category = listing_form.cleaned_data["category"]
            image = request.FILES['image']

            # Starting listing bid value is obtained from NewBid form
            # and is assigned to current_bid value, which is the same value
            # of new_bid
            value = bid_form.cleaned_data['value']
            creator = User.objects.get(pk=request.user.id)

            new_listing = Listing(title=title, descr=descr, category=category, image=image, creator=creator, current_bid=value)
            new_listing.save()

            # Creates a new bid for the new listing, assigning the recently created listing's id
            l = Listing.objects.get(pk=new_listing.id)

            new_bid = Bid(bidder=creator, value=value, listing=l)
            new_bid.save()

            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/new_listing.html", {
                "listing_form": listing_form, 
                "bid_form": bid_form
                })
    else:
        return render(request, "auctions/new_listing.html", {
            "listing_form": NewListing(),
            "bid_form": NewBid()
            })