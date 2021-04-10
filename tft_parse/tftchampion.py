from .api import UnitDto
from typing import Union


class TFTChampion:
    """TFTChampion aggregation class

    Attributes:
        champion_name (str): champion_name
        occurrence (int): Number of times champion occurred
        chosen_dist (dict): Chosen distribution
        item (dict): Item usage (Regardless of star)
        item_1 (dict): Item usage for 1 star champions
        item_2 (dict): Item usage for 2 star champions
        item_3 (dict): Item usage for 3 star champions
        item_comb (dict): Item combination (Regardless of star)
        item_comb1 (dict): Item combination for 1 star champions
        item_comb2 (dict): Item combination for 2 star champions
        item_comb3 (dict): Item combination for 3 star champions
        tier_dist (dict): Tier distribution
    """

    # noinspection PyTypeChecker
    def __init__(self, champion_name):
        self.champion_name = champion_name
        self.occurrence: int = None
        self.chosen_dist: dict = None
        self.item: dict = None
        self.item_1: dict = None
        self.item_2: dict = None
        self.item_3: dict = None
        self.item_comb: dict = None
        self.item_comb1: dict = None
        self.item_comb2: dict = None
        self.item_comb3: dict = None
        self.tier_dist: dict = None

    def initalize(self) -> None:
        """Create brand new class

        Class is not initialized initially to prevent writing to brand new class when user is expecting to write to
        existing class
        """
        self.occurrence: int = 0
        self.chosen_dist: dict = {}
        self.item: dict = {}
        self.item_1: dict = {}
        self.item_2: dict = {}
        self.item_3: dict = {}
        self.item_comb: dict = {}
        self.item_comb1: dict = {}
        self.item_comb2: dict = {}
        self.item_comb3: dict = {}
        self.tier_dist: dict = {}

    def from_dict(self, data: dict) -> None:
        """Initialize class from a json object (e.g. from Firestore)

        Args:
            data (dict): Data that contains TFTChampion data
        """
        self.champion_name = data['champion_name']
        self.occurrence = data['occurrence']
        self.chosen_dist = data['chosen_dist']
        self.item = data['item']
        self.item_1 = data['item_1']
        self.item_2 = data['item_2']
        self.item_3 = data['item_3']
        self.item_comb = data['item_comb']
        self.item_comb1 = data['item_comb1']
        self.item_comb2 = data['item_comb2']
        self.item_comb3 = data['item_comb3']
        self.tier_dist = data['tier_dist']

    def to_dict(self):
        """Convert class to dict object"""
        if self.occurrence is None:
            raise ValueError(f"TFTChampion class '{self.champion_name}' has not been initialized")
        output = {
            'champion_name': self.champion_name,
            'occurrence': self.occurrence,
            'chosen_dist': self.chosen_dist,
            'item': self.item,
            'item_1': self.item_1,
            'item_2': self.item_2,
            'item_3': self.item_3,
            'item_comb': self.item_comb,
            'item_comb1': self.item_comb1,
            'item_comb2': self.item_comb2,
            'item_comb3': self.item_comb3,
            'tier_dist': self.tier_dist,
        }

        return output

    def add_unit(self, data: Union[UnitDto, dict]):
        """Add unit info to class

        Args:
            data (UnitDto/dict): Data for unit to be added to class
        """
        # Convert UnitDto to class
        if isinstance(data, dict):
            data = UnitDto(data)

        # ==== Sanity Check ==== #
        # Check if class has been initialized yet
        if self.item is None:
            raise ValueError(f"TFTChampion class '{data.champion_name}' has not been initialized")

        # Check if class's champion_name is same as incoming data's champion_name
        if self.champion_name != data.champion_name:
            raise ValueError(f"Incorrect champion_name. Class is '{self.champion_name}' and "
                             f"input data is {data.champion_name}")

        # ==== Parse data ==== #
        # ---- Chosen ---- #
        if data.is_chosen():
            # If chosen is never in dict then initialize
            if data.chosen not in self.chosen_dist.keys():
                self.chosen_dist[data.chosen] = 1
            else:
                # Self increment by 1
                self.chosen_dist[data.chosen] += 1

        # ---- Item ---- #
        # need to sort data first because the key for item_comb is a sorted list as str

        items = sorted(data.items)
        # Individual items
        for item in items:
            item = str(item)
            # Item
            if item not in self.item:
                self.item[item] = 1
            else:
                self.item[item] += 1
            # 1 star level
            if item not in self.item_1.keys():
                self.item_1[item] = 1
            else:
                self.item_1[item] += 1
            # 2 stars level
            if item not in self.item_2.keys():
                self.item_2[item] = 1
            else:
                self.item_2[item] += 1
            # 3 stars level
            if item not in self.item_3.keys():
                self.item_3[item] = 1
            else:
                self.item_3[item] += 1

        # Item Combination
        items = str(items)
        if items not in self.item_comb:
            self.item[item] = 1
        else:
            self.item[item] += 1
        # 1 star level
        if items not in self.item_comb1.keys():
            self.item_comb1[item] = 1
        else:
            self.item_comb1[item] += 1
        # 2 stars level
        if items not in self.item_comb2.keys():
            self.item_comb2[item] = 1
        else:
            self.item_comb2[item] += 1
        # 3 stars level
        if items not in self.item_comb3.keys():
            self.item_comb3[item] = 1
        else:
            self.item_comb3[item] += 1
