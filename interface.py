import pygame
from settings import *


class Interface:
    def __init__(self, screen):
        self.font = pygame.font.Font("ShareTech-Regular.ttf", 32)
        self.screen = screen

    def draw_pause(self):
        text = self.font.render("Paused", True, (255, 255, 255))
        self.screen.blit(text, (20, 20))
    
    def draw_background(self, BG_COLOR):
        self.screen.fill(BG_COLOR)

