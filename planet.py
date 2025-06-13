import pygame
import pygame.gfxdraw
from settings import *
from utils import *

class Planet:
    def __init__(self, mass, radius, x, y, vx, vy, color=(255, 255, 255)):
        self.x = x
        self.y = y

        self.vx = vx
        self.vy = vy

        self.ax = 0
        self.ay = 0

        self.prev_x = x - vx * settings.dt
        self.prev_y = y - vy * settings.dt

        self.mass = mass
        self.radius = radius
        self.color = color
        self.update_trail_size()

    def reset_acceleration(self):
        self.ax = 0
        self.ay = 0

    def update_trail_size(self):
        self.trail_size = self.radius / 3

    def apply_force(self, fx, fy):
        self.ax += fx / self.mass
        self.ay += fy / self.mass

    def update_position(self):
        # Store current position as previous before update
        self.prev_x, self.prev_y = self.x, self.y

        # Calculate new position
        new_x = self.x + self.vx * settings.dt + 0.5 * self.ax * settings.dt**2
        new_y = self.y + self.vy * settings.dt + 0.5 * self.ay * settings.dt**2

        # Update position
        self.x, self.y = new_x, new_y
        
        # Collision-induced position correction
        # if hasattr(self, 'collision_partner') and self.collision_partner is not None:
        #     partner = self.collision_partner
        #     dx = partner.x - self.x
        #     dy = partner.y - self.y
        #     dist_sq = dx*dx + dy*dy
        #     min_dist = self.radius + partner.radius
            
        #     if dist_sq < min_dist**2 and dist_sq > EPSILON**2:
        #         # Mass-weighted correction
        #         overlap = min_dist - dist_sq**0.5
        #         total_mass = self.mass + partner.mass
        #         correction = overlap / total_mass
        #         self.x -= dx * correction * partner.mass / dist_sq**0.5
        #         self.y -= dy * correction * partner.mass / dist_sq**0.5
        #         partner.x += dx * correction * self.mass / dist_sq**0.5
        #         partner.y += dy * correction * self.mass / dist_sq**0.5
        #         print(f"Corrected dy: {self.y - partner.y:.2f}")
        #     elif dist_sq >= min_dist**2:
        #         # Clear collision partner when unfused
        #         self.collision_partner = None
        #         partner.collision_partner = None

    def reset_acceleration(self):
        self.ax_old = self.ax
        self.ay_old = self.ay
        self.ax = 0
        self.ay = 0

    def update_velocity(self):
        self.vx += 0.5 * (self.ax_old + self.ax) * settings.dt
        self.vy += 0.5 * (self.ay_old + self.ay) * settings.dt

    def draw(self, screen):
        screen_x, screen_y = cartesian_to_screen_coords(self.x, self.y)
        if check_within_drawing_range(screen_x, screen_y, self.radius / settings.scale):
            pygame.gfxdraw.filled_circle(
                screen, 
                int(screen_x), 
                int(screen_y), 
                int(self.radius / settings.scale), 
                self.color
            )
            pygame.gfxdraw.aacircle(
                screen,
                int(screen_x),
                int(screen_y),
                int(self.radius / settings.scale + 4),
                self.color
            )

    @staticmethod
    def generate_random_planet(mass_low, mass_high, radius_low, radius_high, x_low, x_high, y_low, y_high, vx_low, vx_high, vy_low, vy_high):
        return Planet(
            random.uniform(mass_low, mass_high), 
            random.uniform(radius_low, radius_high), 
            random.uniform(x_low, x_high), 
            random.uniform(y_low, y_high), 
            random.uniform(vx_low, vx_high), 
            random.uniform(vy_low, vy_high), 
            (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        )