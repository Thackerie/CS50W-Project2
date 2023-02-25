from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings

from .forms import NewListingForm, WatchlistForm, BidForm
from .models import User, Listing, Category, Bid



def new(request):
    if request.method == "POST":
        form = NewListingForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user
            id = len(Listing.objects.all())+1
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            startingPrice = form.cleaned_data["startingPrice"]
            image = "listing_images/"+ form.data["image"].replace(" ","_")
            categories = form.cleaned_data["categories"]
            listing = Listing(id=id, owner=user,title=title, description=description, starting_price=startingPrice, image=image, active=True)
            listing.save()
            listing.categories.set(categories)
           
            
    return render(request, "auctions/new.html", {
        "form": NewListingForm()
    })


def listing(request, name):
    #getting listing object from name given
    listing = Listing.objects.filter(title__exact = name.replace("_"," "))
    #getting all data from the listing object
    data = listing.values()
    #handling watchlist button
    if request.method == "POST":
        user = User.objects.get(username=request.user.username)
        #instatiating the form
        watchlistForm = WatchlistForm(request.POST)
        if watchlistForm.is_valid():
            #instatiating user object based on the name in the request
            #adding the listing to the user using its id
            user.watchlist.add(data[0]["id"])
            user.save()
        
        bidForm = BidForm(request.POST)
        if bidForm.is_valid():
            bid = Bid(amount= bidForm.cleaned_data["bid"], bidder=user, listing=listing[0])
            bid.save()

    #getting correlating user object of the owner of the listing using the owner_id
    owner = User.objects.filter(id__exact = data[0]["owner_id"])[0]

    #getting all category objects related to the listing object
    categories = listing[0].categories.all()

    return render(request, "auctions/listing.html", {
        "name" : name,
        "root" : settings.MEDIA_URL,
        "watchlistForm" : WatchlistForm(),
        "bidForm" : BidForm(),
        "data" : data[0],
        "owner" : owner,
        "categories" : categories
    })

def make_listing_touple(listingObjects):
    listings = []
    highestBid = None
    for listing in listingObjects:
        amount= 0
        #getting the highest bid for that listing
        for bid in Bid.objects.filter(listing=listing) :
            try:
                if bid.amount > amount:
                    amount = bid.amount
                    highestBid = bid
            except IndexError:
                pass
        #adding name list and listing object list together in a list of touples
        listings.append((listing, str(listing).replace("_"," "), highestBid))
        highestBid = None

    return listings

def index(request):
    noResults = False
    noBids = False
    listingObjects = Listing.objects.filter(active__exact = True)
    listings = make_listing_touple(listingObjects)
    #listings.append(Bid.objects.filter(listing=1))
    if len(listings) == 0:
        noResults = True
    if listings[2] == None:
        noBids = True
    return render(request, "auctions/index.html", {
        "listings" : listings,
        "noResults" : noResults,
        "noBids" : noBids
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