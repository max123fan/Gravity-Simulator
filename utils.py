import math
import random
import time
from settings import *

def cartesian_to_screen_coords(x, y):
    return (x / settings.scale + settings.WIDTH // 2, -y / settings.scale + settings.HEIGHT // 2)

def screen_coords_to_cartesian(x, y):
    return ((x - settings.WIDTH / 2) * settings.scale, (-y + settings.HEIGHT / 2) * settings.scale)

def check_within_drawing_range(screen_x, screen_y, radius):
    return (
        -radius <= screen_x <= settings.WIDTH + radius and
        -radius <= screen_y <= settings.HEIGHT + radius
    )

def color_interpolate(color1, color2, ratio):
    return tuple(
        int(color1[i] * (1 - ratio) + color2[i] * ratio)
        for i in range(3)
    )

def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def calculate_normal_angle(planet1, planet2):
    dx = planet2.x - planet1.x
    dy = planet2.y - planet1.y
    return math.atan2(dy, dx)

def calculate_v_rel(planet1, planet2):
    vx_rel = planet2.vx - planet1.vx
    vy_rel = planet2.vy - planet1.vy
    return math.sqrt(vx_rel**2 + vy_rel**2)

def calculate_angle(x1, y1, x2, y2):
    return math.atan2((y2 - y1) /(x2 - x1))

def first_sig_figs(x, sig):
    if x == 0:
        return '0'
    s = f"{x:.{sig}g}"
    return s

def calculate_total_energy(planets):
    kinetic_energy = 0
    potential_energy = 0
    
    # Kinetic energy: KE = 0.5 * m * (vx^2 + vy^2)
    for planet in planets:
        velocity_squared = planet.vx**2 + planet.vy**2
        kinetic_energy += 0.5 * planet.mass * velocity_squared
    
    # Potential energy: PE = -g * m1 * m2 / r
    for i, planet1 in enumerate(planets):
        for planet2 in planets[i+1:]:  # Avoid double-counting
            dx = planet2.x - planet1.x
            dy = planet2.y - planet1.y
            real_distance = math.sqrt(dx**2 + dy**2 + settings.EPSILON**2)
            distance_max = planet1.radius + planet2.radius
            distance_max = max(real_distance, distance_max)
            potential_energy -= settings.g * planet1.mass * planet2.mass / distance_max
    
    total_energy = kinetic_energy + potential_energy
    print(f"KE: {kinetic_energy:.2f}, U: {potential_energy:.2f}, Total: {total_energy:.2f}")
    
    return total_energy

class FPSCounter:
    def __init__(self):
        self.frame_count = 0
        self.current_frame_count = settings.FPS
        self.last_time = time.time()

    def tick(self):
        self.frame_count += 1
        current_time = time.time()
        if current_time - self.last_time >= 1.0:
            self.current_frame_count = self.frame_count
            self.frame_count = 0
            self.last_time = current_time
        return self.current_frame_count
