#from anastruct import SystemElements

import numpy as np
import Module_2DFrame as st
from problem import callength as cl

def f10fem(x):

#    ss = SystemElements()
    
    E = 1.0e+4     # Elastic modulus [ksi]
    I = 1.         # do not use for truss
    ro = 0.1e-0    # Material density [lb/in3]

    P1 = -100.     # Concentrated load [kips]
    P2 = 0.

    NoN = 6        # Number of nodes
    NoE = 10       # Number of elements
    
    a = 360.;      # Span length [in]
    
    # Mesh Data
    
    # Node(i) = [x, y, z]
    Node = [[2*a,a], 
            [2*a,0],
            [a, a], 
            [a, 0],
            [0, a], 
            [0, 0]]

    # Ele(i) = [node1, node2, Mat];
    Ele=[[0,0,0] for i in range(NoE)];
    Ele = [[5, 3, 1],
           [3, 1, 2],
           [6, 4, 3],
           [4, 2, 4],
           [3, 4, 5],
           [1, 2, 6],
           [5, 4, 7],
           [6, 3, 8],
           [3, 2, 9],
           [4, 1, 10]];

    # Material properties
    Mat = [[0,0,0,0] for i in range(NoE)];
    for i in range(NoE): 
        E1=E; A1=x[i];
        Mat[i]= [E1,A1,1,1]; 
    
    # Nodal load [node, Fx, Fy, M]
    Nload= [[1, 0, P2, 0],
            [2, 0, P1, 0], 
            [3, 0, P2, 0], 
            [4, 0, P1, 0]];
    
    BC = [[5, 1, 1, 0], [6, 1, 1, 0]]
    
    # Tính chiều dài thanh
    L, H = cl.callength(np.array(Node), np.array(Ele), NoE, NoE)
    
    # Khởi tạo mô hình tính
    model = st.SystemModel('2Dtruss')
    model['Node'] = Node
    model['Ele'] = Ele
    model['Mat'] = Mat
    model['Nload'] = Nload
    model['Bound'] = BC
    model['L'] = L
    model['H'] = H
    
    model = st.Solve2Dtruss(model)
    dis = model['disp']
    D = dis.flatten()
    R = model['force'][:,0,0]
       
    return D, R, model

# Chương trình tính hàm mục tiêu và vi phạm ràng buộc
def f10con(x):

    # Call f25bar to get displacements and axial forces
    D, R, model = f10fem(x) 

    # Compute areas
    L, H = model['L'], model['H']
    A = x @ H

    # Compute stresses
    S = R / A

    # Maximum stress constraint
    sc = np.max(np.abs(S))
    s_max = 25

    # Constraints
    cv = sc / s_max - 1
    
    # Tính hàm mục tiêu
    rho = 0.1
    f1 = np.dot(A,L)*rho
    f2 = np.max(np.abs(D))
    f = [f1, f2]

    # Tính vi phạm ràng buộc
    g = cv
    
    return f, g, model

if __name__ == "__main__":
    x=[1 for i in range(10)];
    D, N, ss = f10fem(x)    

    st.show_geometry(ss, show_node=True, show_ele=True, pos=-1)
    st.show_axial(ss)