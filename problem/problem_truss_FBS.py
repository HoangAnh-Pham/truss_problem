import numpy as np
from jmetal.core.problem import FloatProblem
from jmetal.core.solution import FloatSolution

from problem import truss10 
from problem import truss25
from problem import truss72
from problem import truss200

"""
.. module:: problem
   :platform: Unix, Windows
   :synopsis: Constrained test problems for multi-objective optimization

.. moduleauthor:: Hoang-Anh Pham <anhph2@huce.edu.vn>
"""

def FBS(self, x, L, H, D, cv, rho):
    
    # FBS
    x_new = [x[i] * cv for i in range(len(x))]
        
    # Check if the lower bounds are OK
    vlow = max(1,max(self.lower_bound/np.array(x_new)))
    x_new = [x_new[i] * vlow for i in range(len(x))]
    
    # Check if the upper bounds are OK
    vup = min(1, min(self.upper_bound/np.array(x_new)))
    
    # Evaluate the fitness of new solution
    A = x_new @ H
    # Tính hàm mục tiêu
    f1 = np.dot(A,L)*rho
    f2 = np.max(np.abs(D))/(cv*vlow)

    # Tính vi phạm ràng buộc (Jmetal: g<0 -> vi phạm; g>0 khả thi)
    g = min(0, vup-1)
    
    return x_new, f1, f2, g

class truss2bar(FloatProblem):
    """Class representing problem 2bartruss."""

    def __init__(self):
        super(truss2bar, self).__init__()
        number_of_variables = 3

        self.obj_directions = [self.MINIMIZE, self.MINIMIZE]
        self.obj_labels = ["weight", "stress"]

        self.lower_bound = [1,0.0001,0.0001]
        self.upper_bound = [3,0.01,0.01]

    def number_of_objectives(self) -> int:
        return len(self.obj_directions)

    def number_of_constraints(self) -> int:
        return 1

    def evaluate(self, solution: FloatSolution) -> FloatSolution:
        y = solution.variables[0]
        x1 = solution.variables[1]
        x2 = solution.variables[2]
        
        sAC = 20*np.sqrt(16+y**2)/(y*x1)
        sBC = 80*np.sqrt(1+y**2)/(y*x2)
        
        f1 = x1*np.sqrt(16+y**2) + x2*np.sqrt(1+y**2)
        f2 = max(sAC,sBC)
        
        # jmetal: g(x) >= 0 -> feasible
        
        cv = min(0,10**5/max(sAC,sBC)-1)
              
        solution.objectives[0] = f1
        solution.objectives[1] = f2
        
        solution.constraints[0] = cv

        return solution

    def name(self):
        return "truss2bar"

class truss10bar(FloatProblem):
    """Class representing problem 10bartruss."""

    def __init__(self):
        super(truss10bar, self).__init__()
        number_of_variables = 10

        self.obj_directions = [self.MINIMIZE, self.MINIMIZE]
        self.obj_labels = ["weight", "displacement"]

        self.lower_bound = [0.1 for _ in range(number_of_variables)]
        self.upper_bound = [40.0 for _ in range(number_of_variables)]

    def number_of_objectives(self) -> int:
        return len(self.obj_directions)

    def number_of_constraints(self) -> int:
        return 1

    def evaluate(self, solution: FloatSolution) -> FloatSolution:
        x = solution.variables
        s_max = 25
        rho = 0.1
        
        # Phân tích kết cấu
        D, R, model = truss10.f10fem(x) 
        
        # Compute areas
        L, H = model['L'], model['H']
        A = x @ H
        
        # Compute stresses
        S = R / x
        
        # Maximum stress
        sc = np.max(np.abs(S))
        
        # Constraints
        # cv = s_max/sc - 1
        cv = sc/s_max

        # FBS
        x_new, f1, f2, g = FBS(self, x, L, H, D, cv, rho)
        
        # Get solution
        solution.variables = x_new
        solution.objectives[0] = f1
        solution.objectives[1] = f2
        solution.constraints[0] = g

        return solution

    def name(self):
        return "truss10bar"
    
class truss25bar(FloatProblem):
    """Class representing problem 25bartruss."""

    def __init__(self):
        super(truss25bar, self).__init__()
        number_of_variables = 8

        self.obj_directions = [self.MINIMIZE, self.MINIMIZE]
        self.obj_labels = ["weight", "displacement"]

        self.lower_bound = [0.01 for _ in range(number_of_variables)]
        self.upper_bound = [3.5 for _ in range(number_of_variables)]

    def number_of_objectives(self) -> int:
        return len(self.obj_directions)

    def number_of_constraints(self) -> int:
        return 1

    def evaluate(self, solution: FloatSolution) -> FloatSolution:
        x = solution.variables
        s_max = truss25.data['sigma']
        rho = truss25.data['ro']
        
        # Phân tích kết cấu
        D, R, model = truss25.f25fem(x) 
        
        # Compute areas
        L, H = model['L'], model['H']
        A = x @ H
        
        # Compute stresses
        S = R / A
        
        # Maximum stress constraint
        sc = np.max(np.abs(S))
        
        # Constraints
        # cv = s_max/sc - 1
        cv = sc/s_max

        # FBS
        x_new, f1, f2, g = FBS(self, x, L, H, D, cv, rho)
        
        # Get solution
        solution.variables = x_new
        solution.objectives[0] = f1
        solution.objectives[1] = f2
        solution.constraints[0] = g

        return solution

    def name(self):
        return "truss25bar" 
    
class truss72bar(FloatProblem):
    """Class representing problem 10bartruss."""

    def __init__(self):
        super(truss72bar, self).__init__()
        number_of_variables = 16

        self.obj_directions = [self.MINIMIZE, self.MINIMIZE]
        self.obj_labels = ["weight", "displacement"]

        self.lower_bound = [0.1 for _ in range(number_of_variables)]
        self.upper_bound = [2.5 for _ in range(number_of_variables)]

    def number_of_objectives(self) -> int:
        return len(self.obj_directions)

    def number_of_constraints(self) -> int:
        return 1

    def evaluate(self, solution: FloatSolution) -> FloatSolution:
        x = solution.variables
        s_max = truss72.data['sigma']
        rho = truss72.data['ro']
        
        # Phân tích kết cấu
        D, R, model = truss72.f72fem(x)
        
        # Compute areas
        L, H = model['L'], model['H']
        A = x @ H
        
        # Compute stresses
        S = R / A
        
        # Maximum stress constraint
        sc = np.max(np.abs(S))
        
        # Constraints
        # cv = s_max/sc - 1
        cv = sc/s_max

        # FBS
        x_new, f1, f2, g = FBS(self, x, L, H, D, cv, rho)
        
        # Get solution
        solution.variables = x_new
        solution.objectives[0] = f1
        solution.objectives[1] = f2
        solution.constraints[0] = g

        return solution

    def name(self):
        return "truss72bar" 
    
class truss200bar(FloatProblem):
    """Class representing problem 10bartruss."""

    def __init__(self):
        super(truss200bar, self).__init__()
        number_of_variables = 29

        self.obj_directions = [self.MINIMIZE, self.MINIMIZE]
        self.obj_labels = ["weight", "displacement"]

        self.lower_bound = [0.1 for _ in range(number_of_variables)]
        self.upper_bound = [15.0 for _ in range(number_of_variables)]

    def number_of_objectives(self) -> int:
        return len(self.obj_directions)

    def number_of_constraints(self) -> int:
        return 1

    def evaluate(self, solution: FloatSolution) -> FloatSolution:
        x = solution.variables
        s_max = truss200.data['sigma']
        rho = truss200.data['ro']
        
        # Phân tích kết cấu
        D, R, model = truss200.f200fem(x)
        
        # Compute areas
        L, H = model['L'], model['H']
        A = x @ H
        
        # Compute stresses
        S = R / A
        
        # Maximum stress constraint
        sc = np.max(np.abs(S))
        
        # Constraints
        # cv = s_max/sc - 1
        cv = sc/s_max

        # FBS
        x_new, f1, f2, g = FBS(self, x, L, H, D, cv, rho)
        
        # Get solution
        solution.variables = x_new
        solution.objectives[0] = f1
        solution.objectives[1] = f2
        solution.constraints[0] = g

        return solution

    def name(self):
        return "truss200bar"

