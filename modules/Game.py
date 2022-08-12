from .Constants import *
from .Player import *
from .Blocks import *
import pygame
import random



class Game:
    def __init__(self, players):
        self.drop_timer = 0
        self.players = players
        self.piece_order = []


    def Draw_player_board(self, p):
        for i in range(self.players[p].board_height):
            for j in range(self.players[p].board_width):
                if self.players[p].board[i][j]:
                    colors = [
                        self.players[p].board[i][j].color_2,
                        self.players[p].board[i][j].color_1,
                        self.players[p].board[i][j].color_2,
                        self.players[p].board[i][j].color_1,
                    ]
                    for k in range(len(BLOCK_SIZE_LAYERS)):
                        pygame.draw.rect(
                            self.window, 
                            colors[k%len(colors)], 
                            pygame.Rect( 
                                BLOCK_SIZE*j + (BLOCK_SIZE*(self.players[p].board_width+1))*p + BLOCK_SIZE_LAYERS[k][1], 
                                BLOCK_SIZE*i + BLOCK_SIZE_LAYERS[k][1], 
                                BLOCK_SIZE_LAYERS[k][0], 
                                BLOCK_SIZE_LAYERS[k][0] 
                            )
                        )
        
        if self.players[p].current_piece:
            for i in range(self.players[p].current_piece.rotation_size):
                for j in range(self.players[p].current_piece.rotation_size):
                    if self.players[p].current_piece.vector[i][j]:
                        colors = [
                            self.players[p].current_piece.color_2,
                            self.players[p].current_piece.color_1,
                            self.players[p].current_piece.color_2,
                            self.players[p].current_piece.color_1,
                        ]
                        for k in range(len(BLOCK_SIZE_LAYERS)):
                            pygame.draw.rect(
                                self.window, 
                                colors[k%len(colors)], 
                                pygame.Rect( 
                                    BLOCK_SIZE*(j+self.players[p].current_piece.c) + (BLOCK_SIZE*(self.players[p].board_width+1))*p + BLOCK_SIZE_LAYERS[k][1], 
                                    BLOCK_SIZE*(i+self.players[p].current_piece.r) + BLOCK_SIZE_LAYERS[k][1], 
                                    BLOCK_SIZE_LAYERS[k][0], 
                                    BLOCK_SIZE_LAYERS[k][0] 
                                )
                            )


    def Get_next_piece(self, idx):
        if idx >= len(self.piece_order):
            for i in range(idx - len(self.piece_order) + 1):
                self.piece_order.append(random.choice(PIECES))
            return self.piece_order[idx]
        else:
            return self.piece_order[idx]


    def Update_players(self):
        for p in range(len(self.players)):
            if not self.players[p].current_piece:
                self.players[p].Next_piece(self.Get_next_piece(self.players[p].placed_count)())
            self.players[p].Update()
            self.Draw_player_board(p)


    def Update(self):
        self.Update_players()