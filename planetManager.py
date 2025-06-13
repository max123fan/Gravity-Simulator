import pygame
import math
from utils import *
from physics import Physics
from trailManager import TrailManager
from settings import *
from collisionFXManager import CollisionFXManager


class PlanetManager:
    def __init__(self, screen, planets):
        self.planets = planets
        self.screen = screen
        self.trail_manager = TrailManager(self.screen)
        self.collision_fx_manager = CollisionFXManager(self.screen)
        self.physics = Physics()
        

    def update(self):
        """Basic physics and trail update"""
        merge_actions, bounce_actions = self.physics.update(self)
        # collision_actions = (merge_actions, bounce_actions)
        # sample output:([], [(<planet.Planet object at 0x0000020E81BCA1D0>, <planet.Planet object at 0x0000020E81BCA380>)])

        if settings.collision_fx:
            for planet1, planet2 in merge_actions:
            # Create merge VFX at midpoint
                v_rel = calculate_v_rel(planet1, planet2)
                self.collision_fx_manager.add_merge_effect(
                (planet1.x + planet2.x) / 2,
                (planet1.y + planet2.y) / 2,
                int(planet1.radius + planet2.radius), 
                v_rel)
        
            for planet1, planet2 in bounce_actions:
                # Create bounce VFX at collision point
                normal_angle = calculate_normal_angle(planet1, planet2)
                v_rel = calculate_v_rel(planet1, planet2)

                self.collision_fx_manager.add_bounce_effect(
                (planet1.x + planet2.x) / 2, 
                (planet1.y + planet2.y) / 2, 
                int(planet1.radius + planet2.radius),
                v_rel, 
                normal_angle)

            
            self.collision_fx_manager.update()
        
        if settings.trails:
            self.trail_manager.update_trails(self)
       

    def draw_planets(self):
        for planet in self.planets:
            planet.draw(self.screen)

    def draw_collision_fx(self):
        self.collision_fx_manager.draw()

    def draw_trails(self):
        """Draw everything in correct order"""
        self.trail_manager.draw_trails()

    def clear_trails(self):
        self.trail_manager.clear_trails()

    def get_collision_pairs(self):
        """Brute-force collision checking (simple but works)"""
        pairs = []
        for i in range(len(self.planets)):
            for j in range(i+1, len(self.planets)):
                p1 = self.planets[i]
                p2 = self.planets[j]
                distance = calculate_distance(p1, p2)
                if distance < p1.radius + p2.radius:
                    pairs.append((p1, p2, distance))
        return pairs

    def remove_planet(self, planet):
        """Safe removal with trail cleanup"""
        if planet in self.planets:
            self.planets.remove(planet)
            self.trail_manager.stop_tracking_planet(planet)
