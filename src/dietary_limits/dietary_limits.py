"""
Contains classes returning dietary limits based on nhmrc guidelines

@author Nicholas Pritchard nicholas.pritchard@uwa.edu.au
"""
import enum

import pandas as pd
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
    ul: float = float('nan')
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
    water_food: Nutrient = None
    # water_liquid: Nutrient = None
    # Carbs can be taken as the rest
    # Fats
    # alinoleic: Nutrient = None
    # linoleic: Nutrient = None
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
    # choline: Nutrient = None
    vitamin_c: Nutrient = None
    vitamin_d: Nutrient = None
    vitamin_e: Nutrient = None
    # vitamin_k: Nutrient = None
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


def init_linoleic():
    return {
        Sex.Female: _fetch_csv('../../data/female-linoleic.csv'),
        Sex.Male: _fetch_csv('../../data/male-linoleic.csv')
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
        # 'alinoleic': init_alinoleic(),
        # 'linoleic': init_linoleic(),
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


def find_best_index(target, values):
    for i in range(len(values)):
        if target <= values[i]:
            return i
    return -1


def calculate_protein(human: Human, protein_data: dict):
    return human.weight * protein_data[human.sex]['RDI (g/kg/day)'][
        find_best_index(human.age, protein_data[human.sex]['Age (years)'])]


def calculate_fibre(human: Human, fibre_data: dict):
    best_index = find_best_index(human.age, fibre_data[human.sex]['Age'])
    return fibre_data[human.sex]['AI (g/day)'][best_index]


def calculate_water(human: Human, water_data: dict):
    best_index = find_best_index(human.age, water_data[human.sex]['Age'])
    return water_data[human.sex]['Fluids (L/day)'][best_index], \
           water_data[human.sex]['Food (L/day)'][best_index]


def calculate_alinoleic(human: Human, alinoleic_data: dict):
    best_index = find_best_index(human.age, alinoleic_data[human.sex]['Age'])
    return alinoleic_data[human.sex]['AI (g/day)'][best_index]


def calculate_linoleic(human: Human, linoleic_data: dict):
    best_index = find_best_index(human.age, linoleic_data[human.sex]['Age'])
    return linoleic_data[human.sex]['AI (g/day)'][best_index]


def calculate_n3fat(human: Human, n3fat_data: dict):
    best_index = find_best_index(human.age, n3fat_data[human.sex]['Age'])
    rdi = n3fat_data[human.sex]['AI (mg/day)'][best_index]
    ul = n3fat_data[human.sex]['UI (mg/day)'][best_index]
    return rdi, ul


def calculate_minerals(human: Human, mineral_data: dict):
    current_data = mineral_data[human.sex]
    best_index = find_best_index(human.age, current_data['Age'])
    return {
        'calcium': Nutrient(unit="mg/day", rdi=current_data['Calcium RDI (mg/day)'][best_index], ul=current_data['Calcium UL (mg/day)'][best_index]),
        'chromium': Nutrient(unit="ug/day", rdi=current_data['Chromium RDI (ug/day)'][best_index]),
        'copper': Nutrient(unit="mg/day", rdi=current_data['Copper RDI (mg/day)'][best_index], ul=current_data['Copper UL (mg/day)'][best_index]),
        'fluoride': Nutrient(unit="mg/day", rdi=current_data['Fluoride RDI (mg/day)'][best_index], ul=current_data['Fluoride UL (mg/day)'][best_index]),
        'iodine': Nutrient(unit="ug/day", rdi=current_data['Iodine RDI (ug/day)'][best_index], ul=current_data['Iodine UL (ug/day)'][best_index]),
        'iron': Nutrient(unit="mg/day", rdi=current_data['Iron RDI (mg/day)'][best_index], ul=current_data['Iron UL (mg/day)'][best_index]),
        'magnesium': Nutrient(unit="mg/day", rdi=current_data['Magnesium RDI (mg/day)'][best_index]),  # , ul=current_data['Magnesium UL (mg/day)'][best_index]),
        'manganese': Nutrient(unit="mg/day", rdi=current_data['Manganese RDI (mg/day)'][best_index]),
        'molybdenum': Nutrient(unit="ug/day", rdi=current_data['Molybdenum RDI (ug/day)'][best_index]),
        'phosphorus': Nutrient(unit="mg/day", rdi=current_data['Phosphorus RDI (mg/day)'][best_index], ul=current_data['Phosphorus UL (mg/day)'][best_index]),
        'potassium': Nutrient(unit="mg/day", rdi=current_data['Potassium RDI (mg/day)'][best_index]),
        'selenium': Nutrient(unit="ug/day", rdi=current_data['Selenium RDI (ug/day)'][best_index], ul=current_data['Selenium UL (ug/day)'][best_index]),
        'sodium': Nutrient(unit="mg/day", rdi=current_data['Sodium RDI (mg/day)'][best_index], ul=current_data['Sodium UL (mg/day)'][best_index]),
        'zinc': Nutrient(unit="mg/day", rdi=current_data['Zinc RDI (mg/day)'][best_index], ul=current_data['Zinc UL (mg/day)'][best_index])
    }


def calculate_vitamins(human: Human, vitamin_data: dict):
    current_data = vitamin_data[human.sex]
    best_index = find_best_index(human.age, current_data['Age'])
    return {
        'vitamin_a': Nutrient(unit="ug/day", rdi=current_data['Vitamin A RDI (ug/day)'][best_index], ul=current_data['Vitamin A UL (ug/day)'][best_index]),
        'thiamin': Nutrient(unit="mg/day", rdi=current_data['Thiamin RDI (mg/day)'][best_index]),
        'riboflavin': Nutrient(unit="mg/day", rdi=current_data['Riboflavin RDI (mg/day)'][best_index]),
        'niacin': Nutrient(unit="mg/day", rdi=current_data['Niacin RDI (mg/day)'][best_index]),
        'vitamin_b6': Nutrient(unit="mg/day", rdi=current_data['Vitamin B6 RDI (mg/day)'][best_index], ul=current_data['Vitamin B6 UL (mg/day)'][best_index]),
        'vitamin_b12': Nutrient(unit="ug/day", rdi=current_data['Vitamin B12 RDI (ug/day)'][best_index]),
        'folate': Nutrient(unit="ug/day", rdi=current_data['Folate RDI (ug/day)'][best_index], ul=current_data['Folate UL (ug/day)'][best_index]),
        'pantothenic_acid': Nutrient(unit="mg/day", rdi=current_data['Pantothenic Acid RDI (mg/day)'][best_index]),
        'biotin': Nutrient(unit="ug/day", rdi=current_data['Biotin RDI (ug/day)'][best_index]),
        # 'choline': Nutrient(unit="mg/day", rdi=current_data['Choline RDI (mg/day)'][best_index], ul=current_data['Choline UL (mg/day)'][best_index]),
        'vitamin_c': Nutrient(unit="mg/day", rdi=current_data['Vitamin C RDI (mg/day)'][best_index]),
        'vitamin_d': Nutrient(unit="ug/day", rdi=current_data['Vitamin D RDI (ug/day)'][best_index], ul=current_data['Vitamin D UL (ug/day)'][best_index]),
        'vitamin_e': Nutrient(unit="mg/day", rdi=current_data['Vitamin E RDI (mg/day)'][best_index], ul=current_data['Vitamin E UL (mg/day)'][best_index]),
        # 'vitamin_k': Nutrient(unit="ug/day", rdi=current_data['Vitamin K RDI (ug/day)'][best_index])
    }


def nutrition_limits(human_model: Human, nutrient_data: dict) -> NutritionLevels:
    output = NutritionLevels()
    output.energy = Nutrient(unit="kj", rdi=calculate_energy(human_model))
    output.protein = Nutrient(unit="g/day",
                              rdi=calculate_protein(human_model, nutrient_data['protein']))
    water_liquid, water_food = calculate_water(human_model, nutrient_data['water'])
    #output.water_liquid = Nutrient(unit="L/day", rdi=water_liquid)
    output.water_food = Nutrient(unit="g/day", rdi=water_food * 1000)
    output.fibre = Nutrient(unit="g/day", rdi=calculate_fibre(human_model, nutrient_data['fibre']))
    # output.alinoleic = Nutrient(unit="g/day", rdi=calculate_alinoleic(human_model, nutrient_data['alinoleic']))
    # output.linoleic = Nutrient(unit="g/day", rdi=calculate_linoleic(human_model, nutrient_data['linoleic']))
    n3_rdi, n3_ul = calculate_n3fat(human_model, nutrient_data['n3fat'])
    output.n3fat = Nutrient(unit="mg/day", rdi=n3_rdi, ul=n3_ul)
    vitamin_dict = calculate_vitamins(human_model, nutrient_data['vitamins'])
    output.vitamin_a = vitamin_dict['vitamin_a']
    output.thiamin = vitamin_dict['thiamin']
    output.riboflavin = vitamin_dict['riboflavin']
    output.niacin = vitamin_dict['niacin']
    output.vitamin_b6 = vitamin_dict['vitamin_b6']
    output.vitamin_b12 = vitamin_dict['vitamin_b12']
    output.folate = vitamin_dict['folate']
    output.pantothenic_acid = vitamin_dict['pantothenic_acid']
    output.biotin = vitamin_dict['biotin']
    # output.choline = vitamin_dict['choline']
    output.vitamin_c = vitamin_dict['vitamin_c']

    output.vitamin_d = vitamin_dict['vitamin_d']
    output.vitamin_e = vitamin_dict['vitamin_e']
    # output.vitamin_k = vitamin_dict['vitamin_k']
    mineral_dict = calculate_minerals(human_model, nutrient_data['minerals'])
    output.calcium = mineral_dict['calcium']
    output.chromium = mineral_dict['chromium']
    output.copper = mineral_dict['copper']
    output.fluoride = mineral_dict['fluoride']
    output.iodine = mineral_dict['iodine']
    output.iron = mineral_dict['iron']
    output.magnesium = mineral_dict['magnesium']
    output.manganese = mineral_dict['manganese']
    output.molybdenum = mineral_dict['molybdenum']
    output.phosphorus = mineral_dict['phosphorus']
    output.potassium = mineral_dict['potassium']
    output.selenium = mineral_dict['selenium']
    output.sodium = mineral_dict['sodium']
    output.zinc = mineral_dict['zinc']
    return output


if __name__ == "__main__":
    data = initialize_data()
    test_human = Human(age=25, sex=Sex.Male, height=1.83, weight=83.9, activity=1.2)
    # test_human = Human(age=12, sex=Sex.Male, height=1.2, weight=46, activity=1.2)
    # test_human = Human(age=25, sex=Sex.Female, height=1.73, weight=83.9, activity=1.2)
    # test_human = Human(age=12, sex=Sex.Female, height=1.10, weight=40, activity=1.2)
    test_nutrients = nutrition_limits(test_human, data)
    for i in test_nutrients:
        print(i)
