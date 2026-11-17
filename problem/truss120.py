
import numpy as np
import math
import Module_2DFrame as st
import truss120data

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

data = truss120data.truss120data()

# Chương trình tính toán FEM
def f120fem(x):
    
    nvars = data['nvars']
    NoE = data['NoE']

    # Sơ đồ hình học
    Node = data['Node']
    Ele = data['Ele']

    # Tiết diện
    Mat = data['Mat']
    Mat[0:nvars, 1] = x

    # Tải trọng
    Nload = [data['Nodeload']]

    # Gối tựa
    BC = data['Bound']

    # Tính chiều dài thanh
    L, H = callength(np.array(Node), np.array(Ele), NoE, nvars)
    
    # Khởi tạo mô hình tính
    model = st.SystemModel('3Dtruss')
    model['Node'] = Node
    model['Ele'] = Ele
    model['Mat'] = Mat
    model['Bound'] = BC
    model['L'] = L
    model['H'] = H
    
    # Phân tích kết cấu
    model['Nload'] = Nload[0]
    model = st.Solve3Dtruss(model)
    dis = model['disp']
    D = dis.flatten()
    R = model['force'][:,0,0]
    
    return np.array(D), np.array(R), model

# Chương trình tính hàm mục tiêu và vi phạm ràng buộc
def f120con(x):

    # Call f120bar to get displacements and axial forces
    D, R, model = f120fem(x) 

    # Compute areas
    L, H = model['L'], model['H']
    A = x @ H

    # Compute stresses
    S = R / A

    sc = np.max(np.abs(S))
    dc = np.max(np.abs(D))
    
    # Maximum stress constraint
    fy = data['fy']
    E = data['E']
    s_max = 0.6*fy
    
    d_max = 0.1969; #in

    # Compressive stresses (negative stresses)
    Smin = S[S < 0]
    
    # Buckling stress calculation
    k = 1
    anfa = 0.4993
    beta = 0.6777
    
    # Radius of gyration
    ri = anfa * (A ** beta)
    
    # Slenderness ratio
    lamda = k * L / ri
    
    # Critical slenderness ratio
    Cc = math.sqrt(2 * math.pi**2 * E / fy)
    
    # Calculate buckling stress for each element
    s_min = np.zeros(len(A))
    for i in range(len(A)):
        if lamda[i] < Cc:
            s_min[i] = ((1 - lamda[i]**2 / (2 * Cc**2)) * fy / 
                       (5/3 + 3*lamda[i]/(8*Cc) - lamda[i]**3/(8*Cc**3)))
        else:
            s_min[i] = (12 * math.pi**2 * E) / (23 * lamda[i]**2)
    
    # Constraint calculations
    Cmax = sc / s_max - 1
    
    # Buckling constraints (only for elements in compression)
    compression_indices = S < 0
    if np.any(compression_indices):
        Cmin = -Smin / s_min[compression_indices] - 1
    else:
        Cmin = np.array([])
    
    Cdis = dc / d_max - 1
    
    # Combine all inequality constraints
    cv = np.concatenate([
        np.array([Cmax]),      # Maximum stress constraint
        Cmin,                  # Buckling constraints
        np.array([Cdis])       # Displacement constraint
    ])
    
    # Tính hàm mục tiêu
    rho = data['ro']
    f1 = np.dot(A,L)*rho
    f2 = np.max(np.abs(D))
    f = [f1, f2]

    # Tính vi phạm ràng buộc
    g = max(cv)
    
    return f, g, model

# Chạy thử
# x có giá trị [0.775,20]

x = np.ones(data['nvars'])
f, g, model = f120con(x); print(f,g)
st.show_geometry3D(model)