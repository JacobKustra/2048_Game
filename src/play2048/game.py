import pygame
import random
import copy


def play_game():
    pygame.init()
    
    clock = pygame.time.Clock() 

    screen_width = 750
    screen_height = 750
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('2048 Game by Jacob Kustra')

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

    FONT = pygame.font.SysFont("Arial", 60, bold=True)
    FONT_COLOR_WHITE = (228, 235, 240)
    FONT_COLOR = (117, 100, 82)
    BEIGE = (239, 229, 218)
    BACKGROUND = (189, 172, 152)
    GRID = (156, 138, 122)

    TILE_COLORS = {
        2: (239, 229, 218),
        4: (235, 216, 182),
        8: (243, 178, 120), # White text starts at 8
        16: (247, 148, 99), 
        32: (247, 129, 101),
        64: (247, 101, 68),
        128: (240, 211, 110),
        256: (242, 211, 98),
        512: (246, 212, 94),
        1024: (248, 213, 78),
        2048: (250, 211, 60),
    }
    
    # "x,y": [value, has combined this round?]
    tiles = {
        "11": [2, 0],
        "33": [2, 0],
        "00": [2, 0],
        "01": [4096, 0],
        "12": [16, 0],
        "10": [2, 0],
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
                tiles[temp_tile] = [2, 0]
                break


    def tile_color(tile):
        tile_num = tiles[tile][0]
        black_color = (26, 25, 24)
        if tile_num >= 4096:
            return black_color
        else:
            return TILE_COLORS[tiles[tile][0]]


    def tile_text_color(tile):
        tile_num = tiles[tile][0]
        if tile_num < 8:
            return FONT_COLOR
        else:
            return FONT_COLOR_WHITE

        

    def draw_tiles():
        for tile in tiles:
            color = tile_color(tile)
            text_color = tile_text_color(tile)
            coords_string = list(tile)
            coords = []
            for num in coords_string:
                coords.append(int(num))

            tile_x = (coords[0] * tile_size) + ((coords[0] + 1) * 10)
            tile_y = (coords[1] * tile_size) + ((coords[1] + 1) * 10)
            pygame.draw.rect(screen, color, (tile_x, tile_y, tile_size, tile_size))
            text = FONT.render(str(tiles[tile][0]), 1, text_color)
            screen.blit(
                text,
                (
                    tile_x + (tile_size / 2 - text.get_width() / 2),
                    tile_y + (tile_size / 2 - text.get_height() / 2),
                ),
            )




    def valid_move(tiles, move):
        final_tiles = {}
        final_tiles_set = {}

        if move == UP:
            # Sort by column up to down (1 to 16)
            # Use for Up Move
            tiles = dict(sorted(tiles.items()))
            for tile in tiles:
                coords_string = list(tile)
                
                coords = []
                final_coords = []
                # Add the final coords in

                tile_data = tiles[tile]
                for num in coords_string:
                    coords.append(int(num))
                    final_coords.append(int(num))

                if coords[1] == 0:
                    new_tile = f"{coords[0]}{coords[1]}"
                    final_tiles[new_tile] = tile_data

                # at least one possible move up
                elif coords[1] >= 1:

                    # Set up loop to loop through y value times, capturing
                    # the highest y it can do?
                    final_coords[1] -= 1
                    new_tile = f"{final_coords[0]}{final_coords[1]}"

                    # if tile above it, can combine?
                    if new_tile in final_tiles:
                        for i in list(final_tiles):
                            # Can combine?
                            if i == new_tile:
                                
                                # Issue here with combination
                                if final_tiles[i][1] == 0 and (final_tiles[i][0] == tile_data[0]):
                                    # Combine
                                    new_num = final_tiles[i][0] + final_tiles[new_tile][0]
                                    final_tiles[i] = [new_num, 1]
                                    # Don't add new tile, just edit existing
                                else:
                                    final_coords[1] += 1
                                    new_tile = f"{final_coords[0]}{final_coords[1]}"
                                    final_tiles[new_tile] = tile_data
                                    # Finish this tile here
                    # no tile above it
                    else:
                        if coords[1] >= 2:
                            # two possible moves up
                            final_coords[1] -= 1
                            new_tile = f"{final_coords[0]}{final_coords[1]}"

                            # if tile above it, can combine?
                            if new_tile in final_tiles:
                                for i in list(final_tiles):
                                    # Can combine?
                                    if i == new_tile:
                                        if final_tiles[i][1] == 0 and (final_tiles[i][0] == tile_data[0]):
                                            # Combine
                                            new_num = final_tiles[i][0] + final_tiles[new_tile][0]
                                            final_tiles[i] = [new_num, 1]
                                            # Don't add new tile, just edit existing
                                        else:
                                            final_coords[1] += 1
                                            new_tile = f"{final_coords[0]}{final_coords[1]}"
                                            final_tiles[new_tile] = tile_data
                                            # Finish this tile here
                            else:

                                if coords[1] == 3:
                                    # three possible moves up
                                    final_coords[1] -= 1
                                    new_tile = f"{final_coords[0]}{final_coords[1]}"

                                    # if tile above it, can combine?
                                    if new_tile in final_tiles:
                                        for i in list(final_tiles):
                                            # Can combine?
                                            if i == new_tile:
                                                if final_tiles[i][1] == 0 and (final_tiles[i][0] == tile_data[0]):
                                                    # Combine
                                                    new_num = final_tiles[i][0] + final_tiles[new_tile][0]
                                                    final_tiles[i] = [new_num, 1]
                                                    # Don't add new tile, just edit existing
                                                else:
                                                    final_coords[1] += 1
                                                    new_tile = f"{final_coords[0]}{final_coords[1]}"
                                                    final_tiles[new_tile] = tile_data
                                                    # Finish this tile here
                                    else:
                                        final_tiles[new_tile] = tile_data
                                else:
                                    final_tiles[new_tile] = tile_data
                        else:
                            # One tile move
                            final_tiles[new_tile] = tile_data
            final_tiles_set = final_tiles_set | final_tiles 


        elif move == DOWN:
            # Sort by column, down to Up (16 to 1)
            # Use for Down Move
            tiles = dict(sorted(tiles.items(), reverse=True))

            for tile in tiles:
                coords_string = list(tile)
                
                coords = []
                final_coords = []
                # Add the final coords in

                tile_data = tiles[tile]
                for num in coords_string:
                    coords.append(int(num))
                    final_coords.append(int(num))

                if coords[1] == 3:
                    new_tile = f"{coords[0]}{coords[1]}"
                    final_tiles[new_tile] = tile_data

                # at least one possible move down
                elif coords[1] <= 2:

                    # Set up loop to loop through y value times, capturing
                    # the highest y it can do?
                    final_coords[1] += 1
                    new_tile = f"{final_coords[0]}{final_coords[1]}"

                    # if tile above it, can combine?
                    if new_tile in final_tiles:
                        for i in list(final_tiles):
                            # Can combine?
                            if i == new_tile:
                                
                                # Issue here with combination
                                if final_tiles[i][1] == 0 and (final_tiles[i][0] == tile_data[0]):
                                    # Combine
                                    new_num = final_tiles[i][0] + final_tiles[new_tile][0]
                                    final_tiles[i] = [new_num, 1]
                                    # Don't add new tile, just edit existing
                                else:
                                    final_coords[1] -= 1
                                    new_tile = f"{final_coords[0]}{final_coords[1]}"
                                    final_tiles[new_tile] = tile_data
                                    # Finish this tile here
                    # no tile above it
                    else:
                        if coords[1] <= 1:
                            # two possible moves down
                            final_coords[1] += 1
                            new_tile = f"{final_coords[0]}{final_coords[1]}"

                            # if tile above it, can combine?
                            if new_tile in final_tiles:
                                for i in list(final_tiles):
                                    # Can combine?
                                    if i == new_tile:
                                        if final_tiles[i][1] == 0 and (final_tiles[i][0] == tile_data[0]):
                                            # Combine
                                            new_num = final_tiles[i][0] + final_tiles[new_tile][0]
                                            final_tiles[i] = [new_num, 1]
                                            # Don't add new tile, just edit existing
                                        else:
                                            final_coords[1] -= 1
                                            new_tile = f"{final_coords[0]}{final_coords[1]}"
                                            final_tiles[new_tile] = tile_data
                                            # Finish this tile here
                            else:

                                if coords[1] == 0:
                                    # three possible moves down
                                    final_coords[1] += 1
                                    new_tile = f"{final_coords[0]}{final_coords[1]}"

                                    # if tile above it, can combine?
                                    if new_tile in final_tiles:
                                        for i in list(final_tiles):
                                            # Can combine?
                                            if i == new_tile:
                                                if final_tiles[i][1] == 0 and (final_tiles[i][0] == tile_data[0]):
                                                    # Combine
                                                    new_num = final_tiles[i][0] + final_tiles[new_tile][0]
                                                    final_tiles[i] = [new_num, 1]
                                                    # Don't add new tile, just edit existing
                                                else:
                                                    final_coords[1] -= 1
                                                    new_tile = f"{final_coords[0]}{final_coords[1]}"
                                                    final_tiles[new_tile] = tile_data
                                                    # Finish this tile here
                                    else:
                                        final_tiles[new_tile] = tile_data
                                else:
                                    final_tiles[new_tile] = tile_data
                        else:
                            # One tile move
                            final_tiles[new_tile] = tile_data
            final_tiles_set = final_tiles_set | final_tiles 


        if move == LEFT:
            # Sort by row left to right
            # Use for Left Move
            tiles = dict(sorted(tiles.items(), key=lambda x: (x[0][1], x[0][0])))

            for tile in tiles:
                coords_string = list(tile)
                
                coords = []
                final_coords = []
                # Add the final coords in

                tile_data = tiles[tile]
                for num in coords_string:
                    coords.append(int(num))
                    final_coords.append(int(num))

                if coords[0] == 0:
                    new_tile = f"{coords[0]}{coords[1]}"
                    final_tiles[new_tile] = tile_data

                # at least one possible move left
                elif coords[0] >= 1:

                    # Set up loop to loop through y value times, capturing
                    # the highest y it can do?
                    final_coords[0] -= 1
                    new_tile = f"{final_coords[0]}{final_coords[1]}"

                    # if tile above it, can combine?
                    if new_tile in final_tiles:
                        for i in list(final_tiles):
                            # Can combine?
                            if i == new_tile:
                                
                                # Issue here with combination
                                if final_tiles[i][1] == 0 and (final_tiles[i][0] == tile_data[0]):
                                    # Combine
                                    new_num = final_tiles[i][0] + final_tiles[new_tile][0]
                                    final_tiles[i] = [new_num, 1]
                                    # Don't add new tile, just edit existing
                                else:
                                    final_coords[0] += 1
                                    new_tile = f"{final_coords[0]}{final_coords[1]}"
                                    final_tiles[new_tile] = tile_data
                                    # Finish this tile here
                    # no tile above it
                    else:
                        if coords[0] >= 2:
                            # two possible moves left
                            final_coords[0] -= 1
                            new_tile = f"{final_coords[0]}{final_coords[1]}"

                            # if tile above it, can combine?
                            if new_tile in final_tiles:
                                for i in list(final_tiles):
                                    # Can combine?
                                    if i == new_tile:
                                        if final_tiles[i][1] == 0 and (final_tiles[i][0] == tile_data[0]):
                                            # Combine
                                            new_num = final_tiles[i][0] + final_tiles[new_tile][0]
                                            final_tiles[i] = [new_num, 1]
                                            # Don't add new tile, just edit existing
                                        else:
                                            final_coords[0] += 1
                                            new_tile = f"{final_coords[0]}{final_coords[1]}"
                                            final_tiles[new_tile] = tile_data
                                            # Finish this tile here
                            else:

                                if coords[0] == 3:
                                    # three possible moves left
                                    final_coords[0] -= 1
                                    new_tile = f"{final_coords[0]}{final_coords[1]}"

                                    # if tile above it, can combine?
                                    if new_tile in final_tiles:
                                        for i in list(final_tiles):
                                            # Can combine?
                                            if i == new_tile:
                                                if final_tiles[i][1] == 0 and (final_tiles[i][0] == tile_data[0]):
                                                    # Combine
                                                    new_num = final_tiles[i][0] + final_tiles[new_tile][0]
                                                    final_tiles[i] = [new_num, 1]
                                                    # Don't add new tile, just edit existing
                                                else:
                                                    final_coords[0] += 1
                                                    new_tile = f"{final_coords[0]}{final_coords[1]}"
                                                    final_tiles[new_tile] = tile_data
                                                    # Finish this tile here
                                    else:
                                        final_tiles[new_tile] = tile_data
                                else:
                                    final_tiles[new_tile] = tile_data
                        else:
                            # One tile move
                            final_tiles[new_tile] = tile_data
            final_tiles_set = final_tiles_set | final_tiles 


        elif move == RIGHT:
            # Sort by row, right to left starting at the bottom
            # Use for Right Move
            tiles = dict(sorted(tiles.items(), key=lambda x: (x[0][1], x[0][0]), reverse=True))

            for tile in tiles:
                coords_string = list(tile)
                
                coords = []
                final_coords = []
                # Add the final coords in

                tile_data = tiles[tile]
                for num in coords_string:
                    coords.append(int(num))
                    final_coords.append(int(num))

                if coords[0] == 3:
                    new_tile = f"{coords[0]}{coords[1]}"
                    final_tiles[new_tile] = tile_data

                # at least one possible move right
                elif coords[0] <= 2:

                    # Set up loop to loop through y value times, capturing
                    # the highest y it can do?
                    final_coords[0] += 1
                    new_tile = f"{final_coords[0]}{final_coords[1]}"

                    # if tile above it, can combine?
                    if new_tile in final_tiles:
                        for i in list(final_tiles):
                            # Can combine?
                            if i == new_tile:
                                
                                # Issue here with combination
                                if final_tiles[i][1] == 0 and (final_tiles[i][0] == tile_data[0]):
                                    # Combine
                                    new_num = final_tiles[i][0] + final_tiles[new_tile][0]
                                    final_tiles[i] = [new_num, 1]
                                    # Don't add new tile, just edit existing
                                else:
                                    final_coords[0] -= 1
                                    new_tile = f"{final_coords[0]}{final_coords[1]}"
                                    final_tiles[new_tile] = tile_data
                                    # Finish this tile here
                    # no tile above it
                    else:
                        if coords[0] <= 1:
                            # two possible moves right
                            final_coords[0] += 1
                            new_tile = f"{final_coords[0]}{final_coords[1]}"

                            # if tile above it, can combine?
                            if new_tile in final_tiles:
                                for i in list(final_tiles):
                                    # Can combine?
                                    if i == new_tile:
                                        if final_tiles[i][1] == 0 and (final_tiles[i][0] == tile_data[0]):
                                            # Combine
                                            new_num = final_tiles[i][0] + final_tiles[new_tile][0]
                                            final_tiles[i] = [new_num, 1]
                                            # Don't add new tile, just edit existing
                                        else:
                                            final_coords[0] -= 1
                                            new_tile = f"{final_coords[0]}{final_coords[1]}"
                                            final_tiles[new_tile] = tile_data
                                            # Finish this tile here
                            else:

                                if coords[0] == 0:
                                    # three possible moves right
                                    final_coords[0] += 1
                                    new_tile = f"{final_coords[0]}{final_coords[1]}"

                                    # if tile above it, can combine?
                                    if new_tile in final_tiles:
                                        for i in list(final_tiles):
                                            # Can combine?
                                            if i == new_tile:
                                                if final_tiles[i][1] == 0 and (final_tiles[i][0] == tile_data[0]):
                                                    # Combine
                                                    new_num = final_tiles[i][0] + final_tiles[new_tile][0]
                                                    final_tiles[i] = [new_num, 1]
                                                    # Don't add new tile, just edit existing
                                                else:
                                                    final_coords[0] -= 1
                                                    new_tile = f"{final_coords[0]}{final_coords[1]}"
                                                    final_tiles[new_tile] = tile_data
                                                    # Finish this tile here
                                    else:
                                        final_tiles[new_tile] = tile_data
                                else:
                                    final_tiles[new_tile] = tile_data
                        else:
                            # One tile move
                            final_tiles[new_tile] = tile_data
            final_tiles_set = final_tiles_set | final_tiles 

        return final_tiles_set


    def reset_merges(tiles):
        # Resets merges each tiles values to go from 1 to 0
        for tile in tiles:
            tile_val = tiles[tile][1]
            if tiles[tile][1] == 1:
                tiles[tile][1] = 0




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
                new_tiles = valid_move(tiles, move)
                reset_merges(new_tiles)
                tiles = copy.deepcopy(new_tiles)
                place_tiles(tiles)
                move = None
                game_state = AWAITING_INPUT


        for i in range(grid):
            temp_x = i * cell_size
            for j in range(grid):
                temp_y = j * cell_size
                if (i % 2) == 0:
                    if (j % 2) == 0:
                        pygame.draw.rect(screen, BACKGROUND, (temp_x, temp_y, cell_size, cell_size))
                    else:
                        pygame.draw.rect(screen, BACKGROUND, (temp_x, temp_y, cell_size, cell_size))
                else:
                    if (j % 2) == 0:
                        pygame.draw.rect(screen, BACKGROUND, (temp_x, temp_y, cell_size, cell_size))
                    else:
                        pygame.draw.rect(screen, BACKGROUND, (temp_x, temp_y, cell_size, cell_size))


        # Horizontal Bars
        pygame.draw.rect(screen, GRID, (0, 0, screen_width, 10))
        pygame.draw.rect(screen, GRID, (0, (tile_size + 10), screen_width, 10))
        pygame.draw.rect(screen, GRID, (0, (2 * (tile_size + 10)), screen_width, 10))
        pygame.draw.rect(screen, GRID, (0, (3 * (tile_size + 10)), screen_width, 10))
        pygame.draw.rect(screen, GRID, (0, (screen_height - 10), screen_width, 10))

        # Vertical Bars
        pygame.draw.rect(screen, GRID, (0, 0, 10, screen_height))
        pygame.draw.rect(screen, GRID, ((tile_size + 10), 0, 10, screen_height))
        pygame.draw.rect(screen, GRID, ((2 * (tile_size + 10)), 0, 10, screen_height))
        pygame.draw.rect(screen, GRID, ((3 * (tile_size + 10)), 0, 10, screen_height))
        pygame.draw.rect(screen, GRID, ((screen_width - 10), 0, 10, screen_height))
        
        draw_tiles()

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
