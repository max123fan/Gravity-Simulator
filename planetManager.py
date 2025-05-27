import pygame
from physics import Physics
from settings import *

class PlanetManager:
    def __init__(self, planets):
        self.planets = planets
        self.physics = Physics()

    def update_all_physics(self):
        self.physics.update_all(self)
    
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

    def remove_planet(self, planet):
        if planet in self.planets:
            self.planets.remove(planet)

    def get_collision_pairs(self):
        colliding_pairs = []
        for i in range(len(self.planets)):
            for j in range(i+1, len(self.planets)):
                planet1 = self.planets[i]
                planet2 = self.planets[j]
                if planet1.radius + planet2.radius > ((planet1.x - planet2.x)**2 + (planet1.y-planet2.y)**2)**0.5:
                    colliding_pairs.append((planet1, planet2))
        return colliding_pairs
    
    def merge_colors(self, planet1, planet2):
        mass_merged = planet1.mass + planet2.mass
        color_merged = (
            int((planet1.mass * planet1.color[0] + planet2.mass * planet2.color[0]) / mass_merged),
            int((planet1.mass * planet1.color[1] + planet2.mass * planet2.color[1]) / mass_merged),
            int((planet1.mass * planet1.color[2] + planet2.mass * planet2.color[2]) / mass_merged)
        )
        return color_merged
                
