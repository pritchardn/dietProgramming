import csv
import json
from collections import defaultdict
from pathlib import Path
from src.dietary_limits.dietary_limits import Restriction


def food_count_to_percentage(food_counter: dict, diet_count: int) -> dict:
    out = {}
    for food, count in food_counter.items():
        out[food] = count / diet_count
    return out


def count_foods(dirpath: Path) -> (dict, int):
    food_counter = defaultdict(int)
    diet_counter = 0
    for file in dirpath.glob("*.out"):
        with open(file, 'r') as ifile:
            diet_counter += 1
            data = json.load(ifile)
        foods = data["foods"]
        for food in foods:
            food_counter[food] += 1
    out = food_count_to_percentage(food_counter, diet_counter)
    return out, diet_counter


def main():
    fieldnames = ['Food', 'Percentage']
    for restriction in Restriction:
        restriction = Restriction(restriction)
        foods, count = count_foods(Path(f"../../results/{restriction.name}"))
        print(restriction)
        print(count)
        with open(f"{restriction.name}.csv", 'w') as ofile:
            writer = csv.writer(ofile)
            writer.writerow(fieldnames)
            writer.writerows(foods.items())


if __name__ == "__main__":
    main()
