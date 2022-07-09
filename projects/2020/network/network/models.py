
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    follows = models.ManyToManyField("User", related_name="followings")
    likes = models.ManyToManyField("Post", related_name="liked_uses")

class Post(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    subjet = models.CharField(max_length=124)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.poster}: {self.timestamp}  {self.subjet}"
    