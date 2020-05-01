"""
Actions Objects List module
=================

This module contains enums Actions, Objects and Modes which are used for more obvoius encoding of game parts.
"""

from enum import Enum


class Actions(Enum):
    """Actions enum encoding the possible actions."""

    LEFT = -1, 0
    UP = 0, -1
    RIGHT = 1, 0
    DOWN = 0, 1
    TAKE = 4
    PUT_FEED = 5
    PUT = 6
    FEED = 7


class Objects(Enum):
    """Objects enum encoding the possible objects."""

    SCRAT = 0
    HIPPO = 1
    WATERMELON = 2


class Modes(Enum):
    """Modes enum encoding the possible game modes."""

    IAMRLAGENT = 1
    AUTOMATICRL = 2
