#!/usr/bin/env python3
"""
3. Deletion-resilient hypermedia pagination
"""

import csv
import math
from typing import List, Dict, Any


class Server:
    """Server class to paginate a database of popular baby names."""
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset: List[List] = []
        self.__indexed_dataset: Dict[int, List] = {}

    def dataset(self) -> List[List]:
        """Loads and caches the dataset."""
        if not self.__dataset:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]  # Skip header
        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Creates an indexed version of the dataset."""
        if not self.__indexed_dataset:
            dataset = self.dataset()
            self.__indexed_dataset = {
                i: row for i, row in enumerate(dataset)
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10)\
            -> Dict[str, Any]:
        """
        Returns a page of the dataset with deletion-resilient pagination.
        """
        assert isinstance(index, int) and index >= 0
        assert isinstance(page_size, int) and page_size > 0

        indexed_data = self.indexed_dataset()
        data = []
        current_index = index
        collected = 0
        max_index = max(indexed_data.keys())

        while collected < page_size and current_index <= max_index:
            item = indexed_data.get(current_index)
            if item:
                data.append(item)
                collected += 1
            current_index += 1

        total_pages = math.ceil(len(indexed_data) / page_size)

        return {
            "index": index,
            "next_index": current_index,
            "page_size": len(data),
            "data": data,
            "total_pages": total_pages
        }
