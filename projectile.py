import pygame 
import math
import sys
pygame.init()
width = 800
height = 600
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption('Projectile Motion')
font = pygame.font.SysFont(None, 24)
clock = pygame.time.Clock()
fps = 60
pixel_to_meter = 100
gravity = 9.8
projectiles = []
def draw_text(text, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


class Projectile: 
    def __init__(self,x,y,speed,angle):
        self.x = x 
        self.y = y
        self.angle = math.radians(angle)
        self.vx = speed*math.cos(self.angle)
        self.vy = speed*math.sin(self.angle)

        self.time = 0
        self.trajectory = []

    def update(self,dt):
        self.time += dt 
        self.x = self.vx * self.time
        self.y = self.vy * self.time + 0.5 * gravity * self.time ** 2

        self.trajectory.append((self.x,self.y))

    def draw(self):
        pixeled_x = self.x * pixel_to_meter
        pixeled_y = height - (self.y * pixel_to_meter)

        pygame.draw.circle(screen,(250,0,0),(int(pixeled_x),int(pixeled_y)), 5)

        for point in self.trajectory:
            traj_x = point[0] * pixel_to_meter
            traj_y = height-(point[1]*pixel_to_meter)
            pygame.draw.circle(screen,(255,255,255),(int(traj_x), int(traj_y)), 2)

    

def get_user_input():
    input_active = True
    user_text = ''
    input_box = pygame.Rect(width//2 - 100, height//2 - 30, 200, 40)
    prompt = "Enter speed (m/s) and angle (degrees) separated by space: "
    speed = None
    angle = None
    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    try:
                        parts = user_text.strip().split()
                        if len(parts) != 2:
                            raise ValueError
                        speed = float(parts[0])
                        angle = float(parts[1])
                        input_active = False
                    except ValueError:
                        user_text=''
                elif event.key==pygame.K_BACKSPACE:
                    user_text=user_text[:-1]
                else:
                    user_text += event.unicode

        screen.fill((255,255,255))
        draw_text(prompt+user_text,(0,0,0), 50, height//2 - 10)
        pygame.display.flip()
        clock.tick(fps)

    return speed, angle
    

def main():
    running = True

    speed, angle = get_user_input()

    projectile = Projectile(0, 0, speed, angle)
    projectiles.append(projectile)

    while running:
        dt = clock.tick(fps) / 1000  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                x= mx / pixel_to_meter
                y= (height - my) / pixel_to_meter
                new_projectile = Projectile(x, y, speed, angle)
                projectiles.append(new_projectile)

        screen.fill((255,255,255))
        for proj in projectiles[:]:
            proj.update(dt)
            proj.draw()
            if proj.y < 0:
                projectiles.remove(proj)
        draw_text("Click to launch another projectile with the same speed and angle.", (0,0,0), 10, 10)
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()