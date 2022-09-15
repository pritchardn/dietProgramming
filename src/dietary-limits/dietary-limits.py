"""
Contains classes returning dietary limits based on nhmrc guidelines

@author Nicholas Pritchard nicholas.pritchard@uwa.edu.au
"""
import enum
from pydantic import BaseModel


class Sex(enum):
    Male = 0
    Female = 1


class Unit(enum):
    ug = 6
    mg = 3
    g = 1


class Nutrient(BaseModel):
    rdi: float
    ul: float = None
    unit: str


class Human(BaseModel):
    age: int
    sex: Sex
    height: int
    weight: float
    activity: float


class NutritionLevels(BaseModel):
    energy: Nutrient(unit="Kj")
    protein: Nutrient(unit="g/kg")
    fibre: Nutrient(unit="g")
    water: Nutrient(unit="mL")
    # Carbs can be taken as the rest
    # Fats
    alinoleic: Nutrient(unit="g")
    linoleic: Nutrient(unit="g")
    n3fat: Nutrient(unit="mg")
    # Vitamins
    vitamin_a: Nutrient(unit="ug")
    thiamin: Nutrient(unit="mg")
    riboflavin: Nutrient(unit="mg")
    niacin: Nutrient(unit="mg")
    vitamin_b6: Nutrient(unit="mg")
    vitamin_b12: Nutrient(unit="ug")
    folate: Nutrient(unit="ug")
    pantothenic_acid: Nutrient(unit="mg")
    biotin: Nutrient(unit="ug")
    choline: Nutrient(unit="mg")
    vitamin_c: Nutrient(unit="mg")
    vitamin_d: Nutrient(unit="ug")
    vitamin_e: Nutrient(unit="mg")
    vitamin_k: Nutrient(unit="ug")
    # Minerals
    calcium: Nutrient(unit="mg")
    chromium: Nutrient(unit="ug")
    copper: Nutrient(unit="mg")
    fluoride: Nutrient(unit="mg")
    iodine: Nutrient(unit="ug")
    iron: Nutrient(unit="mg")
    magnesium: Nutrient(unit="mg")
    manganese: Nutrient(unit="mg")
    molybdenum: Nutrient(unit="ug")
    phosphorus: Nutrient(unit="mg")
    potassium: Nutrient(unit="mg")
    selenium: Nutrient(unit="ug")
    sodium: Nutrient(unit="mg")
    zinc: Nutrient(unit="mg")


def nutrition_limits(human_model: Human) -> NutritionLevels:
    return NutritionLevels()
