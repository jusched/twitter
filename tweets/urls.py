from django.urls import path

from .views import (tweet_detail_view, 
                          tweet_list_view, 
                          tweet_action_view,
                          tweet_delete_view, 
                          tweet_create_view)

urlpatterns = [
    # List all tweets
    path('', tweet_list_view),
    path('action/', tweet_action_view),
    # Create a new Tweet
    path('create/', tweet_create_view),
    #Takes the tweet_id and passes to the function to search for it.
    path('<int:tweet_id>/', tweet_detail_view),
    path('<int:tweet_id>/delete/', tweet_delete_view),
]
