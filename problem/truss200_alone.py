
import numpy as np
    
#material properties
modE = 30000
rho = 0.283 #lb/in3

#define function for assigning cross-section
def assignA(x):
    A = np.asarray([x[0],
                    x[0],
                    x[0],
                    x[0],
                    x[1],
                    x[5],
                    x[5],
                    x[1],
                    x[5],
                    x[5],
                    x[1],
                    x[5],
                    x[5],
                    x[1],
                    x[5],
                    x[5],
                    x[1],
                    x[3],
                    x[2],
                    x[2],
                    x[2],
                    x[2],
                    x[2],
                    x[2],
                    x[3],
                    x[4],
                    x[5],
                    x[5],
                    x[4],
                    x[5],
                    x[5],
                    x[4],
                    x[5],
                    x[5],
                    x[4],
                    x[5],
                    x[5],
                    x[4],
                    x[6],
                    x[6],
                    x[6],
                    x[6],
                    x[7],
                    x[10],
                    x[10],
                    x[7],
                    x[10],
                    x[10],
                    x[7],
                    x[10],
                    x[10],
                    x[7],
                    x[10],
                    x[10],
                    x[7],
                    x[3],
                    x[8],
                    x[8],
                    x[8],
                    x[8],
                    x[8],
                    x[8],
                    x[3],
                    x[9],
                    x[10],
                    x[10],
                    x[9],
                    x[10],
                    x[10],
                    x[9],
                    x[10],
                    x[10],
                    x[9],
                    x[10],
                    x[10],
                    x[9],
                    x[11],
                    x[11],
                    x[11],
                    x[11],
                    x[12],
                    x[15],
                    x[15],
                    x[12],
                    x[15],
                    x[15],
                    x[12],
                    x[15],
                    x[15],
                    x[12],
                    x[15],
                    x[15],
                    x[12],
                    x[3],
                    x[13],
                    x[13],
                    x[13],
                    x[13],
                    x[13],
                    x[13],
                    x[3],
                    x[14],
                    x[15],
                    x[15],
                    x[14],
                    x[15],
                    x[15],
                    x[14],
                    x[15],
                    x[15],
                    x[14],
                    x[15],
                    x[15],
                    x[14],
                    x[16],
                    x[16],
                    x[16],
                    x[16],
                    x[17],
                    x[20],
                    x[20],
                    x[17],
                    x[20],
                    x[20],
                    x[17],
                    x[20],
                    x[20],
                    x[17],
                    x[20],
                    x[20],
                    x[17],
                    x[3],
                    x[18],
                    x[18],
                    x[18],
                    x[18],
                    x[18],
                    x[18],
                    x[3],
                    x[19],
                    x[20],
                    x[20],
                    x[19],
                    x[20],
                    x[20],
                    x[19],
                    x[20],
                    x[20],
                    x[19],
                    x[20],
                    x[20],
                    x[19],
                    x[21],
                    x[21],
                    x[21],
                    x[21],
                    x[22],
                    x[25],
                    x[25],
                    x[22],
                    x[25],
                    x[25],
                    x[22],
                    x[25],
                    x[25],
                    x[22],
                    x[25],
                    x[25],
                    x[22],
                    x[3],
                    x[23],
                    x[23],
                    x[23],
                    x[23],
                    x[23],
                    x[23],
                    x[3],
                    x[24],
                    x[25],
                    x[25],
                    x[24],
                    x[25],
                    x[25],
                    x[24],
                    x[25],
                    x[25],
                    x[24],
                    x[25],
                    x[25],
                    x[24],
                    x[26],
                    x[26],
                    x[26],
                    x[26],
                    x[27],
                    x[28],
                    x[27],
                    x[27],
                    x[28],
                    x[27]])
    return A

#define truss layout
nodeCords = np.array([[   0,1800],
                      [ 240,1800],
                      [ 480,1800],
                      [ 720,1800],
                      [ 960,1800],
                      [   0,1656],
                      [ 120,1656],
                      [ 240,1656],
                      [ 360,1656],
                      [ 480,1656],
                      [ 600,1656],
                      [ 720,1656],
                      [ 840,1656],
                      [ 960,1656],
                      [   0,1512],
                      [ 240,1512],
                      [ 480,1512],
                      [ 720,1512],
                      [ 960,1512],
                      [   0,1368],
                      [ 120,1368],
                      [ 240,1368],
                      [ 360,1368],
                      [ 480,1368],
                      [ 600,1368],
                      [ 720,1368],
                      [ 840,1368],
                      [ 960,1368],
                      [   0,1224],
                      [ 240,1224],
                      [ 480,1224],
                      [ 720,1224],
                      [ 960,1224],
                      [   0,1080],
                      [ 120,1080],
                      [ 240,1080],
                      [ 360,1080],
                      [ 480,1080],
                      [ 600,1080],
                      [ 720,1080],
                      [ 840,1080],
                      [ 960,1080],
                      [   0, 936],
                      [ 240, 936],
                      [ 480, 936],
                      [ 720, 936],
                      [ 960, 936],
                      [   0, 792],
                      [ 120, 792],
                      [ 240, 792],
                      [ 360, 792],
                      [ 480, 792],
                      [ 600, 792],
                      [ 720, 792],
                      [ 840, 792],
                      [ 960, 792],
                      [   0, 648],
                      [ 240, 648],
                      [ 480, 648],
                      [ 720, 648],
                      [ 960, 648],
                      [   0, 504],
                      [ 120, 504],
                      [ 240, 504],
                      [ 360, 504],
                      [ 480, 504],
                      [ 600, 504],
                      [ 720, 504],
                      [ 840, 504],
                      [ 960, 504],
                      [   0, 360],
                      [ 240, 360],
                      [ 480, 360],
                      [ 720, 360],
                      [ 960, 360],
                      [ 240,   0],
                      [ 720,   0]])

###########################Member#Node--Node
elemNodes = np.array([[0,1], #member 1 node1 - node2
                      [1,2], #member 2 node2 - node3
                      [2,3], #member 3 node3 - node4
                      [3,4], #member 4 node4 - node5
                      [5,0], #member 5 node6 - node1
                      [0,6], #member 6 node1 - node7
                      [6,1], #member 7 node7 - node2
                      [7,1], #member 8 node8 - node2
                      [1,8], #member 9 node2 - node9
                      [8,2], #member 10 node9 - node3
                      [9,2], #member 11 node10 - node3
                      [2,10], #member 12 node3 - node11
                      [10,3], #member 13 node11 - node4
                      [11,3], #member 14 node12 - node4
                      [3,12], #member 15 node4 - node13
                      [12,4], #member 16 node13 - node5
                      [13,4], #member 17 node14 - node5
                      [5,6], #member 18 node6 - node7
                      [6,7], #member 19 node7 - node8
                      [7,8], #member 20 node8 - node9
                      [8,9], #member 21 node9 - node10
                      [9,10], #member 22 node10 - node11
                      [10,11], #member 23 node11 - node12
                      [11,12], #member 24 node12 - node13
                      [12,13], #member 25 node13 - node14
                      [14,5], #member 26 node15 - node6
                      [14,6], #member 27 node15 - node7
                      [6,15], #member 28 node7 - node16
                      [15,7], #member 29 node16 - node8
                      [15,8], #member 30 node16 - node9
                      [8,16], #member 31 node9 - node17
                      [16,9], #member 32 node17 - node10
                      [16,10], #member 33 node17 - node11
                      [10,17], #member 34 node11 - node18
                      [17,11], #member 35 node18 - node12
                      [17,12], #member 36 node18 - node13
                      [12,18], #member 37 node13 - node19
                      [18,13], #member 38 node19 - node14
                      [14,15], #member 39 node15 - node16
                      [15,16], #member 40 node16 - node17
                      [16,17], #member 41 node17 - node18
                      [17,18], #member 42 node18 - node19
                      [19,14], #member 43 node20 - node15
                      [14,20], #member 44 node15 - node21
                      [20,15], #member 45 node21 - node16
                      [21,15], #member 46 node22 - node16
                      [15,22], #member 47 node16 - node23
                      [22,16], #member 48 node23 - node17
                      [23,16], #member 49 node24 - node17
                      [16,24], #member 50 node17 - node25
                      [24,17], #member 51 node25 - node18
                      [25,17], #member 52 node26 - node18
                      [17,26], #member 53 node18 - node27
                      [26,18], #member 54 node27 - node19
                      [27,18], #member 55 node28 - node19
                      [19,20], #member 56 node20 - node21
                      [20,21], #member 57 node21 - node22
                      [21,22], #member 58 node22 - node23
                      [22,23], #member 59 node23 - node24
                      [23,24], #member 60 node24 - node25
                      [24,25], #member 61 node25 - node26
                      [25,26], #member 62 node26 - node27
                      [26,27], #member 63 node27 - node28
                      [28,19], #member 64 node29 - node20
                      [28,20], #member 65 node29 - node21
                      [20,29], #member 66 node21 - node30
                      [29,21], #member 67 node30 - node22
                      [29,22], #member 68 node30 - node23
                      [22,30], #member 69 node23 - node31
                      [30,23], #member 70 node31 - node24
                      [30,24], #member 71 node31 - node25
                      [24,31], #member 72 node25 - node32
                      [31,25], #member 73 node32 - node26
                      [31,26], #member 74 node32 - node27
                      [26,32], #member 75 node27 - node33
                      [32,27], #member 76 node33 - node28
                      [28,29], #member 77 node29 - node30
                      [29,30], #member 78 node30 - node31
                      [30,31], #member 79 node31 - node32
                      [31,32], #member 80 node32 - node33
                      [33,28], #member 81 node34 - node29
                      [28,34], #member 82 node29 - node35
                      [34,29], #member 83 node35 - node30
                      [35,29], #member 84 node36 - node30
                      [29,36], #member 85 node30 - node37
                      [36,30], #member 86 node37 - node31
                      [37,30], #member 87 node38 - node31
                      [30,38], #member 88 node31 - node39
                      [38,31], #member 89 node39 - node32
                      [39,31], #member 90 node40 - node32
                      [31,40], #member 91 node32 - node41
                      [40,32], #member 92 node41 - node33
                      [41,32], #member 93 node42 - node33
                      [33,34], #member 94 node34 - node35
                      [34,35], #member 95 node35 - node36
                      [35,36], #member 96 node36 - node37
                      [36,37], #member 97 node37 - node38
                      [37,38], #member 98 node38 - node39
                      [38,39], #member 99 node39 - node40
                      [39,40], #member 100 node40 - node41
                      [40,41], #member 101 node41 - node42
                      [42,33], #member 102 node43 - node34
                      [42,34], #member 103 node43 - node35
                      [34,43], #member 104 node35 - node44
                      [43,35], #member 105 node44 - node36
                      [43,36], #member 106 node44 - node37
                      [36,44], #member 107 node37 - node45
                      [44,37], #member 108 node45 - node38
                      [44,38], #member 109 node45 - node39
                      [38,45], #member 110 node39 - node46
                      [45,39], #member 111 node46 - node40
                      [45,40], #member 112 node46 - node41
                      [40,46], #member 113 node41 - node47
                      [46,41], #member 114 node47 - node42
                      [42,43], #member 115 node43 - node44
                      [43,44], #member 116 node44 - node45
                      [44,45], #member 117 node45 - node46
                      [45,46], #member 118 node46 - node47
                      [47,42], #member 119 node48 - node43
                      [42,48], #member 120 node43 - node49
                      [48,43], #member 121 node49 - node44
                      [49,43], #member 122 node50 - node44
                      [43,50], #member 123 node44 - node51
                      [50,44], #member 124 node51 - node45
                      [51,44], #member 125 node52 - node45
                      [44,52], #member 126 node45 - node53
                      [52,45], #member 127 node53 - node46
                      [53,45], #member 128 node54 - node46
                      [45,54], #member 129 node46 - node55
                      [54,46], #member 130 node55 - node47
                      [55,46], #member 131 node56 - node47
                      [47,48], #member 132 node48 - node49
                      [48,49], #member 133 node49 - node50
                      [49,50], #member 134 node50 - node51
                      [50,51], #member 135 node51 - node52
                      [51,52], #member 136 node52 - node53
                      [52,53], #member 137 node53 - node54
                      [53,54], #member 138 node54 - node55
                      [54,55], #member 139 node55 - node56
                      [56,47], #member 140 node57 - node48
                      [56,48], #member 141 node57 - node49
                      [48,57], #member 142 node49 - node58
                      [57,49], #member 143 node58 - node50
                      [57,50], #member 144 node58 - node51
                      [50,58], #member 145 node51 - node59
                      [58,51], #member 146 node59 - node52
                      [58,52], #member 147 node59 - node53
                      [52,59], #member 148 node53 - node60
                      [59,53], #member 149 node60 - node54
                      [59,54], #member 150 node60 - node55
                      [54,60], #member 151 node55 - node61
                      [60,55], #member 152 node61 - node56
                      [56,57], #member 153 node57 - node58
                      [57,58], #member 154 node58 - node59
                      [58,59], #member 155 node59 - node60
                      [59,60], #member 156 node60 - node61
                      [61,56], #member 157 node62 - node57
                      [56,62], #member 158 node57 - node63
                      [62,57], #member 159 node63 - node58
                      [63,57], #member 160 node64 - node58
                      [57,64], #member 161 node58 - node65
                      [64,58], #member 162 node65 - node59
                      [65,58], #member 163 node66 - node59
                      [58,66], #member 164 node59 - node67
                      [66,59], #member 165 node67 - node60
                      [67,59], #member 166 node68 - node60
                      [59,68], #member 167 node60 - node69
                      [68,60], #member 168 node69 - node61
                      [69,60], #member 169 node70 - node61
                      [61,62], #member 170 node62 - node63
                      [62,63], #member 171 node63 - node64
                      [63,64], #member 172 node64 - node65
                      [64,65], #member 173 node65 - node66
                      [65,66], #member 174 node66 - node67
                      [66,67], #member 175 node67 - node68
                      [67,68], #member 176 node68 - node69
                      [68,69], #member 177 node69 - node70
                      [70,61], #member 178 node71 - node62
                      [70,62], #member 179 node71 - node63
                      [62,71], #member 180 node63 - node72
                      [71,63], #member 181 node72 - node64
                      [71,64], #member 182 node72 - node65
                      [64,72], #member 183 node65 - node73
                      [72,65], #member 184 node73 - node66
                      [72,66], #member 185 node73 - node67
                      [66,73], #member 186 node67 - node74
                      [73,67], #member 187 node74 - node68
                      [73,68], #member 188 node74 - node69
                      [68,74], #member 189 node69 - node75
                      [74,69], #member 190 node75 - node70
                      [70,71], #member 191 node71 - node72
                      [71,72], #member 192 node72 - node73
                      [72,73], #member 193 node73 - node74
                      [73,74], #member 194 node74 - node75
                      [70,75], #member 195 node71 - node76
                      [75,71], #member 196 node76 - node72
                      [75,72], #member 197 node76 - node73
                      [72,76], #member 198 node73 - node77
                      [76,73], #member 199 node77 - node74
                      [76,74]]) #member 200 node77 - node75

numElem = elemNodes.shape[0]
numNodes = nodeCords.shape[0]
tdof = 2*numNodes
xx = nodeCords[:,0]
yy = nodeCords[:,1]

L = np.zeros((numElem,)) #lengths of members
c = np.zeros((numElem,))
s = np.zeros((numElem,))
for e in range(numElem):
    indice = elemNodes[e,:]
    elemDof = np.array([indice[0]*2, indice[0]*2+1, indice[1]*2, indice[1]*2+1 ])
    xa = xx[indice[1]]-xx[indice[0]]
    ya = yy[indice[1]]-yy[indice[0]]
    L[e] = np.sqrt(xa*xa+ya*ya)
    c[e] = xa/L[e]
    s[e] = ya/L[e]

#load case 1
LC1 = np.zeros((tdof,1))
LC1[0] = 1
LC1[10] = 1
LC1[28] = 1
LC1[38] = 1
LC1[56] = 1
LC1[66] = 1
LC1[84] = 1
LC1[94] = 1
LC1[112] = 1
LC1[122] = 1
LC1[140] = 1

#load case 2
LC2 = np.zeros((tdof,1))
LC2[1] = -10
LC2[3] = -10
LC2[5] = -10
LC2[7] = -10
LC2[9] = -10
LC2[11] = -10
LC2[15] = -10
LC2[19] = -10
LC2[23] = -10
LC2[27] = -10
LC2[29] = -10
LC2[31] = -10
LC2[33] = -10
LC2[35] = -10
LC2[37] = -10
LC2[39] = -10
LC2[43] = -10
LC2[47] = -10
LC2[51] = -10
LC2[55] = -10
LC2[57] = -10
LC2[59] = -10
LC2[61] = -10
LC2[63] = -10
LC2[65] = -10
LC2[67] = -10
LC2[71] = -10
LC2[75] = -10
LC2[79] = -10
LC2[83] = -10
LC2[85] = -10
LC2[87] = -10
LC2[89] = -10
LC2[91] = -10
LC2[93] = -10
LC2[95] = -10
LC2[99] = -10
LC2[103] = -10
LC2[107] = -10
LC2[111] = -10
LC2[113] = -10
LC2[115] = -10
LC2[117] = -10
LC2[119] = -10
LC2[121] = -10
LC2[123] = -10
LC2[127] = -10
LC2[131] = -10
LC2[135] = -10
LC2[139] = -10
LC2[141] = -10
LC2[143] = -10
LC2[145] = -10
LC2[147] = -10
LC2[149] = -10

presDof=np.array([150,151,152,153])
actDof=np.setdiff1d(np.arange(tdof),presDof)
    
def StructAnalysis(x):
    Area = assignA(x)
    stiffness=np.zeros((tdof,tdof))
    for e in range(numElem):
        indice = elemNodes[e,:]
        elemDof = np.array([indice[0]*2, indice[0]*2+1, indice[1]*2, indice[1]*2+1 ])
        EA = modE*Area[e]
        k1=(EA/L[e])* np.array([[ c[e]*c[e], c[e]*s[e],-c[e]*c[e],-c[e]*s[e]],
                                [ c[e]*s[e], s[e]*s[e],-c[e]*s[e],-s[e]*s[e]],
                                [-c[e]*c[e],-c[e]*s[e], c[e]*c[e], c[e]*s[e]],
                                [-c[e]*s[e],-s[e]*s[e], c[e]*s[e], s[e]*s[e]]])
        stiffness[np.ix_(elemDof,elemDof)] +=k1
    
    U1=np.zeros((tdof,1))
    S1=np.zeros((numElem,1))      
    disp1=np.linalg.solve(stiffness[np.ix_(actDof,actDof)],LC1[np.ix_(actDof)]);
    U1[np.ix_(actDof)]=disp1
    for e in range(numElem):
        indice= elemNodes[e,:]
        elemDof=np.array([indice[0]*2, indice[0]*2+1, indice[1]*2, indice[1]*2+1 ])
        S1[e] = (modE/L[e]) * np.dot(np.array([-c[e],-s[e],c[e],s[e]]),U1[np.ix_(elemDof)])
    
    U2=np.zeros((tdof,1))
    S2=np.zeros((numElem,1))
    disp2=np.linalg.solve(stiffness[np.ix_(actDof,actDof)],LC2[np.ix_(actDof)]);
    U2[np.ix_(actDof)]=disp2
    for e in range(numElem):
        indice= elemNodes[e,:]
        elemDof=np.array([indice[0]*2, indice[0]*2+1, indice[1]*2, indice[1]*2+1 ])
        S2[e] = (modE/L[e]) * np.dot(np.array([-c[e],-s[e],c[e],s[e]]),U2[np.ix_(elemDof)])

    U3 = U1 + U2
    S3 = S1 + S2
    
    w = weight(x)
    A = np.array(Area)
    dis = np.maximum.reduce(np.abs([U1,U2,U3]))
    sc = np.maximum.reduce(np.abs([S1,S2,S3]))
            
    return A, w, dis, sc

#define weight function
def weight(x):
    A = assignA(x)
    return np.dot(A,L)*rho
    
# TEST
# x=[i+1 for i in range(29)];
# A, w, dis, sc = StructAnalysis(x)
# print(np.max(dis))
# print(np.max(sc))




