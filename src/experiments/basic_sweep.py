import os

import numpy as np
from multiprocessing import Pool

from src.dietary_limits.dietary_limits import initialize_data, Human, Sex
from src.dietary_limits.nutrition_values import initialize_food_data, initialize_liquid_data
from src.solver.solver import solve


def bmi_solve(height, bmi_target):
    return height ** 2 * bmi_target


LIMITS_DATA = None
FOOD_DATA = None
OUT_DIR = ""


def single_trial(human):
    diet = solve(LIMITS_DATA, FOOD_DATA, human, 1.2)
    diet.save_to_file(OUT_DIR)


def basic_sweep(sex: Sex, age_range, height_range, bmi_range, activity_range):
    people = []
    for age in age_range:
        for height in height_range:
            for bmi in bmi_range:
                for activity in activity_range:
                    weight = round(bmi_solve(height, bmi), 2)
                    human = Human(age=age, sex=sex, height=height, weight=weight,
                                  activity=activity)
                    people.append(human)
    with Pool(16) as pool:
        pool.map(single_trial, people)


def main():
    male_height_range = np.arange(1.63, 1.93, 0.05)
    female_height_range = np.arange(1.5, 1.79, 0.05)
    bmi_range = np.arange(18.5, 30.0, 0.5)
    age_range = range(18, 80)
    activity_range = np.arange(1.0, 2.0, 0.1)

    num_trials_int = len(bmi_range) * len(age_range) * len(activity_range)
    male_trials = num_trials_int * len(male_height_range)
    female_trials = num_trials_int * len(female_height_range)
    num_total_trials = male_trials + female_trials
    print(num_total_trials)

    limits_data = initialize_data()
    food_data = initialize_food_data()
    liquid_data = initialize_liquid_data()
    out_dir = "../../results/"
    os.makedirs(out_dir, exist_ok=True)

    global LIMITS_DATA
    LIMITS_DATA = limits_data
    global FOOD_DATA
    FOOD_DATA = food_data
    global OUT_DIR
    OUT_DIR = out_dir

    for key, dataset in liquid_data.items():
        food_data[key].extend(dataset)

    basic_sweep(Sex.Male, age_range, male_height_range, bmi_range, activity_range)
    basic_sweep(Sex.Female, age_range, female_height_range, bmi_range, activity_range)


if __name__ == "__main__":
    main()
