import random
from django.db import models


class Tweet(models.Model):
    # id is automatically created. primary_key=True.

    content = models.TextField(blank=True, null=True)

    # Blank and Null = Not required in the form/database
    image = models.FileField(upload_to='images/', blank=True, null=True)

    class Meta:
        # descending order
        ordering = ['-id']

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "likes": random.randint(0, 20)
        }
    
    

