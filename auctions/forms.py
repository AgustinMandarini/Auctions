from django import forms
from .models import CATEGORY_CHOICES

class NewListing(forms.Form):

	title = forms.CharField(max_length=80)
	descr = forms.CharField(widget=forms.Textarea)
	category = forms.ChoiceField(choices=CATEGORY_CHOICES)
	image = forms.ImageField()

class NewBid(forms.Form):

	value = forms.DecimalField(max_digits=7, decimal_places=2)
