import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Set up display
pygame.display.set_caption('Speed4Speed')
width = 800
height = 600
size = (width, height)
fps = 120

# changing the logo
logo = pygame.image.load("images/logo.png")
pygame.display.set_icon(logo)

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


# Load fonts and images
font = pygame.font.Font(None, 40)
background = pygame.image.load("images/roadway.png")
car_photo = pygame.image.load("images/car.png")
truck_photo = pygame.transform.scale(pygame.image.load("images/pickup.png"), (70, 145))
slowDown = pygame.transform.scale(pygame.image.load("images/slowdown.png"), (37, 45))
heart_image = pygame.image.load("images/heart.png")

# Load sounds
truck_pass_sound = pygame.mixer.Sound("sounds/truck_pass.wav")
truck_pass_sound.set_volume(0.5)
tires = pygame.mixer.Sound("sounds/tires_skid.ogg")
tires.set_volume(0.5)
crash = pygame.mixer.Sound("sounds/crash.ogg")
crash.set_volume(2)
soundtrack = pygame.mixer.Sound("sounds/soundtrack.mp3")
soundtrack.set_volume(0.5)
soundtrack.play(-1)

# Initialize game variables
lives = 3
background_y = 0
car_width = 72

# Initialize slowdown variable
slowdown_image = pygame.transform.scale(pygame.image.load("images/slowdown.png"), (55, 35))
slowdown_rect = slowdown_image.get_rect()
slowdown_rect.y = -100

# Initialize pause button and create a rect object from it
pause_button_image = pygame.image.load("images/pause_button.png")
pause_button_rect = pause_button_image.get_rect(topleft=(10, 10))

# Initialize countdown sound
countdown_sound = pygame.mixer.Sound("sounds/countdown.mp3")

# Initialize quit button and create a rect object from it
quit_button_image = pygame.image.load("images/quit_button.png")
quit_button_rect = quit_button_image.get_rect(topright=(width - 10, 10))

# Load the button click sound
button_click_sound = pygame.mixer.Sound("sounds/click.wav")


# Start Screen
def start_screen():
    global game_active

    # Load background and start button images
    background_image = pygame.image.load("images/startscreen.png")
    start_button_image = pygame.image.load("images/start_button.png")
    start_button_rect = start_button_image.get_rect(center=(width // 2, height // 2))  # Adjust position

    exit_button_image = pygame.image.load("images/exit_button.png")
    exit_button_rect = exit_button_image.get_rect(center=(width // 2, height // 2 + 50))  # Adjust position

    # loop for the game to start
    while not game_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                button_click_sound.play()
                if start_button_rect.collidepoint(event.pos):
                    countdown()
                    game_active = True
                    playing()
                button_click_sound.play()
                if exit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    quit()

        screen.blit(background_image, (0, 0))
        screen.blit(start_button_image, start_button_rect)
        screen.blit(exit_button_image, exit_button_rect)

        pygame.display.update()
        clock.tick(fps)


def countdown():
    countdown_font = pygame.font.Font(None, 100)  # Create a font object for rendering text
    countdown_texts = ["3", "2", "1", "GO!"]  # Text to display during countdown

    for index, countdown_text in enumerate(countdown_texts):
        screen.blit(background, (0, 0))  # Clear the screen with the background image

        # Render the countdown text using the chosen font, size, and color
        countdown_render = countdown_font.render(countdown_text, True, (255, 182, 193))
        countdown_rect = countdown_render.get_rect(center=(width // 2, height // 2))  # Calculate text's position
        screen.blit(countdown_render, countdown_rect)  # Draw the rendered text onto the screen

        if index == 0:  # Play the countdown sound only for the first iteration
            pygame.mixer.Sound.play(countdown_sound)  # Play the countdown sound effect

        pygame.display.update()
        pygame.time.wait(1300)


# Display message and remaining lives
def message_with_lives(message, lives_left):
    message_font = font.render(message, True, (255, 182, 193))  # Render the message text with the specified font and color
    rect = message_font.get_rect()  # Get the rectangle that encloses the rendered message text
    rect.center = ((width // 2), (height // 2))  # Set the center position of the message text rectangle
    screen.blit(message_font, rect)  # Draw the rendered message text on the screen at the specified position

    heart_spacing = 5  # Adjust the spacing between hearts

    # Calculate the starting x-coordinate and y-coordinate for the hearts
    heart_start_x = quit_button_rect.left - (heart_image.get_width() + heart_spacing) * lives_left
    heart_position_y = quit_button_rect.centery - heart_image.get_height() // 2

    # Draw hearts for the remaining lives
    for i in range(lives_left):
        heart_x = heart_start_x + i * (heart_image.get_width() + heart_spacing)  # Calculate x-coordinate for each heart
        screen.blit(heart_image, (heart_x, heart_position_y))  # Draw the heart image at the calculated position

    pygame.display.update()  # Update the display to show the message and hearts
    time.sleep(3)  # Pause for 3 seconds to display the message and hearts before continuing


# Handle crashing with remaining lives
def crashed_with_lives(message):
    global lives
    lives -= 1  # Decrement the player's remaining lives

    # Check if the player has remaining lives
    if lives > 0:
        # Display a message and the remaining lives
        message_with_lives(message, lives)

        # Continue playing the game
        playing()
    else:
        # Player has no remaining lives, game over
        game_over()


# Display game over screen
def game_over():
    # Display "Game Over!" message in the center of the screen
    message_font = font.render("Game Over!", True, (255, 255, 255))
    rect = message_font.get_rect()
    rect.center = ((width // 2), (height // 2))
    screen.blit(message_font, rect)

    pygame.display.update()

    # Create a "Play Again" button rectangle
    play_again_button = pygame.Rect(300, 350, 200, 50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                button_click_sound.play()
                if play_again_button.collidepoint(event.pos):
                    # Reset game state and start the game again
                    global lives, game_active
                    lives = 3
                    game_active = False
                    start_screen()

        # Draw the "Play Again" button and add the text "Replay"
        pygame.draw.rect(screen, (255, 182, 193), play_again_button)
        play_again_text = font.render("Replay", True, (255, 255, 255))
        play_again_text_rect = play_again_text.get_rect(center=play_again_button.center)
        screen.blit(play_again_text, play_again_text_rect)

        pygame.display.update()
        clock.tick(fps)


# Draw truck on screen
def truck(truck_x, truck_y):
    screen.blit(truck_photo, (truck_x, truck_y))


# Draw slowdown power-up on screen
def slow(x, y):
    screen.blit(slowDown, (x, y))


# Draw car on screen
def car(x, y):
    screen.blit(car_photo, (x, y))


# Display current score
def Score(count):
    score_font = pygame.font.Font(None, 30)
    score_font_render = score_font.render("Score: %d" % count, True, (255, 255, 255))
    # Adjust the position of the score text
    screen.blit(score_font_render,
                (pause_button_rect.right + 10, pause_button_rect.centery - score_font_render.get_height() // 2))


# Deal with the pause button functionality
def pause():
    # Create a font and render the "Paused" text
    paused_font = pygame.font.Font(None, 80)
    paused_text = paused_font.render("Paused", True, (255, 182, 193))
    paused_rect = paused_text.get_rect(center=(width // 2, height // 2))

    # Create a "Continue" button rectangle
    continue_button = pygame.Rect(width // 2 - 75, height // 2 + 50, 150, 50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                button_click_sound.play()
                if event.key == pygame.K_p:
                    return  # Resume the game when the "P" key is pressed

            if event.type == pygame.MOUSEBUTTONDOWN:
                if continue_button.collidepoint(event.pos):
                    button_click_sound.play()
                    return  # Resume the game when the "Continue" button is clicked

        # Display the "Paused" text in the center of the screen
        screen.blit(paused_text, paused_rect)

        # Draw the "Continue" button and add the text "Continue"
        pygame.draw.rect(screen, (255, 182, 193), continue_button)
        continue_text = font.render("Continue", True, (0, 0, 0))
        continue_text_rect = continue_text.get_rect(center=continue_button.center)
        screen.blit(continue_text, continue_text_rect)

        pygame.display.update()
        clock.tick(fps)


def confirm_quit():
    # Create a font and render the confirmation text
    confirm_font = pygame.font.Font(None, 40)
    confirm_text = confirm_font.render("Are you sure you want to quit?", True, (255, 182, 193))
    confirm_rect = confirm_text.get_rect(center=(width // 2, height // 2))

    # Create "Yes" and "No" button rectangles
    yes_button = pygame.Rect(width // 2 - 50, height // 2 + 50, 100, 40)
    no_button = pygame.Rect(width // 2 - 50, height // 2 + 100, 100, 40)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if yes_button.collidepoint(event.pos):
                    button_click_sound.play()
                    return True  # Player confirmed quitting
                elif no_button.collidepoint(event.pos):
                    button_click_sound.play()
                    return False  # Player canceled quitting

        # Display the confirmation text
        screen.blit(confirm_text, confirm_rect)

        # Draw the "Yes" and "No" buttons and add corresponding text
        pygame.draw.rect(screen, (255, 182, 193), yes_button)
        pygame.draw.rect(screen, (255, 182, 193), no_button)

        yes_text = font.render("Yes", True, (0, 0, 0))
        yes_text_rect = yes_text.get_rect(center=yes_button.center)
        screen.blit(yes_text, yes_text_rect)

        no_text = font.render("No", True, (0, 0, 0))
        no_text_rect = no_text.get_rect(center=no_button.center)
        screen.blit(no_text, no_text_rect)

        pygame.display.update()
        clock.tick(fps)


# Main game loop
def playing():
    global lives, background_y, game_active

    # Initialize car position and movement
    x = 351
    y = 480
    x_change = 0

    # Initialize truck properties
    truck_height = 145
    truck_width = 70
    truck_x = random.randrange(50, 770)
    truck_y = -truck_height
    truck_speed = 2

    # Initialize slowdown power-up properties
    slow_height = 35
    slow_width = 55
    slow_x = random.randrange(50, 770)
    slow_y = -slow_height
    powerup_start_time = 0
    POWERUP_DURATION = 1000

    score = 0
    last_truck_pass_time = 0

    start_time = pygame.time.get_ticks()

    while game_active:
        clock.tick(fps)

        for event in pygame.event.get():
            # Event handling
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -6
                if event.key == pygame.K_RIGHT:
                    x_change = 6
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pause_button_rect.collidepoint(event.pos):
                    button_click_sound.play()
                    pause()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if quit_button_rect.collidepoint(event.pos):
                    button_click_sound.play()
                    if confirm_quit():
                        game_active = False
                        start_screen()

        # Update car position
        x += x_change

        # Update background scrolling
        background_y += truck_speed
        if background_y >= height:
            background_y = 0

        screen.blit(background, (0, background_y))
        screen.blit(background, (0, background_y - height))

        # Update truck position and appearance
        truck_y += truck_speed
        if truck_y > height:
            truck_y = -truck_height
            truck_x = random.randrange(50, width - truck_width - 50)

            score += 1
            truck_speed += 0.2

        truck(truck_x, truck_y)

        # Update slowdown power-up position and appearance
        current_time = pygame.time.get_ticks()
        if current_time - start_time >= 30000:  # 30 seconds in milliseconds
            slow_y += truck_speed
            if slow_y > height:
                slow_y = -slow_height
                slow_x = random.randrange(50, 770)

            slow(slow_x, slow_y)

            if slow_y + slow_height > truck_y and slow_y < truck_y + truck_height:
                if slow_x + slow_width > truck_x and slow_x < truck_x + truck_width:
                    slow_y = -slow_height
                    slow_x = random.randrange(50, 770)

        # Draw car and score
        car(x, y)
        Score(score)

        # Check for collisions
        if x > (width - car_width - 30) or x < 30:  # Adjusted the bounds to avoid off-road
            tires.play()
            crash.play()
            crashed_with_lives("YOU WENT OFF ROAD!")

        if y + car_photo.get_height() > truck_y and y < truck_y + truck_height:
            if x + car_width > truck_x and x < truck_x + truck_width:
                crash.play()
                crashed_with_lives("YOU HIT A TRUCK!")

        # Apply slowdown power-up effect
        is_slowed_down = False
        if y < slow_y + slow_height:
            if slow_x < x + car_width and slow_x + slow_width > x:
                if not is_slowed_down:
                    truck_speed -= 1
                    is_slowed_down = True
                    powerup_start_time = pygame.time.get_ticks()
                slow_y = -slow_height
                slow_x = random.randrange(50, 770)

        # Revert slowdown effect after specified duration
        if is_slowed_down and pygame.time.get_ticks() - powerup_start_time >= POWERUP_DURATION:
            truck_speed += 1
            is_slowed_down = False

        # Display hearts for remaining lives in the top left corner
        heart_spacing = 5  # Adjust the spacing between hearts

        heart_start_x = quit_button_rect.left - (heart_image.get_width() + heart_spacing) * lives
        heart_position_y = quit_button_rect.centery - heart_image.get_height() // 2

        for i in range(lives):
            heart_x = heart_start_x + i * (heart_image.get_width() + heart_spacing)
            screen.blit(heart_image, (heart_x, heart_position_y))

        # Play the truck pass sound when the truck gets close to the car vertically
        if abs(y - truck_y) < truck_height:
            current_time = pygame.time.get_ticks()
            if current_time - last_truck_pass_time > 2000:  # Adjust the delay as needed
                truck_pass_sound.play()
                last_truck_pass_time = current_time

        screen.blit(pause_button_image, pause_button_rect)
        screen.blit(quit_button_image, quit_button_rect)

        pygame.display.flip()


# Initialize game state
game_active = False
start_button = pygame.Rect(300, 250, 200, 50)
start_screen()
