from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    context = {}
    return render(request, 'schmilka/index.html', context)

def results(request, username):
    context = { 'username': username }
    return render(request, 'schmilka/results.html', context)
