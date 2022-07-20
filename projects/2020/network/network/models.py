
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    follows = models.ManyToManyField('User', related_name="followers")

class Post(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    subject = models.CharField(max_length=124)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.poster.username}:  {self.subject} {self.timestamp}"

    def likes(self):
        return self.like_set.all().count()

    def serialize(self):
        return {
            "id": self.id,
            "poster": self.poster.username,
            "subject": self.subject,         
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M"),
        }

class Like(models.Model):
    liker = models.ForeignKey('User',on_delete=models.CASCADE, related_name="liked_posts")
    timestamp = models.DateTimeField(auto_now=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name="likes")

    def __str__(self):
        return f"{self.post} is liked by {self.liker}"


class Comment(models.Model):
    commenter = models.ForeignKey('User', on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name="comments")
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=256)

    def __str__(self):
        return f"{self.commenter} comments on {self.post}: {self.content}"
    