import numpy as np

def truss25data():
    """
    Generate data for a 25-element truss structure.
    
    """
    # FE DATA
    nvars = 8

    E = 1e4  # ksi
    I = 1.0
    B = 200.0
    H = 100.0
    b = 75.0  # in
    ro = 0.1  # lb/in3
    sigma = 40

    NoE = 25

    Node = np.array([
        [-b/2, 0, 2*H],
        [b/2, 0, 2*H],
        [-b/2, b/2, H],
        [b/2, b/2, H],
        [b/2, -b/2, H],
        [-b/2, -b/2, H],
        [-B/2, B/2, 0],
        [B/2, B/2, 0],
        [B/2, -B/2, 0],
        [-B/2, -B/2, 0]
    ])
    
    Ele = np.array([
        [1, 2, 1, -1, -1],
        [1, 4, 2, -1, -1], [2, 3, 2, -1, -1], [1, 5, 2, -1, -1], [2, 6, 2, -1, -1],
        [2, 5, 3, -1, -1], [2, 4, 3, -1, -1], [1, 3, 3, -1, -1], [1, 6, 3, -1, -1],
        [3, 6, 4, -1, -1], [4, 5, 4, -1, -1],
        [3, 4, 5, -1, -1], [5, 6, 5, -1, -1],
        [3, 10, 6, -1, -1], [6, 7, 6, -1, -1], [4, 9, 6, -1, -1], [5, 8, 6, -1, -1],
        [3, 8, 7, -1, -1], [4, 7, 7, -1, -1], [6, 9, 7, -1, -1], [5, 10, 7, -1, -1],
        [3, 7, 8, -1, -1], [4, 8, 8, -1, -1], [5, 9, 8, -1, -1], [6, 10, 8, -1, -1]
    ])
    
    Mat = np.tile([E, 1, I, ro], (nvars, 1))
    
    Nodeload1 = np.array([
        [1, 1, -10, -10],
        [2, 0, -10, -10],
        [3, 0.5, 0, 0],
        [6, 0.6, 0, 0]
    ])
    
    Nodeload2 = np.array([
        [1, 0, 20, -5],
        [2, 0, -20, -5]
    ])
    
    Nodeload3 = np.array([
        [1, 1, 10, -5],
        [2, 0, 10, -5],
        [3, 0.5, 0, 0],
        [6, 0.5, 0, 0]
    ])
    
    Eload = np.zeros((NoE, 5))
    
    Bound = np.array([
        [7, 1, 1, 1],
        [8, 1, 1, 1],
        [9, 1, 1, 1],
        [10, 1, 1, 1]
    ])

    NoE = len(Ele)
    
    # XV and XB
    XB = np.array([0.01, 3.5])
    XV = np.array([
        0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0,
        1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0,
        2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.8, 3.0, 3.2, 3.4
    ])

    # Return all data as a dictionary
    return {
        'ro': ro,
        'sigma': sigma,
        'nvars': nvars,
        'NoE': NoE,
        'XV': XV,
        'XB': XB,
        'Node': Node,
        'Ele': Ele,
        'Mat': Mat,
        'Eload': Eload,
        'Bound': Bound,
        'Nodeload1': Nodeload1,
        'Nodeload2': Nodeload2,
        'Nodeload3': Nodeload3,
    }
