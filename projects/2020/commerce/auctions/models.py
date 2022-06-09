from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class User(AbstractUser):
    pass

class Listing(models.Model):
    CATEGORY_CHOICES = [
        ('FASHION', 'Fashion'), 
        ('TOYS', 'Toys'), 
        ('ELECTRONICS', 'Electronics'), 
        ('HOME','Home')
    ]

    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    created_date = models.DateTimeField(auto_now=True)
    starting_bid = models.FloatField(blank=True, null=True)
    current_bid = models.FloatField(blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    category = models.CharField(
        max_length=24,
        choices = CATEGORY_CHOICES,
    )

    def __str__(self):
        return f"{self.title}: {self.current_bid}"


class Bid(models.Model):
    auction = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    offer = models.FloatField()
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}: {self.auction}"


class Comment(models.Model):
    auction = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=256)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}: {self.auction}"





