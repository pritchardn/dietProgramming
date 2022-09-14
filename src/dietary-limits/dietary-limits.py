"""
Contains classes returning dietary limits based on nhmrc guidelines

@author Nicholas Pritchard nicholas.pritchard@uwa.edu.au
"""
import enum


class Sex(enum):
    Male = 0
    Female = 1


class Pregnant(enum):
    NA = 0
    Trimester1 = 1
    Trimester2 = 2
    Trimester3 = 3
    Lactating = 4


def nutrition_limits(age: int, sex: Sex, height: int, weight: float, activity_level: float, pregnancy_state: Pregnant):
    return {}
