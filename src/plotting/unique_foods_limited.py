import glob
import os
import json

from src.dietary_limits.dietary_limits import Restriction, Sex


def unique_items(target: str, filenames: list):
    all_files = filenames.copy()
    all_files.remove(target)
    ingredients = set()
    unique_foods = set()
    for filename in all_files:
        with open(filename, 'r') as ifile:
            data = json.load(ifile)
            for food in data["foods"]:
                ingredients.add(food)
    with open(target, 'r') as ifile:
        data = json.load(ifile)
        for food in data["foods"]:
            if food not in ingredients:
                unique_foods.add(food)
    return unique_foods


def write_results(output_dir: str, data: dict):
    for filename, val in data.items():
        print(val)


def calc_unique_foods(input_dir, output_dir):
    for restriction in Restriction:
        restriction = Restriction(restriction)
        results = {}
        for sex in Sex:
            sex = Sex(sex)
            search_string = os.path.join(input_dir, f"{restriction.name}", f"{sex.name}-*.out")
            print(search_string)
            filenames = glob.glob(search_string)
            print(filenames)
            for file in filenames:
                results[file] = unique_items(file, filenames)
        write_results(output_dir, results)


def main():
    input_dir = "/home/nikolas/DietExamples"
    output_dir = "/home/nikolas/DietExamples"
    calc_unique_foods(input_dir, output_dir)


if __name__ == "__main__":
    main()
