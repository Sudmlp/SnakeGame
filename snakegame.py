import pygame
import random

# Initialize Pygame
pygame.init()

# Define colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
dark_green = (0, 200, 0)

# Game window dimensions
dis_width = 800
dis_height = 600

# Set up display
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game')

# Game variables
block_size = 20
snake_speed = 10

# Fonts
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

def our_snake(snake_list):
    """Draw the snake on the screen"""
    for i, segment in enumerate(snake_list):
        if i == len(snake_list)-1:
            pygame.draw.rect(dis, dark_green, [segment[0], segment[1], block_size, block_size])
        else:
            pygame.draw.rect(dis, green, [segment[0], segment[1], block_size, block_size])

def your_score(score):
    """Display the current score"""
    value = score_font.render("Your Score: " + str(score), True, white)
    dis.blit(value, [0, 0])

def game_loop():
    """Main game loop"""
    game_over = False
    game_close = False

    # Initial snake position and movement
    x1 = dis_width / 2
    y1 = dis_height / 2
    x1_change = block_size
    y1_change = 0

    snake_list = []
    snake_length = 3  # Initial length
    
    # Generate initial food position
    food_x = round(random.randrange(0, dis_width - block_size) / block_size) * block_size
    food_y = round(random.randrange(0, dis_height - block_size) / block_size) * block_size

    while not game_over:
        while game_close:
            # Game over screen
            dis.fill(black)
            game_over_msg = font_style.render("Game Over! Press Q-Quit or C-Play Again", True, red)
            dis.blit(game_over_msg, [dis_width/6, dis_height/3])
            your_score(snake_length - 3)
            pygame.display.update()

            # Handle game over input
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        # Handle keyboard input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change != block_size:
                    x1_change = -block_size
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change != -block_size:
                    x1_change = block_size
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change != block_size:
                    y1_change = -block_size
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change != -block_size:
                    y1_change = block_size
                    x1_change = 0

        # Check wall collision
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True

        # Update snake position
        x1 += x1_change
        y1 += y1_change
        dis.fill(black)
        
        # Draw food
        pygame.draw.rect(dis, red, [food_x, food_y, block_size, block_size])
        
        # Update snake body
        snake_head = [x1, y1]
        snake_list.append(snake_head)
        
        if len(snake_list) > snake_length:
            del snake_list[0]

        # Check self collision
        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        # Draw snake and score
        our_snake(snake_list)
        your_score(snake_length - 3)
        pygame.display.update()

        # Check food collision
        if x1 == food_x and y1 == food_y:
            # Generate new food position
            food_x = round(random.randrange(0, dis_width - block_size) / block_size) * block_size
            food_y = round(random.randrange(0, dis_height - block_size) / block_size) * block_size
            # Ensure food doesn't spawn on snake
            while [food_x, food_y] in snake_list:
                food_x = round(random.randrange(0, dis_width - block_size) / block_size) * block_size
                food_y = round(random.randrange(0, dis_height - block_size) / block_size) * block_size
            snake_length += 1

        # Control game speed
        clock = pygame.time.Clock()
        clock.tick(snake_speed)

    pygame.quit()
    quit()

# Start the game
game_loop()