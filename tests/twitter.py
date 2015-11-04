#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Load all import
import tweepy
import sys

from unidecode import unidecode
from ConfigParser import SafeConfigParser

# Set configuration
reload(sys)
sys.setdefaultencoding('utf8')

# Load configuration from config.ini
parser = SafeConfigParser()
parser.read('../config.ini')

# Constants
N_TWEETS = 1

CONSUMER_KEY        = parser.get('twitter', 'CONSUMER_KEY')
CONSUMER_SECRET     = parser.get('twitter', 'CONSUMER_SECRET')
ACCESS_TOKEN        = parser.get('twitter', 'ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = parser.get('twitter', 'ACCESS_TOKEN_SECRET')

# Identification
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

# Retrieve user information
tweets = api.user_timeline(id = 'Schmidely_Steph', count = N_TWEETS)

# Display information about tweet
for tweet in tweets:
    print "Text: " + tweet.text
    print "Retweeter: " + str(tweet.retweeted)
    print "Favoris/Like: " + str(tweet.favorited)
