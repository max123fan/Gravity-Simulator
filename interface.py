import pygame
from settings import *
from events import *
from utils import *
from arrowManager import ArrowManager
from sliderManager import SliderManager
from background import Background

class Interface:
    def __init__(self, screen, planet_manager):
        self.screen = screen
        self.paused_font = pygame.font.Font("ShareTech-Regular.ttf", 32)
        self.velocity_arrows_font = pygame.font.Font("ShareTech-Regular.ttf", 18)
        self.fps_font = pygame.font.Font("ShareTech-Regular.ttf", 14)
        self.toggle_font = pygame.font.Font("ShareTech-Regular.ttf", 14)
        self.planet_data_font = pygame.font.SysFont("arial", 14)

        self.planet_manager = planet_manager
        self.fps_counter = FPSCounter()
        self.arrow_manager = ArrowManager(screen, planet_manager)
        self.slider_manager = SliderManager(screen)
        self.background = Background(screen)

        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        
        self.to_display_data = None
                                                        
    def execute_events(self, event):
        if event.type == pygame.QUIT:
            settings.running = False
        
        mouse_pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not settings.draw_velocity_arrows_mode:
                planet = self.planet_manager.check_mouse_on_planet(mouse_pos)
                if not self.slider_manager.is_mouse_over_slider(mouse_pos):
    
                    if not planet or self.to_display_data == planet:
                        self.set_planet_to_display_data(None)
                    else:  
                        self.set_planet_to_display_data(planet)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if settings.paused:
                    self.arrow_manager.apply_arrows()
                    settings.draw_velocity_arrows_mode = False
                settings.toggle_pause()
            
            if event.key == pygame.K_v and settings.paused:
                if settings.draw_velocity_arrows_mode:
                    self.arrow_manager.clear_arrows()
                settings.toggle_draw_velocity_arrows_mode()
                
            if event.key == pygame.K_z:
                settings.toggle_trails()
                self.planet_manager.clear_trails()

            if event.key == pygame.K_x:
                settings.toggle_collision_fx()
                self.planet_manager.clear_collision_fx()

            if event.key == pygame.K_c:
                settings.toggle_background_fx()

            # if event.key == pygame.K_MINUS:
            #     settings.set_scale(settings.scale * 1.2)
            # if event.key == pygame.K_EQUALS:
            #     settings.set_scale(settings.scale * 0.833)

            # if event.key == pygame.K_0:
            #     settings.set_dt(settings.dt * 1.2)
            # if event.key == pygame.K_9:
            #     settings.set_dt(settings.dt * 0.833)

        if event.type == PLANET_MERGED:
            planet1, planet2 = event.planet1, event.planet2
            if planet1 == self.to_display_data or planet2 == self.to_display_data:
                self.set_planet_to_display_data(None)

        self.slider_manager.update_sliders(mouse_pos, event)

        if settings.draw_velocity_arrows_mode:
            self.arrow_manager.update_arrows(mouse_pos, event)

    def update_slider(self):
        self.slider_manager.update_handle_positions()
        
    def update_background(self):
        self.background.update()

    def draw_pause(self):
        text = self.paused_font.render("Paused", True, self.WHITE)
        self.screen.blit(text, (settings.WIDTH - 100, 10))
    
    def draw_background_fx(self):
        self.background.draw()
    
    def clear_background(self, BG_COLOR):
        self.screen.fill(BG_COLOR)

    def draw_fps_text(self):
        fps = self.fps_counter.tick()
        text = self.fps_font.render("FPS: %s" % fps, True, self.WHITE)
        self.screen.blit(text, (5, 5))

    def draw_arrows(self):
        self.arrow_manager.draw_arrows()
    
    def draw_sliders(self):
        self.slider_manager.draw_sliders()

    def draw_velocity_arrows_text(self):
        if settings.draw_velocity_arrows_mode:
            text = self.velocity_arrows_font.render("Drag an arrow from a planet to draw a velocity vector, unpause to apply", True, self.WHITE)  
        else:
            text = self.velocity_arrows_font.render("Press V to enable velocity vector mode", True, self.WHITE)
            

        self.screen.blit(text, (140, 10))

    def draw_planet_data_text(self):
        planet = self.to_display_data
        if not planet: return


        text_x = 10
        text_y = 80

        sig_figs = 7
        fields = ["mass", "radius", "x", "y", "vx", "vy", "ax", "ay"]
        text_to_render = []

        for field in fields:
            value = getattr(planet, field)
            formatted = first_sig_figs(value, sig_figs)
            text_to_render.append(f"{field}: {formatted}")
      
        for i in range(len(text_to_render)):
            line = text_to_render[i]
            rendered_text = self.planet_data_font.render(line, True, self.WHITE)
            self.screen.blit(rendered_text, (text_x, text_y + 20 * i))

    def draw_toggle_text(self):
        TOGGLE_X = 5

        toggle_list = [(settings.trails, "Trails (Z)"), (settings.collision_fx, "Collision FX (X)"), (settings.background_fx, "Background FX (C)")]

        for i in range(len(toggle_list)):
            toggle = toggle_list[i]
            if toggle[0]:
                toggle_text = self.toggle_font.render("%s ON" % toggle[1], True, self.GREEN)
            else:
                toggle_text = self.toggle_font.render("%s OFF" % toggle[1], True, self.RED)

            self.screen.blit(toggle_text, (TOGGLE_X, 25 + i * 15 ))

    def set_planet_to_display_data(self, planet):
        self.to_display_data = planet
        self.planet_manager.set_selected_planet(planet)




