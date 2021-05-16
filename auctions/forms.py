from django import forms
from django.core.exceptions import ValidationError

from .models import Listing, Bid, Comment

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        exclude = ['seller', 'curr_bid', 'watchers', 'create_time']


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['value', 'listing']
        widgets = {
            'listing': forms.HiddenInput()
        }
        labels = {
            'value': 'Enter your bid'
        }

    def clean(self):
        cleaned_data = super().clean()

        # get the highest bid for current listing
        listing = cleaned_data['listing']
        listing_bids = listing.listing_bids.all()

        if listing_bids:
            curr_bid = listing_bids.order_by('-value').first().value
        else:
            curr_bid = listing.start_bid

        # check if new bid has a valid value   
        if curr_bid >= cleaned_data['value']:
            raise ValidationError(f'Please enter a bid value than {curr_bid}')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'listing']

        widgets = {
            'listing': forms.HiddenInput(),
            'text': forms.TextInput(attrs={'id': 'comment-field'})
        }

        labels = {
            'text': ''
        }
        
