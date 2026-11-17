
import numpy as np
import math
import Module_2DFrame as st
import truss942data

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

_, data = truss942data.truss942data(excel_file='26StoreyTruss.xls', lcase=3)

# Chương trình tính toán FEM
def f942fem(x):
    
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
    #model['Nload'][:,1:3] = 0
    
    model = st.Solve3Dtruss(model)
    dis = model['disp']
    D = dis.flatten()
    R = model['force'][:,0,0]
    
    return np.array(D), np.array(R), model

# Chương trình tính hàm mục tiêu và vi phạm ràng buộc
def f942con(x):

    # Call f120bar to get displacements and axial forces
    D, R, model = f942fem(x) 

    # Compute areas
    L, H = model['L'], model['H']
    A = x @ H

    # Compute stresses
    S = R / A

    sc = np.max(np.abs(S))
    dc = np.max(np.abs(D[0:12]))
    #dc = np.max(np.abs(D))
    
    # Maximum stress constraint
    fy = data['fy']
    s_max = fy
    
    d_max = 15; #in
    
    # Constraint calculations
    Cmax = sc / s_max - 1
    Cdis = dc / d_max - 1
    
    # Combine all inequality constraints
    cv = np.concatenate([
        np.array([Cmax]),      # Maximum stress constraint
        np.array([Cdis])       # Displacement constraint
    ])
    
    # Tính hàm mục tiêu
    rho = data['ro']
    f1 = np.dot(A,L)*rho
    f2 = np.max(np.abs(D))
    f = [f1, f2]

    # Tính vi phạm ràng buộc
    #print(cv)
    g = max(cv)
    
    return f, g, model

# Chạy thử
# x có giá trị [1,200]

x = [   1.0839,
    1.0391,
    2.6717,
    1.7760,
    1.0141,
   13.7595,
    2.8718,
    5.4322,
    3.4958,
   18.1466,
    4.5200,
    5.1518,
   13.4414,
    2.0178,
    3.5073,
    1.1301,
   21.9859,
    2.2404,
    7.3811,
    1.0076,
   25.7885,
    2.6873,
   15.0954,
   21.3053,
   32.0365,
    1.2327,
   11.5003,
   16.0536,
   13.2467,
   13.5621,
   33.6164,
    2.9304,
    1.5948,
    2.2816,
    1.0947,
    1.0003,
   49.4738,
    3.0683,
    2.1761,
    2.6731,
    1.0359,
    1.2765,
   71.3230,
    3.0174,
    2.0306,
    3.3444,
    1.0067,
    1.2545,
   84.4509,
    2.9686,
    1.1744,
    3.2602,
    7.6698,
    6.0808,
   38.2940,
    1.0064,
   54.9719,
    2.5101,
    1.1473]
#x = np.ones(data['nvars'])
f, g, model = f942con(x); print(f,g)

# st.node_name = 'r'
# mat = 59
# elist = np.arange(len(model['Ele'][:, 0])) + 1
# emat = model['Ele'][:, 2]
# ID = elist[emat==mat]
# st.show_geometry3D(model, etype='E', ID=ID)

# d = model['disp']; 
# #print(d)
# dx = d[:,0]
# idxmax = abs(dx)>15
# for i in range(len(dx)):
#     if idxmax[i]==True:
#         print(i+1, dx[i])
#         print(model['Node'][i]/12)