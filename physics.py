import pygame
from settings import *
from math import *

class Physics:
    def __init__(self):
        pass

    def calculate_gravity(self, planet1, planet2):
        dx = planet2.x - planet1.x
        dy = planet2.y - planet1.y

        distance_squared = dx**2 + dy**2 + EPSILON**2
        distance = sqrt(distance_squared)
        
        force = G * planet1.mass * planet2.mass / distance_squared

        fx = force * dx / distance
        fy = force * dy / distance


        return fx, fy
    
    def update_all(self, planets):    
        for planet in planets:
            planet.ax, planet.ay = 0.0, 0.0   

        for i in range(len(planets)):
            for j in range(i+1, len(planets)):
                fx, fy = self.calculate_gravity(planets[i], planets[j])
                planets[i].ax += fx / planets[i].mass
                planets[i].ay += fy / planets[i].mass
                planets[j].ax -= fx / planets[j].mass
                planets[j].ay -= fy / planets[j].mass
                
        for planet in planets:
            planet.update_velocity()
            planet.update_position()
