from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.test import APIClient

from .models import Tweet

User = get_user_model()


class TweetTestCase(TestCase): 
    # This is where the test db gets created.
    # Everything created here will be available for all methods
    # Everything created inside the methods, only have the method as the scope
    def setUp(self):
        self.user = User.objects.create_user(username='sebas', password='1234')

    def test_tweet_exists(self):
        
        # self.assertEqual(self.user.username, 'sebas')
        tweet = Tweet.objects.create(content="test tweet", user=self.user)
        self.assertEqual(tweet.id, 1)
        self.assertEqual(tweet.user, self.user)

    def get_client(self):
        client = APIClient()
        client.login(username=self.user.username, password='1234')
        return client
    
    def test_tweet_list(self):
        client = self.get_client()
        response = client.get('/api/tweets/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)

    def test_action_like(self):
        client = self.get_client()
        response = client.post('/api/tweets/action', {"id": 1, "action": "like"})
        self.assertEqual(response.status_code, 200)
        print(response.json())
        



