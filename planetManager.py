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
                planet1.radius + planet2.radius, 
                v_rel)
        
            for planet1, planet2 in bounce_actions:
                # Create bounce VFX at collision point
                normal_angle = calculate_normal_angle(planet1, planet2)
                v_rel = calculate_v_rel(planet1, planet2)

                self.collision_fx_manager.add_bounce_effect(
                (planet1.x + planet2.x) / 2, 
                (planet1.y + planet2.y) / 2, 
                planet1.radius + planet2.radius,
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

    def clear_collision_fx(self):
        self.collision_fx_manager.clear_effects()

    def get_collision_pairs(self):
        pairs = []
        for i in range(len(self.planets)):
            for j in range(i+1, len(self.planets)):
                p1 = self.planets[i]
                p2 = self.planets[j]
                distance = calculate_distance(p1.x, p1.y, p2.x, p2.y)
                if distance < p1.radius + p2.radius:
                    pairs.append((p1, p2, distance))
        return pairs

    def remove_planet(self, planet):
        """Safe removal with trail cleanup"""
        if planet in self.planets:
            self.planets.remove(planet)
            self.trail_manager.stop_tracking_planet(planet)

    def set_selected_planet(self, selected_planet):
        for planet in self.planets:
            planet.is_selected = False
        if selected_planet == None:
            return
        selected_planet.is_selected = True

    def check_mouse_on_planet(self, screen_mouse_coords):
        cartesian_mouse_coords = screen_coords_to_cartesian(*screen_mouse_coords)
        for planet in self.planets:
            if calculate_distance(*cartesian_mouse_coords, planet.x, planet.y) < planet.radius:
                return planet
            
    

