import pygame 
import math
import sys

pygame.init()

screen = pygame.display.set_mode((800,600))
pygame.display.set_caption('Projectile Motion')
font = pygame.font.SysFont(None, 24)

clock = pygame.time.clock()
fps = 60

gravity = 9.8
projectiles = []

def draw_text(text, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))
    