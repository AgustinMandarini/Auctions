from django.contrib.auth.models import AbstractUser
from django.db import models

CATEGORY_CHOICES = [
	('A', 'Art'),
	('B', 'Books'),
    ('C', 'Clothing'),
    ('E', 'Electronics'),
    ('F', 'Furniture'),
    ('G', 'Gaming'),
    ('H', 'Home'),
    ('M', 'Miscellaneous'),
    ('OC', 'Outdoor/Camping'),
    ('T', 'Toys')
]

class User(AbstractUser):
	pass

class Listing(models.Model):
	creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
	title = models.CharField(max_length=80)
	category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
	descr = models.TextField()
	current_bid = models.DecimalField(max_digits=7, decimal_places=2)
	created = models.DateField(auto_now_add=True)
	closed = models.DateField(auto_now=True)
	status = models.BooleanField(default=True)
	image = models.ImageField(null=True, default='default.jpg', upload_to='media/images')

	def __str__(self):
		return f"{self.title} {self.descr} {self.current_bid} {self.created} {self.closed} {self.status}"

class Bid(models.Model):

	bidder = models.ForeignKey(User, default=True, on_delete=models.CASCADE, related_name="bid")
	listing = models.ForeignKey(Listing, default=True, on_delete=models.CASCADE, related_name="bid")
	value = models.DecimalField(max_digits=7, decimal_places=2)
	
	def __str__(self):
		return f"{self.value} {self.bidder} {self.listing}"

class Comments(models.Model):

	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
	listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
	content = models.CharField(max_length=1000)
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.content} {self.creator} {self.listing_comment}"

