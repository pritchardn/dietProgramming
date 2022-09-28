"""
Solves the Stiegler diet problem with additional nutrition constraints and local food limits_data.

@author Nicholas Pritchard nicholas.pritchard@uwa.edu.au
"""
from src.dietary_limits.dietary_limits import initialize_data, Human, Sex, nutrition_limits
from src.dietary_limits.nutrition_values import initialize_food_data

from ortools.linear_solver import pywraplp

if __name__ == "__main__":
    limits_data = initialize_data()
    food_data = initialize_food_data()
    human = Human(age=25, sex=Sex.Male, height=1.83, weight=83.9, activity=1.2)
    nutrient_limits = nutrition_limits(human, limits_data)

    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        exit(1)

    # Create variables
    foods = [solver.NumVar(0.0, solver.infinity(), x) for x in food_data['name']]
    print(f"Number of variables = {solver.NumVariables()}")

    # Add constraints
    constraints = []
    i = 0
    for nut_name, nut_val in nutrient_limits:
        print(nut_name)
        print(nut_val.rdi)
        print(nut_val.ul)
        print(nut_val.unit)
        print("---------")
        constraints.append(solver.Constraint(0, solver.infinity()))
        for j, item in enumerate(food_data[nut_name]):
            constraints[i].SetCoefficient(foods[j], item)
        i += 1

    print(f"Number of constraints = {solver.NumConstraints()}")

    # Objective function
    objective = solver.Objective()
    for food in foods:
        objective.SetCoefficient(food, 1)
    objective.SetMinimization()

    status = solver.Solve()

    # Check that the problem has an optimal solution.
    if status != solver.OPTIMAL:
        print('The problem does not have an optimal solution!')
        if status == solver.FEASIBLE:
            print('A potentially suboptimal solution was found.')
        else:
            print('The solver could not solve the problem.')
            exit(1)

    print('\nAdvanced usage:')
    print('Problem solved in ', solver.wall_time(), ' milliseconds')
    print('Problem solved in ', solver.iterations(), ' iterations')
