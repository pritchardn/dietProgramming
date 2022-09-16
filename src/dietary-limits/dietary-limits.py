"""
Contains classes returning dietary limits based on nhmrc guidelines

@author Nicholas Pritchard nicholas.pritchard@uwa.edu.au
"""
import enum

import pandas as pd
import numpy as np
import json
from pydantic import BaseModel


class Sex(enum.Enum):
    Male = 0
    Female = 1


class Unit(enum.Enum):
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
    activity: float  # TODO: make enum 1.2-2.2


class NutritionLevels(BaseModel):
    energy: Nutrient = None
    protein: Nutrient = None
    fibre: Nutrient = None
    water: Nutrient = None
    # Carbs can be taken as the rest
    # Fats
    alinoleic: Nutrient = None
    linoleic: Nutrient = None
    n3fat: Nutrient = None
    # Vitamins
    vitamin_a: Nutrient = None
    thiamin: Nutrient = None
    riboflavin: Nutrient = None
    niacin: Nutrient = None
    vitamin_b6: Nutrient = None
    vitamin_b12: Nutrient = None
    folate: Nutrient = None
    pantothenic_acid: Nutrient = None
    biotin: Nutrient = None
    choline: Nutrient = None
    vitamin_c: Nutrient = None
    vitamin_d: Nutrient = None
    vitamin_e: Nutrient = None
    vitamin_k: Nutrient = None
    # Minerals
    calcium: Nutrient = None
    chromium: Nutrient = None
    copper: Nutrient = None
    fluoride: Nutrient = None
    iodine: Nutrient = None
    iron: Nutrient = None
    magnesium: Nutrient = None
    manganese: Nutrient = None
    molybdenum: Nutrient = None
    phosphorus: Nutrient = None
    potassium: Nutrient = None
    selenium: Nutrient = None
    sodium: Nutrient = None
    zinc: Nutrient = None


def _fetch_csv(filename: str) -> dict:
    frame = pd.read_csv(filename)
    return frame.to_dict('list')


def init_energy():
    return {
        'adult': {
            Sex.Female: _fetch_csv('../../data/adult-female-energy.csv'),
            Sex.Male: _fetch_csv('../../data/adult-male-energy.csv')
        },
        'child': {
            Sex.Female: _fetch_csv('../../data/child-female-energy.csv'),
            Sex.Male: _fetch_csv('../../data/child-male-energy.csv')
        }
    }


def init_protein():
    return {
        Sex.Female: _fetch_csv('../../data/female-protein.csv'),
        Sex.Male: _fetch_csv('../../data/male-protein.csv')
    }


def init_fibre():
    return {
        Sex.Female: _fetch_csv('../../data/female-fibre.csv'),
        Sex.Male: _fetch_csv('../../data/male-fibre.csv')
    }


def init_water():
    return {
        Sex.Female: _fetch_csv('../../data/female-water.csv'),
        Sex.Male: _fetch_csv('../../data/male-water.csv')
    }


def init_alinoleic():
    return {
        Sex.Female: _fetch_csv('../../data/female-alinoleic.csv'),
        Sex.Male: _fetch_csv('../../data/male-alinoleic.csv')
    }


def init_n3fat():
    return {
        Sex.Female: _fetch_csv('../../data/female-n3fats.csv'),
        Sex.Male: _fetch_csv('../../data/male-n3fats.csv')
    }


def init_minerals():
    return {
        Sex.Female: _fetch_csv("../../data/female-minerals.csv"),
        Sex.Male: _fetch_csv("../../data/male-minerals.csv")
    }


def init_vitamins():
    return {
        Sex.Female: _fetch_csv("../../data/female-vitamins.csv"),
        Sex.Male: _fetch_csv("../../data/male-vitamins.csv")
    }


def initialize_data():
    nutrient_data = {
        'energy': init_energy(),
        'protein': init_protein(),
        'fibre': init_fibre(),
        'water': init_water(),
        'alinoleic': init_alinoleic(),
        'n3fat': init_n3fat(),
        'minerals': init_minerals(),
        'vitamins': init_vitamins()
    }
    return nutrient_data


def cal_to_kj(calories: float):
    return calories * 4.184


def calculate_energy(human: Human):
    """
    Uses the IOM equations to estimate EER
    Institute of Medicine Equation. (2022, March 27). In Wikipedia. https://en.wikipedia.org/wiki/Institute_of_Medicine_Equation
    :param human: mass (kg), height (m), age (years), sex and activity level are of interest
    :return: EER (MJ)
    """
    if human.age >= 19:
        if human.sex == Sex.Male:
            output = 662 - (9.53 * human.age) + human.activity * (
                        (15.91 * human.weight) + (539.6 * human.height))
        else:
            output = 354 - (6.91 * human.age) + human.activity * (
                        (9.36 * human.weight) + (726 * human.height))
    else:
        if human.sex == Sex.Male:
            output = 88.5 - (61.9 * human.age) + human.activity * (
                        (26.7 * human.weight) + (903 * human.height))
        else:
            output = 135.3 - (30.8 * human.age) + human.activity * (
                        (10 * human.weight) + (934 * human.height))
    return cal_to_kj(output)


def nutrition_limits(human_model: Human, nutrient_data: dict) -> NutritionLevels:
    output = NutritionLevels()
    output.energy = Nutrient(unit="kj", rdi=calculate_energy(human_model))
    return output


if __name__ == "__main__":
    data = initialize_data()
    test_human = Human(age=25, sex=Sex.Male, height=1.83, weight=83.9, activity=1.2)
    test_nutrients = nutrition_limits(test_human, data)
    print(test_nutrients.energy)
