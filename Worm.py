#https://www.youtube.com/watch?v=aLxJM-cfqnc
#https://www.youtube.com/watch?v=oXz3f4_g3gA
#https://www.youtube.com/watch?v=lLh7vhMBCj4
#https://www.youtube.com/watch?v=SLkfoip1JQw

import pygame  # Import the pygame library for game development
import random  # Import the random library for generating random positions

# Initialize Pygame and font module
pygame.init()  # Initialize all imported pygame modules
pygame.font.init()  # Initialize the font module in pygame

# Screen dimensions
WIDTH, HEIGHT = 600, 600  # Define the width and height of the game screen

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Create a screen of specified dimensions
pygame.display.set_caption("WORM")  # Set the title of the game window

# Colors 
BLACK = (0, 0, 0)  # Define the color black
GRAY = (98, 126, 93)  # Define the color gray
GREEN = (13, 169, 101)  # Define the color green
WHITE = (255, 255, 255)  # Define the color white

# Game settings
clock = pygame.time.Clock()  # Create a clock object to control the game speed
cell_size = 20  # Define the size of each cell in the grid

# Load fonts
ephesis_font = pygame.font.Font("C:/Users/ecobee/Downloads/Ephesis-Regular.ttf", 40)  # Load a specific font

# Background image (scaled to fit the screen)
background_image = pygame.image.load("C:/Users/ecobee/Downloads/grass background.jpg")  # Load the background image
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))  # Scale the background image to fit the screen

# Game over image (scaled to fit the screen)
game_over_image = pygame.image.load('C:/Users/ecobee/Downloads/download.png')  # Load the game over image
game_over_image = pygame.transform.scale(game_over_image, (WIDTH, HEIGHT))  # Scale the game over image to fit the screen

# Text rendering for the start screen
start_text = ephesis_font.render("Play", True, (255, 255, 0), (55, 186, 32))  # Render the "Play" text
start_text_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # Get the rectangle of the start text and center it

# Initial worm settings (starting position and direction)
initial_worm_pos = [(300, 300)]  # Define the starting position of the worm
worm = initial_worm_pos  # Create a copy of the initial worm position
worm_dir = (0, 0)  # Initially, the worm is not moving

# Initial leaf position
leaf = (random.randint(0, (WIDTH - cell_size) // cell_size) * cell_size,
        random.randint(0, (HEIGHT - cell_size) // cell_size) * cell_size)  # Generate a random position for the leaf

# Game state 
game_state = 'main'  # Set the initial game state to 'main'
game_over = False  # Initialize the game over flag

# Initial number of lives and points
life = 3  # Set the initial number of lives
points = 0  # Set the initial number of points

# Main game loop
while True:
    screen.fill(GRAY)  # Fill the screen with gray color

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If the quit event is triggered
            pygame.quit()  # Quit the game
            exit()  # Exit the program
        if event.type == pygame.KEYDOWN:  # If a key is pressed
            # Change direction based on arrow key pressed
            if event.key == pygame.K_UP and worm_dir != (0, cell_size):
                worm_dir = (0, -cell_size)  # Move the worm up
            elif event.key == pygame.K_DOWN and worm_dir != (0, -cell_size):
                worm_dir = (0, cell_size)  # Move the worm down
            elif event.key == pygame.K_LEFT and worm_dir != (cell_size, 0):
                worm_dir = (-cell_size, 0)  # Move the worm left
            elif event.key == pygame.K_RIGHT and worm_dir != (-cell_size, 0):
                worm_dir = (cell_size, 0)  # Move the worm right

    # Main menu state
    if game_state == 'main':
        screen.blit(background_image, (0, 0))  # Draw the background image
        screen.blit(start_text, start_text_rect)  # Draw the start text

        # Start game on mouse click
        if pygame.mouse.get_pressed()[0]:  # If the left mouse button is pressed
            game_state = 'playing'  # Change the game state to 'playing'
            worm = [(300, 300)]  # Reset the worm position
            worm_dir = (0, 0)  # Reset the worm direction
            # Generate a new random leaf position
            leaf = (random.randint(0, (WIDTH) // cell_size) * cell_size,
                    random.randint(0, (HEIGHT) // cell_size) * cell_size)
            life = 3  # Reset lives
            
    # Game playing state
    elif game_state == 'playing':
        screen.blit(background_image, (0, 0))  # Draw the background image

        # Move the worm
        if worm_dir != (0, 0):  # If the worm is moving
            new_head = (worm[0][0] + worm_dir[0], worm[0][1] + worm_dir[1])  # Calculate the new head position
            
            # Check for wall collisions
            if not (0 <= new_head[0] < WIDTH and 0 <= new_head[1] < HEIGHT):  # If the worm hits the wall
                life -= 1  # Decrease life by 1
                if life == 0:  # If no lives are left
                    game_state = 'game_over'  # Change the game state to 'game over'
                else:
                    worm = initial_worm_pos[:]  # Respawn the worm at the initial position
                    worm_dir = (0, 0)  # Stop the worm movement
            # Check for self-collision
            elif new_head in worm:  # If the worm collides with itself
                life -= 1  # Decrease life by 1
                if life == 0:  # If no lives are left
                    game_state = 'game_over'  # Change the game state to 'game over'
                else:
                    worm = initial_worm_pos[:] # Respawn the worm at the initial position
                    worm_dir = (0, 0)  # Stop the worm movement
            else:
                worm.insert(0, new_head)  # Add the new head to the worm
                # Check if the worm has eaten the leaf
                if worm[0] == leaf:  # If the worm's head is at the leaf's position
                    points += 1  # Increase points by 1
                    # Generate a new random leaf position
                    leaf = (random.randint(0, (WIDTH - cell_size) // cell_size) * cell_size,
                            random.randint(0, (HEIGHT - cell_size) // cell_size) * cell_size)
                else:
                    worm.pop()  # Remove the last segment if no leaf is eaten

        # Draw the worm
        for segment in worm:
            #* symbol in your code is used to unpack the segment tuple so that its values are passed as individual arguments to the pygame.draw.rect() function
            pygame.draw.rect(screen, GRAY, (segment, cell_size, cell_size))  # Draw each segment of the worm

        # Draw the leaf
        pygame.draw.rect(screen, GREEN, (leaf, cell_size, cell_size))  # Draw the leaf

        # Draw the life counter
        life_text = ephesis_font.render(f"Lives: {life}", True, BLACK)  # Render the lives text
        screen.blit(life_text, (10, 10))  # Draw the lives text on the screen

    # Game over state
    elif game_state == 'game_over':
        screen.blit(game_over_image, (0, 0))  # Draw the game over image

        # Display total points on the game over screen
        game_over_points_text = ephesis_font.render(f"Total Points: {points}", True, WHITE)  # Render the points text
        game_over_points_rect = game_over_points_text.get_rect(center=(WIDTH // 2, HEIGHT // 1.3 + 50))  # Center the points text
        screen.blit(game_over_points_text, game_over_points_rect)  # Draw the points text on the screen

    pygame.display.update()  # Update the display
    clock.tick(10)  # Control the game speed (frames per second)
