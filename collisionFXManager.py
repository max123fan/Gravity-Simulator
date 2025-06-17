import pygame
from settings import *
from utils import *
from collisionFX import *

class CollisionFXManager:
    def __init__(self, screen):
        self.screen = screen
        self.effects = []
        
    def add_merge_effect(self, x, y, combined_radius, v_rel):
        self.effects.append(MergeEffect(self.screen, x, y, combined_radius, v_rel))
    
    def add_bounce_effect(self, x, y, combined_radius, v_rel, normal_angle):
        self.effects.append(BounceEffect(self.screen, x, y, combined_radius, v_rel, normal_angle))
    
    def update(self):
        for effect in self.effects[:]:
            effect.update()
            if effect.is_complete():
                self.effects.remove(effect)
    
    def draw(self):
        for effect in self.effects:
            effect.draw()
    
    def clear_effects(self):
        self.effects = []
