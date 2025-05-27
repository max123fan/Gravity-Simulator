import pygame
import pygame.gfxdraw
from settings import *

class Planet:
    def __init__(self, mass, radius, x, y, vx, vy, color=(255, 255, 255)):
        self.mass = mass
        self.radius = radius
        self.color = color

        self.x = x
        self.y = y

        self.vx = vx
        self.vy = vy

        self.ax = 0
        self.ay = 0

        self.prev_x = self.x - self.vx * DT
        self.prev_y = self.y - self.vy * DT

        self.clear_trail()

        self.trail_size = max(int(self.radius / 3), 1)

    def update_position(self):
        temp_x, temp_y = self.x, self.y
        
        self.x = 2 * self.x - self.prev_x + self.ax * DT**2
        self.y = 2 * self.y - self.prev_y + self.ay * DT**2
        
        self.prev_x, self.prev_y = temp_x, temp_y


    def update_velocity(self):
        self.vx = (self.x - self.prev_x) / DT
        self.vy = (self.y - self.prev_y) / DT

    def reset_acceleration(self):
        self.ax, self.ay = 0, 0


    def draw(self, screen):
        screen_x, screen_y = cartesian_to_screen_coords(self.x, self.y)
        if check_within_drawing_range(screen_x, screen_y, self.radius):
            pygame.draw.circle(screen, self.color, (screen_x, screen_y), self.radius / SCALE)

        
    def update_trail(self):
        self.positions.append((self.x, self.y))
        self.color_history.append(self.color)
        if len(self.positions) > TRAIL_LENGTH:
            self.positions.pop(0)
    
    def clear_trail(self):
        self.positions = []
        self.color_history = []

    def draw_trail(self, screen):
        if not self.positions:
            return
        
        for i, (x, y) in enumerate(self.positions):
            screen_x, screen_y = cartesian_to_screen_coords(x, y)
            if not check_within_drawing_range(screen_x, screen_y, self.trail_size):
                return
            
            fade_ratio = i / len(self.positions)
            alpha = int(200 * fade_ratio)
            
            trail_color = (*self.color_history[i], alpha)
            
            pygame.gfxdraw.filled_circle(screen, screen_x, screen_y, self.trail_size, trail_color)