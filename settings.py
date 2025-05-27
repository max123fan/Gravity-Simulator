G = 500
DT = 0.02
SCALE = 1
EPSILON = 1e-4 
TRAIL_LENGTH = 200

MERGE_ENERGY_LOSS = 0.7
BOUNCE_ENERGY_LOSS = 0.9
RANDOMNESS_IN_COLLISIONS = False

WIDTH, HEIGHT = 800, 800
BG_COLOR = (0, 0, 0)  # Black background

def cartesian_to_screen_coords(x, y):
    screen_x = round(x / SCALE + WIDTH / 2)
    screen_y = round(-y / SCALE + HEIGHT / 2)
    return screen_x, screen_y

def check_within_drawing_range(screen_x, screen_y, radius=0):
    return (-radius <= screen_x < WIDTH + radius) and (-radius <= screen_y < HEIGHT + radius)

