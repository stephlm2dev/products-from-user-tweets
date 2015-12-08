#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Imports
import amazonproduct
import sys

from ConfigParser import SafeConfigParser

# System config
reload(sys)
sys.setdefaultencoding('utf-8')


class Amazon:
    """ Constructor of Amazon Class
        Keyword arguments:
            self   -- object itself
            config -- config file for AWS access
            locale -- locale to localize the requests
    """
    def __init__(self, config, locale = 'fr'):
       
        parser = SafeConfigParser()
        parser.read(config)

        # Config
        ACCESS_KEY_ID     = parser.get('Credentials', 'access_key')
        SECRET_ACCESS_KEY = parser.get('Credentials', 'secret_key')
        ASSOCIATE_TAG     = parser.get('Credentials', 'associate_tag')

        self.api = amazonproduct.API(
                access_key_id = ACCESS_KEY_ID,
                secret_access_key = SECRET_ACCESS_KEY,
                associate_tag = ASSOCIATE_TAG,
                locale = locale)

    """ Search  
    """
    def search_items(self, section, keywords, n_items):
        results = self.api.item_search(section, Keywords = keywords)
        for item in results:
            print item.ItemAttributes.Title