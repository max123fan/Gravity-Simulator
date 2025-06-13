import pygame
from settings import *
from utils import *
from collisionFX import *

class CollisionFXManager:
    def __init__(self, screen):
        self.screen = screen
        self.effects = []
        
    def add_merge_effect(self, x, y, combined_radius, v_rel):
        """Create a planetary merge explosion"""
        self.effects.append(MergeEffect(self.screen, x, y, combined_radius, v_rel))
    
    def add_bounce_effect(self, x, y, combined_radius, v_rel, normal_angle):
        """Create a collision spark"""
        self.effects.append(BounceEffect(self.screen, x, y, combined_radius, v_rel, normal_angle))
    
    def update(self):
        """Update all active effects"""
        for effect in self.effects[:]:
            effect.update()
            if effect.is_complete():
                self.effects.remove(effect)
    
    def draw(self):
        """Draw all active effects"""
        for effect in self.effects:
            effect.draw()
