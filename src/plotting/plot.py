import glob
import os

import matplotlib.pyplot as plt
from parse import *

from src.dietary_limits.dietary_limits import Sex


def plot(sex: Sex, bmis, ages, activities):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d', title=f"{sex.name.title()} diet costs")
    colors = ('r', 'g', 'b', 'k')

    c_list = []
    for c in colors:
        c_list.extend([c] * (len(bmis) // 4))

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


def process_files(filenames: list) -> tuple[list, list, list, list]:
    bmis, ages, activities, costs = [], [], [], []
    for filename in filenames:
        bmi, age, activity = filename_to_params(filename, Sex.Male)
        bmis.append(bmi)
        ages.append(age)
        activities.append(activity)
        costs.append(4)
    return bmis, ages, activities, costs


def main():
    data_path = "../../results"
    male_files = glob.glob(f"{data_path}{os.sep}Male-*.out")
    female_files = glob.glob(f"{data_path}{os.sep}Female-*.out")
    print(len(male_files))
    print(len(female_files))
    bmis, ages, activities, costs = process_files(male_files)
    print("Processed files")
    plot(Sex.Male, bmis, ages, activities)


if __name__ == "__main__":
    main()
