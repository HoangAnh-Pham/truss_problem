import numpy as np
import math

def truss120data():
    """
    120-bar 3D truss optimization problem
    x = design variables (input - 0<=x<=1)
    """
    
    nvars = 7
    
    # FE data
    # Material properties
    ro = 0.288  # lb/in^3
    E = 30450   # ksi
    fy = 58  # ksi
    A = 1
    I = 1
    
    # Geometry (position in inches)
    r1 = 625.59  # in 15.89 m
    r2 = 492.12  # in 12.04 m
    r3 = 273.26  # in 6.94 m
    h1 = 118.11  # in 3 m
    h2 = 196.85  # in 5.85 m
    h3 = 275.59  # in 7 m
    
    # Initialize node array
    node = np.zeros((49, 3))
    
    for i in range(1, 50):  # 1 to 49 (MATLAB indexing)
        # Layer z=0
        if i <= 12:
            node[i-1, :] = [r1 * math.cos((i-1) * math.pi / 6), 
                           r1 * math.sin((i-1) * math.pi / 6), 
                           0]
        elif 12 < i <= 36:
            node[i-1, :] = [r2 * math.cos((i-13) * math.pi / 12), 
                           r2 * math.sin((i-13) * math.pi / 12), 
                           h1]
        elif 36 < i <= 48:
            node[i-1, :] = [r3 * math.cos((i-37) * math.pi / 6), 
                           r3 * math.sin((i-37) * math.pi / 6), 
                           h2]
        elif i == 49:
            node[i-1, :] = [0, 0, h3]
    
    # Initialize element array
    ele = np.zeros((120, 3), dtype=int)
    nele = 0
    
    # Group 1
    for i in range(1, 13):  # 1 to 12
        ele[nele, :] = [49, 49-i, 1]
        nele += 1
    
    # Group 2
    for i in range(1, 12):  # 1 to 11
        ele[nele, :] = [36+i, 36+i+1, 2]
        nele += 1
    
    ele[nele, :] = [48, 37, 2]
    nele += 1
    
    # Group 3
    for i in range(1, 13):  # 1 to 12
        ele[nele, :] = [36+i, 2*i+11, 3]
        nele += 1
    
    # Group 4
    for i in range(1, 12):  # 1 to 11
        ele[nele, :] = [37+i, 2*i+12, 4]
        nele += 1
        ele[nele, :] = [37+i, 2*i+14, 4]
        nele += 1
    
    ele[nele, :] = [37, 36, 4]
    nele += 1
    ele[nele, :] = [37, 14, 4]
    nele += 1
    
    # Group 5
    for i in range(1, 24):  # 1 to 23
        ele[nele, :] = [12+i, 12+i+1, 5]
        nele += 1
    
    ele[nele, :] = [36, 13, 5]
    nele += 1
    
    # Group 6
    for i in range(1, 13):  # 1 to 12
        ele[nele, :] = [11+2*i, i, 6]
        nele += 1
    
    # Group 7
    for i in range(2, 13):  # 2 to 12
        ele[nele, :] = [i, 2*i+10, 7]
        nele += 1
        ele[nele, :] = [i, 2*i+12, 7]
        nele += 1
    
    ele[nele, :] = [1, 14, 7]
    nele += 1
    ele[nele, :] = [1, 36, 7]
    nele += 1
    
    # Cross-section areas
    # MATLAB kron equivalent: np.kron
    material_props = np.array([E, A, I, ro])
    Mat = np.kron(material_props, np.ones((nvars, 1)))
    
    # Loading
    P1 = -13.49  # kip
    P2 = -6.744  # kip
    P3 = -2.248  # kip
    
    # Create load array
    # Nodes 13 to 49 (37 nodes total)
    load_nodes = np.arange(13, 50).reshape(-1, 1)  # nodes 13-49
    load_x = np.zeros((37, 1))  # x-direction loads
    load_y = np.zeros((37, 1))  # y-direction loads
    
    # z-direction loads
    load_z = np.concatenate([
        np.array([P2]).reshape(-1, 1),           # First node (13)
        np.full((23, 1), P3),                    # Nodes 14-36 (23 nodes)
        np.full((12, 1), P2),                    # Nodes 37-48 (12 nodes)
        np.array([P1]).reshape(-1, 1)           # Last node (49)
    ])
    
    # Prescribed displacement
    # node    dof  displacement(m)      
    # dof = 1 for x-axis, 2 for y-axis, 3 for z-axis
    bound_nodes = np.arange(1, 13).reshape(-1, 1)  # nodes 1-12
    bound_dofs = np.tile([1, 1, 1], (12, 1))       # constrain all 3 DOFs
    Bound = np.hstack([bound_nodes, bound_dofs])
    
    # Bounds
    XB = np.array([0.775, 20])
    XV = []
    
    # Store data in object
    Node = node
    Ele = ele
    Bound = Bound
    
    NoE = len(Ele)
    NLoad = np.hstack([load_nodes, load_x, load_y, load_z])
    Eload = np.zeros((NoE, 5))
    
    # Return all data as a dictionary
    return {
        'ro': ro,
        'fy': fy,
        'E': E,
        'nvars': nvars,
        'NoE': NoE,
        'XV': XV,
        'XB': XB,
        'Node': Node,
        'Ele': Ele,
        'Mat': Mat,
        'Eload': Eload,
        'Bound': Bound,
        'Nodeload': NLoad,
    }