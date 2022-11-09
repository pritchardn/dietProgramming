import glob
import json
import os

import matplotlib
matplotlib.rcParams['figure.dpi'] = 600
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import rgb2hex
import matplotlib.colors as colors
from parse import *

from src.dietary_limits.dietary_limits import Sex, Restriction


def plot(sex: Sex, bmis, ages, activities, costs, whole_min, whole_max, restriction):
    fig, (ax1, ax2) = plt.subplots(1, 2, subplot_kw={"projection": "3d"})
    fig.suptitle(f"{sex.name.title()} diet costs - {restriction}")
    cmap = cm.plasma
    norm = colors.Normalize(vmin=whole_min, vmax=whole_max)
    m = cm.ScalarMappable(norm=norm, cmap=cmap)
    c_list = []
    for cost in costs:
        color = rgb2hex(m.to_rgba(cost))
        c_list.append(color)
    print("Color map built")

    ax1.scatter(bmis, ages, activities, c=c_list, marker='.', label='Cost of diets', alpha=0.05, linewidths=0.5)
    # Make legend, set axes limits and labels
    ax1.set_xlabel('BMI')
    ax1.set_ylabel('Age')
    ax1.set_zlabel('Activity')
    plt.gca().invert_xaxis()
    #plt.gca().invert_yaxis()

    ax2.scatter(bmis, ages, activities, c=c_list, marker='.', label='Cost of diets', alpha=0.05, linewidths=0.5)
    # Make legend, set axes limits and labels
    ax2.set_xlabel('BMI')
    ax2.set_ylabel('Age')
    ax2.set_zlabel('Activity')
    plt.gca().invert_xaxis()
    plt.gca().invert_yaxis()

    # Customize the view angle so it's easier to see that the scatter points lie
    # on the plane y=0
    ax1.view_init(elev=20., azim=-35, roll=0)
    ax2.view_init(elev=20., azim=-35, roll=0)
    cbar_formatter = matplotlib.ticker.ScalarFormatter()
    cbar_formatter.set_scientific(False)
    cbar_formatter.set_useOffset(False)
    fig.colorbar(m, ax=[ax1, ax2], location='bottom', orientation='horizontal', format=cbar_formatter)

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


def process_files(filenames: list, sex:Sex) -> tuple[list, list, list, list]:
    bmis, ages, activities, costs = [], [], [], []
    for filename in filenames:
        cost = get_diet_cost(filename)
        if cost == 0.0:
            continue
        bmi, age, activity = filename_to_params(filename, sex)
        bmis.append(bmi)
        ages.append(age)
        activities.append(activity)
        costs.append(cost)
    return bmis, ages, activities, costs


def main():
    for restriction in Restriction:
        restriction = Restriction(restriction)
        data_path = f"../../results/{restriction.name}"
        male_files = glob.glob(f"{data_path}{os.sep}Male-*.out")
        female_files = glob.glob(f"{data_path}{os.sep}Female-*.out")
        print(len(male_files))
        print(len(female_files))
        bmis_m, ages_m, activities_m, costs_m = process_files(male_files, Sex.Male)
        bmis_f, ages_f, activities_f, costs_f = process_files(female_files, Sex.Female)
        whole_min = min([min(costs_m), min(costs_f)])
        whole_max = max([max(costs_m), max(costs_f)])

        print("Processed files")
        plot(Sex.Male, bmis_m, ages_m, activities_m, costs_m, whole_min, whole_max, restriction.name)
        plot(Sex.Female, bmis_f, ages_f, activities_f, costs_f, whole_min, whole_max, restriction.name)


if __name__ == "__main__":
    main()
