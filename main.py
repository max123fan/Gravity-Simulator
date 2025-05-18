import pygame
from settings import *
from planet import Planet

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 2e30, 30, (255, 255, 0))
    earth = Planet(147e9, 0, 6e24, 10, (100, 100, 255), 0, 30e3)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        earth.update_position(TIME_STEP)

        screen.fill(BG_COLOR)
        sun.draw(screen)
        earth.draw(screen)
        pygame.display.flip()
        clock.tick(60)
    
    force_x

if __name__ == "__main__":
    main()
