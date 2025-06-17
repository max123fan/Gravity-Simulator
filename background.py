import pygame
import random
from settings import *

class Background:
    def __init__(self, screen):
        self.screen = screen
        self.stars = []
        self.setup_background()
        # Initialize stars with random positions, sizes, and brightness
        
    def setup_background(self):
        for _ in range(settings.NUM_STARS):
            x = random.randint(0, settings.WIDTH - 1)
            y = random.randint(0, settings.HEIGHT - 1)
            size = random.choice([1, 2])  # 1x1 or 2x2 pixels
            brightness = random.randint(0, 255)  # Initial brightness
            fade_rate = random.uniform(2, 4)  # Faster fade speed
            self.stars.append({
                'x': x, 'y': y, 'size': size, 'brightness': brightness,
                'fading_in': random.choice([True, False]), 'fade_rate': fade_rate
            })

    def update(self):
        for star in self.stars:
            if star['brightness'] <= 5 or star['brightness'] >= 250:
                star['fading_in'] = not star['fading_in']
            if star['fading_in']:
                star['brightness'] = min(255, star['brightness'] + star['fade_rate'])
            else:
                star['brightness'] = max(0, star['brightness'] - star['fade_rate'])

    def draw(self):
        for star in self.stars:
            b = int(star['brightness'])
            color = (b, b, b)  # (0, 0, 0) to (255, 255, 255)
            pygame.draw.rect(self.screen, color, (star['x'], star['y'], star['size'], star['size']))