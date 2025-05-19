import pygame
from physics import Physics
from settings import *

class PlanetManager:
    def __init__(self, planets):
        self.planets = planets
        self.physics = Physics()

    def update_all_physics(self):
        self.physics.update_all(self.planets)
    
    def draw_all_planets(self, screen):
        for planet in self.planets:
            planet.draw(screen)
    
    def draw_all_trails(self, screen):
        for planet in self.planets:
            planet.draw_trail(screen)

    def update_all_trails(self):
        for planet in self.planets:
            planet.update_trail()

    def clear_all_trails(self):
        for planet in self.planets:
            planet.clear_trail()
