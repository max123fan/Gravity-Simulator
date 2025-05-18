import pygame
from settings import *

class Planet:
    def __init__(self, x, y, mass, radius, color=(255, 255, 255), vx=0, vy=0):
        self.x, self.y = x, y
        self.old_x, self.old_y = x, y
        self.vx, vy = vx, vy
        self.ax, self.ay = 0

        self.mass = mass
        self.radius = radius
        self.color = color

    def update_position(self, dt):
        # Store current position before updating
        old_x, old_y = self.x, self.y
        
        self.x = 2 * self.x - self.prev_x + self.ax * dt**2
        self.y = 2 * self.y - self.prev_y + self.ay * dt**2
        
        self.prev_x, self.prev_y = old_x, old_y

    def update_velocity(self, dt):
        self.vx += self.ax * dt #(dvx = ax dt)
        self.vy += self.ay * dt #(dvy = ay dt)

    def draw(self, screen):
        screen_x = int(self.x * SCALE + WIDTH // 2)
        screen_y = int(self.y * SCALE + HEIGHT // 2)
        pygame.draw.circle(screen, self.color, (screen_x, screen_y), self.radius)
        