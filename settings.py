# settings.py
class _Settings:
    def __init__(self):
        self.FPS = 90

        # Physics
        self.g = 200
        self.dt = 0.005
        self.scale = 1

        self.trails = True
        self.collision_fx = True
        self.paused = False
        
        # Simulation
        self.EPSILON = 1e-7 
        self.TRAIL_LENGTH = 200
        self.MERGE_ENERGY_LOSS = 1
        self.BOUNCE_ENERGY_LOSS = 1
        self.RANDOMNESS_IN_COLLISIONS = False
        
        # Display
        self.WIDTH, self.HEIGHT = 800, 800
        self.BG_COLOR = (0, 0, 0)


    def set_scale(self, value):
        if value <= 0:
            raise ValueError("Scale must be positive")
        self.scale = value

    def set_dt(self, value):
        if value <= 0:
            raise ValueError("DT must be positive")
        self.dt = value
    
    def toggle_trails(self):
        self.trails = not self.trails

    def toggle_collision_fx(self):
        self.collision_fx = not self.collision_fx
    
    def toggle_pause(self):
        self.paused = not self.paused


        

# Singleton instance - accessible everywhere
settings = _Settings()