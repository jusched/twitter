import random
from django.conf import settings
from django.db import models


User = settings.AUTH_USER_MODEL


class TweetLike(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # References tweet model
    tweet = models.ForeignKey("Tweet", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class Tweet(models.Model):

    # References the model itself
    parent = models.ForeignKey("self", null=True, on_delete=models.SET_NULL)
    # id is automatically created. primary_key=True.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='tweet_user', blank=True, through=TweetLike)
    content = models.TextField(blank=True, null=True)

    # Blank and Null = Not required in the form/database
    image = models.FileField(upload_to='images/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return self.content

    class Meta:
        # descending order
        ordering = ['-id']

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "likes": random.randint(0, 20)
        }
    
    

