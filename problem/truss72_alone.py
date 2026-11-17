
import numpy as np
import navpy as nv
import math
    
#material properties
modE = 1e+4;
rho = 0.1 #lb/in3
sigma_a = 40;

a = 120.; b = 60.; 

Node = [[0, 0, 4*b], [a, 0, 4*b], [a, a, 4*b], [0, a, 4*b],
        [0, 0, 3*b], [a, 0, 3*b], [a, a, 3*b], [0, a, 3*b],
        [0, 0, 2*b], [a, 0, 2*b], [a, a, 2*b], [0, a, 2*b],
        [0, 0, 1*b], [a, 0, 1*b], [a, a, 1*b], [0, a, 1*b],
        [0, 0, 0*b], [a, 0, 0*b], [a, a, 0*b], [0, a, 0*b]];

Ele = [[1,5,1,-1,-1], [2,6,1,-1,-1], [3,7,1,-1,-1], [4,8,1,-1,-1], 
       [1,6,2,-1,-1], [2,5,2,-1,-1], [2,7,2,-1,-1], [3,6,2,-1,-1], [3,8,2,-1,-1], [4,7,2,-1,-1], [4,5,2,-1,-1], [1,8,2,-1,-1],
       [1,2,3,-1,-1], [2,3,3,-1,-1], [3,4,3,-1,-1], [4,1,3,-1,-1],
       [1,3,4,-1,-1], [2,4,4,-1,-1],
       
       [5,9, 5,-1,-1], [6,10,5,-1,-1], [7,11,5,-1,-1], [8,12,5,-1,-1], 
       [5,10,6,-1,-1], [6, 9,6,-1,-1], [6,11,6,-1,-1], [7,10,6,-1,-1], [7,12,6,-1,-1], [8,11,6,-1,-1], [8,9,6,-1,-1], [5,12,6,-1,-1],
       [5,6, 7,-1,-1], [6, 7,7,-1,-1], [7, 8,7,-1,-1], [8, 5,7,-1,-1],
       [5,7, 8,-1,-1], [6, 8,8,-1,-1],
       
       [9,13,9,-1,-1], [10,14, 9,-1,-1], [11,15, 9,-1,-1], [12,16, 9,-1,-1], 
       [9,14,10,-1,-1],[10,13,10,-1,-1], [10,15,10,-1,-1], [11,14,10,-1,-1], [11,16,10,-1,-1], [12,15,10,-1,-1], [12,13,10,-1,-1], [9,16,10,-1,-1],
       [9,10,11,-1,-1],[10,11,11,-1,-1], [11,12,11,-1,-1], [12, 9,11,-1,-1],
       [9,11,12,-1,-1],[10,12,12,-1,-1],
       
       [13,17,13,-1,-1], [14,18,13,-1,-1], [15,19,13,-1,-1], [16,20,13,-1,-1], 
       [13,18,14,-1,-1], [14,17,14,-1,-1], [14,19,14,-1,-1], [15,18,14,-1,-1], [15,20,14,-1,-1], [16,19,14,-1,-1], [16,17,14,-1,-1], [13,20,14,-1,-1],
       [13,14,15,-1,-1], [14,15,15,-1,-1], [15,16,15,-1,-1], [16,13,15,-1,-1],
       [13,15,16,-1,-1], [14,16,16,-1,-1]];

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

# load case 
Nload1 = [[1, 5, 5, -5]]; 
Nload2 = [[1, 0, 0, -5], [2, 0, 0, -5], [3, 0, 0, -5], [4, 0, 0, -5]]; 

LC1 = np.zeros((tdof,1))
LC2 = np.zeros((tdof,1))
for i in range(len(Nload1)):
    nodeid = Nload1[i][0]
    
    LC1[nodeid*3-3] = Nload1[i][1]
    LC1[nodeid*3-2] = Nload1[i][2]
    LC1[nodeid*3-1] = Nload1[i][3]

for i in range(len(Nload2)):
    nodeid = Nload2[i][0]
    
    LC2[nodeid*3-3] = Nload2[i][1]
    LC2[nodeid*3-2] = Nload2[i][2]
    LC2[nodeid*3-1] = Nload2[i][3]

# Boundary
Bound = [[17, 1, 1, 1], 
         [18, 1, 1, 1],
         [19, 1, 1, 1],
         [20, 1, 1, 1]];
presDof = np.array([48,49,50,51,52,53,54,55,56,57,58,59])
    
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
    
    # solve load case 1
    U1=np.zeros((tdof,1))
    S1=np.zeros((numElem,1))      
    disp1=np.linalg.solve(stiffness[np.ix_(actDof,actDof)],LC1[np.ix_(actDof)]);
    U1[np.ix_(actDof)]=disp1
    # solve load case 2
    U2=np.zeros((tdof,1))
    S2=np.zeros((numElem,1))      
    disp2=np.linalg.solve(stiffness[np.ix_(actDof,actDof)],LC2[np.ix_(actDof)]);
    U2[np.ix_(actDof)]=disp2
    
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
        
        Ue = np.dot(Te,U2[np.ix_(elemDof)])
        S2[e] = (modE/L[e]) * (Ue[3]-Ue[0])

    w = weight(x)
    A = np.array(Area)
    dis1 = np.maximum.reduce(np.abs(U1))
    sc1 = np.maximum.reduce(np.abs(S1))
    
    dis2 = np.maximum.reduce(np.abs(U2))
    sc2 = np.maximum.reduce(np.abs(S2))
    
    dis = max(dis1,dis2)
    sc = max(sc1,sc2)

    return A, w, dis, sc

#define weight function
def weight(x):
    A = assignA(x)
    return np.dot(A,L)*rho
    
# TEST
x=[i+1 for i in range(16)];

A, w, dis, sc = StructAnalysis(x)
print(np.max(dis))
print(np.max(sc))




