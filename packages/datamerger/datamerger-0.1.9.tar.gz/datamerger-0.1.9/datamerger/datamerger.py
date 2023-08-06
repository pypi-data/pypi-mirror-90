import pandas as pd
from typing import List
import tqdm


class Merger:
    def __init__(
        self,
        primary: List[dict],
        secondary: List[dict],
        sorter=lambda x: x.items()[0],
        normalize=lambda x: x,
    ):
        self.primary = pd.DataFrame.from_records(
            sorted(self.map(normalize, primary), key=sorter)
        )

        self.secondary = pd.DataFrame.from_records(
            sorted(self.map(normalize, secondary), key=sorter)
        )

        self.sorter = sorter

    def merge(self, criteria, merge_function):
        """
        Merge attributes by criteria using merge_function
        """
        secondary = self.secondary

        for count, attributes in tqdm.tqdm(self.primary.iterrows()):
            for other_count, other_attributes in secondary.iterrows():
                if criteria(attributes, other_attributes):
                    del secondary[other_count]
                    attributes = merge_function(attributes, other_attributes)
                    break
            self.primary[count] = attributes

        return self.primary

    @staticmethod
    def map(mapping, dataset: pd.DataFrame):
        """
        Map equivalent naming conventions
        """
        for count, attributes in tqdm.tqdm(dataset.iterrows()):
            for key, value in list(attributes.items()):
                if other_key := mapping(
                    key
                ):  # mapping should return None, or the mapping
                    attributes[other_key] = value
                    del attributes[key]
            dataset[count] = attributes

        return dataset

    @staticmethod
    def append(attributes: dict, other_attributes: dict):
        """
        Example merger function that appends
        """
        primary_keys = set(attributes.keys())
        secondary_keys = set(other_attributes.keys())

        for key in secondary_keys - primary_keys:
            attributes[key] = other_attributes[key]

        return primary_keys


class MergerDF(Merger):
    def __init__(
        self,
        primary: pd.DataFrame,
        secondary: pd.DataFrame,
        sorter=lambda x: x.items()[0],
        normalize=lambda x: x,
    ):
        self.primary_df = primary
        self.secondary_df = secondary
        super().__init__(
            primary.to_dict("records"), secondary.to_dict("records"), sorter, normalize
        )
