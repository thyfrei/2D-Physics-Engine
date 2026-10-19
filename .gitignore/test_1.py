import pygame as pg
import math

pg.init()

#Screen Dimentions 
screen = pg.display.set_mode((800,600)) #(weidth, Height)
pg.display.set_caption("Physics Engine")
#font
font = pg.font.Font(None, 142)
#clock
clock = pg.time.Clock()

#Deceting Collision
def checkCollision(ball_1, ball_2):
    dx = ball_1.x-ball_2.x
    dy = ball_1.y-ball_2.y

    dist = math.sqrt(dx**2 + dy**2)

    if (dist <= ball_1.radius+ball_2.radius):
        return True
    else:
        return False
    
#bouncing the ball
def resolveCollision(ball_1, ball_2, e):

    dx = ball_2.x - ball_1.x
    dy = ball_2.y - ball_1.y

    distance = math.sqrt(dx**2 + dy**2)

    # Avoid division by zero
    if distance == 0:
        return

    # Unit normal vector
    nx = dx / distance
    ny = dy / distance

    # Relative velocity
    rv_x = ball_2.v_x - ball_1.v_x
    rv_y = ball_2.v_y - ball_1.v_y

    # Relative velocity along the normal
    velocity_normal = rv_x * nx + rv_y * ny

    # If balls are moving apart, do nothing
    if velocity_normal >= 0:
        return

    # Calculate impulse
    j = -(1 + e) * velocity_normal
    j /= (1 / ball_1.mass + 1 / ball_2.mass)

    # Apply impulse to ball 1
    ball_1.v_x -= (j / ball_1.mass) * nx
    ball_1.v_y -= (j / ball_1.mass) * ny

    # Apply impulse to ball 2
    ball_2.v_x += (j / ball_2.mass) * nx
    ball_2.v_y += (j / ball_2.mass) * ny



    
#Structuring the Body (Ball)

class Ball():

    def __init__(self, x, y, v_x, v_y, r, m):
        self.x = x
        self.y = y
        self.v_x = v_x
        self.v_y = v_y
        self.radius = r
        self.mass = m

    #calculating change of position and velocity 

    def update(self, dt, e):
        self.v_y += 981*dt

        self.x += self.v_x*dt
        self.y += self.v_y*dt

        #bottom wall
        if (self.y +self.radius >= 600):
            self.y = 600 - self.radius
            self.v_y = -e* abs(self.v_y)
            self.v_x *= 0.98 #friction effect
        #top wall
        if (self.y-self.radius <=0):
            self.y = self.radius
            self.v_y = e* abs(self.v_y)
        #right wall
        if (self.x+self.radius >= 800):
            self.x = 800-self.radius
            self.v_x = -e* abs (self.v_x)
        #left wall
        if (self.x-self.radius <=0):
            self.x = self.radius
            self.v_x = e* abs(self.v_x)

#balls
            
ball_1 = Ball(200, 0, -200,10,10,1)
ball_2 = Ball(400, 10, 100,0,30,1)


running = True

while running:
    dt = clock.tick(60)/1000
    ball_1.update(dt,0.8)
    ball_2.update(dt,0.8)

    for event in pg.event.get():
        if event.type == pg.QUIT: #Is the current event a request to close the window?
            running = False

    screen.fill((25,40,25))
    #draw balls
    pg.draw.circle(screen, (255, 0, 0), (int(ball_1.x), int(ball_1.y)), ball_1.radius)
    pg.draw.circle(screen, (255, 100, 0), (int(ball_2.x), int(ball_2.y)), ball_2.radius)

    if checkCollision(ball_1, ball_2):
        resolveCollision(ball_1, ball_2, 0.8)

        text = font.render("Collided" , True, (246, 2, 1))
        screen.blit(text , (20,20))
    

    pg.display.flip()
    

pg.quit()
