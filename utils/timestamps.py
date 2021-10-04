import datetime
from enum import Enum


class TimestampFormat(str, Enum):
    """
    t  Short Time       16:20
    T  Long Time        16:20:30
    d  Short Date       20/04/2021
    D  Long Date        20 April 2021
    f  Short Date/Time  20 April 2021 16:20
    F  Long Date/Time   Tuesday, 20 April 2021 16:20
    R  Relative Time    2 months ago
    """
    SHORT_TIME = "t"
    LONG_TIME = "T"
    SHORT_DATE = "d"
    LONG_DATE = "D"
    SHORT_DATE_TIME = "f"
    LONG_DATE_TIME = "F"
    RELATIVE_TIME = "R"


class Timestamp:
    """
    Example usage:

    date = datetime.datetime.now()
    Timestamp(date).format(TimestampFormat.RELATIVE_TIME)
    """

    def __init__(self, date: datetime.datetime):
        self.__timestamp = round(date.timestamp())

    def format(self, format: TimestampFormat = TimestampFormat.SHORT_DATE_TIME) -> str:
        return f"<t:{self.__timestamp}:{format.value}>"

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return self.format(TimestampFormat.SHORT_DATE_TIME)
