from enum import Enum


class Variant(Enum):
    """Lichess chess variants"""

    STANDARD = 1
    CRAZYHOUSE = 10
    CHESS960 = 2
    KING_OF_THE_HILL = 4
    THREE_CHECK = 5
    ANTICHESS = 6
    ATOMIC = 7
    HORDE = 8
    RACING_KINGS = 9
    FROM_POSITION = 3


class TimeMode(Enum):
    """Lichess time modes"""

    REALTIME = 1
    CORRESPONDENCE = 2
    UNLIMITED = 0


class Color(Enum):
    """Lichess start colors"""

    WHITE = "white"
    BLACK = "black"
    RANDOM = "random"
