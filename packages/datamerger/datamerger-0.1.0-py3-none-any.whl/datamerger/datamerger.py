import pandas as pd
from typing import List
from tqdm import tqdm

class Merger:
    def __init__(self, primary: List[dict], secondary: List[dict], sorter = lambda x: x.items()[0], normalize = lambda x: x):
        self.primary = self.map(pd.DataFrame.from_records(sorted(primary, key=sorter)), normalize)

        self.secondary = self.map(pd.DataFrame.from_records(sorted(secondary, key=sorter)), normalize)

        self.sorter = sorter

    def merge(self, criteria, merge_function):
        """
        Merge attributes by criteria using merge_function
        """
        secondary = self.secondary

        for count, attributes in tqdm.tqdm(self.primary):
            for other_count, other_attributes in secondary:
                if criteria(attributes, other_attributes):
                    del secondary[other_count]
                    attributes = merge_function(attributes, other_attributes)
                    break
            self.primary[count] = attributes

        return self.primary

    def map(self, mapping, dataset: pd.DataFrame):
        """
        Map equivalent naming conventions
        """
        for count, attributes in tqdm.tqdm(dataset):
            for key, value in list(attributes.values()):
                if other_key := mapping(key): # mapping should return None, or the mapping
                    attributes[other_key] = value
                    del attributes[key]
            dataset[count] = attributes

        return dataset


    def append(self, attributes: dict, other_attributes: dict):
        """
        Example merger function that appends
        """
        primary_keys = set(attributes.keys())
        secondary_keys = set(other_attributes.keys())

        for key in (secondary_keys - primary_keys):
            attributes[key] = other_attributes[key]

        return primary_keys
