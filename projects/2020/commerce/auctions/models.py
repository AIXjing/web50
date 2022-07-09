from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    created_date = models.DateTimeField(auto_now=True)
    starting_bid = models.FloatField(blank=True, null=True)
    current_bid = models.FloatField(blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="creator")
    current_bidder = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="winner")

    # for watchlist: many to many relationships. 
    # a listing can be watched by many users, and a user can watch many listings.
    watchers = models.ManyToManyField(User, blank=True, related_name="wishlistings")
    is_active = models.BooleanField(default=True)
    # comments = models.ForeignKey(Comment, on_delete=models.CASCADE, blank=True, null=True)

    CATEGORY_CHOICES = [
        ('FASHION', 'Fashion'), 
        ('TOYS', 'Toys'), 
        ('ELECTRONICS', 'Electronics'), 
        ('HOME','Home')
    ]
    category = models.CharField(
        max_length=24,
        choices = CATEGORY_CHOICES,
    )

    def __str__(self):
        return f"{self.title}: {self.current_bid}"

# not really use this class in views.py
class Bid(models.Model):
    auction = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    offer = models.FloatField()
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}: {self.auction}"

class Comment(models.Model):
    commentor = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_comments")
    comment_content = models.CharField(max_length=256)
    date = models.DateTimeField(auto_now=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="comments")

    def __str__(self):
        return f"{self.commentor} ({self.comment_content}:)"



