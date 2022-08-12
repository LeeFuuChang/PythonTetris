from .Constants import *



class Block:
    color = None
    rotation_size = 0
    vector = [[]]
    mass = []
    def __init__(self):
        self.r = 0
        self.c = (DEFAULT_BOARD_SIZE[0]//2) - round(self.rotation_size/2)
        self.realr = 0
        self.rr_offset = 0
        self.realc = 0
        self.rc_offset = 0
        self.realw = 0
        self.realh = 0
        self.init()

    def init(self):
        self.Update()
        self.r = -self.rr_offset
        self.c = (DEFAULT_BOARD_SIZE[0]//2) - round(self.rotation_size/2)
        self.realr = self.r + self.rr_offset
        self.realc = self.c + self.rc_offset

    def Move_to_r(self, r):
        self.r = r
        self.Update()

    def Move_to_c(self, c):
        self.c = c
        self.Update()

    def Move_up(self):
        self.r -= 1
        self.Update()

    def Move_down(self):
        self.r += 1
        self.Update()

    def Move_left(self):
        self.c -= 1
        self.Update()

    def Move_right(self):
        self.c += 1
        self.Update()

    def Update(self):
        self.mass = [0]*self.rotation_size
        rr_offset = 0
        rr_offset_flag = True
        rc_offset = 0
        rc_offset_flag = True
        for i in range(self.rotation_size):
            for j in range(self.rotation_size):
                if self.vector[j][i]: self.mass[i] += 1
            if all([ n==0 for n in self.vector[i] ]):
                if rr_offset_flag:
                    rr_offset += 1
            else:
                rr_offset_flag = False
            if all([ n==0 for n in [ r[i] for r in self.vector ] ]):
                if rc_offset_flag:
                    rc_offset += 1
            else:
                rc_offset_flag = False
        self.rr_offset = rr_offset
        self.rc_offset = rc_offset
        self.realr = self.r + self.rr_offset
        self.realc = self.c + self.rc_offset
        self.realw = self.rotation_size - self.mass.count(0)
        self.realh = max(self.mass)

    def Lrot(self):
        new = []
        for i in range(self.rotation_size):
            new.append([])
            for j in range(self.rotation_size):
                new[-1].append(self.vector[ j ][self.rotation_size-i-1])
        self.vector = new
        self.Update()

    def Rrot(self):
        new = []
        for i in range(self.rotation_size):
            new.append([])
            for j in range(self.rotation_size):
                new[-1].append(self.vector[ self.rotation_size-j-1 ][i])
        self.vector = new
        self.Update()





"""
Ｏ
Ｏ
Ｏ
Ｏ
"""
class I_a(Block):
    color_1 = I_a_COLOR_1
    color_2 = I_a_COLOR_2
    vector = [
        [ 0 , 1 , 0 , 0],
        [ 0 , 1 , 0 , 0],
        [ 0 , 1 , 0 , 0],
        [ 0 , 1 , 0 , 0],
    ]
    rotation_size = 4
    def __init__(self):
        super().__init__()





"""
Ｏ
Ｏ
ＯＯ
"""
class L_a(Block):
    color_1 = L_a_COLOR_1
    color_2 = L_a_COLOR_2
    vector = [
        [ 0 , 1 , 0 ],
        [ 0 , 1 , 0 ],
        [ 0 , 1 , 1 ],
    ]
    rotation_size = 3
    def __init__(self):
        super().__init__()

"""
  Ｏ
  Ｏ
ＯＯ
"""
class L_b(Block):
    color_1 = L_b_COLOR_1
    color_2 = L_b_COLOR_2
    vector = [
        [ 0 , 1 , 0 ],
        [ 0 , 1 , 0 ],
        [ 1 , 1 , 0 ],
    ]
    rotation_size = 3
    def __init__(self):
        super().__init__()





"""
ＯＯ
ＯＯ
"""
class O_a(Block):
    color_1 = O_a_COLOR_1
    color_2 = O_a_COLOR_2
    vector = [
        [ 0 , 0 , 0 , 0 ],
        [ 0 , 1 , 1 , 0 ],
        [ 0 , 1 , 1 , 0 ],
        [ 0 , 0 , 0 , 0 ]
    ]
    rotation_size = 4
    def __init__(self):
        super().__init__()





"""
  Ｏ
ＯＯＯ
"""
class T_a(Block):
    color_1 = T_a_COLOR_1
    color_2 = T_a_COLOR_2
    vector = [
        [ 0 , 0 , 0 ],
        [ 0 , 1 , 0 ],
        [ 1 , 1 , 1 ],
    ]
    rotation_size = 3
    def __init__(self):
        super().__init__()





"""
  ＯＯ
ＯＯ
"""
class Z_a(Block):
    color_1 = Z_a_COLOR_1
    color_2 = Z_a_COLOR_2
    vector = [
        [ 0 , 0 , 0 ],
        [ 1 , 1 , 0 ],
        [ 0 , 1 , 1 ],
    ]
    rotation_size = 3
    def __init__(self):
        super().__init__()

"""
ＯＯ
  ＯＯ
"""
class Z_b(Block):
    color_1 = Z_b_COLOR_1
    color_2 = Z_b_COLOR_2
    vector = [
        [ 0 , 0 , 0 ],
        [ 0 , 1 , 1 ],
        [ 1 , 1 , 0 ],
    ]
    rotation_size = 3
    def __init__(self):
        super().__init__()








PIECES = [
    I_a,
    L_a, L_b,
    O_a,
    T_a,
    Z_a, Z_b,
]