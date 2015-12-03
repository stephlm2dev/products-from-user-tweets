# Django import
from django.http              import HttpResponseRedirect, HttpResponse
from django.template          import RequestContext
from django.shortcuts         import render
from django.core.urlresolvers import reverse

# Our import
from twitter            import Twitter
from DocumentProcessing import DocumentProcessing

# Views
def index(request):
    # Request our context from the request passed to us.
    context = RequestContext(request)

    return render(request, 'schmilka/index.html', context)

def ajaxTwitterUser(request):
    # Request our context from the request passed to us.
    context = RequestContext(request)

    if request.method == 'GET':
        query = request.GET['query']

    twitter = Twitter("config.ini")
    twittos = twitter.get_users(query)
    return HttpResponse(twittos)

def process(request):
    username = request.POST['twittos']

    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(reverse('app:results', args=(username,)))

def results(request, username):
    # Request our context from the request passed to us.
    context = RequestContext(request)

    twitter  = Twitter("config.ini")
    timeline = twitter.get_tweets_from(username, 10)
    name     = twitter.get_name(username)
    tokens   = twitter.get_tokens(timeline)
    (tweets, hashtags) = tokens    

    content = {
      'username': name,
      'timeline': timeline,
      'hashtags': hashtags,
      'formatted_tweets': tweets
    }
    return render(request, 'schmilka/results.html', content, context)
