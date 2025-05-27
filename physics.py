import pygame
from settings import *

import math
import random

class Physics:
    def __init__(self):
        pass

    def calculate_gravity(self, planet1, planet2):
        dx = planet2.x - planet1.x
        dy = planet2.y - planet1.y

        distance_squared = dx**2 + dy**2 + EPSILON**2
        distance = math.sqrt(distance_squared)
        
        force = G * planet1.mass * planet2.mass / distance_squared

        fx = force * dx / distance
        fy = force * dy / distance

        return fx, fy
    
    def handle_collisions(self, collision_pairs, planet_manager):
        if len(collision_pairs) == 0:
            return
        
        processed_planets = set()

        sorted_pairs = sorted(
            collision_pairs,
            key=lambda pair: math.sqrt((pair[0].x - pair[1].x)**2 + (pair[0].y - pair[1].y)**2)
        )

        for planet1, planet2 in sorted_pairs:
            if planet1 in processed_planets or planet2 in processed_planets:
                continue

            dx = planet2.x - planet1.x
            dy = planet2.y - planet1.y
            distance = math.sqrt(dx**2 + dy**2 + EPSILON**2)

            vx_rel = planet2.vx - planet1.vx
            vy_rel = planet2.vy - planet1.vy
            v_rel = math.sqrt(vx_rel**2 + vy_rel**2)

            total_mass = planet1.mass + planet2.mass
            total_radius = planet1.radius + planet2.radius
            v_escape = math.sqrt(2 * G * total_mass / total_radius)

            cos_theta = (dx * vx_rel + dy * vy_rel) / (distance * max(v_rel, EPSILON))
            sin_theta = math.sqrt(max(1 - cos_theta**2, 0))
            b = (distance * sin_theta) / total_radius
            b = min(max(b, 0), 1)

            v_merge = 1.1 * v_escape * (1 - b**2)

            mass_ratio = max(planet1.mass / planet2.mass, planet2.mass / planet1.mass)

            if RANDOMNESS_IN_COLLISIONS and abs(v_rel - v_merge) / v_merge < 0.1:
                merge_probability = 1 - b
            else:
                merge_probability = 0

            if v_rel < v_merge or (random.random() < merge_probability):
                mass_merged = planet1.mass + planet2.mass
                radius_merged = (planet1.radius**2 + planet2.radius**2)**(1/2)
                x_merged = (planet1.mass * planet1.x + planet2.mass * planet2.x) / mass_merged
                y_merged = (planet1.mass * planet1.y + planet2.mass * planet2.y) / mass_merged
                vx_merged = (planet1.mass * planet1.vx + planet2.mass * planet2.vx) / mass_merged * MERGE_ENERGY_LOSS
                vy_merged = (planet1.mass * planet1.vy + planet2.mass * planet2.vy) / mass_merged * MERGE_ENERGY_LOSS

                planet1.x = x_merged
                planet1.y = y_merged
                planet1.vx = vx_merged
                planet1.vy = vy_merged
                planet1.reset_acceleration()
                planet1.prev_x = x_merged - vx_merged * DT
                planet1.prev_y = y_merged - vy_merged * DT

                planet1.color = planet_manager.merge_colors(planet1, planet2)

                planet1.mass = mass_merged
                planet1.radius = radius_merged

                planet_manager.remove_planet(planet2)
                processed_planets.add(planet1)
                processed_planets.add(planet2)

                # collision_point = ((planet1.x + planet2.x) / 2, (planet1.y + planet2.y) / 2)
                # energy = 0.5 * (planet1.mass * planet2.mass / mass_merged) * v_rel**2
                # interface.add_visual("merge", collision_point, intensity=energy)
            else:
                nx, ny = dx / distance, dy / distance
                
                dv_parallel = (planet2.vx - planet1.vx) * nx + (planet2.vy - planet1.vy) * ny
                
                if dv_parallel > 0:
                    continue
                
                reduced_mass = (planet1.mass * planet2.mass) / (planet1.mass + planet2.mass)
                impulse = 2 * reduced_mass * dv_parallel
                
                planet1.vx += impulse * nx / planet1.mass * BOUNCE_ENERGY_LOSS
                planet1.vy += impulse * ny / planet1.mass * BOUNCE_ENERGY_LOSS
                planet2.vx -= impulse * nx / planet2.mass * BOUNCE_ENERGY_LOSS
                planet2.vy -= impulse * ny / planet2.mass * BOUNCE_ENERGY_LOSS
                
                overlap = (planet1.radius + planet2.radius) - distance
                if overlap > 0:
                    correction = 0.5 * overlap
                    planet1.x -= correction * nx
                    planet1.y -= correction * ny
                    planet2.x += correction * nx
                    planet2.y += correction * ny
                
                processed_planets.update([planet1, planet2])

                # collision_point = ((planet1.x + planet2.x) / 2, (planet1.y + planet2.y) / 2)
                # energy = 0.5 * (planet1.mass * planet2.mass / mass_merged) * v_rel**2
                # interface.add_visual("bounce", collision_point, intensity=energy)

    
    def update_all(self, planet_manager):    
        for planet in planet_manager.planets:
            planet.reset_acceleration()

        num_planets = len(planet_manager.planets)
        if num_planets > 1:
            for i in range(num_planets):
                for j in range(i+1, num_planets):
                    fx, fy = self.calculate_gravity(planet_manager.planets[i], planet_manager.planets[j])
                    planet_manager.planets[i].ax += fx / planet_manager.planets[i].mass
                    planet_manager.planets[i].ay += fy / planet_manager.planets[i].mass
                    planet_manager.planets[j].ax -= fx / planet_manager.planets[j].mass
                    planet_manager.planets[j].ay -= fy / planet_manager.planets[j].mass
        
        self.handle_collisions(planet_manager.get_collision_pairs(), planet_manager)

        for planet in planet_manager.planets:
            planet.update_position()

        for planet in planet_manager.planets:
            planet.update_velocity()
            


        
