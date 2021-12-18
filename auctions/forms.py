from django import forms

class NewListing(forms.Form):

	title = forms.CharField(max_length=80)
	descr = forms.CharField(widget=forms.Textarea)
	starting_bid = forms.DecimalField(max_value=1000000, decimal_places=2)
	image = forms.ImageField()