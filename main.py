import pygame
from settings import *
from planet import Planet
from planetManager import PlanetManager
from trailManager import TrailManager
from physics import Physics
from interface import Interface

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    interface = Interface(screen)
    paused = False
    trails = True
    #(mass, radius, x, y, vx, vy, color=(255, 255, 255)):

    # planet1 = Planet(1200, 8, -100, -300, 0, -10, (255, 0, 0))
    # planet2 = Planet(600, 10, 100, -300, 0, 50, (0, 255, 0))
    # planet3 = Planet(700, 6, 100, 300, 0, 10, (0, 0, 255))
    planet4 = Planet(600, 5, 100, 0, 0, 0, (255, 0, 184))
    planet5 = Planet(800, 5, -100, 0, 100, 0, (0, 255, 202))

    planetManager = PlanetManager([planet4, planet5])

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    trails = not trails
                    planetManager.clear_all_trails()
        
        interface.draw_background(BG_COLOR)

        if not paused:        
            planetManager.update_all_physics()
        else:
            interface.draw_pause()
        
        if trails:
            if not paused:
                planetManager.update_all_trails()
            planetManager.draw_all_trails(screen)
        
        planetManager.draw_all_planets(screen)

        pygame.display.flip()
        clock.tick(60)
    

if __name__ == "__main__":
    main()
