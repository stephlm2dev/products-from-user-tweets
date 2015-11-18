# Django import
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render
from django.core.urlresolvers import reverse

# Our import
from twitter import Twitter

# Views
def index(request):
    context = {}
    return render(request, 'schmilka/index.html', context)

def process(request):
    username = request.POST['twittos']

    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(reverse('app:results', args=(username,)))

def results(request, username):
    # Request our context from the request passed to us.
    context = RequestContext(request)

    twitterAPI = Twitter("config.ini")
    timeline = twitterAPI.get_tweets_from(username, 10)
    name = twitterAPI.get_name(username)
    content = {
      'username': name,
      'timeline': timeline
    }
    return render(request, 'schmilka/results.html', content, context)
