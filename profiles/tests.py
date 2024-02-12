from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.test import APIClient

from .models import Profile


User = get_user_model()


# Test case for the Profile model
class ProfileTestCase(TestCase):
    def setUp(self):
        # Create two user instances for all the tests
        self.user = User.objects.create_user(username='seba', password='pass1')
        self.userb = User.objects.create_user(username='seba2', password='pass2')
    
    def get_client(self):
        # Create an authenticated APIClient instance for all the tests
        client = APIClient()
        client.login(username=self.user.username, password='pass1')
        return client

    # Test if a profile is created via a signal
    def test_profile_created_via_signal(self):
        qs = Profile.objects.all()
        self.assertEqual(qs.count(), 2)
    
    def test_following(self):
        first = self.user
        second = self.userb
        # Add second user as a follower of the first user's profile
        first.profile.followers.add(second)
        # Get the users that the second user is following
        second_user_following_whom = second.following.all()
        # Filter the users that the second user is following to check if the first user is being followed
        qs = second_user_following_whom.filter(user=first)
        # Get the users that the first user is following
        first_user_following_no_one = first.following.all()
        # Assert that the second user is following the first user
        self.assertTrue(qs.exists())
        # Assert that the first user is not following anyone
        self.assertFalse(first_user_following_no_one.exists())

    def test_follow_api_endpoint(self):
        client = self.get_client()
        # Send a POST request to the follow API endpoint for the second user
        response = client.post(
            f"/api/profiles/{self.userb.username}/follow",
            {"action": "follow"}
        )
        # Get the response data as JSON
        r_data = response.json()
        # Get the count of followers from the response data
        count = r_data.get("count")
        # Assert that the count is 1
        self.assertEqual(count, 1)
    
    # Test the unfollow API endpoint
    def test_unfollow_api_endpoint(self):
        first = self.user
        second = self.userb
        # Add second user as a follower of the first user's profile
        first.profile.followers.add(second)
        client = self.get_client()
        # Send a POST request to the unfollow API endpoint for the second user
        response = client.post(
            f"/api/profiles/{self.userb.username}/follow",
            {"action": "unfollow"}
        )
        r_data = response.json()
        # Get the count of followers from the response data
        count = r_data.get("count")
        # Assert that the count is 0
        self.assertEqual(count, 0)
    
    # Test the cannot follow API endpoint
    def test_cannot_follow_api_endpoint(self):
        client = self.get_client()
        # Send a POST request to the follow API endpoint for the first user
        response = client.post(
            f"/api/profiles/{self.user.username}/follow",
            {"action": "follow"}
        )
        r_data = response.json()
        # Get the count of followers from the response data
        count = r_data.get("count")
        # Assert that the count is 0
        self.assertEqual(count, 0)