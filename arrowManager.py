import pygame
from utils import *
from settings import *

class ArrowManager:
    def __init__(self, screen, planet_manager):
        self.screen = screen
        self.planet_manager = planet_manager
        self.selected_planet = None
        self.dragging = False
        self.start_pos = None

        self.DRAG_THRESHOLD = 5

        self.arrows = {}

    def update_arrows(self, screen_mouse_coords, event):
        cartesian_mouse_coords = screen_coords_to_cartesian(*screen_mouse_coords)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            planet = self.planet_manager.check_mouse_on_planet(screen_mouse_coords)
            if planet:
                self.selected_planet = planet
                self.click_pos = pygame.mouse.get_pos()  # Screen coords for click/drag check
                self.start_pos = pygame.mouse.get_pos()  # Screen coords for drag threshold
                if not planet.has_arrow:
                    planet.arrow_start = (planet.x, planet.y)
                    planet.arrow_end = cartesian_mouse_coords
                    self.arrows[planet] = cartesian_mouse_coords

        elif event.type == pygame.MOUSEMOTION and self.selected_planet:
            current_pos = pygame.mouse.get_pos()
            dx = current_pos[0] - self.start_pos[0]
            dy = current_pos[1] - self.start_pos[1]
            if not self.dragging and (dx * dx + dy * dy) >= self.DRAG_THRESHOLD * self.DRAG_THRESHOLD:
                self.dragging = True
                if not self.selected_planet.has_arrow:
                    self.selected_planet.has_arrow = True

            if self.dragging:
                self.selected_planet.arrow_end = cartesian_mouse_coords
                self.arrows[self.selected_planet] = cartesian_mouse_coords

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.selected_planet and not self.dragging:
                current_pos = pygame.mouse.get_pos()
                dx = current_pos[0] - self.click_pos[0]
                dy = current_pos[1] - self.click_pos[1]
                if dx * dx + dy * dy < self.DRAG_THRESHOLD * self.DRAG_THRESHOLD:
                    if self.selected_planet.has_arrow:
                        self.selected_planet.has_arrow = False
                        self.selected_planet.arrow_end = self.selected_planet.arrow_start
                        self.arrows.pop(self.selected_planet, None)
                    else:
                        self.selected_planet.has_arrow = True
                        self.selected_planet.arrow_end = cartesian_mouse_coords
                        self.arrows[self.selected_planet] = cartesian_mouse_coords

            self.selected_planet = None
            self.dragging = False
            self.start_pos = None
            self.click_pos = None
        

    def apply_arrows(self):
        for planet in self.planet_manager.planets:
            if planet.has_arrow:
                dx = planet.arrow_end[0] - planet.arrow_start[0]
                dy = planet.arrow_end[1] - planet.arrow_start[1]
                planet.vx = dx * settings.ARROW_SCALE
                planet.vy = dy * settings.ARROW_SCALE
                planet.has_arrow = False
                planet.arrow_end = planet.arrow_start
        self.arrows.clear()

    def draw_arrows(self):
        for planet, pos in self.arrows.items():
            planet.draw_arrow(self.screen, pos)
        
    def clear_arrows(self):
        self.arrows = {}
        for planet in self.planet_manager.planets:
            planet.has_arrow = False
            planet.arrow_end = planet.arrow_start