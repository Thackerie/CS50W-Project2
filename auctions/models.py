from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name= models.CharField(max_length=64,)
    def __str__(self) ->str:
        return f"{self.name}"

class Listing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Listings")
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=200)
    image = models.ImageField(upload_to="listing_images", blank=True)

    categories = models.ManyToManyField(Category, related_name="listings")

    starting_price = models.FloatField()

    watchlisted = models.ManyToManyField(User, related_name="watchlist", null=True, blank=True)

    #active bool to check if bidding is still ongoing
    active = models.BooleanField()
    def __str__(self) -> str:
        title = self.title.replace(" ","_")
        return f"{title}"
    
class Bid(models.Model):
    amount= models.FloatField()
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="Bids")

    def __str__(self) -> str:
        return f"Bid on {self.listing}  by {self.bidder} "
    
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Comments")
    content = models.CharField(max_length=200)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="Comments")