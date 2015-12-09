#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Load all import
import sys
import re
import string
import tweepy
import hunspell

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

        # Stemmer object
        self.stemmerEN = hunspell.HunSpell('/usr/share/myspell/dicts/en_US.dic', '/usr/share/myspell/dicts/en_US.aff')
        self.stemmerFR = hunspell.HunSpell('/usr/share/myspell/dicts/fr_FR.dic', '/usr/share/myspell/dicts/fr_FR.aff')

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
                clear_text = self.__purify(tweet.retweeted_status.text, tweet.lang)
            else:
                clear_text = self.__purify(tweet.text, tweet.lang)
            new_tweets.append(clear_text)
        return new_tweets

    """Clean a tweet
       Keyword arguments:
         self  -- object itself
         tweet -- a tweet
    """
    def __purify(self, tweet, lang):
        # Remove URL - use regex
        tweet = re.sub(r"http\S+", "", tweet)

        # Convert to lowercase
        tweet = tweet.lower()

        # Remove preposition like l', d' ...
        tweet = re.sub(r'[A-Za-z][\'|\’]', '', tweet)

        # Remove hashtag (start with #)
        tweet = re.sub(r'#[a-z]*', ' ', tweet)

        # Remove user mention (start with @)
        tweet = re.sub(r'@[a-z]*', ' ', tweet)

        # TODO Convert smiley to text

        # Remove punctuation
        tweet = "".join(character for character in tweet if character not in string.punctuation)

        # Stem each word
        tweet = self.__stem(tweet, lang)

        # Remove useless word such as 'de,du, le, la ...'
        # Remove single letter (can be appear after __stem)
        tweet = ' '.join([word
            for word in tweet.split()
                if len(word) > 1 and
                   word not in self.cachedStopWordsEN and
                   word not in self.cachedStopWordsFR
            ]
        )
        return tweet

    """Get all hashtags from tweets
       Keyword arguments:
         self     -- object itself
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
            if hashtag:
              hashtags.append(hashtag)
        return hashtags

    """Get all hashtags from a tweet
       Keyword arguments:
         self  -- object itself
         tweet -- user tweet
    """
    def __get_hashtags_from(self, tweet):
        return [ tag.strip("#") for tag in tweet.split() if tag.startswith("#")]

    """Stem words in the tweet (FR and EN) and merge the result
       Keyword arguments:
         self  -- object itself
         tweet -- user tweet
         lang  -- tweet lang
    """
    def __stem(self, tweet, lang):
        stem_EN = self.__stem_in(tweet, self.stemmerEN)
        stem_FR = self.__stem_in(tweet, self.stemmerFR)

        words = []
        unknow_words = []
        # Merge function
        # Key → word
        # Value → [exist, stem]
        for key, value in stem_FR.iteritems():
            stem_EN_value = stem_EN[key]
            if not(value[0]) and not(stem_EN_value[0]):
                unknow_words.append(key)
            elif value[0] and stem_EN_value[0]:
                if lang == "fr" and value[1] != None:
                    words.append(value[1])
                elif lang == "en" and stem_EN_value[1] != None:
                    words.append(stem_EN_value[1])
            elif value[0]: # french word
                words.append(value[1])
            else: # english word
                words.append(stem_EN_value[1])

        return (" ".join(words + unknow_words))

    """Stem a word (FR and EN)
       Keyword arguments:
         self  -- object itself
         tweet -- user tweet
         lang  -- lang dictionnary
    """
    def __stem_in(self, tweet, lang):
        hashmap_lang  = {}
        for word in tweet.split():
            information = [] # [exist, suggested_word]
            exists = lang.spell(word)
            information.append(exists)
            if (exists):
                stem_word = lang.stem(word)
            else:
                suggested_word = lang.suggest(word)
                if (suggested_word):
                    stem_word = lang.stem(suggested_word[0])
                else:
                    stem_word = False

            if (stem_word):
                information.append(stem_word[0])
            else:
                information.append(None)

            hashmap_lang[word] = information
        return hashmap_lang

    """Created tokens from cleaned tweets and hashtags
       Keyword arguments:
         self     -- object itself
         timeline -- timeline of a user
    """
    def get_tokens(self, timeline):
        tweets = self.__clean_tweets(timeline)
        hashtags = self.__get_hashtags(timeline)

        # Split into different token and output in a single list
        tweets_list_tokens = [tweet.split() for tweet in tweets if tweet]
        # tweets_tokens = [item for sublist in tweets_list_tokens for item in sublist]

        return (tweets_list_tokens, hashtags)

    def get_users(self, query, page = 1, per_page = 5):
        users = self.api.search_users(query, per_page, page)
        users_name = [user.screen_name for user in users]
        return (";".join(users_name))
