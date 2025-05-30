#!/usr/bin/env python3
""" FIFOCache module - a caching system using FIFO (First In, First Out).
"""

from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """ FIFOCache inherits from BaseCaching and uses FIFO strategy.
    Discards the oldest item when the cache exceeds MAX_ITEMS.
    """

    def __init__(self):
        """ Initialize the FIFOCache by calling the parent constructor. """
        super().__init__()
        self.order = []  # Keeps track of the order of keys added

    def put(self, key, item):
        """ Add an item to the cache using FIFO policy.

        """
        if key is None or item is None:
            return

        if key not in self.cache_data:
            if len(self.cache_data) >= self.MAX_ITEMS:
                # Discard the first item added
                oldest_key = self.order.pop(0)
                del self.cache_data[oldest_key]
                print("DISCARD:", oldest_key)
            self.order.append(key)
        self.cache_data[key] = item

    def get(self, key):
        """ Retrieve an item from the cache.
        """
        return self.cache_data.get(key, None)
