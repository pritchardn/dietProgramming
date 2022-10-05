"""
Solves the Stiegler diet problem with additional nutrition constraints and local food limits_data.

@author Nicholas Pritchard nicholas.pritchard@uwa.edu.au
"""
import os

from ortools.linear_solver import pywraplp

from src.dietary_limits.dietary_limits import initialize_data, Human, Sex, nutrition_limits, \
    Restriction
from src.dietary_limits.nutrition_values import initialize_food_data, initialize_liquid_data
from src.solver.diet import Diet


def solve(limits_data, food_data, human: Human, upper_bound) -> Diet:
    nutrient_limits = nutrition_limits(human, limits_data)
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        exit(1)

    # Create variables
    foods = [solver.NumVar(0.0, solver.infinity(), x) for x in food_data['name']]

    # Add constraints
    constraints = []
    i = 0
    days_of_diet = 1
    for nut_name, nut_val in nutrient_limits:
        constraints.append(solver.Constraint(nut_val.rdi * days_of_diet, days_of_diet * (
            nut_val.ul if nut_val.ul > 0.0 else nut_val.rdi * upper_bound)))
        for j, item in enumerate(food_data[nut_name]):
            constraints[i].SetCoefficient(foods[j], item)
        i += 1

    # Objective function
    objective = solver.Objective()
    for i, food in enumerate(foods):
        objective.SetCoefficient(food, food_data['price'][i])
    objective.SetMinimization()

    status = solver.Solve()
    # Check that the problem has an optimal solution.
    if status != solver.OPTIMAL:
        print('The problem does not have an optimal solution!')
        if status == solver.FEASIBLE:
            print('A potentially suboptimal solution was found.')
        else:
            print('The solver could not solve the problem.')
            return Diet(human=human,
                        nutritionLevels=nutrient_limits,
                        foods={},
                        nutrients={},
                        cost=0.0,
                        solve_time_ms=0.0,
                        solve_iterations=0,
                        restriction=Restriction.FULL)

    total_nutrients = {nutrient[0]: 0 for nutrient in nutrient_limits}
    total_cost = 0.0
    diet_foods = {}
    for i, food in enumerate(foods):
        if food.solution_value() != 0.0:
            diet_foods[food_data['name'][i]] = food.solution_value() * 100
            total_cost += (food.solution_value() * food_data['price'][i])
            for nut_name, nut_val in nutrient_limits:
                total_nutrients[nut_name] += food.solution_value() * food_data[nut_name][i]

    out_diet = Diet(human=human,
                    nutritionLevels=nutrient_limits,
                    foods=diet_foods,
                    nutrients=total_nutrients,
                    cost=total_cost,
                    solve_time_ms=solver.wall_time(),
                    solve_iterations=solver.iterations(),
                    restriction=Restriction.FULL)
    return out_diet


def main():
    limits_data = initialize_data()
    food_data = initialize_food_data()
    liquid_data = initialize_liquid_data()
    for key, dataset in liquid_data.items():
        food_data[key].extend(dataset)
    human = Human(age=25, sex=Sex.Male, height=1.83, weight=83.9, activity=1.0)
    diet = solve(limits_data, food_data, human, 1.2)
    out_dir = "../../results/"
    os.makedirs(out_dir, exist_ok=True)
    diet.save_to_file(out_dir)


if __name__ == "__main__":
    main()
