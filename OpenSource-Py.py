import pygame
import time
import random

pygame.init()

width = 800
height = 600
window = pygame.display.set_mode((width, height))

pygame.display.set_caption("Snake")

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
purple = (128, 0, 128)
grey = (128, 128, 128)

block_size = 20

font_style = pygame.font.SysFont(None, 50)
fps_font = pygame.font.SysFont(None, 30)

def Your_score(score):
    value = font_style.render("Your Score: " + str(score), True, black)
    window.blit(value, [0, 0])

def our_snake(snake_list):
    for x in snake_list:
        pygame.draw.rect(window, green, [x[0], x[1], block_size, block_size])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    window.blit(mesg, [width / 6, height / 3])

def generate_food(snake_List, special=False):
    if not special:
        foodx = round(random.randrange(0, width - block_size) / block_size) * block_size
        foody = round(random.randrange(0, height - block_size) / block_size) * block_size
        if [foodx, foody] not in snake_List:
            return foodx, foody
        else:
            return generate_food(snake_List)
    else:
        foodx = round(random.randrange(0, width - block_size) / block_size) * block_size
        foody = round(random.randrange(0, height - block_size) / block_size) * block_size
        return foodx, foody

def generate_portal(snake_List, foodx, foody):
    portalx = round(random.randrange(0, width - block_size) / block_size) * block_size
    portaly = round(random.randrange(0, height - block_size) / block_size) * block_size
    if [portalx, portaly] not in snake_List and (portalx, portaly) != (foodx, foody):
        return portalx, portaly
    else:
        return generate_portal(snake_List, foodx, foody)

def generate_obstacle(snake_List, foodx, foody, portal1_x, portal1_y, portal2_x, portal2_y):
    obstaclex = round(random.randrange(0, width - block_size) / block_size) * block_size
    obstacley = round(random.randrange(0, height - block_size) / block_size) * block_size
    if [obstaclex, obstacley] not in snake_List and \
       (obstaclex, obstacley) != (foodx, foody) and \
       (obstaclex, obstacley) != (portal1_x, portal1_y) and \
       (obstaclex, obstacley) != (portal2_x, portal2_y):
        return obstaclex, obstacley
    else:
        return generate_obstacle(snake_List, foodx, foody, portal1_x, portal1_y, portal2_x, portal2_y)

def gameLoop():
    snake_speed = 15

    game_over = False
    game_close = False

    x1 = width / 2
    y1 = height / 2
    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx, foody = generate_food(snake_List)

    portal1_x, portal1_y = generate_portal(snake_List, foodx, foody)
    portal2_x, portal2_y = generate_portal(snake_List, foodx, foody)

    obstacle_x, obstacle_y = generate_obstacle(snake_List, foodx, foody, portal1_x, portal1_y, portal2_x, portal2_y)

    clock = pygame.time.Clock()

    while not game_over:

        while game_close == True:
            window.fill(white)
            message("You Lost! Press Q to Quit or C to Play Again", red)
            Your_score(Length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -block_size
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = block_size
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -block_size
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = block_size
                    x1_change = 0

        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        window.fill(white)

        pygame.draw.rect(window, purple, [portal1_x, portal1_y, block_size, block_size])
        pygame.draw.rect(window, purple, [portal2_x, portal2_y, block_size, block_size])

        pygame.draw.rect(window, grey, [obstacle_x, obstacle_y, block_size, block_size])

        pygame.draw.rect(window, red, [foodx, foody, block_size, block_size])

        if x1 == foodx and y1 == foody:
            foodx, foody = generate_food(snake_List)
            Length_of_snake += 1

            snake_speed += 1

        if (x1, y1) == (portal1_x, portal1_y):
            x1, y1 = portal2_x, portal2_y
        elif (x1, y1) == (portal2_x, portal2_y):
            x1, y1 = portal1_x, portal1_y

        if (x1, y1) == (obstacle_x, obstacle_y):
            snake_speed -= 5
            obstacle_x, obstacle_y = generate_obstacle(snake_List, foodx, foody, portal1_x, portal1_y, portal2_x, portal2_y)

        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_List)
        Your_score(Length_of_snake - 1)

        fps = clock.get_fps()
        fps_text = fps_font.render("FPS: " + str(int(fps)), True, black)
        window.blit(fps_text, (width - 100, 0))

        pygame.display.update()

        clock.tick(snake_speed)

    pygame.quit()

gameLoop()
