import pygame


def play_game():
    pygame.init()

    
    screen_width = 800
    screen_height = 800
    square = min(screen_width, screen_height)
    screen = pygame.display.set_mode((square, square))
    
    grid = 4
    cell_size = (square / grid)

    clock = pygame.time.Clock()
    running = True

    pygame.key.set_repeat(0)

    player_pos = [[2,2]]

    
    # Maybe this should not be FPS based at all
    # I am thinking it may be better to implement it independent of frames
    # and just have: Human input -> animations/resulting actions, then pause
    # until the next human input.
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                temp_pos = player_pos[0].copy()
                temp_pos[1] -= 1
                player_pos.insert(0, temp_pos)
                player_pos.pop()
                print("UP") 
            if event.key == pygame.K_DOWN:
                temp_pos = player_pos[0].copy()
                temp_pos[1] += 1
                player_pos.insert(0, temp_pos)
                player_pos.pop()
                print("DOWN")
            if event.key == pygame.K_LEFT:
                temp_pos = player_pos[0].copy()
                temp_pos[0] -= 1
                player_pos.insert(0, temp_pos)
                player_pos.pop()
                print("LEFT")
            if event.key == pygame.K_RIGHT:
                temp_pos = player_pos[0].copy()
                temp_pos[0] += 1
                player_pos.insert(0, temp_pos)
                player_pos.pop()
                print("RIGHT") 


        for i in range(grid):
            temp_x = i * cell_size
            for j in range(grid):
                temp_y = j * cell_size
                if (i % 2) == 0:
                    if (j % 2) == 0:
                        pygame.draw.rect(screen, "white", (temp_x, temp_y, cell_size, cell_size))
                    else:
                        pygame.draw.rect(screen, "gray", (temp_x, temp_y, cell_size, cell_size))
                else:
                    if (j % 2) == 0:
                        pygame.draw.rect(screen, "gray", (temp_x, temp_y, cell_size, cell_size))
                    else:
                        pygame.draw.rect(screen, "white", (temp_x, temp_y, cell_size, cell_size))

        for x in player_pos:
            player_x = x[0] * cell_size
            player_y = x[1] * cell_size
            pygame.draw.rect(screen, "red", (player_x, player_y, cell_size, cell_size))
        
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
