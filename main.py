import pygame
from settings import *
from utils import *
from planet import Planet
from planetManager import PlanetManager
from trailManager import TrailManager
from physics import Physics
from interface import Interface
from arrowManager import ArrowManager
from background import Background



def main():
    pygame.init()
    screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT), pygame.SRCALPHA)
    clock = pygame.time.Clock()
    
    planets = []


    #(mass, radius, x, y, vx, vy, color=(255, 255, 255)):

    planet1 = Planet(100000, 20, 0, 0, 0, 0, (255, 255, 255))
    planet2 = Planet(300, 8, -170, 0, 0, -350, (0, 255, 105))
    planet3 = Planet(600, 10, -250, 0, 0, -200, (255, 0, 0))
    planet4 = Planet(200, 4, 80, 40, 0, 500, (0, 255, 255))
    planet5 = Planet(600, 5, 0, -150, 400, 0, (255, 0, 100))
    planet6 = Planet(500, 7, -100, 250, -100, -200, (0, 55, 255))
    planet7 = Planet(500, 5, 200, 50, 0, 300, (255, 255, 0))
    planets = [planet1, planet2, planet3, planet4, planet5, planet6, planet7]

    # planet8 = Planet(1, 0.1, 0.97, -0.243, 0.466, 0.432, (105, 255, 105))
    # planet9 = Planet(1, 0.1, -0.97, 0.243, 0.466, 0.432, (255, 0, 0))
    # planet10 = Planet(1, 0.1, 0, 0, -0.932, -0.864, (0, 255, 255))
    # settings.g = 1
    # settings.scale = 0.007
    # planets = [planet8, planet9, planet10]


    # for _ in range(20):
    #     planets.append(Planet.generate_random_planet(300, 2000, 2, 15, -300, 300, -300, 300, -100, 100, -100, 100))


    planet_manager = PlanetManager(screen, planets)

    interface = Interface(screen, planet_manager)


    while settings.running:
        interface.clear_background(settings.BACKGROUND_COLOR)

        if settings.background_fx:
            interface.update_background()
            interface.draw_background_fx()

        for event in pygame.event.get():
           interface.execute_events(event)

        if not settings.paused:        
            planet_manager.update()
            #calculate_total_energy(planet_manager.planets)
     

        if settings.trails:
            planet_manager.draw_trails()
        
        planet_manager.draw_planets()

        if settings.collision_fx:
            planet_manager.draw_collision_fx()


        
        interface.update_slider()
        interface.draw_sliders()
        interface.draw_arrows()
        interface.draw_toggle_text()
        interface.draw_fps_text()
        interface.draw_planet_data_text()
        if settings.paused:
            interface.draw_pause()
            interface.draw_velocity_arrows_text()

        clock.tick(settings.FPS)
        pygame.display.flip()
        
        
    

if __name__ == "__main__":
    main()
