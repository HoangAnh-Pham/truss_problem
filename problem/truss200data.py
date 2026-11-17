import numpy as np

def truss200data():
    """
    Generate data for a 200-element truss structure.
    
    """
    # FE DATA
    nvars = 29

    E = 3e4  # ksi
    I = 1.0
    B = 240.0
    H = 144.0  # in
    ro = 0.283  # lb/in3
    sigma = 10
    
    NoN = 77
    NoE = 200

    Node = np.zeros((NoN, 2))
    for i in range(1, 6):  # MATLAB 1:5 -> Python 0:5, adjusted for 1-based logic
        for j in range((i-1)*14 + 1, (i-1)*14 + 6):  # 1-based indexing in MATLAB
            jj = j - 1  # Convert to 0-based for Python
            Node[jj, 0] = (j - ((i-1)*14 + 1)) * B
            Node[jj, 1] = 360 + 10*H - (2*i - 2)*H
        for j in range((i-1)*14 + 6, (i-1)*14 + 15):
            jj = j - 1
            Node[jj, 0] = (j - ((i-1)*14 + 6)) * B / 2
            Node[jj, 1] = 360 + 10*H - (2*i - 1)*H
    for j in range(71, 76):
        jj = j - 1
        Node[jj, 0] = (j - 71) * B
        Node[jj, 1] = 360
    Node[75, 0] = B  # Node 76 in MATLAB (1-based)
    Node[76, 0] = 3 * B  # Node 77
    
    Ele = np.zeros((NoE, 5))
    for i in range(1, 5):
        Ele[i-1, :] = [i, i+1, 1, -1, -1]
    for i in range(1, 6):
        Ele[3*i + 2 - 1, :] = [i, 2*i + 4, 2, -1, -1]
    for i in range(7, 13):
        Ele[i + 12 - 1, :] = [i, i+1, 3, -1, -1]
    n = np.array([6, 20, 34, 48, 62]) - 1  # Adjust for 0-based indexing
    j = 0
    for i in range(18, 171, 38):
        Ele[i-1, :] = [n[j] + 1, n[j] + 2, 4, -1, -1]
        Ele[i + 7 - 1, :] = [n[j] + 8, n[j] + 9, 4, -1, -1]
        j += 1
    for i in range(1, 6):
        Ele[3*i + 23 - 1, :] = [2*i + 4, i + 14, 5, -1, -1]
    for i in range(1, 5):
        Ele[3*i + 3 - 1, :] = [i, 2*i + 5, 6, -1, -1]
        Ele[3*i + 4 - 1, :] = [i + 1, 2*i + 5, 6, -1, -1]
        Ele[3*i + 24 - 1, :] = [2*i + 5, i + 14, 6, -1, -1]
        Ele[3*i + 25 - 1, :] = [2*i + 5, i + 15, 6, -1, -1]
    for i in range(15, 19):
        Ele[i + 24 - 1, :] = [i, i + 1, 7, -1, -1]
    for i in range(15, 20):
        Ele[3*i - 2 - 1, :] = [i, 2*i - 10, 8, -1, -1]
    for i in range(21, 27):
        Ele[i + 36 - 1, :] = [i, i + 1, 9, -1, -1]
    for i in range(15, 20):
        Ele[3*i + 19 - 1, :] = [2*i - 10, i + 14, 10, -1, -1]
    for i in range(15, 19):
        Ele[3*i - 1 - 1, :] = [i, 2*i - 9, 11, -1, -1]
        Ele[3*i - 1, :] = [i + 1, 2*i - 9, 11, -1, -1]
        Ele[3*i + 20 - 1, :] = [2*i - 9, i + 14, 11, -1, -1]
        Ele[3*i + 21 - 1, :] = [2*i - 9, i + 15, 11, -1, -1]
    for i in range(29, 33):
        Ele[i + 48 - 1, :] = [i, i + 1, 12, -1, -1]
    for i in range(29, 34):
        Ele[3*i - 6 - 1, :] = [i, 2*i - 24, 13, -1, -1]
    for i in range(35, 41):
        Ele[i + 60 - 1, :] = [i, i + 1, 14, -1, -1]
    for i in range(29, 34):
        Ele[3*i + 15 - 1, :] = [2*i - 24, i + 14, 15, -1, -1]
    for i in range(29, 33):
        Ele[3*i - 5 - 1, :] = [i, 2*i - 23, 16, -1, -1]
        Ele[3*i - 4 - 1, :] = [i + 1, 2*i - 23, 16, -1, -1]
        Ele[3*i + 16 - 1, :] = [2*i - 23, i + 14, 16, -1, -1]
        Ele[3*i + 17 - 1, :] = [2*i - 23, i + 15, 16, -1, -1]
    for i in range(43, 47):
        Ele[i + 72 - 1, :] = [i, i + 1, 17, -1, -1]
    for i in range(43, 48):
        Ele[3*i - 10 - 1, :] = [i, 2*i - 38, 18, -1, -1]
    for i in range(49, 55):
        Ele[i + 84 - 1, :] = [i, i + 1, 19, -1, -1]
    for i in range(43, 48):
        Ele[3*i + 11 - 1, :] = [2*i - 38, i + 14, 20, -1, -1]
    for i in range(43, 47):
        Ele[3*i - 9 - 1, :] = [i, 2*i - 37, 21, -1, -1]
        Ele[3*i - 8 - 1, :] = [i + 1, 2*i - 37, 21, -1, -1]
        Ele[3*i + 12 - 1, :] = [2*i - 37, i + 14, 21, -1, -1]
        Ele[3*i + 13 - 1, :] = [2*i - 37, i + 15, 21, -1, -1]
    for i in range(57, 61):
        Ele[i + 96 - 1, :] = [i, i + 1, 22, -1, -1]
    for i in range(57, 62):
        Ele[3*i - 14 - 1, :] = [i, 2*i - 52, 23, -1, -1]
    for i in range(63, 69):
        Ele[i + 108 - 1, :] = [i, i + 1, 24, -1, -1]
    for i in range(57, 62):
        Ele[3*i + 7 - 1, :] = [2*i - 52, i + 14, 25, -1, -1]
    for i in range(57, 61):
        Ele[3*i - 13 - 1, :] = [i, 2*i - 51, 26, -1, -1]
        Ele[3*i - 12 - 1, :] = [i + 1, 2*i - 51, 26, -1, -1]
        Ele[3*i + 8 - 1, :] = [2*i - 51, i + 14, 26, -1, -1]
        Ele[3*i + 9 - 1, :] = [2*i - 51, i + 15, 26, -1, -1]
    for i in range(71, 75):
        Ele[i + 120 - 1, :] = [i, i + 1, 27, -1, -1]
    Ele[194, :] = [71, 76, 28, -1, -1]
    Ele[196, :] = [73, 76, 28, -1, -1]
    Ele[197, :] = [73, 77, 28, -1, -1]
    Ele[199, :] = [75, 77, 28, -1, -1]
    Ele[195, :] = [72, 76, 29, -1, -1]
    Ele[198, :] = [74, 77, 29, -1, -1]
    
    
    
    Mat = np.tile([E, 1, I, ro], (nvars, 1))
    
    Nodeload1 = np.array([
        [1, 1, 0, 0], [6, 1, 0, 0], [15, 1, 0, 0], [20, 1, 0, 0],
        [29, 1, 0, 0], [34, 1, 0, 0], [43, 1, 0, 0], [48, 1, 0, 0],
        [57, 1, 0, 0], [62, 1, 0, 0], [71, 1, 0, 0]
    ])
    Nodeload2 = []
    for i in range(1, 7):
        Nodeload2.append([i, 0, -10, 0])
    for i in range(8, 15, 2):
        Nodeload2.append([i, 0, -10, 0])
    for i in range(15, 21):
        Nodeload2.append([i, 0, -10, 0])
    for i in range(22, 27, 2):
        Nodeload2.append([i, 0, -10, 0])
    for i in range(28, 35):
        Nodeload2.append([i, 0, -10, 0])
    for i in range(36, 41, 2):
        Nodeload2.append([i, 0, -10, 0])
    for i in range(42, 49):
        Nodeload2.append([i, 0, -10, 0])
    for i in range(50, 55, 2):
        Nodeload2.append([i, 0, -10, 0])
    for i in range(56, 63):
        Nodeload2.append([i, 0, -10, 0])
    for i in range(64, 69, 2):
        Nodeload2.append([i, 0, -10, 0])
    for i in range(70, 76):
        Nodeload2.append([i, 0, -10, 0])
    Nodeload2 = np.array(Nodeload2)
    
    Eload = np.zeros((NoE, 5))
    
    Bound = np.array([
        [76, 1, 1, 0],
        [77, 1, 1, 0]
    ])
    
    # XV and XB
    XB = np.array([0.1, 15])
    XV = np.array([
        0.1, 0.347, 0.44, 0.539, 0.954, 1.081, 1.174, 1.333, 1.488, 1.764,
        2.142, 2.697, 2.8, 3.131, 3.565, 3.813, 4.805, 5.952, 6.572, 7.192,
        8.525, 9.3, 10.85, 13.33, 14.29, 17.17, 19.18, 23.68, 28.08, 33.7
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
    }

model = truss200data()