from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ForeignKey("User", on_delete=models.CASCADE, related_name="following")
    posters = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="poster")




class Post(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_post')
    timestamp = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(max_length=255)

    # why we need this?
    def serialize(self):
        return {
            "poster": self.poster,
            "likes": self.likes,
            "timestamp": self.timestamp,
            "subject": self.subject,
        }