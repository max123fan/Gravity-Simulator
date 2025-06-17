import pygame
import math
from settings import *

class SliderManager:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("arial", 12)
        # Variables for slider dimensions and positions (screen coords)
        self.BAR_WIDTH = 250
        self.BAR_HEIGHT = 10
        self.BAR_X = 30
        self.DT_BAR_Y = 60  # Screen y=600-60=540
        self.scale_BAR_Y = 40  # Screen y=600-40=560
        self.HANDLE_WIDTH = 8
        self.HANDLE_HEIGHT = 18
        self.LABEL_X_OFFSET = 10
        self.LABEL_Y_OFFSET = 2
        self.sliders = [
            {
                'name': 'dt',
                'bar_rect': pygame.Rect(self.BAR_X, settings.HEIGHT - self.DT_BAR_Y, self.BAR_WIDTH, self.BAR_HEIGHT),
                'handle_rect': pygame.Rect(self.BAR_X, settings.HEIGHT - self.DT_BAR_Y + self.HANDLE_HEIGHT // 2, self.HANDLE_WIDTH, self.HANDLE_HEIGHT),
                'min_value': 0.0001,
                'max_value': 100,
                'value': settings.dt,
                'dragging': False
            },
            {
                'name': 'scale',
                'bar_rect': pygame.Rect(self.BAR_X, settings.HEIGHT - self.scale_BAR_Y, self.BAR_WIDTH, self.BAR_HEIGHT),
                'handle_rect': pygame.Rect(self.BAR_X, settings.HEIGHT - self.scale_BAR_Y + self.HANDLE_HEIGHT // 2, self.HANDLE_WIDTH, self.HANDLE_HEIGHT),
                'min_value': 0.001,
                'max_value': 10000,
                'value': settings.scale,
                'dragging': False
            }
        ]
        self.update_handle_positions()

    def update_handle_positions(self):
        for slider in self.sliders:
            min_log = math.log10(slider['min_value'])
            max_log = math.log10(slider['max_value'])
            value_log = math.log10(max(slider['min_value'], min(slider['value'], slider['max_value'])))
            norm_coords = (value_log - min_log) / (max_log - min_log)
            handle_x = slider['bar_rect'].x + norm_coords * slider['bar_rect'].width
            slider['handle_rect'].x = handle_x - slider['handle_rect'].width / 2
            slider['handle_rect'].y = slider['bar_rect'].y  + slider['bar_rect'].height / 2 - slider['handle_rect'].height / 2

    def update_sliders(self, mouse_coords, event):
        for slider in self.sliders:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if slider['handle_rect'].collidepoint(mouse_coords):
                    slider['dragging'] = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                slider['dragging'] = False
            elif event.type == pygame.MOUSEMOTION and slider['dragging']:
                x = max(slider['bar_rect'].x, min(slider['bar_rect'].x + slider['bar_rect'].width, mouse_coords[0]))
                norm_coords = (x - slider['bar_rect'].x) / slider['bar_rect'].width
                min_log = math.log10(slider['min_value'])
                max_log = math.log10(slider['max_value'])
                value_log = min_log + norm_coords * (max_log - min_log)
                slider['value'] = 10 ** value_log
                slider['handle_rect'].x = x - slider['handle_rect'].width / 2
                if slider['name'] == 'dt':
                    settings.dt = slider['value']

                elif slider['name'] == 'scale':
                    settings.scale = slider['value']
                self.update_handle_positions()

    def draw_sliders(self):
        for slider in self.sliders:
            pygame.draw.rect(self.screen, (100, 100, 100), slider['bar_rect'])
            pygame.draw.rect(self.screen, (220, 220, 220), slider['handle_rect'])
            label = self.font.render(f"{slider['name']}: {slider['value']:.6f}", True, (255, 255, 255))
            label_y = slider['bar_rect'].y - self.LABEL_Y_OFFSET
            self.screen.blit(label, (slider['bar_rect'].x + slider['bar_rect'].width + self.LABEL_X_OFFSET, label_y))
    
    def is_mouse_over_slider(self, mouse_coords):
        for slider in self.sliders:
            if slider['handle_rect'].collidepoint(mouse_coords):
                return True              
        return False