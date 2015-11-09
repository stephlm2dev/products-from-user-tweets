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

class Twitter:
    def __init__(self, config):
        # Load configuration from config.ini
        parser = SafeConfigParser()
        parser.read(config)

        # Constants
        CONSUMER_KEY        = parser.get('twitter', 'CONSUMER_KEY')
        CONSUMER_SECRET     = parser.get('twitter', 'CONSUMER_SECRET')
        ACCESS_TOKEN        = parser.get('twitter', 'ACCESS_TOKEN')
        ACCESS_TOKEN_SECRET = parser.get('twitter', 'ACCESS_TOKEN_SECRET')

        # Identification
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

        self.api = tweepy.API(auth)

    def get_tweets_from(self, user, n_tweets):
        # Retrieve last n_tweets of the user
        # Usefull data: tweet.{text/retweeted/favorited}
        tweets = api.user_timeline(id = user, count = n_tweets)


