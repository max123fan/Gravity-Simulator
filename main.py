import pygame
from settings import *

from utils import *
from planet import Planet
from planetManager import PlanetManager
from trailManager import TrailManager
from physics import Physics
from interface import Interface


def main():
    pygame.init()
    screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
    clock = pygame.time.Clock()
    interface = Interface(screen)
    
    fps_counter = FPSCounter()


    #(mass, radius, x, y, vx, vy, color=(255, 255, 255)):

    # planet1 = Planet(1000, 10, 100, 0, -50, 0, (255, 255, 0))
    # planet2 = Planet(1000, 10, -100, 0, 100, 0, (0, 255, 105))
    # planet3 = Planet(1500, 10, 0, 0, 50, 0, (255, 0, 0))
    # planet4 = Planet(800, 7, -100, 40, 0, 100, (0, 255, 255))
    # planet5 = Planet(600, 5, -180, -150, -10, 120, (255, 0, 100))
    # planet6 = Planet(500, 7, -30, 120, 50, 80, (0, 55, 255))
    # planet7 = Planet(500, 5, 120, 50, 10, 30, (255, 255, 0))
    # planet8 = Planet(700, 5, 160, 100, 40, -20, (0, 255, 105))
    # planet9 = Planet(500, 4, 150, 50, -200, 0, (255, 0, 0))
    # planet10 = Planet(800, 7, -100, 40, 50, 100, (0, 255, 255))
    # planet11 = Planet(600, 5, -120, -150, -10, -50, (255, 0, 100))
    # planet12 = Planet(2000, 7, -150, 120, 50, -80, (0, 55, 255))

    planets = []
    # planets = [planet1, planet2, planet3, planet4, planet5, planet6, planet7, planet8, planet9, planet10, planet11, planet12]

    for _ in range(15):
        planets.append(Planet.generate_random_planet(300, 2000, 3, 8, -300, 300, -300, 300, -100, 100, -100, 100))


    planet_manager = PlanetManager(screen, planets)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    settings.toggle_pause()

                if event.key == pygame.K_z:
                    settings.toggle_trails()
                    planet_manager.clear_trails()

                if event.key == pygame.K_x:
                    settings.toggle_collision_fx()

                if event.key == pygame.K_MINUS:
                    settings.set_scale(settings.scale * 1.2)
                if event.key == pygame.K_EQUALS:
                    settings.set_scale(settings.scale * 0.833)

                if event.key == pygame.K_0:
                    settings.set_dt(settings.dt * 1.2)
                if event.key == pygame.K_9:
                    settings.set_dt(settings.dt * 0.833)
                    
        
        interface.draw_background(settings.BG_COLOR)

        if not settings.paused:        
            planet_manager.update()
            #calculate_total_energy(planet_manager.planets)
        else:
            interface.draw_pause()
        
        if settings.trails:
            planet_manager.draw_trails()
        
        planet_manager.draw_planets()

        if settings.collision_fx:
            planet_manager.draw_collision_fx()
        
        
        interface.draw_fps_counter(fps_counter.tick())
        clock.tick(settings.FPS)
        pygame.display.flip()
        
        
    

if __name__ == "__main__":
    main()
