import time

import pygame
pygame.init()

import matplotlib.pyplot as plt

from ncap import NCap
ncap = NCap('/dev/ttyACM0', baud_rate=115200)

from ball import Ball
from brick import Brick
from paddle import Paddle
from themes import *

def run_game():
    global ncap
    score = 0
    lives = 5
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
    while carryOn:
        res_code_x, res_x = ncap.read_value(ncap.Y_CHANN)
        if res_code_x == 0:
            Exception("Error: Could not read Y channel")

        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                carryOn = False # Flag that we are done so we exit this loop

        paddle.move(res_x[0])

        all_sprites_list.update()

        if ball.rect.x>=790:
            ball.vel_x = -ball.vel_x
        if ball.rect.x<=0:
            ball.vel_x = -ball.vel_x
        if ball.rect.y>590:
            ball.vel_y = -ball.vel_y
            lives -= 1
            if lives == 0:
                font = pygame.font.Font(None, 74)
                text = font.render("GAME OVER", 1, WHITE)
                screen.blit(text, (250,300))
                pygame.display.flip()
                pygame.time.wait(1500)

                carryOn=False

        # Detect collisions between the ball and the top of the screen
        if ball.rect.y<40:
            ball.vel_y = -ball.vel_y

        # Detect collisions between the ball and the paddles
        if pygame.sprite.collide_mask(ball, paddle):
            ball.rect.x -= ball.vel_x
            ball.rect.y -= ball.vel_y
            ball.bounce()

        # Check if there is the ball collides with any of bricks
        brick_collision_list = pygame.sprite.spritecollide(ball,all_bricks,False)
        for brick in brick_collision_list:
            ball.bounce()
            score += 1
            brick.kill()
            if len(all_bricks)==0:
                font = pygame.font.Font(None, 74)
                text = font.render("CONGRATULATIONS, YOU WIN!", 1, WHITE)
                screen.blit(text, (200,300))
                pygame.display.flip()
                pygame.time.wait(1500)

                carryOn=False

        screen.fill(DARKBLUE)
        pygame.draw.line(screen, WHITE, [0, 38], [800, 38], 2)

        font = pygame.font.Font(None, 34)
        text = font.render("Score: " + str(score), 1, WHITE)
        screen.blit(text, (20,10))
        text = font.render("Lives: " + str(lives), 1, WHITE)
        screen.blit(text, (650,10))

        all_sprites_list.draw(screen)

        pygame.display.flip()

        clock.tick(60)

        iterations += 1

    print("Time taken: ", time.time() - start)
    print("Frequency: ", iterations/(time.time() - start), "Hz")


def run_menu():
    global display_menu, keep_going, ncap

    size = (WIDTH, HEIGHT)

    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Advanced Instrumentation: Breakout Game")

    # The loop will carry on until the user exits the game (e.g. clicks the close button).
    carryOn = True

    # The clock will be used to control how fast the screen updates
    clock = pygame.time.Clock()
    start = time.time()
    iterations = 0
    colors = [RED, WHITE]
    btn_colors = [0, 1]
    read_A = False
    while carryOn:
        res_code , res = ncap.read_value(ncap.BTN_D_CHANN)
        if res_code == 0:
            raise Exception("Could not read Button D.")
        if res[0] == 0:
            btn_colors = [0, 1]
        res_code , res = ncap.read_value(ncap.BTN_B_CHANN)
        if res_code == 0:
            raise Exception("Could not read Button B.")
        if res[0] == 0:
            btn_colors = [1, 0]
        res_code , res = ncap.read_value(ncap.BTN_A_CHANN)
        if res_code == 0:
            raise Exception("Could not read Button A.")
        if res[0] == 0:
            read_A = True

        if read_A and btn_colors == [0, 1]:
            display_menu = GAME_MEMU
            return True
        elif read_A and btn_colors == [1, 0]:
            display_menu = TEDS_MEMU
            return True


        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                carryOn = False # Flag that we are done so we exit this loop
                keep_going = False

        screen.fill(DARKBLUE)

        font = pygame.font.Font(None, 34)
        pygame.draw.rect(screen, BLACK, pygame.Rect(WIDTH//2 - 150, 200, 300, 60))
        pygame.draw.rect(screen, BLACK, pygame.Rect(WIDTH//2 - 150, 300, 300, 60))
        text = font.render("Play Game", 1, colors[btn_colors[0]])
        screen.blit(text, (WIDTH//2 - text.get_rect().width//2, 200 + 30 - text.get_rect().height//2))
        text = font.render("TEDS", 1, colors[btn_colors[1]])
        screen.blit(text, (WIDTH//2 - text.get_rect().width//2, 300 + 30 - text.get_rect().height//2))

        pygame.display.flip()
        clock.tick(60)
        iterations += 1


def run_teds():
    global display_menu, ncap

    size = (WIDTH, HEIGHT)

    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Advanced Instrumentation: Breakout Game")

    # The loop will carry on until the user exits the game (e.g. clicks the close button).
    carryOn = True

    # The clock will be used to control how fast the screen updates
    clock = pygame.time.Clock()
    iterations = 0
    colors = [RED, WHITE]
    btn_colors = [0, 1, 1, 1, 1, 1, 1, 1, 1]
    read_A = False
    while carryOn:
        time.sleep(0.13)
        res_code , res = ncap.read_value(ncap.BTN_B_CHANN)
        if res_code == 0:
            raise Exception("Could not read Button B.")
        if res[0] == 0:
            i = btn_colors.index(0)
            if i + 1 < 9:
                btn_colors[i], btn_colors[i+1] = btn_colors[i+1], btn_colors[i]
        res_code , res = ncap.read_value(ncap.BTN_D_CHANN)
        if res_code == 0:
            raise Exception("Could not read Button D.")
        if res[0] == 0:
            i = btn_colors.index(0)
            if i > 0:
                btn_colors[i], btn_colors[i-1] = btn_colors[i-1], btn_colors[i]
        res_code , res = ncap.read_value(ncap.BTN_C_CHANN)
        if res_code == 0:
            raise Exception("Could not read Button C.")
        if res[0] == 0:
            display_menu = MAIN_MENU
            return True
        res_code , res = ncap.read_value(ncap.BTN_A_CHANN)
        if res_code == 0:
            raise Exception("Could not read Button A.")
        if res[0] == 0:
            read_A = True

        if read_A:
            read_A = False
            if btn_colors == [0, 1, 1, 1, 1, 1, 1, 1, 1]:
                res_code, res = ncap.read_meta()
                if res_code == 0:
                    raise Exception("Could not read META TEDS.")
                print("META TEDS: ", res)
            else:
                i = btn_colors.index(0)
                res_code, res = ncap.read_tc(ncap.channels[i-1])
                if res_code == 0:
                    raise Exception(f"Could not read TC TEDS {i}.")
                print(f"TC {i-1} TEDS: ", res)


        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                carryOn = False # Flag that we are done so we exit this loop

        screen.fill(DARKBLUE)

        font = pygame.font.Font(None, 34)

        pygame.draw.rect(screen, BLACK, pygame.Rect(WIDTH//2 - 250, 100, 500, 60))
        text = font.render("META TEDS", 1, colors[btn_colors[0]])
        screen.blit(text, (WIDTH//2 - text.get_rect().width//2, 100 + 30 - text.get_rect().height//2))

        pygame.draw.rect(screen, BLACK, pygame.Rect(WIDTH//2 - 250, 180, 150, 60))
        text = font.render("TC 0", 1, colors[btn_colors[1]])
        screen.blit(text, (WIDTH//2 -250 +75 - text.get_rect().width//2, 180 + 30 - text.get_rect().height//2))
        
        pygame.draw.rect(screen, BLACK, pygame.Rect(WIDTH//2 - 75, 180, 150, 60))
        text = font.render("TC 1", 1, colors[btn_colors[2]])
        screen.blit(text, (WIDTH//2 -75 +75 - text.get_rect().width//2, 180 + 30 - text.get_rect().height//2))
        
        pygame.draw.rect(screen, BLACK, pygame.Rect(WIDTH//2 + 100, 180, 150, 60))
        text = font.render("TC 2", 1, colors[btn_colors[3]])
        screen.blit(text, (WIDTH//2 + 100 +75 - text.get_rect().width//2, 180 + 30 - text.get_rect().height//2))
        
        pygame.draw.rect(screen, BLACK, pygame.Rect(WIDTH//2 - 250, 265, 150, 60))
        text = font.render("TC 3", 1, colors[btn_colors[4]])
        screen.blit(text, (WIDTH//2 -250 +75 - text.get_rect().width//2, 265 + 30 - text.get_rect().height//2))
        
        pygame.draw.rect(screen, BLACK, pygame.Rect(WIDTH//2 - 75, 265, 150, 60))
        text = font.render("TC 4", 1, colors[btn_colors[5]])
        screen.blit(text, (WIDTH//2 -75 +75 - text.get_rect().width//2, 265 + 30 - text.get_rect().height//2))
        
        pygame.draw.rect(screen, BLACK, pygame.Rect(WIDTH//2 + 100, 265, 150, 60))
        text = font.render("TC 5", 1, colors[btn_colors[6]])
        screen.blit(text, (WIDTH//2 + 100 +75 - text.get_rect().width//2, 265 + 30 - text.get_rect().height//2))
        
        pygame.draw.rect(screen, BLACK, pygame.Rect(WIDTH//2 - 250 + 87, 350, 150, 60))
        text = font.render("TC 6", 1, colors[btn_colors[7]])
        screen.blit(text, (WIDTH//2 - 250 + 87 + 75 - text.get_rect().width//2, 350 + 30 - text.get_rect().height//2))
        
        pygame.draw.rect(screen, BLACK, pygame.Rect(WIDTH//2 - 250 + 87 + 150 + 25, 350, 150, 60))
        text = font.render("TC 7", 1, colors[btn_colors[8]])
        screen.blit(text, (WIDTH//2 + 87 - text.get_rect().width//2, 350 + 30 - text.get_rect().height//2))

        text = font.render("C: Back", 1, WHITE)
        screen.blit(text, (WIDTH - text.get_rect().width - 10, HEIGHT - text.get_rect().height - 10))

        pygame.display.flip()
        clock.tick(60)
        iterations += 1

MAIN_MENU = 0
GAME_MEMU = 1
TEDS_MEMU = 2

keep_going = True
display_menu = MAIN_MENU

while keep_going:
    if display_menu == MAIN_MENU:
        ncap.write_value(ncap.LED_5_CHANN, b'\xff')
        time.sleep(0.3)
        run_menu()
        ncap.write_value(ncap.LED_5_CHANN, b'\x00')

    elif display_menu == GAME_MEMU:
        ncap.write_value(ncap.LED_6_CHANN, b'\xff')
        time.sleep(0.3)
        run_game()
        ncap.write_value(ncap.LED_6_CHANN, b'\x00')
        display_menu = MAIN_MENU

    elif display_menu == TEDS_MEMU:
        ncap.write_value(ncap.LED_7_CHANN, b'\xff')
        time.sleep(0.3)
        run_teds()
        ncap.write_value(ncap.LED_7_CHANN, b'\x00')
        display_menu = MAIN_MENU
pygame.quit()