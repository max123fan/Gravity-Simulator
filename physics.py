import pygame
from settings import *
from math import *

class Physics:
    def __init__(self, G):
        self.G = G

    def calculate_gravity(self, planet1, planet2):
        displacement_x = planet2.x - planet1.x
        displacement_y = planet2.y - planet1.y

        distance = sqrt(displacement_x**2 + displacement_y**2)
        MIN_DISTANCE = 1.1 * (planet1.radius + planet2.radius)
        distance = max(distance, MIN_DISTANCE)

        force_scaled = G * planet1.mass * planet2.mass / distance**3 #middle step in calculation

        fx = force_scaled * displacement_x
        fy = force_scaled * displacement_y

        return fx, fy
    
    def update_physics(self, planets, TIME_STEP):    
        for planet in planets:
            planet.ax, planet.ay = 0.0, 0.0   

        for i in range(len(planets)):
            for j in range(i+1, len(planets)):
                fx, fy = self.calculate_gravity(planets[i], planets[j])
                planets[i].ax += fx / planets[i].mass
                planets[i].ay += fy / planets[i].mass
                planets[j].ax -= fx / planet[j].mass
                planet[j].ay -= fy / planet[j].mass
                
        for planet in planets:
            planet.update_velocity(TIME_STEP)
            planet.update_position(TIME_STEP)
