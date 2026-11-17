
import numpy as np
import Module_2DFrame as st
import truss25data

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

data = truss25data.truss25data()

# Chương trình tính toán FEM
def f25fem(x):
    
    nvars = data['nvars']
    NoE = data['NoE']

    # Sơ đồ hình học
    Node = data['Node']
    Ele = data['Ele']

    # Tiết diện
    Mat = data['Mat']
    Mat[0:nvars, 1] = x

    # Tải trọng
    Nload = [data['Nodeload1'],
             data['Nodeload2'],
             data['Nodeload3']]

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
        
    return D, R, model

# Chương trình tính hàm mục tiêu và vi phạm ràng buộc
def f25con(x):

    # Call f25bar to get displacements and axial forces
    D, R, model = f25fem(x) 

    # Compute areas
    L, H = model['L'], model['H']
    A = x @ H

    # Compute stresses
    S = R / A

    # Maximum stress constraint
    sc = np.max(np.abs(S))
    s_max = data['sigma']

    # Constraints
    cv = sc / s_max - 1
    
    # Tính hàm mục tiêu
    rho = data['ro']
    f1 = np.dot(A,L)*rho
    f2 = np.max(np.abs(D))
    f = [f1, f2]

    # Tính vi phạm ràng buộc
    g = cv
    
    return f, g, model

# Chạy thử
# x có giá trị [0.01, 3.5]

# x = np.ones(data['nvars'])
# f, g, model = f25con(x)
# print(f,g)
# st.show_geometry3D(model)