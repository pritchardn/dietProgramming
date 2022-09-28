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


def initialize_food_data():
    food_data = pd.read_csv('../../data/nutrients-solid.csv')
    columns = ['Food Name', 'Price ($/100g)', 'Energy with dietary fibre, equated \n(kJ)',
               'Moisture (water) \n(g)', 'Protein \n(g)', 'Fat, total \n(g)',
               'Total dietary fibre \n(g)', 'Total long chain omega 3 fatty acids, equated \n(mg)',
               'Vitamin A retinol equivalents \n(ug)',
               'Thiamin (B1) \n(mg)', 'Riboflavin (B2) \n(mg)',
               'Niacin derived equivalents \n(mg)', 'Pyridoxine (B6) \n(mg)',
               'Cobalamin (B12) \n(ug)', 'Dietary folate equivalents \n(ug)',
               'Pantothenic acid (B5) \n(mg)', 'Biotin (B7) \n(ug)',
               'Vitamin C \n(mg)', 'Vitamin D3 equivalents \n(ug)', 'Vitamin E \n(mg)',
               'Calcium (Ca) \n(mg)', 'Chromium (Cr) \n(ug)', 'Copper (Cu) \n(mg)',
               'Fluoride (F) \n(ug)', 'Iodine (I) \n(ug)', 'Iron (Fe) \n(mg)',
               'Magnesium (Mg) \n(mg)', 'Manganese (Mn) \n(mg)', 'Molybdenum (Mo) \n(ug)',
               'Phosphorus (P) \n(mg)', 'Potassium (K) \n(mg)', 'Selenium (Se) \n(ug)',
               'Sodium (Na) \n(mg)', 'Zinc (Zn) \n(mg)']
    food_data = food_data[columns]
    new_columns = ['name', 'price', 'energy', 'water_food', 'protein', 'fat', 'fibre', 'n3fat',
                   'vitamin_a', 'thiamin', 'riboflavin', 'niacin', 'vitamin_b6',
                   'vitamin_b12', 'folate', 'pantothenic_acid', 'biotin', 'vitamin_c',
                   'vitamin_d', 'vitamin_e', 'calcium',
                   'chromium', 'copper', 'fluoride', 'iodine', 'iron', 'magnesium',
                   'manganese',
                   'molybdenum', 'phosphorus', 'potassium', 'selenium', 'sodium', 'zinc']
    food_data.columns = new_columns
    food_data.replace('', 0.0, inplace=True)
    food_data.replace(float('nan'), 0.0, inplace=True)
    return food_data.to_dict('list')


if __name__ == "__main__":
    data = initialize_food_data()
