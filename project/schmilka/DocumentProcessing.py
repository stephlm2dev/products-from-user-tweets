#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Imports
from __future__ import division
import sys
import math

import models

# System config
reload(sys)
sys.setdefaultencoding('utf-8')


"""Wrap all frequencies of a token in a set
"""
class IDF:
	"""Constructor of IDF Class
	   Keyword arguments:
	     self   -- object itself
    """
	def __init__(self):
		self.nbDoc = 0
		self.tokens = {}

	"""Add a document and update each token of this doc his frequency in the set 
       Keyword arguments:
         self     -- object itself
         document -- the document provided
    """
	def update_with_document(self, document):
		for token in set(document):
			self.__update_with_token(token)
		self.nbDoc += 1

	"""Update the frequencies of a given token
       Keyword arguments:
         self  -- object itself
         token -- the given token
    """
	def __update_with_token(self, token):
		if token in self.tokens:
			self.tokens[token] += 1
		else:
			self.tokens[token] = 1

	"""Get the set of all Inverse Document Frequencies
       Keyword arguments:
         self  -- object itself
    """
	def idf_all(self):
		idf = {}
		for token, tokenCount in self.tokens.iteritems():
			idf[token] = self.nbDoc / tokenCount
		return idf

	"""Get the set of all log Inverse Document Frequencies
       Keyword arguments:
         self  -- object itself
    """
	def idf_log_all(self):
		idf = {}
		for token, tokenCount in self.tokens.iteritems():
			idf[token] = math.log(self.nbDoc / tokenCount)
		return idf


"""Wrap all frequencies of a token in a database
"""
class IDFProvider:
	"""Constructor of IDF Class
	   Keyword arguments:
	     self   -- object itself
    """
	def __init__(self):
		try:
			models.Meta.objects.get(key = "nbDoc")
		except models.Meta.DoesNotExist:
			models.Meta(key = "nbDoc", value = 0).save()

	"""Add a document and update each token of this doc his frequency in the db 
       Keyword arguments:
         self     -- object itself
         document -- the document provided
    """
	def update_with_document(self, document):
		for token in set(document):
			self.__update_with_token(token)
		nbDoc = models.Meta.objects.get(key = "nbDoc").value
		models.Meta(key = "nbDoc", value = nbDoc + 1).save()

	"""Update the frequencies of a given token
       Keyword arguments:
         self  -- object itself
         token -- the given token
    """
	def __update_with_token(self, token):
		try:
			nbDoc = models.IDF.objects.get(token = token).nbDoc
			models.IDF(token = token, nbDoc = nbDoc + 1).save()
		except models.IDF.DoesNotExist:
			models.IDF(token = token, nbDoc = 1).save()

	"""Get the set of all Inverse Document Frequencies
       Keyword arguments:
         self  -- object itself
    """
	def idf_all(self):
		idf = {}
		nbDoc = models.Meta.objects.get(key = "nbDoc").value
		for token in models.IDF.objects.all():
			idf[token.token] = nbDoc / token.nbDoc
		return idf

	"""Get the set of all log Inverse Document Frequencies
       Keyword arguments:
         self  -- object itself
    """
	def idf_log_all(self):
		idf = {}
		nbDoc = models.Meta.objects.get(key = "nbDoc").value
		for token in models.IDF.objects.all():
			idf[token.token] = math.log(nbDoc / token.nbDoc)
		return idf

	"""Get the the Inverse Document Frequencies for a given token
       Keyword arguments:
         self  -- object itself
         token -- given token
    """
	def idf(self, token):
		nbDoc = models.Meta.objects.get(key = "nbDoc").value
		try:
			tokenNbDoc = models.IDF.objects.get(token = token).nbDoc
			return nbDoc / tokenNbDoc
		except models.IDF.DoesNotExist:
			return 0

	"""Get the the log Inverse Document Frequencies for a given token
       Keyword arguments:
         self  -- object itself
         token -- given token
    """
	def idf_log(self, token):
		nbDoc = models.Meta.objects.get(key = "nbDoc").value
		try:
			tokenNbDoc = models.IDF.objects.get(token = token).nbDoc
			return math.log(nbDoc / tokenNbDoc)
		except models.IDF.DoesNotExist:
			return 0


"""Utilities for document processing
"""
class DocumentProcessing:
	"""Get the term frequencies for a given document
       Keyword arguments:
         document -- given document
    """
	@staticmethod
	def tf(document):
		tf = {}
		doc_len = len(document)
		for token in document:
			if not token in tf:
				tf[token] = document.count(token) / doc_len
		return tf

	"""Get the term frequencies for a given tf and idf instance
       Keyword arguments:
         tf  -- given document
         idf -- idf instance
    """
	@staticmethod
	def tfidf(tf, idf):
		tfidf = {}
		for token, f in tf.iteritems():
			tfidf[token] = f * idf.idf_log(token)
		return tfidf