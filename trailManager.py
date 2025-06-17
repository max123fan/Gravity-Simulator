import pygame
from collections import deque
from physics import Physics
from settings import *
from utils import *

class TrailManager:
    def __init__(self, screen):
        self.screen = screen
        self.active_planet_trails = {}
        self.removed_planet_trails = {}
        self.max_length = settings.TRAIL_LENGTH

    def start_tracking_planet(self, planet):
        """Add a planet to active trails if not already tracked."""
        if planet not in self.active_planet_trails and planet not in self.removed_planet_trails:
            self.active_planet_trails[planet] = deque(maxlen=self.max_length)

    def stop_tracking_planet(self, planet):
        """Move a planet's trail from active to removed."""
        if planet in self.active_planet_trails:
            self.removed_planet_trails[planet] = self.active_planet_trails.pop(planet)

    def update_trails(self, planet_manager):
        """Update trails for planets in planet_manager.planets."""
        for planet in planet_manager.planets:
            self.active_planet_trails.setdefault(planet, deque(maxlen=self.max_length))
            self.active_planet_trails[planet].append((planet.x, planet.y, planet.color, planet.trail_size))

            # Fade out removed trails
        for planet in list(self.removed_planet_trails.keys()):
            trail = self.removed_planet_trails[planet]
            if trail:
                trail.popleft()  # Remove the oldest point to shorten the trail
            if not trail:
                self.removed_planet_trails.pop(planet)

    def draw_trails(self):
        """Draw all active and removed planet trails."""
        for planet, trail_data in list(self.active_planet_trails.items()):
            self.draw_single_trail(trail_data)
        for planet, trail_data in list(self.removed_planet_trails.items()):
            self.draw_single_trail(trail_data) 

    def clear_trails(self):
        """Delete all trail data."""
        self.active_planet_trails.clear()
        self.removed_planet_trails.clear()

    def draw_single_trail(self, trail_data):
        """Render an individual planet's trail"""
        if len(trail_data) == 0:
            return
            
        for point_index, point in enumerate(trail_data):
            position_x, position_y, color, size = point
            screen_x, screen_y = cartesian_to_screen_coords(position_x, position_y)
            
            if not check_within_drawing_range(screen_x, screen_y, size / settings.scale):
                continue
                
            fade_progress = point_index / max(1, len(trail_data))
            opacity = int(100 * fade_progress ** 2)
            
            trail_color_with_opacity = (color[0], color[1], color[2], opacity)
            pygame.gfxdraw.filled_circle(
                self.screen,  # Surface (positional)
                int(screen_x),  # x (positional)
                int(screen_y),  # y (positional)
                int(size / settings.scale),  # radius (positional)
                trail_color_with_opacity  # color (positional)
            )