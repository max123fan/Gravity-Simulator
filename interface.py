import pygame
from settings import *
from utils import *

class Interface:
    def __init__(self, screen):
        self.paused_font = pygame.font.Font("ShareTech-Regular.ttf", 32)
        self.fps_font = pygame.font.Font("ShareTech-Regular.ttf", 20)
        self.screen = screen

    def draw_pause(self):
        text = self.paused_font.render("Paused", True, (255, 255, 255))
        self.screen.blit(text, (10, 30))
    
    def draw_background(self, BG_COLOR):
        self.screen.fill(BG_COLOR)

    def draw_fps_counter(self, fps):
        text = self.fps_font.render("FPS: %s" % fps, True, (255, 255, 255))
        self.screen.blit(text, (10, 10))

