from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
	title = models.CharField(max_length=80)
	descr = models.TextField()
	starting_bid = models.DecimalField(max_digits=7, decimal_places=2)
	creation_date = models.DateField(auto_now_add=True)
	close_date = models.DateField(auto_now=True)
	status = models.BooleanField(default=True)
	image = models.ImageField(null=True, blank=True, upload_to='listing_images', default='default.jpg')

	seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="u_listings")

	def __str__(self):
		return f"{self.title} {self.descr} {self.creation_date} {self.starting_bid} {self.close_date} {self.l_comments}"

class Bid(models.Model):

	value = models.DecimalField(max_digits=7, decimal_places=2)
	bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="u_bids")
	listing_bid = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="l_bids")

	def __str__(self):
		return f"{self.value} {self.bidder} {self.listing_bid}"

class Comments(models.Model):

	content = models.CharField(max_length=1000)
	creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="u_comments")
	listing_comment = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="l_comments")

	def __str__(self):
		return f"{self.content} {self.creator} {self.listing_comment}"

