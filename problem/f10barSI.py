
import numpy as np
import Module_2DFrame as st

# Tính chiều dài thanh và ma trận kết nối
def callength(Node, Ele, NoE, nvar):
    
    Ele = Ele.astype(int)
    
    # Khởi tạo ma trận
    H = np.zeros((nvar, NoE))
    L = np.zeros(NoE)
    
    # Vòng lặp qua từng phần tử
    for e in range(NoE):
        # Tạo ma trận tọa độ C
        # Chuyển chỉ số từ 1-based (MATLAB) sang 0-based (Python)
        if np.shape(Node)[1]==3:
            C = np.array([
            [Node[Ele[e,0]-1,0], Node[Ele[e,0]-1,1], Node[Ele[e,0]-1,2]],
            [Node[Ele[e,1]-1,0], Node[Ele[e,1]-1,1], Node[Ele[e,1]-1,2]]
            ])
        else:
            C = np.array([
            [Node[Ele[e,0]-1,0], Node[Ele[e,0]-1,1], 0],
            [Node[Ele[e,1]-1,0], Node[Ele[e,1]-1,1], 0]
            ])
        
        # Trích xuất tọa độ
        x1, y1, z1 = C[0,0], C[0,1], C[0,2]
        x2, y2, z2 = C[1,0], C[1,1], C[1,2]
        
        # Tính toán khoảng cách
        dx = x2 - x1
        dy = y2 - y1
        dz = z2 - z1
        
        # Tính độ dài phần tử
        L[e] = np.sqrt(dx**2 + dy**2 + dz**2)
        
        # Cập nhật ma trận kết nối
        H[Ele[e,2]-1,e] = 1
    
    return L, H

# Chương trình tính toán FEM
def f10barSI(x):
    """
    10-bar 2D truss optimization problem
    Parameters:
        x : array-like, design variables
        f : objective function value
        g : constraint values

    """

    # Vật liệu
    rho = 0.1
    sigma_a = 25.0
    E = 1.0e+4 

    # Sơ đồ hình học
    a = 360.
    Node = [[2*a,a], 
            [2*a,0],
            [a, a], 
            [a, 0],
            [0, a], 
            [0, 0]]

    Ele = [[5, 3, 1, 1, 1],
           [3, 1, 2, 1, 1],
           [6, 4, 3, 1, 1],
           [4, 2, 4, 1, 1],
           [3, 4, 5, 1, 1],
           [1, 2, 6, 1, 1],
           [5, 4, 7, 1, 1],
           [6, 3, 8, 1, 1],
           [3, 2, 9, 1, 1],
           [4, 1, 10, 1, 1]]

    # Tiết diện
    Mat = [[E,xi,1,0] for xi in x]

    # Tải trọng
    Load = [[2, 0, -100, 0],  
            [4, 0, -100, 0]]

    # Gối tựa
    BC = [[5, 1, 1, 0],
          [6, 1, 1, 0]]

    # Tính chiều dài thanh
    L, H = callength(np.array(Node), np.array(Ele), 10, 10)
    
    # Khởi tạo mô hình tính
    model = st.SystemModel('2Dtruss')
    model['Node'] = Node
    model['Ele'] = Ele
    model['Mat'] = Mat
    model['Bound'] = BC
    model['Eload'] = []
    model['Nload'] = Load
    model['Supp'] = []
    model['Spring'] = []
    
    # Phân tích kết cấu
    model = st.Solve2Dtruss(model)
    
    # Chuyển vị và nội lực
    dis = abs(model['disp'])
    N = model['force'][:,0,0]
    
    # Tính ứng suất
    A = H.T @ x
    S = N/A
    
    # Tính hàm mục tiêu
    f1 = np.dot(A,L)*rho
    f2 = np.max(dis)
    f = [f1, f2]
    
    # Tính vi phạm ràng buộc
    g = np.max(abs(S))/sigma_a - 1
    
    return f, g, model

# Chạy thử
x = np.ones(10)
_, _, model = f10barSI(x)
st.show_geometry(model,'S',show_ele=True)
st.show_displacement(model)