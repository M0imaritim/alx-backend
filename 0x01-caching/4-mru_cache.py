#!/usr/bin/env python3
""" MRUCache module - caching system using MRU (Most Recently Used).
"""

from base_caching import BaseCaching
from collections import OrderedDict


class MRUCache(BaseCaching):
    """ MRUCache inherits from BaseCaching and uses MRU strategy.
    Discards most recently used item when cache exceeds MAX_ITEMS.
    """

    def __init__(self):
        """ Initialize the MRUCache and call parent init. """
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """ Add an item to the cache using MRU policy.
        """
        if key is None or item is None:
            return

        if key in self.cache_data:

            self.cache_data.pop(key)

        elif len(self.cache_data) >= self.MAX_ITEMS:

            mru_key, _ = self.cache_data.popitem(last=True)
            print("DISCARD:", mru_key)

        self.cache_data[key] = item

    def get(self, key):
        """ Retrieve an item from the cache.
        """
        if key is None or key not in self.cache_data:
            return None

        value = self.cache_data.pop(key)
        self.cache_data[key] = value
        return value
