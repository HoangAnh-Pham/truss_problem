from math import atan, cos, pi
import numpy as np
from jmetal.core.problem import FloatProblem
from jmetal.core.solution import FloatSolution


class weldedbeam(FloatProblem):
    """Class representing problem welded beam."""

    def __init__(self):
        super(weldedbeam, self).__init__()
        number_of_variables = 4

        self.obj_directions = [self.MINIMIZE, self.MINIMIZE]
        self.obj_labels = ["f1", "f2"]

        self.lower_bound = [0.125, 0.1, 0.1, 0.125]
        self.upper_bound = [5.0, 10.0, 10.0, 5.0]

    def number_of_objectives(self) -> int:
        return len(self.obj_directions)

    def number_of_constraints(self) -> int:
        return 4

    def evaluate(self, solution: FloatSolution) -> FloatSolution:
        x = solution.variables

        f1 = 1.10471 * x[0] ** 2 * x[1] + 0.04811 * x[2] * x[3] * (14.0 + x[1])
        f2 = 2.1952 / (x[3] * x[2] ** 3)

        P = 6000
        L = 14
        t_max = 13600
        s_max = 30000

        R = np.sqrt(0.25 * (x[1] ** 2 + (x[0] + x[2]) ** 2))
        M = P * (L + x[1] / 2)
        J = 2 * np.sqrt(0.5) * x[0] * x[1] * (x[1] ** 2 / 12 + 0.25 * (x[0] + x[2]) ** 2)
        t1 = P / (np.sqrt(2) * x[0] * x[1])
        t2 = M * R / J
        t = np.sqrt(t1 ** 2 + t2 ** 2 + t1 * t2 * x[1] / R)
        s = 6 * P * L / (x[3] * x[2] ** 2)
        P_c = 64746.022 * (1 - 0.0282346 * x[2]) * x[2] * x[3] ** 3

        g1 = -(1 / t_max) * (t - t_max)
        g2 = -(1 / s_max) * (s - s_max)
        g3 = -(1 / (5 - 0.125)) * (x[0] - x[3])
        g4 = -(1 / P) * (P - P_c)

        solution.objectives[0] = f1
        solution.objectives[1] = f2
        
        solution.constraints = [g1,g2,g3,g4]
        
        return solution
    
    def name(self):
        return "weldedbeam"