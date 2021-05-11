from django import forms
from .models import Listing

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        exclude = ['seller', 'curr_bid', 'watchers', 'create_time']

    def clean(self):
        cleaned_data = super().clean()
