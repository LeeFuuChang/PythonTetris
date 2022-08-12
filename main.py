from modules import *
import pygame
import random
import os

pygame.init()







window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
g = Game([Player()])
g.window = window
while(True):
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            break


    window.fill((0, 0, 0))


    keys = pygame.key.get_pressed()
    g.players[0].l_pressed = keys[pygame.K_LEFT]
    g.players[0].r_pressed = keys[pygame.K_RIGHT]
    g.players[0].l_rot_pressed = keys[pygame.K_z]
    g.players[0].r_rot_pressed = keys[pygame.K_x]
    g.players[0].fast_pressed = keys[pygame.K_SPACE]
    g.players[0].instant_pressed = keys[pygame.K_SPACE]
    g.players[0].holding_pressed = keys[pygame.K_LSHIFT]


    g.Update()


    pygame.display.update()
    clock.tick(FPS)