from unicodedata import category
from unittest.util import _MAX_LENGTH
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import CharField, FloatField


class User(AbstractUser):
    pass

class Bids(models.Model):
    bid = FloatField()

class Comments(models.Model):
    comment = CharField(max_length=256)

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    bids = models.ForeignKey(Bids, on_delete=models.CASCADE, related_name="bids")
    comments = models.ForeignKey(Comments, on_delete=models.CASCADE, related_name="comments")



