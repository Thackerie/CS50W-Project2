from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    CATEGORIES = [
        ("1","Category 1"),
        ("2", "Category 2"),
        ("3", "Category 3")
    ]
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Listings")
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=200)
    creation_date = models.DateTimeField()
    #image = models.ImageField()

    #multiple categories somehow
    category = models.CharField(max_length=64, choices=CATEGORIES)

    starting_price = models.FloatField()
    #use Listing.Comments.all() to get all related comments
    watchlisted = models.ManyToManyField(User, related_name="Watchlist", null=True, blank=True)
    def __str__(self) -> str:
        return f"{self.title}: {self.starting_price}"
    
class Bid(models.Model):
    amount= models.FloatField()
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="Bids")
    
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Comments")
    content = models.CharField(max_length=200)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="Comments")