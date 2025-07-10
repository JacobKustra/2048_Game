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

    # "x,y": [value, has combined this round?]
    tiles = {
        "11": [2, 0],
        "33": [2, 0],
        "00": [2, 0],
        "01": [2, 0],
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
            text = FONT.render(str(tiles[tile][0]), 1, FONT_COLOR)
            screen.blit(
                text,
                (
                    tile_x + (tile_size / 2 - text.get_width() / 2),
                    tile_y + (tile_size / 2 - text.get_height() / 2),
                ),
            )


    def calc_farthest_move(new_tiles, tile_to_check, move):
        if len(new_tiles) == 0:
            pass
            # no need to do check of other tiles, just if move is valid

    def valid_move(tile, move, new_tiles):
        coords_string = list(tile)
        coords = []
        final_coords = []
        tile_data = tiles[tile]
        for num in coords_string:
            coords.append(int(num))
        if move == UP:
            if coords[1] == 0:
                new_tile = f"{coords[0]}{coords[1]}"
                new_tiles[new_tile] = tile_data
                # Should this return the final tile?

            elif coords[1] >= 1:
                # at least one possible move up

                # Set up loop to loop through y value times, capturing
                # the highest y it can do?
                coords[1] -= 1
                new_tile = f"{coords[0]}{coords[1]}"

                # if tile above it, can combine?
                if new_tile in new_tiles:
                    for i in new_tiles:
                        # Can combine?
                        if i == new_tile:
                            if new_tiles[i][1] == 0:
                                # Combine
                                new_num = new_tiles[i][0] + new_tiles[new_tile][0]
                                new_tiles[i] = [new_num, 1]
                                print(new_tiles[i])
                                # Don't add new tile, just edit existing
                            else:
                                coords[1] += 1
                                new_tile = f"{coords[0]}{coords[1]}"
                                new_tiles[new_tile] = tile_data
                                # Finish this tile here
                        pass
                else:
                    # move valid, return one move up
                    coords[1] += 1
                    new_tile = f"{coords[0]}{coords[1]}"
                    new_tiles[new_tile] = tile_data
                    # Finish this tile here

                if coords[1] >= 2:
                    # two possible moves up
                    pass
                    if coords[1] == 3:
                        # three possible moves up
                        pass

        # add other moves
        return new_tiles

    

    def move_tiles(tiles):

        '''
        move first,
        then based on move sort tiles,
        then iterate through sorted tiles (first to last),
        while iterating through, check if move is allowed and for possible 
        combinations
        ** moves need to occur to their maximum direction, ie as far as they
        can move in the selected direction **
        '''

        new_tiles = {}

        if move == UP:
            # Sort by column up to down (1 to 16)
            # Use for Up Move
            tiles = dict(sorted(tiles.items()))
            for tile in tiles:
                coords_string = list(tile)
                coords = []
                tile_data = tiles[tile]
                for num in coords_string:
                    coords.append(int(num))
                # Up Limit
                if coords[1] == 0:
                    new_tile = f"{coords[0]}{coords[1]}"
                else:
                    # check if one move up is valid, if yes, then try to 
                    # see if two moves above is valid, etc in order 
                    # to find max move possible
                    coords[1] -= 1
                    new_tile = f"{coords[0]}{coords[1]}"
                    # check here to see if this exsists already
                    if new_tile in new_tiles:
                        # Check if tiles can combine, if not reset it

                        valid_move(tile, move, new_tiles)
                        print(new_tiles)
                        pass

                        # if valid_move():
                        #     pass
                        # else:
                        #     coords[1] += 1
                        #     new_tile = f"{coords[0]}{coords[1]}"
                        
                new_tiles[new_tile] = tile_data



        elif move == DOWN:
            # Sort by column, down to Up (16 to 1)
            # Use for Down Move
            tiles = dict(sorted(tiles.items(), reverse=True))
        elif move == LEFT:
            # Sort by row left to right
            # Use for Left Move
            tiles = dict(sorted(tiles.items(), key=lambda x: (x[0][1], x[0][0])))
        elif move == RIGHT:
            # Sort by row, right to left starting at the bottom
            # Use for Right Move
            tiles = dict(sorted(tiles.items(), key=lambda x: (x[0][1], x[0][0]), reverse=True))

        return new_tiles

        #for tile in tiles:
        #    coords_string = list(tile)
        #    coords = []
        #    tile_data = tiles[tile]
        #    for num in coords_string:
        #        coords.append(int(num))
        #    if move == UP:
        #        if coords[1] == 0:
        #            new_tile = f"{coords[0]}{coords[1]}"
        #        else:
        #            coords[1] -= 1
        #        new_tile = f"{coords[0]}{coords[1]}"
        #        new_tiles[new_tile] = tile_data
        #    elif move == DOWN:
        #        if coords[1] == 3:
        #            pass
        #        else:
        #            coords[1] += 1
        #        new_tile = f"{coords[0]}{coords[1]}"
        #        new_tiles[new_tile] = tile_data
        #    elif move == LEFT:
        #        if coords[0] == 0:
        #            pass
        #        else:
        #            coords[0] -= 1
        #        new_tile = f"{coords[0]}{coords[1]}"
        #        new_tiles[new_tile] = tile_data
        #    elif move == RIGHT:
        #        if coords[0] == 3:
        #            pass
        #        else:
        #            coords[0] += 1
        #        new_tile = f"{coords[0]}{coords[1]}"
        #        new_tiles[new_tile] = tile_data
        #return new_tiles


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
                new_tiles = move_tiles(tiles)
                tiles = new_tiles.copy()
                # place_tiles(tiles)
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

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
