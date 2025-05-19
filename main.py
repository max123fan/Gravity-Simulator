import pygame
from settings import *
from planet import Planet
from planetManager import PlanetManager
from physics import Physics
from interface import Interface

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    interface = Interface(screen)
    paused = False
    trails = False

    #sun = Planet(1, 10, -0.97000436, 0.24308753, 0.46620368, 0.43236573, (255, 255, 0))
    #earth = Planet(1, 10, 0, 0, -0.93240737, -0.86473146, (100, 100, 255),)
    #moon = Planet(1, 10, 0.97000436, -0.24308753, 0.46620368, 0.43236573, (220, 220, 220))
    planet1 = Planet(130, 10, -1, 0, 0, -15, (255, 0, 0))#turqoise
    planet2 = Planet(130, 10, 1, 0, 0, 15, (0, 255, 0))#purple
    planet3 = Planet(100, 8, 0, 2, 25, 0, (0, 0, 255))#white
    planet4 = Planet(100, 8, 0, -2, -25, 0, (255, 255, 0))#white
    planets = [planet1, planet2, planet3, planet4]

    planetManager = PlanetManager(planets)

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
