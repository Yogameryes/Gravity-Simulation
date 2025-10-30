import pygame
import math

width = 1378
height = 768

RED = (255, 0, 0)
rectWidth = 50
rectHeight = 50

gravity = 1
retention = 0.9

pygame.init()
screen = pygame.display.set_mode((width, height))

clock = pygame.time.Clock()
fps = 60
running = True

# camera state
cam_x = 0.0   # world -> screen offset x (pixels)
cam_y = 0.0   # world -> screen offset y (pixels)
panning = False
pan_mouse_start = (0, 0)
pan_cam_start = (0.0, 0.0)


class Ball:
    def __init__(self, x_pos, y_pos, radius, color, mass, x_speed, y_speed):
        self.pos = [float(x_pos), float(y_pos)]
        self.color = color
        self.mass = mass
        # keep simulation velocities as floats
        self.speed = [float(x_speed), float(y_speed)]
        self.radius = int(radius)
        self.area = math.pi * (radius ** 2)
        # history of previous positions (world coordinates) for trail drawing
        self.history = []
        self.max_history = 600

    def update_pos(self):
        prev_posx = self.pos[0]
        prev_posy = self.pos[1]
        # store previous position in history (world coords)
        self.history.append((prev_posx, prev_posy))
        if len(self.history) > self.max_history:
            self.history.pop(0)
        # advance position by velocity (one simulation step per frame)
        self.pos[0] += self.speed[0]
        self.pos[1] += self.speed[1]

    def add_history(self, px, py):
        self.history.append((px, py))
        if len(self.history) > self.max_history:
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
    Ball(width / 2, height / 2, 4, (0, 0, 255), 21 * 10**12, 0, 0),
    Ball(width / 2 - 50, height / 2, 3, (23, 123, 52), 1 * 10**10, 0, 5),
    Ball(width / 2 - 50, height / 2, 3, (23, 123, 52), 1 * 10**10, 0, 5),
]

# simple font for HUD
font = pygame.font.SysFont(None, 20)

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
            j += 1
        i += 1

    # draw all Balls (trails and balls) with camera offset
    for b in Balls:
        b.draw(screen, cam_x=cam_x, cam_y=cam_y)

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()