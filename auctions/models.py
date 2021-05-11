from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.postgres.validators import MinValueValidator

class User(AbstractUser):
    pass

class Listing(models.Model):

    # Categories
    FASHION = "FASHION"
    TOYS = "TOYS"
    ELECTRONICS = "ELECTRONICS"
    HOME = "HOME"

    CATEGORY_CHOICES = [
        (FASHION, 'Fashion'),
        (TOYS, 'Toys'),
        (ELECTRONICS, 'Electronics'),
        (HOME, 'Home')
    ]

    # fields
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=128)
    listing_img = models.ImageField(blank=True, null=True, upload_to='products/images/')
    start_bid = models.DecimalField(decimal_places=2, max_digits=12,  validators=[MinValueValidator(0.00)])
    curr_bid = models.DecimalField(decimal_places=2, max_digits=12,  validators=[MinValueValidator(0.00)])
    url = models.URLField(max_length=200)
    category = models.CharField(max_length=64, choices=CATEGORY_CHOICES)
    watchers = models.ManyToManyField(User, blank=True, related_name='watchlist')
    create_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.seller} listed {self.title} with a starting bid of {self.start_bid}"
       

class Bid(models.Model):
    pass

class Comment(models.Model):
    pass
