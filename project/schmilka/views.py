from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

# Create your views here.

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
    context = { 'username': username }
    return render(request, 'schmilka/results.html', context)
