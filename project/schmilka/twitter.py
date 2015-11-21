#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Load all import
import sys
import re
import nltk
import string
import tweepy

from unidecode import unidecode
from ConfigParser import SafeConfigParser

# Set configuration
reload(sys)
sys.setdefaultencoding('utf8')

class Twitter:
    """Constructor of Twitter Class
       Keyword arguments:
         self   -- object itself
         config -- file that contains the config of Twitter
    """
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

    """Retrieve N tweets from a USER
       Keyword arguments:
         self     -- object itself
         config   -- the username of the user
         n_tweets -- number of tweets to retrieve of the user
    """
    def get_tweets_from(self, user, n_tweets):
        # Retrieve last n_tweets of the user
        # Usefull data: tweet.{text/retweeted/favorited}
        return self.api.user_timeline(id = user, count = n_tweets)

    """Retrieve the display name of a user
       Keyword arguments:
         self     -- object itself
         username -- the username of the user
    """
    def get_name(self, username):
        user = self.api.get_user(username)
        return user.name

    """Clean all tweets
       Keyword arguments:
         self     -- object itself
         timeline -- timeline of a user
    """
    def clean_tweets(self, timeline):
        new_tweets = []
        for tweet in timeline:
            clear_text = ""
            if tweet.retweeted:
                clear_text = self.__clean(tweet.retweeted_status.text)
            else:
                clear_text = self.__clean(tweet.text)
            new_tweets.append(clear_text)
        return new_tweets

    """Clean a tweet
       Keyword arguments:
         self  -- object itself
         tweet -- a tweet
    """
    def __clean(self, tweet):
        # Remove URL - use regex
        tweet = re.sub(r"http\S+", "", tweet)

        # Remove # from hashtag
        tweet = re.sub(r'#', ' ', tweet)

        # Split hashtags with captials
        tweet = " ".join(re.findall('[A-Z][^A-Z]*', tweet))

        # FIXME Remove useless word such as 'de,du, le, la ...'
        # See: http://www.nltk.org/book/ch05.html
        tokens = nltk.word_tokenize(tweet)
        categories = nltk.pos_tag(tokens)
        cleaned_tweet = []
        for (word, tag) in categories:
            # if tag in ("VERB", "ADJ", "NOUN", "X"):
                cleaned_tweet.append(word)

        tweet = " ".join(cleaned_tweet)

        # Remove punctuation
        tweet = "".join(character for character in tweet if character not in string.punctuation)

        # TODO Convert smiley to text


        # Convert to lowercase
        tweet = tweet.lower()
        return tweet
