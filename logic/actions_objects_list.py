from enum import Enum

class Actions(Enum):
    LEFT = -1, 0
    UP = 0, -1
    RIGHT = 1, 0
    DOWN = 0, 1
    TAKE = 4
    PUT_FEED = 5
    PUT = 6
    FEED = 7


class Objects(Enum):
    SCRAT = 0
    HIPPO = 1
    WATERMELON = 2