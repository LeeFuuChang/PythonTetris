from .Constants import *
from .Board import Board, BoardState
from .Blocks import *

class Player:
    def __init__(self):
        self.board, self.board_width, self.board_height = Board()

        self.placed_count = 0

        self.current_piece = None

        self.drop_timer = 0

        self.holding_pressed = False
        self.holding_available = True
        self.holding_piece = None

        self.locking = False
        self.lock_timer = True

        self.move_timer = 0
        self.l_held = False
        self.r_held = False
        self.l_pressed = False
        self.r_pressed = False
        self.instant_pressed = False
        self.instant_available = True

        self.rot_timer = 0
        self.l_rot_held = False
        self.r_rot_held = False
        self.l_rot_pressed = False
        self.r_rot_pressed = False





    def Check_collision(self, p, r, c, rr, rc):
        bs = BoardState.Save_from_board(self.board)
        if rc < 0 or rc+p.realw > bs.w: 
            return 1
        if rr < 0 or rr+p.realh > bs.h: 
            return 2
        for i in range(rr, rr+p.realh):
            for j in range(rc, rc+p.realw):
                if bs.binary[i][j] + p.vector[i-r][j-c] >= 2:
                    return 3
        return 0





    def Clear_row(self, r):
        self.board.pop(r)
        self.board.insert(0, [0]*self.board_width)





    def Next_piece(self, next_piece):
        self.holding_available = True
        self.current_piece = next_piece
        self.current_piece.init()


    def Lock_piece(self):
        if not self.current_piece: return
        for i in range(self.current_piece.rotation_size):
            for j in range(self.current_piece.rotation_size):
                if self.current_piece.vector[i][j]:
                    self.board[self.current_piece.r+i][self.current_piece.c+j] = self.current_piece
        self.current_piece = None
        self.placed_count += 1


    def Update_lock(self):
        if not self.current_piece: return
        if self.Check_collision(self.current_piece, self.current_piece.r+1, self.current_piece.c, self.current_piece.realr+1, self.current_piece.realc):
            self.locking = True
        else:
            self.locking = False

        if self.locking:
            self.lock_timer += 1
            if self.lock_timer/FPS >= BLOCK_LOCK_DELAY_TIME_SEC:
                self.locking = False
                self.lock_timer = 0
                self.Lock_piece()


    def Update_clear(self):
        bs = BoardState.Save_from_board(self.board)
        clearing = []
        for i in range(self.board_height):
            if bs.row_spaces[i]: continue
            clearing.append(i)
        for target in clearing:
            self.board.pop(target)
            self.board.insert(0, [0]*self.board_width)


    def Update_hold(self):
        if not self.current_piece: return
        if not self.holding_pressed and not self.holding_available:
            self.holding_available = True
        if self.holding_pressed and self.holding_available:
            if self.holding_piece:
                self.current_piece, self.holding_piece = self.holding_piece, self.current_piece
                self.current_piece.init()
                self.holding_available = False
            else:
                self.holding_piece = self.current_piece
                self.current_piece = None
                self.holding_available = False


    def Update_rotate(self):
        if not self.current_piece: return
        if not (self.l_rot_pressed or self.r_rot_pressed):
            self.rot_timer = 0
            self.l_rot_held = False
            self.r_rot_held = False
            return

        if (self.l_rot_pressed and not self.l_rot_held) or (self.r_rot_pressed and not self.r_rot_held):
            if self.l_rot_pressed:
                self.current_piece.Lrot()
                if self.Check_collision(self.current_piece, self.current_piece.r, self.current_piece.c, self.current_piece.realr, self.current_piece.realc):
                    self.current_piece.Rrot()
                self.l_rot_held = True
            if self.r_rot_pressed:
                self.current_piece.Rrot()
                if self.Check_collision(self.current_piece, self.current_piece.r, self.current_piece.c, self.current_piece.realr, self.current_piece.realc):
                    self.current_piece.Lrot()
                self.r_rot_held = True

        if self.l_rot_held or self.r_rot_held:
            self.rot_timer += 1

        if self.rot_timer/FPS >= PIXEL_ROT_HELD_TIME_SEC:
            self.rot_timer = 0
            if self.l_rot_held:
                self.current_piece.Lrot()
                while(True):
                    collision = self.Check_collision(self.current_piece, self.current_piece.r, self.current_piece.c, self.current_piece.realr, self.current_piece.realc)
                    if collision == 1:
                        if self.current_piece.realc < 0:
                            self.current_piece.c = -self.current_piece.rc_offset
                        else:
                            self.current_piece.c = self.board_width-self.current_piece.realw-self.current_piece.rc_offset
                    elif collision == 2:
                        if self.current_piece.realr < 0:
                            self.current_piece.r = -self.current_piece.rr_offset
                        else:
                            self.current_piece.r = self.board_height-self.current_piece.realh-self.current_piece.rr_offset
                    elif collision == 3:
                        self.current_piece.Move_up()
                    else:
                        break
            if self.r_rot_held:
                self.current_piece.Rrot()
                while(True):
                    collision = self.Check_collision(self.current_piece, self.current_piece.r, self.current_piece.c, self.current_piece.realr, self.current_piece.realc)
                    if collision == 1:
                        if self.current_piece.realc < 0:
                            self.current_piece.c = -self.current_piece.rc_offset
                        else:
                            self.current_piece.c = self.board_width-self.current_piece.realw-self.current_piece.rc_offset
                    elif collision == 2:
                        if self.current_piece.realr < 0:
                            self.current_piece.r = -self.current_piece.rr_offset
                        else:
                            self.current_piece.r = self.board_height-self.current_piece.realh-self.current_piece.rr_offset
                    elif collision == 3:
                        self.current_piece.Move_up()
                    else:
                        break


    def Update_instant(self):
        if not self.current_piece: return
        if not self.instant_pressed and not self.instant_available:
            self.instant_available = True
        if self.instant_pressed and self.instant_available:
            self.instant_available = False
            while(True):
                current_pos = not self.Check_collision(self.current_piece, self.current_piece.r, self.current_piece.c, self.current_piece.realr, self.current_piece.realc)
                next_pos = not self.Check_collision(self.current_piece, self.current_piece.r+1, self.current_piece.c, self.current_piece.realr+1, self.current_piece.realc)
                if current_pos and next_pos:
                    self.current_piece.Move_down()
                else:
                    break
            self.Lock_piece()


    def Update_move(self):
        if not self.current_piece: return
        if not (self.l_pressed or self.r_pressed):
            self.move_timer = 0
            self.l_held = False
            self.r_held = False
            return

        if (self.l_pressed and not self.l_held) or (self.r_pressed and not self.r_held):
            if self.l_pressed:
                if not self.Check_collision(self.current_piece, self.current_piece.r, self.current_piece.c-1, self.current_piece.realr, self.current_piece.realc-1):
                    self.current_piece.Move_left()
                self.l_held = True  
            if self.r_pressed:
                if not self.Check_collision(self.current_piece, self.current_piece.r, self.current_piece.c+1, self.current_piece.realr, self.current_piece.realc+1):
                    self.current_piece.Move_right()
                self.r_held = True

        if self.l_held or self.r_held:
            self.move_timer += 1

        if self.move_timer/FPS >= PIXEL_MOVE_HELD_TIME_SEC:
            self.move_timer = 0
            if self.l_held:
                if not self.Check_collision(self.current_piece, self.current_piece.r, self.current_piece.c-1, self.current_piece.realr, self.current_piece.realc-1):
                    self.current_piece.Move_left()
            if self.r_held:
                if not self.Check_collision(self.current_piece, self.current_piece.r, self.current_piece.c+1, self.current_piece.realr, self.current_piece.realc+1):
                    self.current_piece.Move_right()


    def Update_current(self):
        if not self.current_piece: return
        self.drop_timer += 1
        if self.drop_timer/FPS >= BLOCK_DROP_PIXEL_TIME_SEC:
            if not self.locking: 
                self.current_piece.Move_down()
            self.drop_timer = 0


    def Update(self):
        self.Update_current()
        self.Update_hold()
        self.Update_move()
        self.Update_rotate()
        self.Update_instant()
        self.Update_lock()
        self.Update_clear()