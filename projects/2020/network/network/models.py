
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    follows = models.ManyToManyField("User", related_name="followers")
    # likes = models.ManyToManyField("Post", related_name="liked_uses")

class Post(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    subject = models.CharField(max_length=124)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.poster.username}:  {self.subject} {self.timestamp}"

    def serialize(self):
        return {
            "id": self.id,
            "poster": self.poster.username,
            "subject": self.subject,         
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p")
        }

class Like(models.Model):
    liker = models.ForeignKey(User, on_delete=models.CASCADE, related_name="liked_post")
    time = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    
    