import glob
import json
import os

import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import Normalize, rgb2hex
from parse import *

from src.dietary_limits.dietary_limits import Sex


def plot(sex: Sex, bmis, ages, activities, costs):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d', title=f"{sex.name.title()} diet costs")
    cmap = cm.PiYG
    norm = Normalize(vmin=min(costs), vmax=max(costs))
    m = cm.ScalarMappable(norm=norm, cmap=cmap)
    c_list = []
    for cost in costs:
        color = rgb2hex(m.to_rgba(cost))
        c_list.append(color)
    print("Color map built")

    ax.scatter(bmis, ages, activities, c=c_list, marker='o', label='Cost of diets', alpha=0.05,
               linewidths=0.01)
    # Make legend, set axes limits and labels
    ax.legend()
    ax.set_xlabel('BMI')
    ax.set_ylabel('Age')
    ax.set_zlabel('Activity')

    # Customize the view angle so it's easier to see that the scatter points lie
    # on the plane y=0
    ax.view_init(elev=20., azim=-35, roll=0)

    plt.show()


def filename_to_params(filename: str, sex: Sex) -> tuple[float, int, float]:
    substr = filename[filename.find(sex.name):]
    matches = parse(f"{sex.name}" + "-{}-{}-{}-{}-{}-{}.out", substr)
    age = int(matches[0])
    bmi = float(matches[1])
    # height = float(matches[2])
    # weight = float(matches[3])
    activity = float(matches[4])
    return bmi, age, activity


def get_diet_cost(filename: str) -> float:
    with open(filename, 'r') as ifile:
        data = json.load(ifile)
        return data["cost"]


def process_files(filenames: list) -> tuple[list, list, list, list]:
    bmis, ages, activities, costs = [], [], [], []
    for filename in filenames:
        bmi, age, activity = filename_to_params(filename, Sex.Male)
        bmis.append(bmi)
        ages.append(age)
        activities.append(activity)
        costs.append(get_diet_cost(filename))
    return bmis, ages, activities, costs


def main():
    data_path = "../../results"
    male_files = glob.glob(f"{data_path}{os.sep}Male-*.out")
    female_files = glob.glob(f"{data_path}{os.sep}Female-*.out")
    print(len(male_files))
    print(len(female_files))
    bmis, ages, activities, costs = process_files(male_files)
    print("Processed files")
    plot(Sex.Male, bmis, ages, activities, costs)


if __name__ == "__main__":
    main()
