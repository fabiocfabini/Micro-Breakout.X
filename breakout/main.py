import sys
import time

import pygame
pygame.init()

from ncap import NCap
from ball import Ball
from brick import Brick
from paddle import Paddle
from inputbox import InputBox
from themes import *


def run_game():
    global ncap

    # Initialize the screen
    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Advanced Instrumentation: Breakout Game")

    # List to hold all the sprites
    all_sprites_list = pygame.sprite.Group()

    # Create paddle Instance
    paddle = Paddle(LIGHTBLUE, 100, 10, REST_VALUE)
    paddle.rect.x = 350
    paddle.rect.y = 560

    # Create ball Instance
    ball = Ball(WHITE,12,12)
    ball.rect.x = 345
    ball.rect.y = 195

    # Create the bricks
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

    # Set the score and lives
    score = 0
    lives = 5

    # The loop will carry on until the user exits the game (e.g. clicks the close button).
    carryOn = True

    # The clock will be used to control how fast the screen updates
    clock = pygame.time.Clock()
    start = time.time()
    iterations = 0
    while carryOn:
        # Read a signal from the Y channel of the sensor
        res_code_x, res_x = ncap.read_value(ncap.Y_CHANN)
        if res_code_x == 0:
            Exception("Error: Could not read Y channel")

        for event in pygame.event.get(): # Loop through all the events
            if event.type == pygame.QUIT: # If user clicked close, set carryOn to False
                carryOn = False

        # Move the paddle
        paddle.move(res_x[0])

        # Update all the objects in the window
        all_sprites_list.update()

        # Check if the ball is bouncing against any of the 4 walls:
        if ball.rect.x>=790:
            ball.vel_x = -ball.vel_x
        if ball.rect.x<=0:
            ball.vel_x = -ball.vel_x
        if ball.rect.y>590: # If the ball is below the screen
            ball.vel_y = -ball.vel_y
            lives -= 1 # Lose a life
            pygame.mixer.music.play(start=1)
            if lives == 0: # Game over
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
            GOOD_HIT.play()
            ball.bounce()
            score += 1
            brick.kill()
            if len(all_bricks)==0:
                font = pygame.font.Font(None, 74)
                text = font.render("CONGRATULATIONS, YOU WIN!", 1,  WHITE)
                screen.blit(text, (WIDTH/2-text.get_rect().width//2,  HEIGHT/2-text.get_rect().height//2))
                pygame.display.flip()
                pygame.time.wait(1500)

                carryOn=False

        screen.fill(DARKBLUE)   # Fill the screen with Dark Blue
        pygame.draw.line(screen, WHITE, [0, 38], [800, 38], 2)  # Draw the line at the top of the screen    

        font = pygame.font.Font(None, 34)   # Display the score and the number of lives at the top of the screen
        text = font.render("Score: " + str(score), 1, WHITE)
        screen.blit(text, (20,10))
        text = font.render("Lives: " + str(lives), 1, WHITE)
        screen.blit(text, (650,10))

        # Draw all the objects in the window
        all_sprites_list.draw(screen)

        # Refresh the screen
        pygame.display.flip()

        # Limit to 60 frames per second
        # This will limit the loop to run at most 60 times per second.
        clock.tick(60)
        iterations += 1

    # Log the time taken
    end = time.time()
    print("Game:")
    print("Time taken: ", end - start)
    print("Frequency: ", iterations/(end - start), "Hz")


def run_menu():
    global display_menu, keep_going, ncap

    # Initialize the screen
    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Advanced Instrumentation: Breakout Game")

    # The loop will carry on until the user exits the game (e.g. clicks the close button).
    carryOn = True

    colors = [RED, WHITE]
    btn_colors = [0, 1, 1]

    read_A = False
    read_C = False
    values_read = {"A": 1, "B": 1, "C": 1, "D": 1}

    iterations = 0
    start = time.time()
    while carryOn:
        # i(index in iterable), button(Name of button), value_read(Last value read)
        for i, (button, value_read) in enumerate(values_read.items()):
            res_code , res = ncap.read_value(ncap.channels[i+1])    # Read value from channel
            if res_code == 0:
                raise Exception(f"Could not read Button {button}.")
            if button == "A" and res[0] == 0 and value_read == 1:   # If button A is pressed, set read_A flag
                read_A = True
            if button == "B" and res[0] == 0 and value_read == 1:   # If button B is pressed, highlight next button
                zero_idx = btn_colors.index(0)
                if zero_idx + 1 < 3:
                    btn_colors[zero_idx], btn_colors[zero_idx+1] = btn_colors[zero_idx+1], btn_colors[zero_idx]
            if button == "C" and res[0] == 0 and value_read == 1:   # If button C is pressed, set read_C flag
                read_C = True
            if button == "D" and res[0] == 0 and value_read == 1:   # If button D is pressed, highlight previous button
                zero_idx = btn_colors.index(0)
                if zero_idx > 0:
                    btn_colors[zero_idx], btn_colors[zero_idx-1] = btn_colors[zero_idx-1], btn_colors[zero_idx]
            values_read[button] = res[0]    # Update value read for button

        if read_A and btn_colors == [0, 1, 1]:      # If button A is pressed and button PLAY is highlighted, start game
            display_menu = GAME_MEMU
            break
        elif read_A and btn_colors == [1, 0, 1]:    # If button A is pressed and button TEDS is highlighted, start TEDS menu
            display_menu = TEDS_MEMU
            break
        elif read_A and btn_colors == [1, 1, 0]:    # If button A is pressed and button OPTIONS is highlighted, exit game
            display_menu = OPTS_MEMU
            break
        elif read_C:                                # If button C is pressed, exit
            keep_going = False
            break

        for event in pygame.event.get(): # Loop through all the events
            if event.type == pygame.QUIT: # If user clicked close
                carryOn = False
                keep_going = False

        screen.fill(DARKBLUE) # Fill the screen with DARK BLUE

        font = pygame.font.Font(None, 34)   # Create font

        # Draw buttons
        pygame.draw.rect(screen,  BLACK, pygame.Rect(WIDTH//2 - 150, 200, 300, 60))
        pygame.draw.rect(screen,  BLACK, pygame.Rect(WIDTH//2 - 150, 300, 300, 60))
        pygame.draw.rect(screen,  BLACK, pygame.Rect(WIDTH//2 - 150, 400, 300, 60))
        text = font.render("PLAY", 1, colors[btn_colors[0]])
        screen.blit(text, (WIDTH//2 - text.get_rect().width//2, 200 + 30 - text.get_rect().height//2))
        text = font.render("TEDS", 1, colors[btn_colors[1]])
        screen.blit(text, (WIDTH//2 - text.get_rect().width//2, 300 + 30 - text.get_rect().height//2))
        text = font.render("OPTIONS", 1, colors[btn_colors[2]])
        screen.blit(text, (WIDTH//2 - text.get_rect().width//2, 400 + 30 - text.get_rect().height//2))

        # refresh screen
        pygame.display.flip()
        iterations += 1

    # Log the time taken
    end = time.time()
    print("MENU:")
    print("Time taken: ", end - start)
    print("Frequency: ", iterations/(end - start), "Hz")


def run_teds():
    global display_menu, ncap

    # Initialize the game engine
    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Advanced Instrumentation: Breakout Game")

    # The loop will carry on until the user exits the game (e.g. clicks the close button).
    carryOn = True

    # Create the input boxes
    value_box = InputBox(WIDTH//2 - 250 + 350 + 100, 40 + 100, 50, 50)
    channel_box = InputBox(WIDTH//2 - 250 + 150, 40 + 100, 50, 50)
    input_boxes = [channel_box, value_box]

    read_A = False
    read_C = False
    values_read = {"A": 1, "B": 1, "C": 1, "D": 1}

    colors = [RED, WHITE]
    btn_colors = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    iterations = 0
    start = time.time()
    while carryOn:
        # i(index in iterable), button(Name of button), value_read(Last value read)
        for i, (button, value_read) in enumerate(values_read.items()):
            res_code , res = ncap.read_value(ncap.channels[i+1])    # Read value from channel
            if res_code == 0:
                raise Exception(f"Could not read Button {button}.")
            if button == "A" and res[0] == 0 and value_read == 1:   # If button A is pressed, set read_A flag
                read_A = True
            if button == "B" and res[0] == 0 and value_read == 1:   # If button B is pressed, highlight next button
                zero_idx = btn_colors.index(0)
                if zero_idx + 1 < 12:
                    btn_colors[zero_idx], btn_colors[zero_idx+1] = btn_colors[zero_idx+1], btn_colors[zero_idx]
            if button == "C" and res[0] == 0 and value_read == 1:   # If button C is pressed, set read_C flag
                read_C = True
            if button == "D" and res[0] == 0 and value_read == 1:   # If button D is pressed, highlight previous button
                zero_idx = btn_colors.index(0)
                if zero_idx > 0:
                    btn_colors[zero_idx], btn_colors[zero_idx-1] = btn_colors[zero_idx-1], btn_colors[zero_idx]
            values_read[button] = res[0]    # Update value read for button

        if read_A:  # If button A is pressed, highlight button
            read_A = False
            i = btn_colors.index(0)
            if i == 0:  # Send Meta Teds
                res_code, res = ncap.read_meta()
                if res_code == 0:
                    raise Exception("Could not read META TEDS.")
                ncap.display_meta(res)
            elif i == 1 and channel_box.text != "": # send Read Command
                res_code, res = ncap.read_value(int.to_bytes(int(channel_box.text), length=1, byteorder="big"))
                if res_code == 0:
                    print(f"Could not read Channel {int(channel_box.text)}.")
                else: ncap.display_response(res, title=f"READ CHANNEL {int(channel_box.text)}")
            elif i == 2 and channel_box.text != "" and value_box.text != "": # send Write Command
                res_code, res = ncap.write_value(int.to_bytes(int(channel_box.text), length=1, byteorder='big'), int.to_bytes(int(value_box.text), length=1, byteorder='big'))
                if res_code == 0:
                    print(f"Could not write to Channel {int(channel_box.text)}.")
                else: ncap.display_response(res, title=f"WRITE {int(value_box.text)} CHANNEL {int(channel_box.text)}")
            elif i > 2:  # Send TC TEDS
                res_code, res = ncap.read_tc(ncap.channels[i-2-1])
                if res_code == 0:
                    raise Exception(f"Could not read TC TEDS {i-2}.")
                ncap.display_tc(res, str(i-2-1))
        if read_C:  # If button C is pressed, return to main menu
            read_C = False
            carryOn = False

        for event in pygame.event.get(): # Loop through the events
            if event.type == pygame.QUIT: # If user clicked close, stop the loop
                carryOn = False
            for box in input_boxes: # If user clicked on input_box or pressed a key, handle it
                box.handle_event(event)

        screen.fill(DARKBLUE) # Fill the screen with Dark Blue

        font = pygame.font.Font(None, 34)   # Create font

        # Draw buttons
        pygame.draw.rect(screen,  LIGHTBLUE, pygame.Rect(WIDTH//2 - 250, 50, 500, 60))
        text = font.render("META TEDS", 1, colors[btn_colors[0]])
        screen.blit(text, (WIDTH//2 - text.get_rect().width//2, 50 + 30 - text.get_rect().height//2))

        text = font.render("CHANNEL:", 1, WHITE)
        screen.blit(text, (WIDTH//2 - 250, 50 + 100))

        text = font.render("VALUE:  ", 1, WHITE)
        screen.blit(text, (WIDTH//2 - 250 + 320, 50 + 100))

        pygame.draw.rect(screen,  LIGHTBLUE, pygame.Rect(WIDTH//2 - 250 + 50, 200, 170, 60))
        text = font.render("READ", 1, colors[btn_colors[1]])
        screen.blit(text, (WIDTH//2 - 250 + 50 + 170 / 2 - text.get_rect().width//2, 200 + 30 - text.get_rect().height//2))

        pygame.draw.rect(screen,  LIGHTBLUE, pygame.Rect(WIDTH//2 + 250 - 170 - 50, 200, 170, 60))
        text = font.render("WRITE", 1, colors[btn_colors[2]])
        screen.blit(text, (WIDTH//2 + 250 - 170 - 50 + 170 / 2 - text.get_rect().width//2, 200 + 30 - text.get_rect().height//2))

        for col in range(2):
            for row in range(4):
                pygame.draw.rect(screen,  LIGHTBLUE, pygame.Rect(30 + row*170 + 20*row, 300 + 100 * col, 170, 60))
                text = font.render(f"TC {row + col*4}", 1, colors[btn_colors[row + col*4 + 3]])
                screen.blit(text, (30 + row*170 + 20*row + 170 / 2 - text.get_rect().width//2, 300 + 100 * col + 30 - text.get_rect().height//2))

        pygame.draw.rect(screen,  LIGHTBLUE, pygame.Rect(WIDTH//2 - 170//2, 500-30, 170, 60))
        text = font.render(f"TC 8", 1, colors[btn_colors[11]])
        screen.blit(text, (WIDTH//2 - text.get_rect().width//2, 500-30+30 - text.get_rect().height//2))

        # Draw instructions
        inst_labels = ["A: CLICK", "D: UP   ", "B: DOWN ", "C: Back "]
        for i, label in enumerate(inst_labels):
            text = font.render(label, 1, WHITE)
            screen.blit(text, (30 + i*190 + i*20, HEIGHT - text.get_rect().height - 10))

        # Draw input boxes
        for box in input_boxes:
                box.draw(screen)

        # Update the screen
        pygame.display.flip()
        iterations += 1

    # Log the time taken
    end = time.time()
    print("Teds:")
    print("Time taken: ", end - start)
    print("Frequency: ", iterations/(end - start), "Hz")


def run_opts():
    global display_menu, ncap

    # Initialize the game engine
    size = (WIDTH,  HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Advanced Instrumentation: Breakout Game")

    # The loop will carry on until the user exits the game (e.g. clicks the close button).
    carryOn = True

    iterations = 0
    btn_colors = [0, 1, 1]
    colors = [RED,  WHITE]
    read_A = False
    read_C = False
    values_read = {"A": 1, "B": 1, "C": 1, "D": 1}
    start = time.time()
    while carryOn:
        # i(index in iterable), button(Name of button), value_read(Last value read)
        for i, (button, value_read) in enumerate(values_read.items()):
            res_code , res = ncap.read_value(ncap.channels[i+1])    # Read value from channel
            if res_code == 0:
                raise Exception(f"Could not read Button {button}.")
            if button == "A" and res[0] == 0 and value_read == 1:   # If button A is pressed, set read_A flag
                read_A = True
            if button == "B" and res[0] == 0 and value_read == 1:   # If button B is pressed, highlight next button
                zero_idx = btn_colors.index(0)
                if zero_idx + 1 < 3:
                    btn_colors[zero_idx], btn_colors[zero_idx+1] = btn_colors[zero_idx+1], btn_colors[zero_idx]
            if button == "C" and res[0] == 0 and value_read == 1:   # If button C is pressed, set read_C flag
                read_C = True
            if button == "D" and res[0] == 0 and value_read == 1:   # If button D is pressed, highlight previous button
                zero_idx = btn_colors.index(0)
                if zero_idx > 0:
                    btn_colors[zero_idx], btn_colors[zero_idx-1] = btn_colors[zero_idx-1], btn_colors[zero_idx]
            values_read[button] = res[0]    # Update value read for button

        j = btn_colors.index(0) # Get index of highlighted button
        if read_A:  # If read_A flag is set
            read_A = False
            if j == 0:      # If highlighted button is background music, increase volume
                BACKGROUND.set_volume(min(BACKGROUND.get_volume() + 0.1, 1))
            elif j == 1:    # If highlighted button is good hit sound, increase volume
                GOOD_HIT.set_volume(min(GOOD_HIT.get_volume() + 0.1, 1))
                GOOD_HIT.play()
            elif j == 2:    # If highlighted button is game music, increase volume
                pygame.mixer.music.set_volume(min(pygame.mixer.music.get_volume() + 0.1, 1))
                pygame.mixer.music.play(start=1)
        elif read_C:        # If read_C flag is set
            read_C = False
            if j == 0:      # If highlighted button is background music, decrease volume
                BACKGROUND.set_volume(max(BACKGROUND.get_volume() - 0.1, 0))
            elif j == 1:    # If highlighted button is good hit sound, decrease volume
                GOOD_HIT.set_volume(max(GOOD_HIT.get_volume() - 0.1, 0))
                GOOD_HIT.play()
            elif j == 2:    # If highlighted button is game music, decrease volume
                pygame.mixer.music.set_volume(max(pygame.mixer.music.get_volume() - 0.1, 0))
                pygame.mixer.music.play(start=1)

        for event in pygame.event.get():        # Loop through all events
            if event.type == pygame.QUIT:       # If user clicked close, stop the loop
                carryOn = False
            if event.type == pygame.KEYDOWN:    # If user pressed a key
                if event.key == pygame.K_ESCAPE:
                    carryOn = False
        if display_menu != OPTS_MEMU:           # If user pressed a button, exit loop
            break

        screen.fill(DARKBLUE)  # Fill the screen with dark blue

        font = pygame.font.Font(None, 34)               # Create font for text
        font_plus_minus = pygame.font.Font(None, 50)    # Create font for + and -

        # Draw text
        text = font_plus_minus.render("-", 1,  WHITE)
        screen.blit(text, (100, 100-text.get_rect().height//2))
        text = font.render("Background Music", 1, colors[btn_colors[0]])
        screen.blit(text, (130, 105-text.get_rect().height//2))
        text = font_plus_minus.render("+", 1,  WHITE)
        screen.blit(text, (350, 100-text.get_rect().height//2))
        # Draw volume bar
        pygame.draw.rect(screen,  LIGHTBLUE, pygame.Rect(WIDTH - 350, 90, 250, 30))
        pygame.draw.rect(screen,  RED, pygame.Rect(WIDTH - 350, 90, 250*BACKGROUND.get_volume(), 30))

        # Draw text
        text = font_plus_minus.render("-", 1,  WHITE)
        screen.blit(text, (100, 200-text.get_rect().height//2))
        text = font.render("Good  Hit  Music", 1, colors[btn_colors[1]])
        screen.blit(text, (130, 205-text.get_rect().height//2))
        text = font_plus_minus.render("+", 1,  WHITE)
        screen.blit(text, (350, 200-text.get_rect().height//2))
        # Draw volume bar
        pygame.draw.rect(screen,  LIGHTBLUE, pygame.Rect(WIDTH - 350, 190, 250, 30))
        pygame.draw.rect(screen,  RED, pygame.Rect(WIDTH - 350, 190, 250*GOOD_HIT.get_volume(), 30))

        # Draw text
        text = font_plus_minus.render("-", 1,  WHITE)
        screen.blit(text, (100, 300-text.get_rect().height//2))
        text = font.render("Bad   Hit  Music", 1, colors[btn_colors[2]])
        screen.blit(text, (130, 305-text.get_rect().height//2))
        text = font_plus_minus.render("+", 1,  WHITE)
        screen.blit(text, (350, 300-text.get_rect().height//2))
        # Draw volume bar
        pygame.draw.rect(screen,  LIGHTBLUE, pygame.Rect(WIDTH - 350, 290, 250, 30))
        pygame.draw.rect(screen,  RED, pygame.Rect(WIDTH - 350, 290, 250*pygame.mixer.music.get_volume(), 30))

        # Draw all instructions
        inst_labels = ["A: MORE", "C: LESS", "D: UP", "B: DOWN", "ESC: BACK"]
        for i, label in enumerate(inst_labels):
            text = font.render(label, 1, WHITE)
            screen.blit(text, (30 + i*130 + i*20, HEIGHT - text.get_rect().height - 10))

        # refresh screen
        pygame.display.flip()
        iterations += 1

    # Log the time taken
    end = time.time()
    print("Opts:")
    print("Time taken: ", end - start)
    print("Frequency: ", iterations/(end - start), "Hz")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <port> <baudrate>")
        exit(1)

    port = sys.argv[1]
    baudrate = int(sys.argv[2])

    # Initialize connection to port
    ncap = NCap(port, baud_rate=baudrate)
    # Calibrate the sensor
    REST_VALUE = ncap.calibrate()

    # Define the sounds
    BAD_HIT    = "/home/fabiocfabini/MPLABXProjects/Micro Breakout.X/breakout/sounds/BadHitSound.mp3"
    GOOD_HIT   = pygame.mixer.Sound("/home/fabiocfabini/MPLABXProjects/Micro Breakout.X/breakout/sounds/GoodHitSound.mp3")
    BACKGROUND = pygame.mixer.Sound("/home/fabiocfabini/MPLABXProjects/Micro Breakout.X/breakout/sounds/BackGroundMusic.mp3")
    pygame.mixer.music.load(BAD_HIT)

    # Define the Menu options
    MAIN_MENU = 0
    GAME_MEMU = 1
    TEDS_MEMU = 2
    OPTS_MEMU = 3

    # Set the initial menu
    keep_going = True
    display_menu = MAIN_MENU

    # Start the background music
    BACKGROUND.play(-1)

    # Start the main loop
    while keep_going:
        if display_menu == MAIN_MENU:
            res_code, res = ncap.write_value(ncap.LED_4_CHANN, b'\xff')         # Turn on the LED RA4
            if res_code == 0:
                raise Exception(f"Error writing to channel {ncap.LED_4_CHANN}")
            time.sleep(0.3)                                                     # Wait some time to load next menu
            run_menu()                                                          # Run the menu
            res_code, res = ncap.write_value(ncap.LED_4_CHANN, b'\x00')         # Turn off the LED RA4
            if res_code == 0:
                raise Exception(f"Error writing to channel {ncap.LED_4_CHANN}")

        elif display_menu == GAME_MEMU:
            res_code, res = ncap.write_value(ncap.LED_5_CHANN, b'\xff')         # Turn on the LED RA5
            if res_code == 0:
                raise Exception(f"Error writing to channel {ncap.LED_5_CHANN}")
            time.sleep(0.3)                                                     # Wait some time to load next menu
            run_game()                                                          # Run the game
            res_code, res = ncap.write_value(ncap.LED_5_CHANN, b'\x00')         # Turn off the LED RA5
            if res_code == 0:
                raise Exception(f"Error writing to channel {ncap.LED_5_CHANN}")
            display_menu = MAIN_MENU

        elif display_menu == TEDS_MEMU:
            res_code, res = ncap.write_value(ncap.LED_6_CHANN, b'\xff')         # Turn on the LED RA6
            if res_code == 0:
                raise Exception(f"Error writing to channel {ncap.LED_6_CHANN}")
            time.sleep(0.3)                                                     # Wait some time to load next menu
            run_teds()                                                          # Run the TEDS
            res_code, res = ncap.write_value(ncap.LED_6_CHANN, b'\x00')         # Turn off the LED RA6
            if res_code == 0:
                raise Exception(f"Error wrtin to channel {ncap.LED_6_CHANN}")
            display_menu = MAIN_MENU

        elif display_menu == OPTS_MEMU:
            res_code, res = ncap.write_value(ncap.LED_7_CHANN, b'\xff')         # Turn on the LED RA7
            if res_code == 0:
                raise Exception(f"Error writing to channel {ncap.LED_6_CHANN}")
            time.sleep(0.3)                                                     # Wait some time to load next menu
            run_opts()                                                          # Run the options
            res_code, res = ncap.write_value(ncap.LED_7_CHANN, b'\x00')         # Turn off the LED RA7
            if res_code == 0:
                raise Exception(f"Error wrtin to channel {ncap.LED_6_CHANN}")
            display_menu = MAIN_MENU

    assert ncap.conn.read_all() == b'', "There is still data in the buffer"     # Check if there is still data in the buffer
    ncap.conn.close()                                                           # Close the connection
    pygame.quit()                                                               # Quit pygame