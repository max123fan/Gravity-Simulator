import pygame
from settings import *
from events import *
from utils import *


import math
import random

class Physics:
    def __init__(self):
        self.locked_pairs = {}
        self.frame = 0

    def calculate_gravity(self, planet1, planet2):
        dx = planet2.x - planet1.x
        dy = planet2.y - planet1.y

        distance_squared = dx**2 + dy**2 + settings.EPSILON**2
        distance = math.sqrt(distance_squared)
        
        force = settings.g * planet1.mass * planet2.mass / distance_squared

        fx = force * dx / distance
        fy = force * dy / distance

        return fx, fy

    def check_merge(self, planet1, planet2, distance, v_rel):
        total_mass = planet1.mass + planet2.mass
        total_radius = planet1.radius + planet2.radius
        v_escape = math.sqrt(2 * settings.g * total_mass / total_radius)

        dx = planet2.x - planet1.x
        dy = planet2.y - planet1.y
        cos_theta = (dx * (planet2.vx - planet1.vx) + dy * (planet2.vy - planet1.vy)) / (distance * max(v_rel, settings.EPSILON))
        sin_theta = math.sqrt(max(1 - cos_theta**2, 0))
        b = (distance * sin_theta) / total_radius
        b = min(max(b, 0), 1)

        mass_ratio = max(planet1.mass, planet2.mass) / min(planet1.mass, planet2.mass)
        mass_merge_boost = 1 + 0.4 * math.log(mass_ratio + 1)

        v_merge = 1.3 * v_escape * (1 - b**2) * mass_merge_boost

        if settings.RANDOMNESS_IN_COLLISIONS and abs(v_rel - v_merge) / v_merge < 0.1:
            return random.random() < (1 - b)

        if mass_ratio >= 5:
            return True

        return v_rel < v_merge
    
    def handle_merge(self, planet1, planet2, planet_manager):
        mass_merged = planet1.mass + planet2.mass
        radius_merged = (planet1.radius**2 + planet2.radius**2)**0.5
        x_merged = (planet1.mass * planet1.x + planet2.mass * planet2.x) / mass_merged
        y_merged = (planet1.mass * planet1.y + planet2.mass * planet2.y) / mass_merged
        vx_merged = (planet1.mass * planet1.vx + planet2.mass * planet2.vx) / mass_merged * settings.MERGE_ENERGY_LOSS
        vy_merged = (planet1.mass * planet1.vy + planet2.mass * planet2.vy) / mass_merged * settings.MERGE_ENERGY_LOSS
        
        planet1.mass = mass_merged
        planet1.radius = radius_merged
        planet1.x, planet1.y = x_merged, y_merged
        planet1.vx, planet1.vy = vx_merged, vy_merged
        planet1.prev_x = x_merged - vx_merged * settings.dt
        planet1.prev_y = y_merged - vy_merged * settings.dt
        planet1.ax, planet1.ay, planet1.ax_old, planet1.ay_old = 0, 0, 0, 0

        planet1.color = color_interpolate(planet1.color, planet2.color, planet2.mass / mass_merged)
        planet1.update_trail_size()

        planet_manager.remove_planet(planet2)


    
    def handle_bounce(self, planet1, planet2):
        distance = calculate_distance(planet1.x, planet1.y, planet2.x, planet2.y)
        nx, ny = (planet2.x - planet1.x)/distance, (planet2.y - planet1.y)/distance
        dv_parallel = (planet2.vx - planet1.vx) * nx + (planet2.vy - planet1.vy) * ny

        if dv_parallel >= 0:
            return
            
        reduced_mass = (planet1.mass * planet2.mass) / (planet1.mass + planet2.mass)
        impulse = 2 * reduced_mass * dv_parallel * settings.BOUNCE_ENERGY_LOSS

        planet1.vx += impulse * nx / planet1.mass
        planet1.vy += impulse * ny / planet1.mass 
        planet2.vx -= impulse * nx / planet2.mass 
        planet2.vy -= impulse * ny / planet2.mass


    def handle_collisions(self, colliding_pairs, planet_manager):
        processed = set()
        merge_actions = []
        bounce_actions = []

        # Unlock previously locked pairs that are now separated
        unlocked_keys = []
        for (p1, p2), action in self.locked_pairs.items():
            dx = p2.x - p1.x
            dy = p2.y - p1.y
            distance = math.sqrt(dx**2 + dy**2 + settings.EPSILON**2)
            if distance >= p1.radius + p2.radius:
                unlocked_keys.append((p1, p2))
        for key in unlocked_keys:
            self.locked_pairs.pop(key, None)
            self.locked_pairs.pop((key[1], key[0]), None)  # remove reverse key if present

        # First pass: Handle merges
        for planet1, planet2, distance in colliding_pairs:
            pair_key = (planet1, planet2) if id(planet1) < id(planet2) else (planet2, planet1)
            if pair_key in self.locked_pairs or planet1 in processed or planet2 in processed:
                continue

            v_rel = calculate_v_rel(planet1, planet2)

            if self.check_merge(planet1, planet2, distance, v_rel):
                merge_actions.append((planet1, planet2))
                self.locked_pairs[pair_key] = 'merge'
                processed.update([planet1, planet2])

        # Second pass: Handle bounces
        for planet1, planet2, distance in colliding_pairs:
            pair_key = (planet1, planet2) if id(planet1) < id(planet2) else (planet2, planet1)
            if (planet1 in processed or planet2 in processed or pair_key in self.locked_pairs):
                continue

            bounce_actions.append((planet1, planet2))
            self.locked_pairs[pair_key] = 'bounce'
            processed.update([planet1, planet2])

        # Apply bounces
        for planet1, planet2 in bounce_actions:
            self.handle_bounce(planet1, planet2)

        # Apply merges
        for planet1, planet2 in merge_actions:
            planet_manager.trail_manager.stop_tracking_planet(planet1)
            planet_manager.trail_manager.stop_tracking_planet(planet2)
            self.handle_merge(planet1, planet2, planet_manager)
            merge_event = pygame.event.Event(PLANET_MERGED, {'planet1': planet1, 'planet2': planet2})
            pygame.event.post(merge_event)

            planet_manager.trail_manager.start_tracking_planet(planet1)

        return merge_actions, bounce_actions
    
    
    def update(self, planet_manager):
        num_planets = len(planet_manager.planets)

        for planet in planet_manager.planets:
            planet.reset_acceleration()

        if num_planets > 1:
            # Step 1: Calculate old acceleration
            for i in range(num_planets):
                pi = planet_manager.planets[i]
                for j in range(i + 1, num_planets):
                    pj = planet_manager.planets[j]
                    fx, fy = self.calculate_gravity(pi, pj)
                    pi.ax += fx / pi.mass
                    pi.ay += fy / pi.mass
                    pj.ax -= fx / pj.mass
                    pj.ay -= fy / pj.mass

        # Step 2: Update positions
        for planet in planet_manager.planets:
            planet.update_position()

        for planet in planet_manager.planets:
            planet.reset_acceleration()

        if num_planets > 1:
            # Step 3: Recalculate acceleration at new positions
            for i in range(num_planets):
                pi = planet_manager.planets[i]
                for j in range(i + 1, num_planets):
                    pj = planet_manager.planets[j]
                    fx, fy = self.calculate_gravity(pi, pj)
                    pi.ax += fx / pi.mass
                    pi.ay += fy / pi.mass
                    pj.ax -= fx / pj.mass
                    pj.ay -= fy / pj.mass

        # Step 4: Handle collisions
        collision_actions = self.handle_collisions(planet_manager.get_collision_pairs(), planet_manager)

        # Step 5: Update velocities
        for planet in planet_manager.planets:
            planet.update_velocity()
            # self.frame += 1
            # print("frame", math.ceil(self.frame/len(planet_manager.planets)) , planet.x, planet.vx, planet.ax)

        return collision_actions

        

            


        
