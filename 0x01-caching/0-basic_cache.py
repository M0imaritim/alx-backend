#!/usr/bin/env python3
""" BasicCache module - a simple dictionary-based caching system.
"""

from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """ BasicCache inherits from BaseCaching and implements
    a basic dictionary cache with no limit.
    """

    def put(self, key, item):
        """ Add an item to the cache_data dictionary."""
        if key is not None and item is not None:
            self.cache_data[key] = item

    def get(self, key):
        """ Retrieve an item from the cache_data dictionary."""
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data[key]
