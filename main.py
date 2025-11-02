import pygame
import math

width = 1360
height = 768

RED = (255, 0, 0)
rectWidth = 50
rectHeight = 50

gravity = 1
retention = 0.9

pygame.init()
screen = pygame.display.set_mode((width, height))

clock = pygame.time.Clock()
fps=60
running = True

# trail settings (seconds). Set TRAIL_NEVER = True to keep trails forever.
TRAIL_SECONDS = 1
TRAIL_NEVER = True

# camera state
cam_x = 0.0   # world -> screen offset x (pixels)
cam_y = 0.0   # world -> screen offset y (pixels)
panning = False
pan_mouse_start = (0, 0)
pan_cam_start = (0.0, 0.0)


class Ball:
    def __init__(self, x_pos, y_pos, radius, color, mass, x_speed, y_speed, density, frag):
        self.pos = [float(x_pos), float(y_pos)]
        self.color = color
        self.base_color = color  # permanent default color used for resets
        self.mass = mass
        self.density = density
        self.frag = frag
        # keep simulation velocities as floats
        self.speed = [float(x_speed), float(y_speed)]
        self.radius = int(radius)
        self.area = math.pi * (radius ** 2)
        # history of previous positions (world coordinates) for trail drawing
        self.history = []
        # set max_history according to global TRAIL_SECONDS / TRAIL_NEVER
        self.update_max_history()

    def update_max_history(self):
        # set max_history to None for infinite history, or integer frames
        global TRAIL_SECONDS, TRAIL_NEVER, fps
        if TRAIL_NEVER:
            self.max_history = None
        else:
            # clamp to at least 0 frames (0 seconds means no history)
            frames = max(0, int(TRAIL_SECONDS * fps))
            self.max_history = frames

    def update_pos(self):
        prev_posx = self.pos[0]
        prev_posy = self.pos[1]
        # store previous position in history (world coords)
        self.history.append((prev_posx, prev_posy))
        # trim history only if max_history is set
        if self.max_history is not None:
            while len(self.history) > self.max_history:
                self.history.pop(0)
        # advance position by velocity (one simulation step per frame)
        self.pos[0] += self.speed[0]
        self.pos[1] += self.speed[1]

    def add_history(self, px, py):
        self.history.append((px, py))
        if self.max_history is not None and len(self.history) > self.max_history:
            self.history.pop(0)

    def draw(self, surface, cam_x=0.0, cam_y=0.0):
        # draw trail from history using camera offset
        if len(self.history) >= 2:
            points = [(int(px + cam_x), int(py + cam_y)) for (px, py) in self.history]
            pygame.draw.lines(surface, (255, 255, 255), False, points, 1)
        # draw ball at screen position
        screen_x = int(self.pos[0] + cam_x)
        screen_y = int(self.pos[1] + cam_y)
        pygame.draw.circle(surface, self.color, (screen_x, screen_y), self.radius)


Balls = [
    Ball(width / 2 , height / 2, 10, (255, 0, 0), 10 * 1e13, 0, 0, 10, False),
    Ball(width / 2 - 248, height / 2, 5, (0, 255, 0), 2 * 1e10, 0, -2.1, 1.3, False),
    Ball(width / 2 + 260, height / 2, 5, (0, 255, 0), 2 * 1e10, 0, 3, 1.4, False),

]

# ensure all balls have correct max_history at start
def apply_trail_settings_to_all():
    for b in Balls:
        b.update_max_history()

apply_trail_settings_to_all()

# simple font for HUD
font = pygame.font.SysFont(None, 20)

def set_trail_seconds(seconds):
    global TRAIL_SECONDS, TRAIL_NEVER
    TRAIL_NEVER = False
    TRAIL_SECONDS = max(0.0, float(seconds))
    apply_trail_settings_to_all()

def toggle_trail_never():
    global TRAIL_NEVER
    TRAIL_NEVER = not TRAIL_NEVER
    apply_trail_settings_to_all()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:

            running = False

        # camera panning with right mouse button
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:  # right click start pan
                panning = True
                pan_mouse_start = event.pos
                pan_cam_start = (cam_x, cam_y)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:  # right click release
                panning = False

        elif event.type == pygame.MOUSEMOTION:
            if panning:
                mx, my = event.pos
                sx, sy = pan_mouse_start
                dx = mx - sx
                dy = my - sy
                # update camera offset relative to when pan started
                cam_x = pan_cam_start[0] + dx
                cam_y = pan_cam_start[1] + dy

        elif event.type == pygame.KEYDOWN:
            # increase/decrease trail time
            if event.key in (pygame.K_PLUS, pygame.K_EQUALS, pygame.K_KP_PLUS):
                # increase by 1 second
                if TRAIL_NEVER:
                    # switch to finite first
                    toggle_trail_never()
                set_trail_seconds(TRAIL_SECONDS + 0.1)
            elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                if TRAIL_NEVER:
                    toggle_trail_never()
                set_trail_seconds(max(0.0, TRAIL_SECONDS - 0.1))
            elif event.key == pygame.K_n:
                toggle_trail_never()

    screen.fill("black")

    # update physics and positions
    i = 0
    while i < len(Balls):
        each = Balls[i]
        # update positions using current velocities
        each.update_pos()
        j = i + 1
        while j < len(Balls):
            other = Balls[j]
            dist_x = each.pos[0] - other.pos[0]
            dist_y = each.pos[1] - other.pos[1]
            distance = math.hypot(dist_x, dist_y)
            distance = max(distance, 2.0)

            G = 6.674e-11
            attraction = (G * each.mass * other.mass) / (distance * distance)

            # accelerations (apply equal & opposite)
            ax = (attraction / each.mass) * (dist_x / distance)
            ay = (attraction / each.mass) * (dist_y / distance)
            each.speed[0] -= ax
            each.speed[1] -= ay
            other.speed[0] += (attraction / other.mass) * (dist_x / distance)
            other.speed[1] += (attraction / other.mass) * (dist_y / distance)


            angleOfTangent = math.atan2(each.speed[0], each.speed[1]) * (180.0 / math.pi)

            hypotTangent = math.hypot(each.speed[0], each.speed[1])

            #Shows Tangent Line
            """ pygame.draw.line(screen, (0, 255, 0),
                             (int(each.pos[0] + cam_x), int(each.pos[1] + cam_y)),
                             (int(each.pos[0] + cam_x + math.sin(math.radians(angleOfTangent)) * hypotTangent * 10),
                              int(each.pos[1] + cam_y + math.cos(math.radians(angleOfTangent)) * hypotTangent * 10)), 2)
            """
            #Shows Line Between Centers
            """
            pygame.draw.line(screen, (150, 150, 150),
                             (int(each.pos[0] + cam_x), int(each.pos[1] + cam_y)),
                             (int(other.pos[0] + cam_x), int(other.pos[1] + cam_y)), 1) """
            
            #Roche Limit
            rocheLimit = each.radius * (2 * each.density / other.density) ** (1/3)
            pygame.draw.line(screen, (150, 150, 150),
                             (int(each.pos[0] + cam_x), int(each.pos[1] + cam_y)),
                             (int(each.pos[0] + rocheLimit + cam_x), int(each.pos[1] + cam_y)), 1)
            
            originalEachColor = each.color
            originalOtherColor = other.color
            
            
            
            


            # check for collision / merging
            if distance < each.radius + other.radius:
                # merge smaller into larger
                if each.mass >= other.mass:
                    each.mass += other.mass
                    each.area += other.area
                    each.radius = int(math.sqrt(each.area / math.pi))
                    Balls.pop(j)
                    continue  # don't increment j, list shifted
                else:
                    other.mass += each.mass
                    other.area += each.area
                    other.radius = int(math.sqrt(other.area / math.pi))
                    Balls.pop(i)
                    i -= 1  # compensate for outer increment below
                    break  # current 'each' removed; stop inner loop

            # flash green while inside Roche limit; otherwise reset to base_color
            if other.frag == False:
                if distance < rocheLimit:
                    other.color = (0, 255, 0)
                    if other.speed[0] > other.speed[1]:
                        for k in range(10):
                            Balls.append(Ball(other.pos[0] + k + 10 + (other.radius/10), other.pos[1], 1, other.base_color, other.mass/10, other.speed[0], other.speed[1], other.density, True))

                        Balls.pop(j)
                    else:
                        for k in range(10):
                            Balls.append(Ball(other.pos[0], other.pos[1] + k + 10 + (other.radius/10), 1, other.base_color, other.mass/10, other.speed[0], other.speed[1], other.density, True))

                        Balls.pop(j)
                else:
                    other.color = other.base_color

            j += 1
        i += 1

    # draw all Balls (trails and balls) with camera offset
    for b in Balls:
        b.draw(screen, cam_x=cam_x, cam_y=cam_y)

    # HUD: trail info and controls
    if TRAIL_NEVER:
        trail_text = "Trail: Forever (press N to toggle)"
    else:
        trail_text = f"Trail: {TRAIL_SECONDS:.0f}s  (+/- to change, N toggles Forever)"
    surf = font.render(trail_text, True, (255, 255, 255))
    screen.blit(surf, (8, 8))

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
