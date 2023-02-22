"""
Contains a data structure containing a solved diet and other relevant meta data.

@author Nicholas Pritchard nicholas.pritchard@uwa.edu.au
"""

import json
import os
import csv

from pydantic import BaseModel

from src.dietary_limits.dietary_limits import Human, NutritionLevels, Restriction


class Diet(BaseModel):
    human: Human
    nutritionLevels: NutritionLevels
    foods: dict
    nutrients: dict
    cost: float
    solve_time_ms: int
    solve_iterations: int
    restriction: Restriction

    def _generate_filename(self) -> str:
        return f"{self.human.sex.name}-{self.human.age}-" \
               f"{round(self.human.weight/self.human.height**2, 1)}-" \
               f"{round(self.human.height, 2)}-" \
               f"{round(self.human.weight, 2)}-{round(self.human.activity, 2)}-{self.restriction}"

    def to_string(self) -> str:
        dict_out = {'human': self.human.dict(), 'restriction': self.restriction,
                    'nutrition_levels': self.nutritionLevels.dict(),
                    'foods': self.foods, 'cost': self.cost, 'nutrients': self.nutrients,
                    'solve_time_ms': self.solve_time_ms,
                    'solve_iterations': self.solve_iterations}
        return json.dumps(dict_out, indent=4)

    def save_to_file(self, filename: str):
        with open(f"{filename}{os.sep}{self._generate_filename()}.out", 'w',
                  encoding='utf-8') as ofile:
            ofile.write(self.to_string())

        with open(f"{filename}{os.sep}{self._generate_filename()}.csv", 'w',
                  encoding='utf-8') as ofile:
            writer = csv.writer(ofile)
            writer.writerow(self.nutrients.keys())
            writer.writerow(self.nutrients.values())
            writer.writerow(self.foods.keys())
            writer.writerow(self.foods.values())
            writer.writerow(['cost'])
            writer.writerow([self.cost])
