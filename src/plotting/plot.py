import glob
import json
import os

import matplotlib
import numpy as np

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

    ax1.scatter(bmis, ages, activities, c=c_list, marker='.', label='Cost of diets', alpha=0.05,
                linewidths=0.5)
    # Make legend, set axes limits and labels
    ax1.set_xlabel('BMI')
    ax1.set_ylabel('Age')
    ax1.set_zlabel('Activity')
    plt.gca().invert_xaxis()
    # plt.gca().invert_yaxis()

    ax2.scatter(bmis, ages, activities, c=c_list, marker='.', label='Cost of diets', alpha=0.05,
                linewidths=0.5)
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
    fig.colorbar(m, ax=[ax1, ax2], location='bottom', orientation='horizontal',
                 format=cbar_formatter)
    plt.savefig(f"cost-cloud-{sex.name}-{restriction}.png")


def plot_activities(age: int, restriction: Restriction, x_labels: list, costs_f: list,
                    costs_m: list):
    plt.clf()
    x_vals = np.arange(len(x_labels))
    width = 0.4
    plt.bar(x_vals, costs_f, width=width, label="Female")
    plt.bar(x_vals + width, costs_m, width=width, label="Male")
    plt.xticks(x_vals + width / 2, x_labels)
    plt.title(f"Age: {age} Diet: {restriction.name}")
    plt.ylabel("Cost ($)")
    plt.xlabel("BMI & Activity")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"activities-{age}-{restriction}.png")


def plot_restrictions(age: int, bmi: float, activity: float, x_labels: list, costs_f: list,
                      costs_m: list):
    plt.clf()
    x_vals = np.arange(len(x_labels))
    width = 0.4
    plt.bar(x_vals, costs_f, width=width, label="Female")
    plt.bar(x_vals + width, costs_m, width=width, label="Male")
    plt.xticks(x_vals + width / 2, x_labels)
    plt.title(f"Age: {age} BMI: {bmi} Activity: {activity}")
    plt.ylabel("Cost ($)")
    plt.xlabel("Diet type")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"restrictions-{age}-{bmi}-{activity}.png")


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


def process_files(filenames: list, sex: Sex) -> tuple[list, list, list, list]:
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
    plotting_data = {}
    for restriction in Restriction:
        restriction = Restriction(restriction)
        data_path = f"../../results/{restriction.name}"
        male_files = glob.glob(f"{data_path}{os.sep}Male-*.out")
        female_files = glob.glob(f"{data_path}{os.sep}Female-*.out")
        print(len(male_files))
        print(len(female_files))
        bmis_m, ages_m, activities_m, costs_m = process_files(male_files, Sex.Male)
        bmis_f, ages_f, activities_f, costs_f = process_files(female_files, Sex.Female)
        plotting_data[restriction] = {"male": (bmis_m, ages_m, activities_m, costs_m),
                                      "female": (bmis_f, ages_f, activities_f, costs_f)}
        print("Processed files")

    for restriction in Restriction:
        restriction = Restriction(restriction)
        bmis_m, ages_m, activities_m, costs_m = plotting_data[restriction]["male"]
        bmis_f, ages_f, activities_f, costs_f = plotting_data[restriction]["female"]
        whole_min = min([min(costs_m), min(costs_f)])
        whole_max = max([max(costs_m), max(costs_f)])
        plot(Sex.Male, bmis_m, ages_m, activities_m, costs_m, whole_min, whole_max,
             restriction.name)
        plot(Sex.Female, bmis_f, ages_f, activities_f, costs_f, whole_min, whole_max,
             restriction.name)

    ages = [20, 50, 80]
    bmis = [18.5, 22.0, 30.0]
    activities = [1.0, 1.5, 2.0]
    for restriction in Restriction:
        restriction = Restriction(restriction)
        data_path = f"../../results/{restriction.name}"
        for age in ages:
            plot_costs_m = []
            plot_costs_f = []
            labels = []
            for bmi in bmis:
                for activity in activities:
                    male_files = glob.glob(
                        f"{data_path}{os.sep}Male-{age}-{round(bmi, 1)}-*-{round(activity, 2)}-*.out")
                    female_files = glob.glob(
                        f"{data_path}{os.sep}Female-{age}-{round(bmi, 1)}-*-{round(activity, 2)}-*.out")
                    bmis_m, ages_m, activities_m, costs_m = process_files(male_files, Sex.Male)
                    bmis_f, ages_f, activities_f, costs_f = process_files(female_files, Sex.Female)
                    plot_costs_m.append(np.mean(costs_m))
                    plot_costs_f.append(np.mean(costs_f))
                    labels.append(f"{bmi}\n{activity}")
            plot_activities(age, restriction, labels, plot_costs_f, plot_costs_m)

    for age in ages:
        for bmi in bmis:
            for activity in activities:
                plot_costs_m = []
                plot_costs_f = []
                labels = []
                for restriction in Restriction:
                    restriction = Restriction(restriction)
                    data_path = f"../../results/{restriction.name}"
                    male_files = glob.glob(
                        f"{data_path}{os.sep}Male-{age}-{round(bmi, 1)}-*-{round(activity, 2)}-*.out")
                    female_files = glob.glob(
                        f"{data_path}{os.sep}Female-{age}-{round(bmi, 1)}-*-{round(activity, 2)}-*.out")
                    bmis_m, ages_m, activities_m, costs_m = process_files(male_files, Sex.Male)
                    bmis_f, ages_f, activities_f, costs_f = process_files(female_files, Sex.Female)
                    plot_costs_m.append(np.mean(costs_m))
                    plot_costs_f.append(np.mean(costs_f))
                    labels.append(f"{restriction.name}")
                plot_restrictions(age, bmi, activity, labels, plot_costs_f, plot_costs_m)


if __name__ == "__main__":
    main()
