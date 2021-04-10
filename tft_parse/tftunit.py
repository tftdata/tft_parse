from typing import Union
from .api import UnitDto


class TFTItem:
    """TFTChampion aggregation class

    Attributes:
        item_id (str): champion_name
        champion (dict): Distribution of item used by champion
        combination (dict): Distribution of item combination
        other_item (dict): Distribution of in use with other item
    """

    def __init__(self, item_id):
        self.item_id = item_id
        self.champion: dict = None
        self.combination: dict = None
        self.other_item: dict = None

    def initialize(self) -> None:
        """Create brand new class

        Class is not initialized initially to prevent writing to brand new class when user is expecting to write to
        existing class
        """
        self.champion = {}
        self.combination = {}
        self.other_item = {}

    def from_dict(self, data: dict) -> None:
        """Initialize class from a json object (e.g. from Firestore)

        Args:
            data (dict): Data that contains TFTChampion data
        """

    def to_dict(self) -> dict:
        """Convert class to dict object

        Returns:
            Dictionary with all attributes
        """
        if self.combination is None:
            raise ValueError("TFTItem class '{}' has not been initialized".format(self.item_id))
        output = {
            'champion': self.champion,
            'combination': self.combination,
            'other_item': self.other_item
        }

        return output

    def add_unit(self, data: Union[UnitDto, dict]):
        """Add item info to class

        Args:
            data: Data for item to be added to class
        """
        # ==== Sanity Check ==== #
        # If dat ais dict then convert to UnitDto
        if isinstance(data, dict):
            data = UnitDto

        # Check if class has been initialized yet
        if self.champion is None:
            raise ValueError(f"TFTUnit class '{data.item}' has not been initialized")

        # ==== Parse data ==== #
        # ---- Champion ---- #
        if data.champion_name not in self.champion.keys():
            self.champion[data.champion_name] = 1
        else:
            self.champion[data.champion_name] += 1

        # ---- Item combination ---- #
        items = data.items
        # Remove first occurrence of item_id. This allows duplicated item to still in list
        items.remove(self.item_id)
        items_comb = str(items)
        if items_comb not in self.combination.keys():
            self.combination[items_comb] = 1
        else:
            self.combination[items_comb] += 1

        # ---- Other Item ---- #
        for item in items:
            if item not in self.other_item.keys():
                self.other_item[item] = 1
            else:
                self.other_item[item] += 1
