import numpy as np
import matplotlib.pyplot as plt


def plot(bmis, ages, activities):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    x = []
    y = []
    z = []

    for bmi in bmis:
        for age in ages:
            for activity in activities:
                x.append(bmi)
                y.append(age)
                z.append(activity)

    # Plot scatterplot data (20 2D points per colour) on the x and z axes.
    colors = ('r', 'g', 'b', 'k')

    c_list = []
    for c in colors:
        c_list.extend([c] * (len(x)//4))
    # By using zdir='y', the y value of these points is fixed to the zs value 0
    # and the (x, y) points are plotted on the x and z axes.

    ax.scatter(x, y, z, c=c_list, marker='o', label='Cost of diets', alpha=0.1, linewidths=0.1)
    # Make legend, set axes limits and labels
    ax.legend()
    ax.set_xlabel('BMI')
    ax.set_ylabel('Age')
    ax.set_zlabel('Activity')

    # Customize the view angle so it's easier to see that the scatter points lie
    # on the plane y=0
    ax.view_init(elev=20., azim=-35, roll=0)

    plt.show()


def main():
    plot(np.arange(18, 35, 0.5), range(18, 85), np.arange(1.0, 2.0, 0.1))


if __name__ == "__main__":
    main()
