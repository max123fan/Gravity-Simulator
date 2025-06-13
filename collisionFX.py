import pygame
from settings import *
from collisionFXSettings import *
from utils import *
import random

import pygame
from settings import *
from collisionFXSettings import *
from utils import *
import random

class MergeEffect:
    def __init__(self, screen, x, y, combined_radius, v_rel):
        self.screen = screen
        self.x = x
        self.y = y
        self.combined_radius = combined_radius
        self.v_rel = v_rel
        self.particle_count = int(min(MERGE_PARTICLE_MIN + 2*(v_rel**2 / combined_radius)**0.25, MERGE_PARTICLE_MAX))
        print(self.particle_count)

        self.particles = []

        self.start_time = pygame.time.get_ticks()
        self.flash_alpha = 0  # New: tracks flash transparency
        self.elapsed_time = 0
        
        # Create particles (original code preserved)
        for _ in range(self.particle_count):
            angle = random.uniform(0, math.pi*2)
            speed = random.uniform(MERGE_SPEED_LOW_CONSTANT, MERGE_SPEED_HIGH_CONSTANT)
            
            self.particles.append({
                'x': x,
                'y': y,
                'vx': math.cos(angle) * speed * v_rel,
                'vy': math.sin(angle) * speed * v_rel,
                'life': random.uniform(MERGE_LIFE_LOW, MERGE_LIFE_HIGH),
                'color': (
                    min(255, MERGE_SPARK_COLOR[0] + random.randint(-20, 20)),
                    min(255, MERGE_SPARK_COLOR[1] + random.randint(-20, 20)),
                    min(255, MERGE_SPARK_COLOR[2] + random.randint(-10, 10))
                ),
                'size': random.uniform(combined_radius * MERGE_SIZE_LOW_CONSTANT, combined_radius * MERGE_SIZE_HIGH_CONSTANT),
                'decay': random.uniform(MERGE_DECAY_LOW, MERGE_DECAY_HIGH)
            })
    
    def update(self):
        dt = settings.dt
        self.elapsed_time += dt
        
        # 2. Particle updates (CORRECT)
        for p in self.particles[:]:
            p['x'] += p['vx'] * dt
            p['y'] += p['vy'] * dt
            p['life'] -= dt
            p['size'] *= p['decay'] ** dt
            if p['life'] <= 0 or p['size'] < 0.5:
                self.particles.remove(p)

        
        # 1. Growing flash calculation (FIXED: Added hasattr check)
        if not hasattr(self, 'current_radius'):
            self.current_radius = 0
        
        if self.elapsed_time < FLASH_DURATION:
            progress = self.elapsed_time / FLASH_DURATION
            self.current_radius = self.combined_radius * FLASH_RADIUS_MULTIPLIER * progress
            self.flash_alpha = int(255 * (1 - 1.5 * progress))
        else:
            self.flash_alpha = 0  # Explicitly set when expired


    def draw(self):
        # 1. Draw flash (FIXED: Added radius/alpha validation)
        
        # 2. Draw particles (CORRECT)
        for p in self.particles:
            alpha = min(255, p['life'] * 4)
            screen_x, screen_y = cartesian_to_screen_coords(int(p['x']), int(p['y']))
            scaled_size = max(1, int(p['size'] / settings.scale))  # Ensures minimum size of 1
            pygame.draw.circle(
                self.screen, 
                (*p['color'], alpha),
                (screen_x,
                screen_y),
                scaled_size
            )
        if hasattr(self, 'current_radius') and self.flash_alpha > 0 and self.current_radius > 0:
            # Calculate scaled dimensions
            scaled_size = int(self.current_radius / settings.scale)
            diameter = int(scaled_size * 2)
            
            # Create surface with scaled size
            flash_surf = pygame.Surface((diameter, diameter), pygame.SRCALPHA)
        

            pygame.draw.circle(
                flash_surf,
                (*FLASH_COLOR, self.flash_alpha),
                (scaled_size, scaled_size),
                scaled_size
            )
            
            screen_x, screen_y = cartesian_to_screen_coords(self.x, self.y)

            self.screen.blit(
                flash_surf,
                (int(screen_x - scaled_size),
                int(screen_y - scaled_size))
            )

    def is_complete(self):
        # Now checks flash duration too
        return (len(self.particles) == 0 and 
                (pygame.time.get_ticks() - self.start_time > FLASH_DURATION))
    
class BounceEffect:
    def __init__(self, screen, x, y, combined_radius, v_rel, normal_angle):
        self.screen = screen
        self.x = x
        self.y = y
        self.normal_angle = normal_angle
        self.start_time = pygame.time.get_ticks()
        self.particle_count = int(min(BOUNCE_PARTICLE_MIN + (v_rel**2 / combined_radius)**0.25, BOUNCE_PARTICLE_MAX))
        print(self.particle_count)
        self.particles = []

        
        # Create impact-directional particles
        for _ in range(self.particle_count):
            # Base angle is the normal direction of the collision (pointing outward)
            angle = self.normal_angle + random.choice([math.pi / 2, -math.pi / 2]) + random.uniform(-math.pi / 8, math.pi / 8)

            # Speed is randomized within bounds
            speed = random.uniform(BOUNCE_SPEED_LOW_CONSTANT, BOUNCE_SPEED_HIGH_CONSTANT)

            self.particles.append({
                'x': x,
                'y': y,
                'vx': math.cos(angle) * speed * v_rel,
                'vy': math.sin(angle) * speed * v_rel,
                'life': random.uniform(BOUNCE_LIFE_LOW, BOUNCE_LIFE_HIGH),
                'size': random.uniform(combined_radius * BOUNCE_SIZE_LOW_CONSTANT, combined_radius * BOUNCE_SIZE_HIGH_CONSTANT),
                'color': (
                    min(255, BOUNCE_SPARK_COLOR[0] + random.randint(-30, 30)),
                    min(255, BOUNCE_SPARK_COLOR[1] + random.randint(-30, 30)),
                    min(255, BOUNCE_SPARK_COLOR[2] + random.randint(-10, 10))
                ),
                'decay': random.uniform(BOUNCE_DECAY_LOW, BOUNCE_DECAY_HIGH)  # Shrink speed
            })

    def update(self):
        dt = settings.dt
        for p in self.particles:
            # Move particles
            p['x'] += p['vx'] * dt
            p['y'] += p['vy'] * dt

            # Subtract time (not frames!)
            p['life'] -= dt

            # Exponential size decay (frame-independent)
            p['size'] *= p['decay'] ** dt
            # Remove dead particles

        self.particles = [p for p in self.particles if p['life'] > 0 and p['size'] > 0.2]
        
        return False  # Don't remove yet

    def draw(self):
        for p in self.particles:
            screen_x, screen_y = cartesian_to_screen_coords(int(p['x']), int(p['y']))
            scaled_size = max(1, int(p['size'] / settings.scale))

            pygame.draw.circle(
                self.screen,
                (p['color']),  # RGBA
                (screen_x,
                screen_y),
                scaled_size
            )

    def is_complete(self):
        return len(self.particles) == 0