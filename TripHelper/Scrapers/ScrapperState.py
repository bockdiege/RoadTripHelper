"""
Clarifies Scrapper States:

Possible States:
LIBERAL: Every call goes through the API
FIll: Only calls where data does not exist go through
LOCKED: No call whatsoever goes through

Default should be update
"""
from enum import Enum


class ScrapperState(Enum):
    LOCKED = 0
    FILL = 1
    LIBERAL = 2
