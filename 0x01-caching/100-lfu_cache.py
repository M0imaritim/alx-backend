#!/usr/bin/env python3
""" LFUCache module - caching system using LFU (Least Frequently Used)
with LRU (Least Recently Used) as a tie-breaker.
"""

from base_caching import BaseCaching
from collections import OrderedDict


class LFUCache(BaseCaching):
    """ LFUCache inherits from BaseCaching and uses LFU strategy.
    """

    def __init__(self):
        """ Initialize the LFUCache and call parent init. """
        super().__init__()
        self.cache_data = OrderedDict()
        self.freq_count = {}

    def put(self, key, item):
        """ Add an item to the cache using LFU + LRU policy.
        """
        if key is None or item is None:
            return

        if key in self.cache_data:

            self.cache_data[key] = item
            self.freq_count[key] += 1
            self.cache_data.move_to_end(key)
        else:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:

                min_freq = min(self.freq_count.values())
                lfu_keys = [
                    k for k, freq in self.freq_count.items()
                    if freq == min_freq
                    ]

                for old_key in self.cache_data:
                    if old_key in lfu_keys:
                        discarded_key = old_key
                        break

                self.cache_data.pop(discarded_key)
                self.freq_count.pop(discarded_key)
                print("DISCARD:", discarded_key)

            self.cache_data[key] = item
            self.freq_count[key] = 1

    def get(self, key):
        """ Retrieve an item from the cache.

        Args:
            key (str): the key of the item

        Returns:
            Any: the item or None if not found
        """
        if key is None or key not in self.cache_data:
            return None

        self.freq_count[key] += 1
        self.cache_data.move_to_end(key)
        return self.cache_data[key]
