import pygame as pg
import math

pg.init()

#Screen Dimentions 
screen = pg.display.set_mode((800,600)) #(weidth, Height)
pg.display.set_caption("Physics Engine")
#font
font = pg.font.Font(None, 42)
#clock
clock = pg.time.Clock()

button_rect = pg.Rect(325, 260, 150, 60)


#Deceting Collision
def checkCollision(ball_1, ball_2):
    dx = ball_1.x-ball_2.x
    dy = ball_1.y-ball_2.y

    dist = math.sqrt(dx**2 + dy**2)

    if (dist <= ball_1.radius+ball_2.radius):
        return True
    else:
        return False
#after collision effect, penetration, correction, impulse
def afterCollision(ball_1 ,ball_2,e):
    dx = ball_1.x-ball_2.x
    dy = ball_1.y-ball_2.y

    dist = math.sqrt(dx**2 + dy**2)

    if (dist==0):
        return
    #impulse (j) = (-(1+e)V_rel_n)/((1/m1)+(1/m2))
    #V_rel_n = v_rel along collision normal
    #normal unit vector (n):

    nx = dx/dist
    ny = dy/dist
    penetration = ball_1.radius+ball_2.radius-dist

    # penetration and correction
    if (penetration>0):
        correction = penetration/((1/ball_1.mass)+(1/ball_2.mass))

        ball_1.x += correction*(1/ball_1.mass)*nx
        ball_1.y += correction*(1/ball_1.mass)*ny

        ball_2.x -= correction*(1/ball_2.mass)*nx
        ball_2.y -= correction*(1/ball_2.mass)*ny

    #relative velocity
    v_rel_x = ball_1.v_x - ball_2.v_x
    v_rel_y = ball_1.v_y - ball_2.v_y

    #relative velocity along normal

    V_rel_nx = v_rel_x*nx
    V_rel_ny = v_rel_y*ny

    V_rel_n = V_rel_nx+V_rel_ny

    #in case of moving apart
    if (V_rel_n >=0):
        return
    #calculate impulse (j)

    j = -(1+e)*V_rel_n
    j /= (1/ball_1.mass)+(1/ball_2.mass)

    #applying impulse
    ball_1.v_x += (j/ball_1.mass)*nx
    ball_1.v_y += (j/ball_1.mass)*ny

    ball_2.v_x -= (j/ball_2.mass)*nx
    ball_2.v_y -= (j/ball_2.mass)*ny

    
#Structuring the Body (Ball), update parameters

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
            self.v_x *= 0.98**(dt*60) #friction effect
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
            
balls = [
    Ball(0, 0, -200, -400, 30, 5),
    Ball(90, 50, 120, 120, 25, 2.5),
    Ball(240, 30, 90, -100, 45, 4.5),
    Ball(400, 70, 170, -180, 30, 5),
    Ball(560, 0, 80, 75, 50, 7.5),
    Ball(740, 20, -220, 250, 10, 1),
]


running = True
simulation_started = False

while running:
    dt = clock.tick(60)/1000
    
    for event in pg.event.get():
        if event.type == pg.QUIT: #Is the current event a request to close the window?
            running = False

         # Start button click
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if button_rect.collidepoint(event.pos):
                    simulation_started = True
                    
    #do simulation only after click
    # if simulation_started:
    #     ball_1.update(dt,0.8)
    #     ball_2.update(dt,0.8)
        
    #     if checkCollision(ball_1, ball_2):
    #                 afterCollision(ball_1, ball_2, 0.8)
            
                    
    screen.fill((25,40,25))
    #draw balls
    for ball in balls:
        if simulation_started:
                ball.update(dt,0.8)

    for i in range (len(balls)):
        for j in range (i+1, len(balls)):
            ball_1 = balls[i]
            ball_2 = balls[j]

            if checkCollision(ball_1, ball_2):
                afterCollision(ball_1, ball_2, 0.88)
                text = font.render(f"Collided {i}&{j}" , True, (246, 2, 1))
                screen.blit(text , (20,20))
                            


                
                # if checkCollision(ball_1, ball_2):
                #             afterCollision(ball_1, ball_2, 0.8)
                    
                            # text = font.render("Collided" , True, (246, 2, 1))
                            # screen.blit(text , (20,20))

    for ball in balls:
        pg.draw.circle(screen, (255,150,0), (int(ball.x), int(ball.y)), ball.radius)


    #start button page

    if not simulation_started:
        pg.draw.rect(screen, (50, 150, 80), button_rect, border_radius=10)

        button_text = font.render(
            "START", True, (255, 255, 255)
        )
        values_text = font.render(
            "e = 0.8", True, (255,255,255)
        )

        text_rect = button_text.get_rect(
            center=button_rect.center
        )

        screen.blit(button_text, text_rect)
        screen.blit(values_text, (20, 60))


    pg.display.flip()
    

pg.quit()
