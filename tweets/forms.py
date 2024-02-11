from django.conf import settings
from django import forms

from .models import Tweet

class TweetForm(forms.ModelForm):
    # Meta class is used to define the model and fields
    class Meta:
        model = Tweet
        fields = ['content']

    def clean_content(self):
        content = self.cleaned_data.get("content")
        if len(content) > settings.MAX_TWEET_LENGTH:
            raise forms.ValidationError("This tweet is too long")
        return content

