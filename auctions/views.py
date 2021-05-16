from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

from .models import User, Listing, Bid, Comment
from .forms import ListingForm, BidForm, CommentForm

def index(request):

    query_results = Listing.objects.all()
    return render(request, "auctions/index.html", {'query_results': query_results})


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


def create_listing(request):
    form = ListingForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        # check if valid values are passed
        if form.is_valid():
            post = form.save(commit=False)  # do something with form before saving
            post.seller = request.user
            post.curr_bid = post.start_bid
            post.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.error(request, 'Invalid values encountered!')

    return render(request, "auctions/create_listing.html", {'form': form})


def listing(request, listing_id):
    '''
    renders the page for the given listing
    '''
    try:
        listing = Listing.objects.get(id=listing_id)
    except:
        return HttpResponseRedirect(reverse('index'))

    # get current bids for listing
    # if bids exists, return the highest bid. else return the starting bid
    listing_bids = listing.listing_bids.all()

    if listing_bids:
        curr_bid = listing_bids.order_by('-value').first().value

    else:
        curr_bid = listing.start_bid

    # comments
    comments = listing.listing_comments.all()
    return render(request, 'auctions/listing.html', {'listing': listing, 'curr_bid': curr_bid,
                                                      'bid_form': BidForm(initial={'listing': listing_id}),
                                                      'comment_form': CommentForm(initial={'listing': listing_id}),
                                                      'comments': comments})


def watchlist(request):
    '''
    similar to home page, renders the listings in the current user's watchlist
    '''
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        user_watchlist = user.watchlist.all()
        return render(request, "auctions/watchlist.html", {'user_pretty_name': user.username.capitalize(), 'user_watchlist': user_watchlist})
    else:
        return HttpResponseRedirect(reverse("index"))

@login_required
def update_watchlist(request, listing_id):
    '''
    adds / removes listings from the current user's watchlist
    '''
    if request.method == "POST":
        listing = Listing.objects.get(id=listing_id)
        watchlist = request.user.watchlist
        if listing in watchlist.all():
            watchlist.remove(listing)
        else:
            watchlist.add(listing)
    
    return HttpResponseRedirect(reverse("listing", kwargs={"listing_id": listing_id}))


def categories(request):
    '''
    renders the possible categories
    '''
    categories = Listing.objects.all().values("category").distinct()
    return render(request, 'auctions/categories.html', {"categories": [x['category'] for x in categories]})


def category(request, category_id):
    '''
    renders the listing in the given category
    '''
    if request.method == 'GET':
        listings = Listing.objects.filter(category=category_id)
        return render(request, 'auctions/category.html', {'listings': listings, 'category': category_id.capitalize()})


@login_required
def bid(request, listing_id):
    form = BidForm(request.POST or None)
    
    if request.method == 'POST':
        if form.is_valid():
            post = form.save(commit=False)  # do something with form before saving
            post.bidder = request.user
            post.save()
            messages.success(request, 'You are now the highest bidder!')

        else:
            messages.error(request, 'Please enter a valid value for bid!')

    return HttpResponseRedirect(reverse("listing", kwargs={"listing_id": listing_id}))


@login_required
def comment(request, listing_id):
    form = CommentForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()

    return HttpResponseRedirect(reverse("listing", kwargs={"listing_id": listing_id}))