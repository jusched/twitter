import random
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render


from .models import Tweet

def home_page(request, *args, **kwargs):

    # return HttpResponse("<h1>Hello World</h1>")
    return render(request, "pages/home.html", context={}, status=200)

def tweet_list_view(request, *args, **kwargs):
    """
    REST API VIEW
    Consumed by JavaScript or Swift/Java/iOS/Andriod
    returns json data
    """

    # Query set
    qs = Tweet.objects.all()
    # For all tweets, returns the id and content.
    tweet_list = [{"id": x.id, "content": x.content, "likes": random.randint(0, 20)} for x in qs]

    data = {
        "response": tweet_list
    }
    return JsonResponse(data)


def tweet_detail(request, tweet_id, *args, **kwargs):
    # Dynamic routing using the tweet_id.
    """
    REST API VIEW
    Consumed by JavaScript or Swift/Java/iOS/Andriod
    returns json data
    """
    data = {
        "id": tweet_id,
    }
    status = 200

    try:
        obj = Tweet.objects.get(id=tweet_id)
        data['content'] = obj.content
    except:
        data['message'] = "Not found"
        status = 404

    return JsonResponse(data, status=status)