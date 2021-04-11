import re
from datetime import datetime

"""Parse Riot API

Implementation of the following Riot API class:
    * MatchDto
    * MetadataDto
    * InfoDto
    
Note some of the class will contain additional functionality 

"""


class BaseDto:
    """Base Dto class

    This class will be the base of all Dto class. It contains
    a few methods that will be used by all class

    """

    def to_dict(self) -> dict:
        """Retrieve dictionary of match data

        Returns:
            Dictionary of parsed data
        """
        return self.data


class MatchDto(BaseDto):
    """Implementation of the MatchDto class

    Attributes:
        metadata (MetadataDto): MetadataDto class
        info (InfoDto): InfoDto class
    """

    def __init__(self, data: dict):
        """Initialzie MatchDto class

        Args:
            data (dict): Match data from Riot
        """
        self.data = data
        self.metadata: MetadataDto = MetadataDto(data['metadata'])
        self.info: InfoDto = InfoDto(data['info'])
        self.patch: str = str(self.info.patch)
        self.tft_set_number: str = str(self.info.tft_set_number)

    def region(self) -> str:
        """Match region

        Same function as self.metadata.region

        Returns:
             Region matches is played on
        """
        return self.metadata.region

    def is_ranked(self) -> bool:
        """Is match ranked

        Returns:
            bool: True if match is ranked
        """
        return self.info.is_rank()


class MetadataDto(BaseDto):
    """Implementation of Metadata

    Attributes:
        data_version (str): Match data version
        match_id (str): Match id
        participants (list[str]): List of participants PUUIDS
    """

    def __init__(self, data: dict):
        """Initialize MetadataDto class

        Args:
            data: MetadataDto data
        """
        self.data: dict = data
        self.data_version: str = data['data_version']
        self.match_id: str = data['match_id']
        self.participants: list[str] = data['participants']
        self.region = self.get_region()
        self.route_region = self.get_route_region()

    def get_match_num(self) -> str:
        """Get match's number

        Returns:
            Match number (without region)
        """
        match_regex = re.compile(r'\_(.*?)')
        match = re.findall(match_regex, self.match_id)

        # Check if there's any match
        if len(match) > 0:
            return match[0]
        else:
            return None

    def get_region(self) -> str:
        """Get match's region

        Returns:
            Match's region as str
        """
        # Regex match region
        region_regex = re.compile(r'(.*?)\_')
        region = re.findall(region_regex, self.match_id)

        # Check if there's any match
        if len(region) > 0:
            return region[0]
        else:
            return None

    def get_route_region(self) -> str:
        """Get match's routed region

        If you need to query riot's API then you might need to use route region value. This function maps match's region
        to it's associated routing region

        Returns:
            Route region (AMERICAS/ASIA/EUROPE)
        """
        # Get region name
        region = self.get_region().upper()

        # Region to route region map
        if region in ['NA1', 'BR1', 'LA1', 'LA2', 'OC1']:
            return 'AMERICAS'
        elif region in ['KR', 'JP1']:
            return 'ASIA'
        elif region in ['EUN1', 'EUW1', 'TR1', 'RU']:
            return 'EUROPE'
        else:
            raise ValueError(f"{region} is not defined")


class InfoDto(BaseDto):
    """Implementation of InfoDto
    
    Attributes:
        game_datetime (long): Unix timestamp.
        game_length (float): Game length in seconds.
        game_version (string): Game client version.
        participants (List[ParticipantDto]): Participants info
        queue_id (int): Please refer to the League of Legends documentation.
        tft_set_number (int): Teamfight Tactics set number.
    """

    def __init__(self, data: dict):
        """Initialize InfoDto class

        Args:
            data: InfoDto class
        """
        self.data: dict = data
        self.game_datetime = data['game_datetime']
        self.game_length = data['game_length']
        self.game_version = data['game_version']
        self.participants: list[ParticipantDto] = [ParticipantDto(participant) for participant in data['participants']]
        self.queue_id: int = data['queue_id']
        self.tft_set_number: int = data['tft_set_number']
        self.patch = self.get_patch()

    def get_patch(self) -> str:
        """Get patch number

        In InfoDto, there's no patch number, only game_version which contains the patch number.

        For example: `Version 11.6.365.1420 (Mar 17 2021/12:30:16) [PUBLIC]`

        This function will regex and get the patch number (11.6)

        Returns:
              Patch number as str
        """
        # Regex search patch version
        patch_regex = re.compile(r'Version (.*?\..*?)\.')
        patch = re.findall(patch_regex, self.game_version)

        # Chek if there's any match
        if len(patch) > 0:
            return str(patch[0])
        else:
            print(f"Unable to regex match patch, game_version: {self.game_version}")
            return None

    def get_game_datetime(self) -> datetime:
        """Datetime object of self.game_datetime"""
        return datetime.utcfromtimestamp(int(self.game_datetime/1000))

    def is_rank(self) -> bool:
        """Is match ranked"""
        return True if int(self.queue_id) == 1100 else False

    def win_players(self) -> list[str]:
        """Puuid that gained LP

        Returns:
            List of puuid that is top 4
        """
        return [participant.puuid for participant in self.participants if participant.gained_lp()]

    def lose_players(self):
        """Puuid that lost LP

        Returns:
            List of puuid that is bottom 4
         """
        return [participant.puuid for participant in self.participants if not participant.gained_lp()]

    def win_traits(self) -> list[list]:
        """Winning player's trait list

        Returns:
            List of traits for those that gained LP
        """
        return [participant.traits_used() for participant in self.participants if participant.gained_lp()]

    def lose_traits(self) -> list[list]:
        """Winning player's trait list

        Returns:
            List of traits for those that lost LP
        """
        return [participant.traits_used() for participant in self.participants if not participant.gained_lp()]

    def win_units(self) -> list:
        """Winning player's units

        Returns:
            List of units (UnitDto) from players that gained LP
        """
        return [participant.units for participant in self.participants if participant.gained_lp()]

    def lose_units(self) -> list:
        """Winning player's units

        Returns:
            List of units (UnitDto) from players that lost LP
        """
        return [participant.units for participant in self.participants if not participant.gained_lp()]

    def placements(self) -> dict:
        """Placement for each player

        Returns:
            A dictionary of {placement: puuid}
        """
        return {participant.placement: participant.puuid for participant in self.participants}

    def placement_info(self) -> dict:
        """Placement info

        Instead of getting info by puuid, returns info by placement. Dict follows:
        {placement: [level, last_round, gold_left, total_damage_to_players, time_eliminated]

        Returns:
              Dictionary that have placement as key, players info as value

        """
        output = {}
        for part in self.participants:
            info = [part.level, part.last_round, part.gold_left, part.total_damage_to_players, part.time_eliminated]
            output[part.placement] = info

        return output


class ParticipantDto(BaseDto):
    """ParticipantDto
    
    Attributes:
        companion (CompanionDto): Participant's companion.
        gold_left (int): Gold left after participant was eliminated.
        last_round (int): The round the participant was eliminated in. Note: If the player was eliminated in stage 2-1
            their last_round would be 5.
        level (int): Participant Little Legend level. Note: This is not the number of active units.
        placement (int): Participant placement upon elimination.
        players_eliminated (int): Number of players the participant eliminated.
        puuid (string): PUUID
        time_eliminated (float): The number of seconds before the participant was eliminated.
        total_damage_to_players (int): Damage the participant dealt to other players.
        traits (list[TraitDto]): A complete list of traits for the participant's active units.
        units (list[UnitDto]): A list of units for the participant.
    """

    def __init__(self, data: dict):
        """Initialize ParticipantDto

        Args:
              data: ParticipantDto data
        """
        self.data: dict = data
        self.companion: dict = data['companion']
        self.gold_left: int = data["gold_left"]
        self.last_round: int = data["last_round"]
        self.level: int = data["level"]
        self.placement: int = data["placement"]
        self.players_eliminated: int = data["players_eliminated"]
        self.puuid: str = data["puuid"]
        self.time_eliminated: float = data["time_eliminated"]
        self.total_damage_to_players: int = data["total_damage_to_players"]
        self.traits: list[TraitDto] = [TraitDto(trait) for trait in data['traits']]
        self.units: list[UnitDto] = [UnitDto(unit) for unit in data['units']]

    def traits_used(self) -> list:
        """Get list of trait played in game

        Each item is in <name>_<tier_current> (e.g. Cultist_1)

        Note:
            * tier_current is current active trait (0 = No style, 1 = Bronze, 2 = Silver, 3 = Gold, 4 = Chromatic)
            * Only returns traits that are active

        Returns:
            List of traits played
        """
        return [trait.trait_name() for trait in self.traits if trait.is_active()]

    def gained_lp(self) -> bool:
        """Did the player gain LP (placement 1-4)"""
        return True if self.placement <= 4 else False


class TraitDto(BaseDto):
    """Implementation of TraitDto
    
    Attributes:
        name (string): Trait name.
        num_units (int): Number of units with this trait.
        style (int): Current style for this trait. (0 = No style, 1 = Bronze, 2 = Silver, 3 = Gold, 4 = Chromatic)
        tier_current (int): Current active style for the trait.
        tier_total (int): Total tiers for the trait.
    """

    def __init__(self, data: dict):
        self.data = data
        self.name = data['name']
        self.num_units = data['num_units']
        self.style = data['style']
        self.tier_current = data['tier_current']
        self.tier_total = data['tier_total']

    def trait_name(self) -> str:
        """Trait name (e.g. Cultist_1)

        Returns:
              Trait with style
        """
        return f'{self.name}_{self.style}'

    def is_active(self) -> bool:
        """Is trait active

        Returns:
            True if trait is active (i.e. style > 0)
        """
        return self.style > 0


class UnitDto(BaseDto):
    """Implementation of UnitDto

    Attributes:
        items (list[int]): A list of the unit's items. Please refer to the Teamfight Tactics documentation for item ids.
        character_id (string): This field was introduced in patch 9.22 with data_version 2.
        chosen (string): If a unit is chosen as part of the Fates set mechanic, the chosen trait will be indicated by 
            this field. Otherwise this field is excluded from the response.
        name (string): Unit name. This field is often left blank.
        rarity (int): Unit rarity. This doesn't equate to the unit cost.
        tier (int): Unit tier.

    Notes:
        * Rarity: rarity is unit cost - 1 
        * Tier: Unit's star level
    """

    def __init__(self, data: dict):
        self.items: list[int] = sorted(data['items'])
        self.character_id: str = data['character_id']
        self.chosen: str = data['chosen'] if 'chosen' in data.keys() else ""
        self.rarity: int = int(data['rarity'])
        self.unit_cost: int = int(self.rarity + 1)
        self.tier: int = int(data['tier'])

    def is_chosen(self) -> bool:
        """Determines whether a unit is chosen.

        Returns:
              True if unit is chosen (self.chosen is not empty)
        """
        return True if self.chosen != "" else False

    def star_level(self) -> int:
        """Unit's star level
        
        Returns:
            unit's star level. This is the same as self.tier
        """
        return int(self.tier)


if __name__ == '__main__':
    from pprint import pprint
    import json

    with open('../docs/source/match.json', 'r') as f:
        data = json.load(f)

    pprint(MatchDto(data).info.__dict__)