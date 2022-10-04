"""
Loads nutrition data into a list.

@author Nicholas Pritchard nicholas.pritchard@uwa.edu.au
"""

import pandas as pd
from pydantic import BaseModel

from src.dietary_limits.dietary_limits import NutritionLevels


class Food(BaseModel):
    name: str
    price: float
    nutrients: NutritionLevels


def data_columns():
    return ['Food Name', 'Price ($/100g)', 'Energy with dietary fibre, equated (kJ)',
            'Moisture (water) (g)', 'Protein (g)', 'Fat, total (g)',
            'Total dietary fibre (g)', 'Total long chain omega 3 fatty acids, equated (mg)',
            'Vitamin A retinol equivalents (ug)',
            'Thiamin (B1) (mg)', 'Riboflavin (B2) (mg)',
            'Niacin derived equivalents (mg)', 'Pyridoxine (B6) (mg)',
            'Cobalamin (B12) (ug)', 'Dietary folate equivalents (ug)',
            'Pantothenic acid (B5) (mg)', 'Biotin (B7) (ug)',
            'Vitamin C (mg)', 'Vitamin D3 equivalents (ug)', 'Vitamin E (mg)',
            'Calcium (Ca) (mg)', 'Chromium (Cr) (ug)', 'Copper (Cu) (mg)',
            'Fluoride (F) (ug)', 'Iodine (I) (ug)', 'Iron (Fe) (mg)',
            'Magnesium (Mg) (mg)', 'Manganese (Mn) (mg)', 'Molybdenum (Mo) (ug)',
            'Phosphorus (P) (mg)', 'Potassium (K) (mg)', 'Selenium (Se) (ug)',
            'Sodium (Na) (mg)', 'Zinc (Zn) (mg)']


def edited_columns():
    return ['name', 'price', 'energy', 'water_food', 'protein', 'fat', 'fibre', 'n3fat',
            'vitamin_a', 'thiamin', 'riboflavin', 'niacin', 'vitamin_b6',
            'vitamin_b12', 'folate', 'pantothenic_acid', 'biotin', 'vitamin_c',
            'vitamin_d', 'vitamin_e', 'calcium',
            'chromium', 'copper', 'fluoride', 'iodine', 'iron', 'magnesium',
            'manganese',
            'molybdenum', 'phosphorus', 'potassium', 'selenium', 'sodium', 'zinc']


def reduce_data(filename: str):
    data = pd.read_csv(filename)
    columns = data_columns()
    data = data[columns]
    new_columns = edited_columns()
    data.columns = new_columns
    data.replace('', 0.0, inplace=True)
    data.replace(float('nan'), 0.0, inplace=True)
    return data.to_dict('list')


def initialize_food_data():
    return reduce_data('../../data/nutrients-solid.csv')


def initialize_liquid_data():
    return reduce_data('../../data/nutrients-liquid.csv')


if __name__ == "__main__":
    food_data = initialize_food_data()
    liquid_data = initialize_liquid_data()
