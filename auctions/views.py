from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from django import forms

from .models import User, Listing, Category

class WatchlistForm(forms.Form):
    watchlist = forms.BooleanField(widget=forms.HiddenInput(attrs={"value": "True", "name" : "watchlist"}))

def watchlist(request):
    noResults = False
    id = request.user.id
    listingObjects = Listing.objects.filter(active__exact = True).filter(watchlisted= id)
    listings = make_listing_touple(listingObjects)
    if len(listings) == 0:
        noResults = True
    return render(request, "auctions/watchlist.html", {
        "listings" : listings,
        "noResults" : noResults
    })

def listing(request, name):
    data = Listing.objects.filter(title__exact = name.replace("_"," ")).values()
    if request.method == "POST":
        form = WatchlistForm(request.POST)
        if form.is_valid():
            username = request.user.username
            value = form.cleaned_data["watchlist"]
            user = User.objects.get(username=username)
            user.watchlist.add(data[0]["id"])
            user.save()
    #getting the data that is related to the given name of a listing

    return render(request, "auctions/listing.html", {
        "name" : name,
        "root" : settings.MEDIA_URL,
        "form" : WatchlistForm(),
        "data" : data[0]
    })

def make_listing_touple(listingObjects):
    listingNames = []
    listings = []
    counter = 0

    for listing in listingObjects:
        #adding names of the listings with removed underscores for pretttier looks to special list of names
        listingNames.append(str(listing).replace("_"," ")) 
        #adding name list and listing object list together in a list of touples
        listings.append((listing, listingNames[counter])) 
        counter += 1
    return listings

def index(request):
    listingObjects = Listing.objects.filter(active__exact = True)

    listings = make_listing_touple(listingObjects)
    return render(request, "auctions/index.html", {
        "listings" : listings
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

def new(request):
    return render(request, "auctions/new.html")

def categories(request):
    categories = []
    #add underscore name thing too 
    for category in Category.objects.all():
        categories.append(category)
    return render(request, "auctions/categories.html", {
        "categories" : categories
    })

def category(request, name:str):
    #instanciating variables
    noResults = False

    #getting all listings labelled with category of name (name:str)
    listingObjects = Listing.objects.filter(active__exact = True).filter(categories__name=name)

    #creating a list containing touples with listing object and name
    listings = make_listing_touple(listingObjects)

    #checking if there are no listings found to display it on the page
    if len(listings) == 0:
        noResults = True

    #rendering the page
    return render(request,"auctions/category.html", {
        "name" : name,
        "listings" : listings,
        "noResults" : noResults
    })
