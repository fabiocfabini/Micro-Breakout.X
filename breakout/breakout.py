import time

import pygame
import matplotlib.pyplot as plt

from ncap import NCap
from ball import Ball
from brick import Brick
from paddle import Paddle
from themes import *

fig1 = plt.figure(num='DORMANT')

fig1.canvas.manager.set_window_title('Signals')
fig1.suptitle('Sensors data', fontsize=20)

ax1 = fig1.add_subplot(111)
ax1.set_xlabel('x label')

N = 500
val_x = []
val_y = []
val_s = []

pygame.init()
ncap = NCap('/dev/ttyACM2', baud_rate=115200)

WIDTH, HEIGHT = 800, 600

score = 0
lives = 3
size = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Advanced Instrumentation: Breakout Game")

# List to hold all the sprites
all_sprites_list = pygame.sprite.Group()

# Create paddle Instance
paddle = Paddle(LIGHTBLUE, 100, 10)
paddle.rect.x = 350
paddle.rect.y = 560

# Create ball Instance
ball = Ball(WHITE,12,12)
ball.rect.x = 345
ball.rect.y = 195

all_bricks = pygame.sprite.Group()
for i in range(7):
    brick = Brick(RED,80,30)
    brick.rect.x = 60 + i* 100
    brick.rect.y = 60
    all_sprites_list.add(brick)
    all_bricks.add(brick)
for i in range(7):
    brick = Brick(ORANGE,80,30)
    brick.rect.x = 60 + i* 100
    brick.rect.y = 100
    all_sprites_list.add(brick)
    all_bricks.add(brick)
for i in range(7):
    brick = Brick(YELLOW,80,30)
    brick.rect.x = 60 + i* 100
    brick.rect.y = 140
    all_sprites_list.add(brick)
    all_bricks.add(brick)

# Add the paddle and the ball to the list of sprites
all_sprites_list.add(paddle)
all_sprites_list.add(ball)

# The loop will carry on until the user exits the game (e.g. clicks the close button).
carryOn = True

# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()
start = time.time()
iterations = 0
# -------- Main Program Loop -----------
while carryOn:
    # ------- Read data from the sensor
    res_code_x, res_x = ncap.read_value(ncap.X_CHANN)
    if res_code_x != 0:
        val_x.append(res_x[0])
    else:
        raise Exception("Error: Could not read X channel")

    # --- Main event loop
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            carryOn = False # Flag that we are done so we exit this loop

    # --- Move Paddle
    paddle.move(val_x[-1])

    # --- Game logic should go here
    all_sprites_list.update()

    #Check if the ball is bouncing against any of the 4 walls:
    if ball.rect.x>=790:
        ball.vel_x = -ball.vel_x
    if ball.rect.x<=0:
        ball.vel_x = -ball.vel_x
    if ball.rect.y>590:
        ball.vel_y = -ball.vel_y
        lives -= 1
        if lives == 0:
            #Display Game Over Message for 3 seconds
            font = pygame.font.Font(None, 74)
            text = font.render("GAME OVER", 1, WHITE)
            screen.blit(text, (250,300))
            pygame.display.flip()
            pygame.time.wait(3000)

            #Stop the Game
            carryOn=False

    if ball.rect.y<40:
        ball.vel_y = -ball.vel_y

    #Detect collisions between the ball and the paddles
    if pygame.sprite.collide_mask(ball, paddle):
        ball.rect.x -= ball.vel_x
        ball.rect.y -= ball.vel_y
        ball.bounce()

    #Check if there is the ball collides with any of bricks
    brick_collision_list = pygame.sprite.spritecollide(ball,all_bricks,False)
    for brick in brick_collision_list:
        ball.bounce()
        score += 1
        brick.kill()
        if len(all_bricks)==0:
            #Display Level Complete Message for 3 seconds
            font = pygame.font.Font(None, 74)
            text = font.render("LEVEL COMPLETE", 1, WHITE)
            screen.blit(text, (200,300))
            pygame.display.flip()
            pygame.time.wait(3000)

            #Stop the Game
            carryOn=False

    # --- Drawing code should go here
    # First, clear the screen to dark blue.
    screen.fill(DARKBLUE)
    pygame.draw.line(screen, WHITE, [0, 38], [800, 38], 2)

    #Display the score and the number of lives at the top of the screen
    font = pygame.font.Font(None, 34)
    text = font.render("Score: " + str(score), 1, WHITE)
    screen.blit(text, (20,10))
    text = font.render("Lives: " + str(lives), 1, WHITE)
    screen.blit(text, (650,10))

    #Now let's draw all the sprites in one go. (For now we only have 2 sprites!)
    all_sprites_list.draw(screen)

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

    iterations += 1
#Once we have exited the main program loop we can stop the game engine:
pygame.quit()

print("Time taken: ", time.time() - start)
print("Frequency: ", iterations/(time.time() - start), "Hz")

ax1.cla()
ax1.plot(val_x, "r", label="$x$")
ax1.plot(val_y, "b", label="$y$")
ax1.plot(val_s, "k", label="$s$")
ax1.legend()
plt.show()