from django import forms

from .models import Category

class WatchlistForm(forms.Form):
    watchlist = forms.BooleanField(widget=forms.HiddenInput(attrs={"value": "True", "name" : "watchlist"}))

class NewListingForm(forms.Form):
    choices = []
    categories = Category.objects.all()
    categoryCount = 1 
    for category in categories:
        choices.append((categoryCount, str(category)))
        categoryCount+= 1
    title = forms.CharField()
    description = forms.CharField()
    image = forms.ImageField(required=False)
    startingPrice = forms.FloatField()
    categories = forms.MultipleChoiceField(choices=choices, required=False)

class BidForm(forms.Form):
    bid = forms.FloatField(initial=1)

class CloseForm(forms.Form):
    closed = forms.BooleanField(widget=forms.HiddenInput(attrs={"value": "True", "name" : "close"}))

class CommentForm(forms.Form):
    comment = forms.CharField()