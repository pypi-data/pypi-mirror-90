from enum import Enum


class DamageType(Enum):
    """Enumeration type defining each Damage type as described in the Destiny API
    """

    NONE = 0
    KINETIC = 1
    ARC = 2
    SOLAR = 3
    VOID = 4
    RAID = 5
    STASIS = 6


class PlayerClass(Enum):
    """Enumeration type defining each player class as described in the Destiny API
    """

    TITAN = 0
    HUNTER = 1
    WARLOCK = 2
    UNKNOWN = 3


class MembershipType(Enum):
    NONE = 0
    XBOX = 1
    PSN = 2
    STEAM = 3
    BLIZZARD = 4
    STADIA = 5
    DEMON = 10
    BUNGIENEXT = 254
    All = -1


class DestinyItemSubType(Enum):
    NONE = 0
    AUTORIFLE = 6
    SHOTGUN = 7
    MACHINEGUN = 8
    HANDCANNON = 9
    ROCKETLAUNCHER = 10
    FUSIONRIFLE = 11
    SNIPERRIFLE = 12
    PULSERIFLE = 13
    SCOUTRIFLE = 14
    SIDEARM = 17
    SWORD = 18
    MASK = 19
    SHADER = 20
    ORNAMENT = 21
    FUSIONRIFLELINE = 22
    GRENADELAUNCHER = 23
    SUBMACHINEGUN = 24
    TRACERIFLE = 25
    HELMETARMOR = 26
    GAUNTLETSARMOR = 27
    CHESTARMOR = 28
    LEGARMOR = 29
    CLASSARMOR = 30
    BOW = 31
    DUMMYREPEATABLEBOUNTY = 32
