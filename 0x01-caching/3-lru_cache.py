#!/usr/bin/env python3
""" LRUCache module - caching system using LRU (Least Recently Used).
"""

from base_caching import BaseCaching
from collections import OrderedDict


class LRUCache(BaseCaching):
    """ LRUCache inherits from BaseCaching and uses LRU strategy.
    Discards least recently used item when cache exceeds MAX_ITEMS.
    """

    def __init__(self):
        """ Initialize the LRUCache and call parent init. """
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """ Add an item to the cache using LRU policy.
        """
        if key is None or item is None:
            return

        if key in self.cache_data:

            self.cache_data.pop(key)
        elif len(self.cache_data) >= self.MAX_ITEMS:

            lru_key, _ = self.cache_data.popitem(last=False)
            print("DISCARD:", lru_key)

        self.cache_data[key] = item

    def get(self, key):
        """ Retrieve an item from the cache and mark it as recently used.
        """
        if key is None or key not in self.cache_data:
            return None

        value = self.cache_data.pop(key)
        self.cache_data[key] = value
        return value
