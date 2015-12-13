# Django import
from django.http              import HttpResponseRedirect, HttpResponse
from django.template          import RequestContext
from django.shortcuts         import render
from django.core.urlresolvers import reverse

# Our import
from twitter            import Twitter
from amazon             import Amazon
from twittosProvider    import TwittosProvider
from DocumentProcessing import IDFProvider
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

    twitter = Twitter("config.ini", False)
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

    amazon = Amazon("config.ini")
    #amazon.search_items("All", "Fallout", 10)

    twitter  = Twitter("config.ini")

    timeline = twitter.get_tweets_from(username, 100)
    name     = twitter.get_name(username)
    tokens   = twitter.get_tokens(timeline)
    (tweets, hashtags) = tokens

    if TwittosProvider.can_update_from_timeline(timeline, username):
        TwittosProvider.update_twittos_and_idf(timeline, username, tweets)

    idf = IDFProvider()
    tf  = DocumentProcessing.tf(tweets)
    tfidf = DocumentProcessing.tfidf(tf, idf)

    # TODO : Optimize this...
    tfidf_sorted = sorted(tfidf, key=tfidf.__getitem__, reverse=True)
    top_tokens = tfidf_sorted[0:10]
    for token in top_tokens:
        # items for this token (list of item)
        # item.ItemAttributes.Title => Name of the product
        # item.DetailPageURL  => Amazon URL of the product
        # item.SmallImage.URL  => Image URL of the product
        items = amazon.search_items("All", token, 2)

    content = {
      'username': name,
      'timeline': timeline,
      'hashtags': hashtags,
      'formatted_tweets': tweets
    }
    return render(request, 'schmilka/results.html', content, context)
