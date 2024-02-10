import random
from django.conf import settings
from django.db import models


User = settings.AUTH_USER_MODEL

class Tweet(models.Model):

    # id is automatically created. primary_key=True.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)

    # Blank and Null = Not required in the form/database
    image = models.FileField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return self.content

    class Meta:
        # descending order
        ordering = ['-id']

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "likes": random.randint(0, 20)
        }
    
    

