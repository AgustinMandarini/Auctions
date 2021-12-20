from django import forms

class NewListing(forms.Form):

	title = forms.CharField(max_length=80)
	descr = forms.CharField(widget=forms.Textarea)
	image = forms.ImageField()

class NewBid(forms.Form):

	value = forms.DecimalField(max_digits=7, decimal_places=2)