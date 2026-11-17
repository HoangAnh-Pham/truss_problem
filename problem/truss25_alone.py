
import numpy as np
import navpy as nv
import math
    
#material properties
modE = 1e+4;
rho = 0.1 #lb/in3
sigma_a = 40;

B = 200.; H = 100.; b = 75.;

Node = [[-b/2, 0, 2*H], 
        [b/2, 0, 2*H],
        [-b/2, b/2, H],
        [b/2, b/2, H],
        [b/2, -b/2, H],
        [-b/2, -b/2, H],
        [-B/2, B/2, 0],
        [B/2, B/2, 0],
        [B/2, -B/2, 0],
        [-B/2, -B/2, 0]];

Ele = [[1, 2, 1],
       [1, 4, 2],
       [2, 3, 2],
       [1, 5, 2],
       [2, 6, 2],
       [2, 5, 3],
       [2, 4, 3],
       [1, 3, 3],
       [1, 6, 3],
       [3, 6, 4],
       [4, 5, 4],
       [3, 4, 5],
       [5, 6, 5],
       [3, 10, 6],
       [6, 7, 6],
       [4, 9, 6],
       [5, 8, 6],
       [3, 8, 7],
       [4, 7, 7],
       [6, 9, 7],
       [5, 10, 7],
       [3, 7, 8],
       [4, 8, 8],
       [5, 9, 8],
       [6, 10, 8]];

#define function for assigning cross-section
def assignA(x):
    A = np.zeros(len(Ele))
    for i in range(len(Ele)):
        A[i] = x[Ele[i][2]-1]
    # print(A)
    return A

#define truss layout
nodeCords = np.array(Node)

# Member#Node--Node
elemNodes = np.array(Ele)

numElem = len(elemNodes)
numNodes = len(nodeCords)
tdof = 3*numNodes
xx = nodeCords[:,0]
yy = nodeCords[:,1]
zz = nodeCords[:,2]

L = np.zeros((numElem,)) #lengths of members
lxy = np.zeros((numElem,))
rx = np.zeros((numElem,))
ry = np.zeros((numElem,))
rz = np.zeros((numElem,))

for e in range(numElem):
    indice = elemNodes[e,:]

    xa = xx[indice[1]-1]-xx[indice[0]-1]
    ya = yy[indice[1]-1]-yy[indice[0]-1]
    za = zz[indice[1]-1]-zz[indice[0]-1]
    
    lxy[e] = np.sqrt(xa*xa+ya*ya)
    L[e] = np.sqrt(xa*xa+ya*ya+za*za)
    rz[e] = math.atan2(ya,xa)
    ry[e] = -math.atan2(za,lxy[e])
    
    # print([xa,ya,za])


#load case 1
Nload1 = [[1, 1, -10, -10], 
          [2, 0, -10, -10],
          [3, 0.5, 0, 0],
          [6, 0.6, 0, 0]];
LC1 = np.zeros((tdof,1))
for i in range(len(Nload1)):
    nodeid = Nload1[i][0]
    
    LC1[nodeid*3-3] = Nload1[i][1]
    LC1[nodeid*3-2] = Nload1[i][2]
    LC1[nodeid*3-1] = Nload1[i][3]

# Boundary
Bound = [[7, 1, 1, 1], 
         [8, 1, 1, 1],
         [9, 1, 1, 1],
         [10, 1, 1, 1]];
presDof = np.array([18,19,20,21,22,23,24,25,26,27,28,29])
    
actDof=np.setdiff1d(np.arange(tdof),presDof)
    
def StructAnalysis(x):
    Area = assignA(x)

    stiffness=np.zeros((tdof,tdof))
    for e in range(numElem):
        Te=np.zeros((6,6))
        indice = elemNodes[e,:]-1
        elemDof = np.array([indice[0]*3, indice[0]*3+1, indice[0]*3+2, 
                            indice[1]*3, indice[1]*3+1, indice[1]*3+2 ])
        dcm = nv.angle2dcm(rz[e],ry[e],rx[e],'ZYX');
        Te[np.ix_([0,1,2],[0,1,2])] +=dcm
        Te[np.ix_([3,4,5],[3,4,5])] +=dcm
        
        EA = modE*Area[e]
        k1 = (EA/L[e])
        # print(L[e])
        Ke = np.zeros((6,6))
        Ke[0,0] = k1; 
        Ke[0,3]= -k1; Ke[3,0]= -k1;
        Ke[3,3] = k1; 
        
        Ke = np.dot(np.dot(np.transpose(Te),Ke),Te) 
        stiffness[np.ix_(elemDof,elemDof)] += Ke
    
    # print(stiffness)
    
    U1=np.zeros((tdof,1))
    S1=np.zeros((numElem,1))      
    disp1=np.linalg.solve(stiffness[np.ix_(actDof,actDof)],LC1[np.ix_(actDof)]);
    U1[np.ix_(actDof)]=disp1
    
    #print(U1)
    for e in range(numElem):
        Te=np.zeros((6,6))
        indice = elemNodes[e,:]-1
        elemDof = np.array([indice[0]*3, indice[0]*3+1, indice[0]*3+2, 
                            indice[1]*3, indice[1]*3+1, indice[1]*3+2 ])
        dcm = nv.angle2dcm(rz[e],ry[e],rx[e],'ZYX');
        Te[np.ix_([0,1,2],[0,1,2])] +=dcm
        Te[np.ix_([3,4,5],[3,4,5])] +=dcm
        
        Ue = np.dot(Te,U1[np.ix_(elemDof)])
        
        S1[e] = (modE/L[e]) * (Ue[3]-Ue[0])
        
    #print(S1)
    # w = weight(x)
    # A = np.array(Area)
    dis = np.max(np.abs(U1))
    sc = np.max(np.abs(S1))

    return dis, sc

#define weight function
def weight(x):
    A = assignA(x)
    return np.dot(A,L)*rho
    
# TEST
# x=[i+1 for i in range(8)];
# w = weight(x)
# dis, sc = StructAnalysis(x)
# print(dis)
# print(sc)




