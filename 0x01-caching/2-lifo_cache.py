#!/usr/bin/env python3
""" LIFOCache module - a caching system using LIFO (Last In, First Out).
"""

from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """ LIFOCache inherits from BaseCaching and uses LIFO strategy.
    Discards the most recently added item when the cache exceeds MAX_ITEMS.
    """

    def __init__(self):
        """ Initialize the LIFOCache by calling the parent constructor. """
        super().__init__()
        self.last_key = None

    def put(self, key, item):
        """ Add an item to the cache using LIFO policy.
        """
        if key is None or item is None:
            return

        if key not in self.cache_data and len(self.cache_data)\
                >= self.MAX_ITEMS:

            if self.last_key in self.cache_data:
                del self.cache_data[self.last_key]
                print("DISCARD:", self.last_key)

        self.cache_data[key] = item
        self.last_key = key

    def get(self, key):
        """ Retrieve an item from the cache.
        """
        return self.cache_data.get(key, None)
