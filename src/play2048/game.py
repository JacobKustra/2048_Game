import pygame


def play_game():
    pygame.init()
    
    clock = pygame.time.Clock() 

    screen_width = 750
    screen_height = 750
    screen = pygame.display.set_mode((screen_width, screen_height))

    # Game States
    AWAITING_INPUT = "awaiting_input"
    PROCESSING = "processing"
    game_state = AWAITING_INPUT 
    processing_start = 0
    PROCESSING_DELAY = 1300

    # Directions
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"
    move = None

    grid = 4
    cell_size = (screen_width / grid)
    tile_size = ((screen_width - 50) / grid)

    running = True

    player_pos = [[2,2], [0, 0], [1, 2], [3,3], [3, 2], [1, 1]]

    while running:

        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if (game_state == AWAITING_INPUT) and (event.type == pygame.KEYDOWN):
                key_to_move = {
                    pygame.K_UP: UP,
                    pygame.K_DOWN: DOWN,
                    pygame.K_LEFT: LEFT,
                    pygame.K_RIGHT: RIGHT
                }
                if event.key in key_to_move:
                    move = key_to_move[event.key]
                    processing_start = current_time
                    game_state = PROCESSING
                    

        if game_state == PROCESSING:
            if current_time - processing_start >= PROCESSING_DELAY :
                move = None
                game_state = AWAITING_INPUT


        

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


        # Horizontal Bars
        pygame.draw.rect(screen, "black", (0, 0, screen_width, 10))
        pygame.draw.rect(screen, "black", (0, (tile_size + 10), screen_width, 10))
        pygame.draw.rect(screen, "black", (0, (2 * (tile_size + 10)), screen_width, 10))
        pygame.draw.rect(screen, "black", (0, (3 * (tile_size + 10)), screen_width, 10))
        pygame.draw.rect(screen, "black", (0, (screen_height - 10), screen_width, 10))

        # Vertical Bars
        pygame.draw.rect(screen, "black", (0, 0, 10, screen_height))
        pygame.draw.rect(screen, "black", ((tile_size + 10), 0, 10, screen_height))
        pygame.draw.rect(screen, "black", ((2 * (tile_size + 10)), 0, 10, screen_height))
        pygame.draw.rect(screen, "black", ((3 * (tile_size + 10)), 0, 10, screen_height))
        pygame.draw.rect(screen, "black", ((screen_width - 10), 0, 10, screen_height))
        
        for x in player_pos:
            player_x = (x[0] * tile_size) + ((x[0] + 1) * 10)
            player_y = (x[1] * tile_size) + ((x[1] + 1) * 10)
            pygame.draw.rect(screen, "red", (player_x, player_y, tile_size, tile_size))
       

        # Position 0, 0 is 10, 10
        # position 1, 1 is 10 + cell_size


        # Move

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
