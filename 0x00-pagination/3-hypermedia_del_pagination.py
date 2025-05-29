#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
from typing import List, Dict, Optional


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset: Optional[List[List]] = None
        self.__indexed_dataset: Optional[Dict[int, List]] = None

    def dataset(self) -> List[List]:
        """Cached dataset

        Returns:
            List[List]: Full dataset (without header row)
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]
        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by original sorting position, starting at 0.

        Returns:
            Dict[int, List]: Indexed dictionary of dataset rows
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            self.__indexed_dataset = {
                i: row for i, row in enumerate(dataset)
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = 0, page_size: int = 10) -> Dict:
        """Return a page of the dataset, resilient to deletions.

        Args:
            index (int): The start index for the page.
            page_size (int): Number of items per page.

        Returns:
            Dict: A dictionary with pagination information and data.
        """
        assert isinstance(index, int) and index >= 0
        assert isinstance(page_size, int) and page_size > 0

        indexed_data = self.indexed_dataset()
        max_index = max(indexed_data.keys())

        data = []
        current_index = index

        # Collect `page_size` number of valid rows
        while len(data) < page_size and current_index <= max_index:
            item = indexed_data.get(current_index)
            if item:
                data.append(item)
            current_index += 1

        return {
            "index": index,
            "next_index": current_index,
            "page_size": len(data),
            "data": data
        }
