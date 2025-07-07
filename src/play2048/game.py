import pygame
import random


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
    PROCESSING_DELAY = 300

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


    FONT_COLOR = (252, 86, 3)
    FONT = pygame.font.SysFont("comicsans", 60, bold=True)

    # "x,y": value
    tiles = {
        "11": [2],
        "33": [2],
    }

    def place_tiles(tiles):
        x = None
        y = None
        while True:
            x = random.randint(0, 3)
            y = random.randint(0, 3)
            temp_tile = f"{x}{y}"
            tile_num = len(tiles) 
            if tile_num == 16:
                break
            elif temp_tile not in tiles:
                tiles[temp_tile] = [2]
                break
        
    def draw_tiles():
        for tile in tiles:
            coords_string = list(tile)
            coords = []
            for num in coords_string:
                coords.append(int(num))

            tile_x = (coords[0] * tile_size) + ((coords[0] + 1) * 10)
            tile_y = (coords[1] * tile_size) + ((coords[1] + 1) * 10)
            pygame.draw.rect(screen, "red", (tile_x, tile_y, tile_size, tile_size))
            text = FONT.render(str(2), 1, FONT_COLOR)
            screen.blit(
                text,
                (
                    tile_x + (tile_size / 2 - text.get_width() / 2),
                    tile_y + (tile_size / 2 - text.get_height() / 2),
                ),
            )

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
                move_tiles()
                place_tiles(tiles)
                print(tiles)
                print()
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
        
        draw_tiles()


        # Move now defunct due to new tile storage type
        # def move_tiles():
        #     for x in player_pos:
        #         if move == UP:
        #             x[1] -= 1
        #         if move == DOWN:
        #             x[1] += 1
        #         if move == LEFT:
        #             x[0] -= 1
        #         if move == RIGHT:
        #             x[0] += 1


        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
