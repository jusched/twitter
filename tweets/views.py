import random
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from .forms import TweetForm
from .models import Tweet


ALLOWED_HOSTS = settings.ALLOWED_HOSTS


def home_page(request, *args, **kwargs):

    # return HttpResponse("<h1>Hello World</h1>")
    return render(request, "pages/home.html", context={}, status=200)


def tweet_create_view(request, *args, **kwargs):
    """
    REST API Create View
    """
    user = request.user
    if not request.user.is_authenticated:
        user = None
        if request.is_ajax():
            return JsonResponse({}, status=401) # Not authorized
        return redirect(settings.LOGIN_URL)
    
    # Starts with data or nothing
    form = TweetForm(request.POST or None)
    next_url = request.POST.get("next") or None
    # This validates the form if it has data
    if form.is_valid():
        obj = form.save(commit=False)
        # Other logic can go here
        obj.user = user
        obj.save()

        if request.is_ajax():
            return JsonResponse(obj.serialize(), status=201) # Created items

        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
        form = TweetForm()

    if form.errors:
        if request.is_ajax():
            return JsonResponse(form.errors, status=400)

    return render(request, 'components/forms.html', context={"form": form})


def tweet_list_view(request, *args, **kwargs):
    """
    REST API VIEW
    Consumed by JavaScript or Swift/Java/iOS/Andriod
    returns json data
    """
    # Query set
    qs = Tweet.objects.all()
    # For all tweets, returns the id and content.
    tweet_list = [x.serialize() for x in qs]

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