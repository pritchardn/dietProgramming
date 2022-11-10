"""
Loads nutrition data into a list.

@author Nicholas Pritchard nicholas.pritchard@uwa.edu.au
"""

import pandas as pd
from pydantic import BaseModel

from src.dietary_limits.dietary_limits import NutritionLevels, Restriction, restricted_foods


class Food(BaseModel):
    name: str
    price: float
    nutrients: NutritionLevels


def data_columns():
    return ['Classification', 'Food Name', 'Price ($/100g)',
            'Energy with dietary fibre, equated (kJ)',
            'Moisture (water) (g)', 'Protein (g)', 'Fat, total (g)',
            'Total dietary fibre (g)', 'Lactose (g)',
            'Total long chain omega 3 fatty acids, equated (mg)',
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
    return ['classification', 'name', 'price', 'energy', 'water_food', 'protein', 'fat', 'fibre',
            'lactose', 'n3fat',
            'vitamin_a', 'thiamin', 'riboflavin', 'niacin', 'vitamin_b6',
            'vitamin_b12', 'folate', 'pantothenic_acid', 'biotin', 'vitamin_c',
            'vitamin_d', 'vitamin_e', 'calcium',
            'chromium', 'copper', 'fluoride', 'iodine', 'iron', 'magnesium',
            'manganese',
            'molybdenum', 'phosphorus', 'potassium', 'selenium', 'sodium', 'zinc']


def filter_foods(data: pd.DataFrame, restriction: Restriction):
    restricted_food = restricted_foods(restriction)
    for food_group in restricted_food:
        data = data[data['classification'].str.startswith(food_group) == False]
    if restriction == Restriction.LACTOSE:
        data = data[data['lactose'] == 0.0]
    return data


def reduce_data(filename: str, restriction: Restriction):
    data = pd.read_csv(filename)
    columns = data_columns()
    data = data[columns]
    new_columns = edited_columns()
    data.columns = new_columns
    data.replace('', 0.0, inplace=True)
    data.replace(float('nan'), 0.0, inplace=True)
    data['classification'] = data['classification'].astype(int)
    data['classification'] = data['classification'].astype(str)
    data = filter_foods(data, restriction)
    return data.to_dict('list')


def initialize_food_data(restriction: Restriction):
    return reduce_data('../../data/nutrients-solid.csv', restriction)


def initialize_liquid_data(restriction: Restriction):
    return reduce_data('../../data/nutrients-liquid.csv', restriction)


if __name__ == "__main__":
    food_data = initialize_food_data(Restriction.FULL)
    liquid_data = initialize_liquid_data(Restriction.FULL)
