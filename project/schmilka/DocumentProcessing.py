#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Imports
from __future__ import division
import sys
import math

# System config
reload(sys)
sys.setdefaultencoding('utf-8')

"""Wrap all term frequencies of a set of documents
"""
class TF:
	"""Constructor of TF Class
	   Keyword arguments:
	     self   -- object itself
    """
	def __init__(self):
		self.tfs = []

	"""Add a document and add his term frequencies to the set
       Keyword arguments:
         self     -- object itself
         document -- the document provided
    """
	def update_with_document(self, document):
		tf = {}
		doc_len = len(document)
		for token in document:
			if not token in tf:
				tf[token] = document.count(token) / doc_len
		self.tfs.append(tf)

	"""Return the set of term frequencies
       Keyword arguments:
         self     -- object itself
    """
	def tfs(self):
		return self.tfs


"""Wrap all frequencies of a token in a set of documents
"""
class IDF:
	"""Constructor of IDF Class
	   Keyword arguments:
	     self   -- object itself
    """
	def __init__(self):
		self.nbDoc = 0
		self.tokens = {}

	"""Add a document and update the frequencies for each token of this doc.
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

	"""Get the Inverse Document Frequencies
       Keyword arguments:
         self  -- object itself
    """
	def idf(self):
		idf = {}
		for token, tokenCount in self.tokens.iteritems():
			idf[token] = self.nbDoc / tokenCount
		return idf

	"""Get the log Inverse Document Frequencies
       Keyword arguments:
         self  -- object itself
    """
	def idf_log(self):
		idf = {}
		for token, tokenCount in self.tokens.iteritems():
			idf[token] = math.log(self.nbDoc / tokenCount)
		return idf


"""Wrap tf and idf for a set of document
"""
class TFIDF:
	"""Constructor of TFIDF Class
       Keyword arguments:
         self  -- object itself
    """
	def __init__(self):
		self.tf = TF()
		self.idf = IDF()

	"""Add a document and update tf and idf with this doc.
       Keyword arguments:
         self     -- object itself
         document -- the document provided
    """
	def update_with_document(self, document):
		self.tf.update_with_document(document)
		self.idf.update_with_document(document)

	"""Get the tfidf
       Keyword arguments:
         self  -- object itself
    """
	def tfidf(self):
		tfidfs = []
		for tf_dict in self.tf.tfs:
			tfidf = {}
			for token, tf in tf_dict.iteritems():
				tfidf[token] = tf * (self.idf.idf_log())[token]
			tfidfs.append(tfidf)
		return tfidfs