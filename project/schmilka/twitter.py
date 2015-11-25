#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Load all import
import sys
import re
import string
import tweepy

from unidecode import unidecode
from nltk.corpus import stopwords
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

        # Put in "cache" stop words from French and English directories
        self.cachedStopWordsEN = stopwords.words("english")
        self.cachedStopWordsFR = stopwords.words("french")

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
    def __clean_tweets(self, timeline):
        new_tweets = []
        for tweet in timeline:
            clear_text = ""
            if tweet.retweeted:
                clear_text = self.__purify(tweet.retweeted_status.text)
            else:
                clear_text = self.__purify(tweet.text)
            new_tweets.append(clear_text)
        return new_tweets

    """Clean a tweet
       Keyword arguments:
         self  -- object itself
         tweet -- a tweet
    """
    def __purify(self, tweet):
        # Remove URL - use regex
        tweet = re.sub(r"http\S+", "", tweet)

        # Convert to lowercase
        tweet = tweet.lower()

        # Remove # from hashtag
        tweet = re.sub(r'#[A-Za-z]*', ' ', tweet)

        # Remove useless word such as 'de,du, le, la ...'
        tweet = ' '.join([word for word in tweet.split() if word not in self.cachedStopWordsFR])
        tweet = ' '.join([word for word in tweet.split() if word not in self.cachedStopWordsEN])

        # TODO Convert smiley to text

        # Remove punctuation
        tweet = "".join(character for character in tweet if character not in string.punctuation)
        return tweet

    """Get all hashtags from tweets
       Keyword arguments:
         self     -- object itsel
         timeline -- timeline of a user
    """
    def __get_hashtags(self, timeline):
        hashtags = []
        for tweet in timeline:
            hashtag = ""
            if tweet.retweeted:
                hashtag = self.__get_hashtags_from(tweet.retweeted_status.text)
            else:
                hashtag = self.__get_hashtags_from(tweet.text)
            hashtags.append(hashtag)
        return hashtags

#        hashtags = []
#        for tweet in timeline:
#            hashtags_list = tweet.entities.hashtags
#            for hashtag in hashtags_list:
#                hashtags.append(hashtag)
#        return hashtags


    """Get all hashtags from a tweet
       Keyword arguments:
         self  -- object itsel
         tweet -- user tweet
    """
    def __get_hashtags_from(self, tweet):
        return [ tag.strip("#") for tag in tweet.split() if tag.startswith("#")]

    """Get cleaned tweets and hashtags
       Keyword arguments:
         self     -- object itsel
         timeline -- timeline of a user
    """
    def get_tokens(self, timeline):
        tweets = self.__clean_tweets(timeline)
        hashtags = self.__get_hashtags(timeline)
        return (tweets, hashtags)
