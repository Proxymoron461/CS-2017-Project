# import modules/ scripts
import pygame
import random
import math
import grid_class

# defining a few colours, using their RGB value
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SEA_BLUE = (0, 191, 255)  # colour for sea

# initialise window height and width
WIDTH = 700
HEIGHT = 500

# initialising the pygame engine
pygame.init()

# setting the borderless window
size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)  # creates display window
pygame.display.set_caption("Pyrate!")  # sets the window title


# define player class
class Player(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y):
        super().__init__()
        self.change_x = 0  # player speed left and right, starts at 0
        self.change_y = 0  # player speed up and down, starts at 0
        self.speed = 3  # player speed variable
        self.size = 30  # player rectangle longest length size
        self.height = 30
        self.width = 18
        self.ship_size = 30  # integer for size of ship rectangle
        # set up player pirate sprites
        self.down_image1 = pygame.image.load("Walking_player_spr.png").convert()
        self.down_image1.set_colorkey(WHITE)
        self.down_image2 = pygame.image.load("Walking_player_spr_2.png").convert()
        self.down_image2.set_colorkey(WHITE)
        self.up_image1 = pygame.image.load("Walking_back_player_spr.png").convert()
        self.up_image1.set_colorkey(WHITE)
        self.up_image2 = pygame.image.load("Walking_back_player_spr_2.png").convert()
        self.up_image2.set_colorkey(WHITE)
        self.left_image1 = pygame.image.load("Walking_left_player_spr.png").convert()
        self.left_image1.set_colorkey(WHITE)
        self.left_image2 = pygame.image.load("Walking_left_player_spr_2.png").convert()
        self.left_image2.set_colorkey(WHITE)
        self.right_image1 = pygame.image.load("Walking_right_player_spr.png").convert()
        self.right_image1.set_colorkey(WHITE)
        self.right_image2 = pygame.image.load("Walking_right_player_spr_2.png").convert()
        self.right_image2.set_colorkey(WHITE)
        self.curr_image = self.down_image1
        # set up player ship sprites
        self.ship_up_spr = pygame.image.load("Ship_up_spr.png").convert()
        self.ship_up_spr.set_colorkey(WHITE)
        self.ship_down_spr = pygame.image.load("Ship_down_spr.png").convert()
        self.ship_down_spr.set_colorkey(WHITE)
        self.ship_left_spr = pygame.image.load("Ship_left_spr.png").convert()
        self.ship_left_spr.set_colorkey(WHITE)
        self.ship_right_spr = pygame.image.load("Ship_right_spr.png").convert()
        self.ship_right_spr.set_colorkey(WHITE)
        self.image_timer = 0
        self.rect = self.curr_image.get_rect()
        self.ship_rect = self.ship_up_spr.get_rect()
        self.health_image = pygame.image.load("Health.png").convert()
        self.health_image.set_colorkey(WHITE)
        self.health_rect = self.health_image.get_rect()
        self.rect.x = start_x  # player x position
        self.rect.y = start_y  # player y position
        self.last_x = 0  # most recent x direction of player
        self.last_y = -1  # most recent y direction of player
        self.health = 5  # integer for player health
        self.max_health = 5  # integer for maximum player health
        self.invulnerable = False  # boolean for if player is invulnerable or not
        self.invulnerable_timer = pygame.time.get_ticks()  # create reference timer for invulnerability period
        self.health_flicker_timer = pygame.time.get_ticks()  # create reference timer for health flicker
        self.inventory = []  # empty list for use as inventory
        self.draw_health = True  # boolean to check if health should be drawn
        self.banner = pygame.image.load("Banner.png").convert()  # sprite for player message banner
        self.banner.set_colorkey(WHITE)
        self.banner_rect = self.banner.get_rect()
        self.pause_timer = 0  # timer for keeping the other timers ticking during the pause period
        self.on_island = False  # boolean for tracking if the player landed on an island

    # method for updating player movement on the map screem
    def move_map(self):
        self.rect.x += self.change_x
        self.rect.y += self.change_y

    # method for updating player movement on islands and in dungeons
    def move_close(self, location_rect):
        self.rect.clamp_ip(location_rect)  # keep player on island
        self.rect.x += self.change_x
        self.rect.y += self.change_y

    # method to draw player pirate sprites to screen
    def draw(self, screen):
        # code to ensure correct image is drawn
        if pygame.time.get_ticks() - self.image_timer > 500:

            if self.curr_image == self.up_image1:
                self.curr_image = self.up_image2
            elif self.curr_image == self.up_image2:
                self.curr_image = self.up_image1

            elif self.curr_image == self.left_image1:
                self.curr_image = self.left_image2
            elif self.curr_image == self.left_image2:
                self.curr_image = self.left_image1

            elif self.curr_image == self.right_image1:
                self.curr_image = self.right_image2
            elif self.curr_image == self.right_image2:
                self.curr_image = self.right_image1

            elif self.curr_image == self.down_image1:
                self.curr_image = self.down_image2
            elif self.curr_image == self.down_image2:
                self.curr_image = self.down_image1

            self.image_timer = pygame.time.get_ticks()  # reset image timer

        screen.blit(self.curr_image, [self.rect.x, self.rect.y])  # blit current player image to screen

    # method to draw player ship sprite to screen
    def draw_map(self, screen):
        screen.blit(self.curr_image, [self.rect.x, self.rect.y])

    # method to take damage from player health
    def take_damage(self, damage):
        self.health -= damage  # take away enemy damage from player health

    # method to output a given message to the screen on a banner sprite
    def message(self, text):
        output_text = font.render(text, True, BLACK)
        screen.blit(self.banner, [0, 0])
        screen.blit(output_text, [20, 10])

    # method to stop player movement
    def halt_speed(self):
        player_obj.change_y = 0
        player_obj.change_x = 0

    # method to draw player health bar
    def draw_player_health(self, screen):
        if self.draw_health:  # if player has health
            for hp in range(self.health):
                screen.blit(self.health_image, [WIDTH - 40, (20 + hp * 35)])

    # method to make player's health bar flicker
    def health_invulnerable_flicker(self, screen):
        # code to make health timer flicker
        if self.invulnerable:
            if (pygame.time.get_ticks() - self.health_flicker_timer) > 300:
                if self.draw_health:
                    self.draw_health = False
                    self.health_flicker_timer = pygame.time.get_ticks()
                else:
                    self.draw_health = True
                    self.health_flicker_timer = pygame.time.get_ticks()
        else:
            self.draw_health = True


# initialise player object
player_obj = Player(350, 250)


# initialise island class
class Island(pygame.sprite.Sprite):
    def __init__(self, height, width, position_x, position_y, type):
        super().__init__()
        self.height = height
        self.width = width
        self.width_map = width / 4
        self.height_map = height / 4
        self.position_x_close = (WIDTH / 2) - (self.width / 2)  # x position of island sprite on overview screen
        self.position_y_close = (HEIGHT / 2) - (self.height / 2)  # y position of island sprite on overview screen
        if type == "centre":  # if centre island object, give specific centre island appearance
            self.image = pygame.image.load("CentreIslandClose.png").convert()
            self.image.set_colorkey(WHITE)
            self.image_map = pygame.image.load("CentreIslandMap.png").convert()
            self.image_map.set_colorkey(WHITE)
            self.door = DungeonDoor((WIDTH / 2) - 15, self.position_y_close + 40)
        else:  # if not centre island object, give random island appearance
            self.appearance = random.choice(["Sand", "Grass", "Rock"])
            if self.appearance == "Sand":  # set sandy island sprites
                self.image = pygame.image.load("SandIslandClose.png").convert()
                self.image.set_colorkey(WHITE)
                self.image_map = pygame.image.load("SandIslandMap.png").convert()
                self.image_map.set_colorkey(WHITE)
            elif self.appearance == "Grass":  # set grassy island sprites
                self.image = pygame.image.load("Grass_island_spr.png").convert()
                self.image.set_colorkey(WHITE)
                self.image_map = pygame.image.load("Grass_map_spr.png").convert()
                self.image_map.set_colorkey(WHITE)
            elif self.appearance == "Rock":  # set rocky island sprites
                self.image = pygame.image.load("Rock_island_spr.png").convert()
                self.image.set_colorkey(WHITE)
                self.image_map = pygame.image.load("Rock_island_map_spr.png").convert()
                self.image_map.set_colorkey(WHITE)

        # rect attributes for island sprite while on map screen
        self.rect = self.image_map.get_rect()
        self.rect.x = position_x
        self.rect.y = position_y

        # rect attributes for island sprite while on overview screen
        self.rect_close = self.image.get_rect()
        self.rect_close.x = self.position_x_close
        self.rect_close.y = self.position_y_close
        self.boundary_rect = [self.position_x_close + 5, self.position_y_close + 5, self.height - 10,
                              self.width - 10]  # rectangle for keeping player in island

        self.overview = False  # boolean to tell if island overview screen should be displayed or not
        self.off = False  # boolean to check if player has left island
        self.chest_open = False  # boolean to check if island chest is open
        self.island_location = False  # boolean to determine if island spawn location is all good (no collisions)
        self.breakables = pygame.sprite.Group()  # create list of breakable items per location
        self.enemies = pygame.sprite.Group()  # create list of enemies per location
        # create graph with grid_class script
        self.graph = grid_class.Grid(self.height, self.width)
        self.chest = TreasureChest(40, self.position_x_close + (self.width / 2) - 20, self.position_y_close + 40 - 20,
                                   "Example Treasure")
        chests.add(self.chest)  # add chest to chest sprite group

    def draw_close(self, screen):  # island drawing code for when game is on island
        screen.blit(self.image, [self.rect_close.x, self.rect_close.y])

    def draw_map(self, screen):  # island drawing code for when game is on map screen
        screen.blit(self.image_map, [self.rect.x, self.rect.y])

    def place_in_graph(self, item, item_pos):  # method to place item in centre of graph
        self.graph.place_in_position(item_pos, item, self)

    # method for what to do if player has collided with the island on the map screen
    def island_collision(self):

        # changes location overview
        map.overview = False
        self.overview = True
        player_obj.on_island = True

        # code to determine player position
        player_obj.rect.y = self.position_y_close + (self.height * 0.8)
        player_obj.rect.x = self.position_x_close + (self.width / 2) - (player_obj.size / 2)
        player_obj.halt_speed()  # stop player position
        player_obj.invulnerable_timer = pygame.time.get_ticks()  # make player invulnerable for length of timer

        # code to set player sprite to pirate
        player_obj.curr_image = player_obj.up_image1

    # method to check if player is in a position to leave the island or not
    def check_leave_island(self):
        # code to check if island is being left
        if player_obj.rect.y + player_obj.size >= self.position_y_close + self.height - player_obj.speed:
            # change game overview screen
            self.overview = False
            map.overview = True
            self.off = True

    def leave_island(self):
        # code to determine player position once left island
        player_obj.rect.y = self.rect.y + self.height_map + 5
        player_obj.rect.x = self.rect.x + (self.width_map / 2) - (player_obj.size / 2)
        player_obj.halt_speed()
        self.off = False
        self.chest.treasure_message_display = False  # stop displaying treasure message
        bullets.empty()  # remove all bullets from group
        # code to set player ship sprite
        player_obj.curr_image = player_obj.ship_down_spr

    # create location overview method
    def location_loop(self):
        # access global variables
        global done

        # ensure player speed does not carry over
        player_obj.halt_speed()

        # reset map ocean timer
        map.ocean_switch_timer = 0

        while self.overview:
            # code for key presses + movement
            location_movement(self, self.enemies)

            # fill screen with background colour
            screen.fill(SEA_BLUE)

            # draw ocean to screen
            map.draw_ocean_island()

            # draw the island up close
            self.draw_close(screen)

            # what happens when player spawns on island
            if player_obj.on_island:
                # land_on_island(self)
                enemy_delay(self.enemies)

            # code to remove enemies from island_obj.enemies list, draw them to screen, and have them attack
            enemy_draw_move(self, self.enemies, self.rect_close)

            # code to do things if not on centre island
            if self != centre_island_obj:
                # code to spawn chest on island
                if not self.enemies:
                    self.chest.draw(screen)

                # code to handle collision and treasure message
                self.chest.check_collision(self.enemies)

                # make player leave if exit bottom of island
                self.check_leave_island()

            # have player attack (on island)
            player_obj.move_close(self.boundary_rect)

            # code to check if enemies are dead or not
            enemy_health_check()

            # code to check if player can be hit
            check_player_invulnerable()

            # code to check collision between player and enemy
            check_player_enemy_collision(self.enemies)

            # code to check collision between bullet and sword
            if sword_obj.will_draw:
                # check sword-bullet collision
                check_sword_bullet_collision()

            # code to check collision between player and bullet
            check_player_bullet_collision()

            # check if breakable object is broken
            sword_obj.check_break(self, self.breakables)

            # check if on centre island
            if self == centre_island_obj:
                # draw the door on the island
                self.door.draw(screen)

                # check collision with door on island
                if pygame.sprite.collide_rect(player_obj, self.door):
                    check_player_door_collision(self, dungeon_entrance_obj, dungeon_entrance_obj.enemies)

                # display tutorial messages
                for tutorial in tutorials:
                    tutorial.show_tutorial(self)

                # remove tutorial messages
                if centre_pot_obj.broken:
                    centre_sword_tutorial.end_tutorial()
                    self.check_leave_island()
                if player_obj.change_x != 0 or player_obj.change_y != 0:
                    movement_tutorial.end_tutorial()
                if player_obj.rect.y + player_obj.size >= self.position_y_close + self.height - (player_obj.speed * 2):
                    pause_tutorial.end_tutorial()

            # draw breakable objects to screen
            for breakable in self.breakables:
                breakable.draw(screen)

            # procedure to check for player death and draw to screen
            player_draw_or_die()

            # code to check bullet shooting
            if bullets:
                draw_bullet()

            # draw sword to screen
            draw_sword(self.enemies)

            # update screen and framerate
            screen_update()


# create dungeon door class, for use
class DungeonDoor(pygame.sprite.Sprite):
    def __init__(self, position_x, position_y):
        super().__init__()
        self.height = 40  # attribute for door height
        self.width = 30  # attribute for door width
        self.image = pygame.image.load("Door.png").convert()  # load sprite from file
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()  # generate rect from sprite
        self.rect.x = position_x  # set door x position
        self.rect.y = position_y  # set door y position
        self.can_open = False  # boolean to check if door can be opened

    # method to draw dungeon door to screen
    def draw(self, screen):
        screen.blit(self.image, [self.rect.x, self.rect.y])

    # method for what to do when a dungeon door is opened
    def open_door(self, curr_location, destination, destination_enemies_list):
        # change game overview
        curr_location.overview = False
        destination.overview = True
        destination.room_entry = True

    # method to check if a dungeon door should be opened or not
    def check_open(self, curr_location):
        if curr_location == centre_island_obj:  # if player on centre island
            # only open door if player has collected all treasures and the centre pot is gone
            if len(player_obj.inventory) == len(islands) - 1 and centre_pot_obj.broken:
                self.can_open = True
            elif centre_pot_obj.broken:
                player_obj.message("Leave the island to the south. Come back with the treasures.")
        elif curr_location == dungeon_entrance_obj:  # if player in dungeon entrance
            if not dungeon_entrance_obj.enemies:
                self.can_open = True
        else:  #  if player in any other location
            self.can_open = True


# create dungeon class, for use
class Dungeon(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.overview = False  # boolean for if dungeon level is on screen
        self.height = 400  # dungeon floor sprite height
        self.width = 600  # dungeon floor sprite width
        # load dungeon sprite from file
        self.image = pygame.image.load("Dungeon_floor_spr.png").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.wall_image = pygame.image.load("Dungeon_wall_spr.png").convert()
        self.wall_image.set_colorkey(WHITE)
        # set dungeon floor sprite position
        self.rect.x = 50
        self.rect.y = 50
        self.chest_open = False  # boolean for if chest is open
        self.breakables = pygame.sprite.Group()  # create list of breakable items per location
        self.enemies = pygame.sprite.Group()  # create list of enemies per location
        # create graph with grid_class script
        self.graph = grid_class.Grid(self.height, self.width)
        self.door = DungeonDoor(self.rect.x + ((self.width / 2) - 15), self.rect.y - 40)
        self.room_entry = True  # boolean for if the player has entered the room

    # method to draw dungeon floor and wall sprites to screen
    def draw(self, screen):
        screen.blit(self.image, [self.rect.x, self.rect.y])

    # method to place item in centre of graph
    def place_in_graph(self, item, item_pos):
        self.graph.place_in_position(item_pos, item, self)

    # method for overview loop
    def location_loop(self):
        # access global variables
        global treasure_message_timer
        global done

        # ensure player speed does not carry over
        player_obj.halt_speed()

        # while in dungeon entrance
        while self.overview:

            # code for key presses + movement
            location_movement(self, self.enemies)

            # display background image
            screen.blit(self.wall_image, [0, 0])

            # draw dungeon entrance floor
            dungeon_entrance_obj.draw(screen)

            # code to check if player has entered room from bottom
            if self.room_entry:
                enter_room_lower(self, self.door)
                enemy_delay(self.enemies)

            # code to draw enemies to screen
            enemy_draw_move(self, self.enemies, self.rect)

            # have player move (within dungeon bounds)
            player_obj.move_close(self)

            # code to check if enemies are dead or not
            enemy_health_check()

            # code to check if player can be hit
            check_player_invulnerable()

            # code to check collision between player and enemy
            check_player_enemy_collision(self.enemies)

            # code to check collision between bullet and sword
            if sword_obj.will_draw:
                # check sword-bullet collision
                check_sword_bullet_collision()

            # code to check collision between player and bullet
            check_player_bullet_collision()

            # check if door can spawn
            if not self.enemies:
                if self == dungeon_entrance_obj:
                    self.door.draw(screen)
                    # check player-door collision
                    if pygame.sprite.collide_rect(player_obj, self.door):
                        check_player_door_collision(self, dungeon_second_room_obj, dungeon_second_room_obj.enemies)
                elif self == dungeon_second_room_obj:
                    end_chest.draw(screen)
                    end_chest.check_end_game(self)

            # display player movements to screen
            player_draw_or_die()

            # code to check bullet shooting
            if bullets:
                draw_bullet()

            # draw sword to screen
            draw_sword(self.enemies)

            # update screen and framerate
            screen_update()


# create dungeon objects
dungeon_entrance_obj = Dungeon()
dungeon_second_room_obj = Dungeon()

# create list of dungeon objects
dungeons = pygame.sprite.Group()
dungeons.add(dungeon_entrance_obj, dungeon_second_room_obj)


# create map class, for use
class Map:
    def __init__(self):
        self.overview = False  # boolean for if map level is on screen
        # load ocean images from file
        self.ocean_image_1 = pygame.image.load("Ocean_1.png").convert()
        self.ocean_image_1.set_colorkey(BLACK)
        self.ocean_image_2 = pygame.image.load("Ocean_2.png").convert()
        self.ocean_image_2.set_colorkey(BLACK)
        self.calm_ocean = pygame.image.load("Base_ocean.png").convert()
        self.calm_ocean.set_colorkey(BLACK)
        self.island_ocean_1 = pygame.image.load("Island_ocean.png").convert()
        self.island_ocean_1.set_colorkey(BLACK)
        self.island_ocean_2 = pygame.image.load("Island_ocean_2.png").convert()
        self.island_ocean_2.set_colorkey(BLACK)
        self.ocean_switch = False  # boolean to check if ocean image should swap or not
        self.curr_image = self.ocean_image_1
        self.curr_image_island = self.island_ocean_1
        self.ocean_switch_timer = 0  # set ocean image timer to 0

    # overview loop method for map screen
    def world_map(self):
        # ensure player speed does not carry over
        player_obj.halt_speed()

        # reset ocean display timer
        map.ocean_switch_timer = 0

        # map loop
        while self.overview:
            # procedure for key presses and movement
            map_movement()

            # fill screen with background colour
            screen.fill(SEA_BLUE)

            # draw map to screen
            map.draw_ocean_map()

            # draw all islands on map
            for island in islands:
                island.draw_map(screen)
                if island.off:
                    # leave_island(island)
                    island.leave_island()
                if pygame.sprite.collide_rect(player_obj, island):
                    island.island_collision()

            # have player move (map overview) and draw it to screen
            player_obj.move_map()
            player_obj.draw(screen)

            # if player is in map/sailing screen and they go off the edge, make them reappear on the opposite one
            self.wraparound()

            # display output and framerate
            screen_update()

    # procedure to ensure map wrap around to keep player on screen
    def wraparound(self):
        # if player is in map/sailing screen and they go off the edge, make them reappear on the opposite one
        if player_obj.rect.x + player_obj.size < 0:
            player_obj.rect.x = WIDTH + (player_obj.speed // 2)
        elif player_obj.rect.x > WIDTH:
            player_obj.rect.x = (0 - player_obj.size) - (player_obj.speed // 2)
        if player_obj.rect.y + player_obj.size < 0:
            player_obj.rect.y = HEIGHT + (player_obj.speed // 2)
        elif player_obj.rect.y > HEIGHT:
            player_obj.rect.y = (0 - player_obj.size) - (player_obj.speed // 2)

    # method to draw ocean background on map screen
    def draw_ocean_map(self):
        if pygame.time.get_ticks() - self.ocean_switch_timer >= 1000:
            if self.ocean_switch:
                self.curr_image = self.ocean_image_1
                self.ocean_switch_timer = pygame.time.get_ticks()
                self.ocean_switch = False
            else:
                self.curr_image = self.ocean_image_2
                self.ocean_switch_timer = pygame.time.get_ticks()
                self.ocean_switch = True

        screen.blit(self.curr_image, [0, 0])  # blit final ocean image to screen

    # method to draw ocean background on island screen
    def draw_ocean_island(self):
        if pygame.time.get_ticks() - self.ocean_switch_timer >= 500:
            if self.ocean_switch:
                self.curr_image_island = self.island_ocean_1
                self.ocean_switch_timer = pygame.time.get_ticks()
                self.ocean_switch = False
            else:
                self.curr_image_island = self.island_ocean_2
                self.ocean_switch_timer = pygame.time.get_ticks()
                self.ocean_switch = True

        screen.blit(self.curr_image_island, [0, 0])


# create map object
map = Map()


# initialise moving enemy class, intended as parent class for future enemies
class Ghost(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y):
        super().__init__()
        self.change_x = 0  # initial x speed
        self.change_y = 0  # initial y speed
        self.height = 36  # set size
        self.width = 28
        # load sprites from file
        self.image1 = pygame.image.load("Ghost_pirate.png").convert()
        self.image1.set_colorkey(WHITE)
        self.image2 = pygame.image.load("Ghost_pirate_2.png").convert()
        self.image2.set_colorkey(WHITE)
        self.curr_image = self.image1
        self.image_timer = 0
        self.rect = self.curr_image.get_rect()
        self.rect.x = start_x  # enemy x position
        self.rect.y = start_y  # enemy y position
        self.health = 2  # integer for health value, each hit does damage of 2
        self.damage = 1  # boolean for damage enemy does to player health
        self.invulnerable = False  # boolean for if enemy can take damage or not
        self.invulnerable_timer = pygame.time.get_ticks()  # sets the current time as reference for invincibility
        self.attack_timer = pygame.time.get_ticks()  # timer for attack calculation
        self.found_location = False  # boolean to check if position is correct
        self.move = True  # boolean to signify moving enemy
        self.speed = 1.5  # integer for enemy speed
        self.type = "default"  # string for enemy type

    def move_attack(self, location_rect):
        # code to attack enemy towards player aggressively
        if self.type == "default":
            if pygame.time.get_ticks() - self.attack_timer > 1000:
                if abs(player_obj.rect.x - self.rect.x) < abs(player_obj.rect.y - self.rect.y):
                    if player_obj.rect.y > self.rect.y:
                        self.change_x = 0
                        self.change_y = self.speed
                        self.attack_timer = pygame.time.get_ticks() - random.randrange(5000)
                    else:
                        self.change_x = 0
                        self.change_y = -self.speed
                        self.attack_timer = pygame.time.get_ticks() - random.randrange(5000)
                elif abs(player_obj.rect.x - self.rect.x) > abs(player_obj.rect.y - self.rect.y):
                    if player_obj.rect.x > self.rect.x:
                        self.change_x = self.speed
                        self.change_y = 0
                        self.attack_timer = pygame.time.get_ticks() - random.randrange(5000)
                    else:
                        self.change_x = -self.speed
                        self.change_y = 0
                        self.attack_timer = pygame.time.get_ticks() - random.randrange(5000)

        elif self.type == "charge":
            # code to make enemy charge at player
            if pygame.time.get_ticks() - self.attack_timer > 2000:
                x_direction = (player_obj.rect.x - self.rect.x) / math.sqrt((player_obj.rect.x - self.rect.x) ** 2 +
                                                                            (player_obj.rect.y - self.rect.y) ** 2)
                y_direction = (player_obj.rect.y - self.rect.y) / math.sqrt((player_obj.rect.x - self.rect.x) ** 2 +
                                                                            (player_obj.rect.y - self.rect.y) ** 2)
                self.change_x = x_direction * 3
                self.change_y = y_direction * 3
                self.attack_timer = pygame.time.get_ticks() - random.randrange(1000)

        elif self.type == "follow":
            # code to make enemy go in reverse of last player direction
            self.change_x = player_obj.last_x * -1
            self.change_y = player_obj.last_y * -1

        # apply position changes and keep enemy on island
        self.rect.clamp_ip(location_rect)
        self.rect.x += self.change_x
        self.rect.y += self.change_y

    # method to draw enemy sprites to screen
    def draw(self, screen):
        # code to ensure correct image is drawn
        if pygame.time.get_ticks() - self.image_timer > 750:
            if self.curr_image == self.image1:
                self.curr_image = self.image2
            else:
                self.curr_image = self.image1
            self.image_timer = pygame.time.get_ticks()
        screen.blit(self.curr_image, [self.rect.x, self.rect.y])  # draw final sprite to screen


# class for stationary, shooting enemies
class Pirate(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y):
        super().__init__()
        # set sprite size
        self.height = 38
        self.width = 24
        # load sprites from file
        self.image1 = pygame.image.load("Pirate_spr.png").convert()
        self.image1.set_colorkey(WHITE)
        self.image2 = pygame.image.load("Pirate_spr_2.png").convert()
        self.image2.set_colorkey(WHITE)
        self.curr_image = self.image1
        self.image_timer = 0
        self.rect = self.curr_image.get_rect()
        self.rect.x = start_x  # enemy x position
        self.rect.y = start_y  # enemy y position
        self.health = 2  # integer for health value, each hit does damage of 2
        self.invulnerable = False  # boolean for if enemy can be hit
        self.invulnerable_timer = pygame.time.get_ticks()  # sets the current time as reference for invincibility
        self.attack_timer = pygame.time.get_ticks()  # sets the current time as reference for attacking
        self.can_attack = False  # boolean for if the enemy can attack
        self.damage = 0  # integer for how much damage dealt to player health
        self.found_location = False  # boolean to check if position is correct
        self.move = False  # boolean to signify that this is not a moving enemy

    # method for projectile attacks
    def attack(self):
        # access global variables
        global screen
        # check enemy can attack
        if pygame.time.get_ticks() - self.attack_timer >= 2000:
            self.can_attack = True
        if self.can_attack and not pygame.sprite.collide_circle(self, player_obj):
            # code to determine bullet direction and speed
            bullet_x_direction = (player_obj.rect.x - self.rect.x) / math.sqrt((player_obj.rect.x - self.rect.x) ** 2 +
                                                                               (player_obj.rect.y - self.rect.y) ** 2)
            bullet_y_direction = (player_obj.rect.y - self.rect.y) / math.sqrt((player_obj.rect.x - self.rect.x) ** 2 +
                                                                               (player_obj.rect.y - self.rect.y) ** 2)
            bullet_x_speed = bullet_x_direction * 5
            bullet_y_speed = bullet_y_direction * 5
            # create bullet object
            bullet = Bullet(15, self.rect.x, self.rect.y, bullet_x_speed, bullet_y_speed)
            bullets.add(bullet)
            bullet.move()
            bullet.draw(screen)
            self.can_attack = False
            self.attack_timer = pygame.time.get_ticks()

    # method to draw sprite to screen
    def draw(self, screen):
        # code to ensure correct image is drawn
        if pygame.time.get_ticks() - self.image_timer > 750:
            if self.curr_image == self.image1:
                self.curr_image = self.image2
            else:
                self.curr_image = self.image1
            self.image_timer = pygame.time.get_ticks()
        screen.blit(self.curr_image, [self.rect.x, self.rect.y])  # output final sprite to screen


# initialise bullet class, for enemy attacks
class Bullet(pygame.sprite.Sprite):
    def __init__(self, size, start_x, start_y, x_speed, y_speed):
        super().__init__()
        self.size = size
        self.image = pygame.image.load("Bullet.png").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = start_x
        self.rect.y = start_y
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.damage = 1  # integer for damage dealt to player health

    # method to draw bullet sprite to screen
    def draw(self, screen):
        screen.blit(self.image, [self.rect.x, self.rect.y])

    # method to move bullet sprite
    def move(self):
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed


# create class of breakable objects
class BreakObject(pygame.sprite.Sprite):
    def __init__(self, x_position, y_position):
        super().__init__()
        self.size = 40  # set sprite size
        # load image from file
        self.image = pygame.image.load("Break_object.png").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x_position
        self.rect.y = y_position
        self.broken = False  # boolean for if object is broken or not

    # method to draw breakable object to screen
    def draw(self, screen):
        if not self.broken:  # if object is not broken
            screen.blit(self.image, [self.rect.x, self.rect.y])


# initialise sword class, for attacking
class Sword(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # set size
        self.width = 22
        self.height = 22
        # load pygame image sprite
        self.image = pygame.image.load("Sword_spr.png").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = player_obj.rect.x + player_obj.size
        self.rect.y = player_obj.rect.y + player_obj.size
        # create variables for sword image/sprite at different directions
        self.image_up = self.image
        self.image_down = pygame.transform.rotate(self.image, 180)
        self.image_left = pygame.transform.rotate(self.image, 90)
        self.image_right = pygame.transform.rotate(self.image, 270)
        self.curr_image = self.image_up
        self.delay = pygame.time.get_ticks()  # amount of milliseconds before sword sprite disappears
        self.will_draw = False  # boolean to draw sword object onto screen

    # method to draw sprite to screen
    def draw(self, screen):
        screen.blit(self.curr_image, [self.rect.x, self.rect.y])

    # method to handle sword positioning when the player attacks
    def attack(self):
        # code to put rectangle x value at area where character is facing
        if player_obj.last_x > 0:
            self.curr_image = self.image_right
            self.rect = self.image.get_rect()
            self.rect.x = player_obj.rect.x + player_obj.width - 2
        elif player_obj.last_x < 0:
            self.curr_image = self.image_left
            self.rect = self.image.get_rect()
            self.rect.x = player_obj.rect.x - self.height + 2

        # code to put rectangle y value at area where character is facing
        if player_obj.last_y > 0:
            self.curr_image = self.image_down
            self.rect = self.image.get_rect()
            self.rect.y = player_obj.rect.y + player_obj.height - 10
        elif player_obj.last_y < 0:
            self.curr_image = self.image_up
            self.rect = self.image.get_rect()
            self.rect.y = player_obj.rect.y - self.height

        # code to set sword position if character facing opposite plane
        if player_obj.last_x == 0:
            self.rect.x = player_obj.rect.x + (player_obj.width / 2) - (self.width / 2)
        if player_obj.last_y == 0:
            self.rect.y = player_obj.rect.y + (player_obj.height / 2) - (self.width / 2)

    # method to handle sword collision with enemies when player attacks
    def attack_collision(self, enemy_list):
        # create list of enemies hit by player sword
        enemies_hit_list = pygame.sprite.spritecollide(self, enemy_list, False)
        for enemy in enemies_hit_list:
            if not enemy.invulnerable:  # if enemy is not invulnerable
                enemy.health -= 2
                enemy.invulnerable = True
                enemies_hit.add(enemy)

    # method to handle sword collision with breakable objects
    def check_break(self, location, location_breakables):
        # create list of objects broken by player sword
        broken_obj_list = pygame.sprite.spritecollide(self, location_breakables, False)
        for break_obj in broken_obj_list:
            if location.overview:  # only break object when in correct location to break it
                break_obj.broken = True


# create sword object, for use during the game
sword_obj = Sword()


# initialise treasure chest class
class TreasureChest(pygame.sprite.Sprite):
    def __init__(self, size, position_x, position_y, treasure):
        super().__init__()
        self.size = size  # set sprite size
        # load sprite from file
        self.image = pygame.image.load("Chest.png").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.open_image = pygame.image.load("ChestOpen.png").convert()
        self.open_image.set_colorkey(WHITE)
        self.rect.x = position_x
        self.rect.y = position_y
        self.treasure = treasure  # string for treasure in chest
        self.game_end = False  # boolean for if game is ended
        self.treasure_message_timer = pygame.time.get_ticks()  # timer for displaying treasure message
        self.treasure_message_display = True  # boolean for displaying treasure message
        self.open = False  # boolean to check if chest is open

    # method to open chest and add treasure to player inventory
    def pick_treasure(self):
        self.image = self.open_image
        player_obj.message("You found " + self.treasure + "!")
        player_obj.inventory.append(self.treasure)

    # method to change treasure chest treasure name
    def set_treasure(self, treasure_name):
        self.treasure = treasure_name

    # method to check for player-chest collision
    def check_collision(self, curr_location_enemies):
        if pygame.sprite.collide_rect(player_obj,
                                      self) and not self.open and not curr_location_enemies:
            # open chest and display message if collision is detected
            self.pick_treasure()
            self.open = True
            self.treasure_message_timer = pygame.time.get_ticks()
            self.treasure_message_display = True

        # code to check if treasure message should be displayed
        if self.open:
            if pygame.time.get_ticks() - self.treasure_message_timer <= 2000 and self.treasure_message_display:
                player_obj.message("You found " + self.treasure + "!")

    # method to draw chest to screen
    def draw(self, screen):
        screen.blit(self.image, [self.rect.x, self.rect.y])

    # method to end game if final chest is reached
    def check_end_game(self, curr_location):
        # access global variables
        global game_end
        # code to check if game is finished
        if pygame.sprite.collide_rect(player_obj, self):
            game_end = True
            curr_location.overview = False


# create class for tutorial rectangles
class TutorialRect(pygame.sprite.Sprite):
    def __init__(self, width, height, x_position, y_position, message):
        super().__init__()
        # set size
        self.width = width
        self.height = height
        self.image = pygame.Surface([self.width, self.height])  # create image
        self.rect = self.image.get_rect()  # generate rect from image
        self.rect.x = x_position
        self.rect.y = y_position
        self.message = message  # string for tutorial message
        self.shown = False  # boolean for if the tutorial message has been shown or not

    # method for displaying the tutorial message to the screen
    def show_tutorial(self, location):
        if self.rect.colliderect(player_obj) and location.overview and not self.shown:
            player_obj.message(self.message)

    # method to end tutorial message
    def end_tutorial(self):
        self.shown = True


# create class for menu in-game
class Menu:
    def __init__(self):
        # load menu logos from file
        self.logo = pygame.image.load("Menu_logo.png").convert()
        self.logo.set_colorkey(WHITE)
        self.start = pygame.image.load("Menu_start.png").convert()
        self.start.set_colorkey(WHITE)
        self.quit = pygame.image.load("Menu_quit.png").convert()
        self.quit.set_colorkey(WHITE)
        self.sword = pygame.image.load("Menu_sword.png").convert()
        self.sword.set_colorkey(WHITE)
        self.sword_rect = self.sword.get_rect()  # generate sword rect from sprite
        self.sword_position = 0  # integer for sword position index
        self.menu_icons = 2  # attribute for total number of menu icons
        self.menu = True  # boolean for if menu should be displayed

    # method to show game initial menu to screen while menu attribute is true
    def display_menu(self):

        while self.menu:
            # fill screen with background colour
            screen.fill(SEA_BLUE)

            # draw map to screen (a little more calm than usual ocean background)
            screen.blit(map.calm_ocean, [0, 0])

            # handle player input to move sword sprite for selection
            self.menu_input()

            # draw menu icons to screen
            screen.blit(self.logo, [175, 50])
            screen.blit(self.start, [200, 200])
            screen.blit(self.quit, [200, 350])
            screen.blit(self.sword, [125, self.sword_rect.y])

            # draw basic text to screen
            output_text = font.render("Use UP, DOWN and SPACE to make your choice.", True, BLACK)
            screen.blit(output_text, [170, 450])

            # update screen and framerate
            screen_update()

    # method to take player inputs and move the sword position accordingly
    def menu_input(self):
        # access global variables
        global done

        for event in pygame.event.get():  # get events from pygame event queue
            if event.type == pygame.QUIT:  # if player clicks close, quit game
                done = True
                self.menu = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # if the user presses escape, quit game
                    done = True
                    self.menu = False
                if event.key == pygame.K_UP:
                    self.sword_position = (self.sword_position - 1) % self.menu_icons
                if event.key == pygame.K_DOWN:
                    self.sword_position = (self.sword_position + 1) % self.menu_icons
                if event.key == pygame.K_SPACE:
                    if self.sword_position == 0:  # if player selects start game, start the game
                        self.start_game()
                    elif self.sword_position == 1:  # if player selects end game, quit the window
                        done = True
                        self.menu = False

        # code for drawing sword selection icon to correct position
        if self.sword_position == 0:
            self.sword_rect.y = 212
        elif self.sword_position == 1:
            self.sword_rect.y = 362

    # method for starting the game from the menu screen
    def start_game(self):
        self.menu = False
        centre_island_obj.overview = True  # make sure player spawns on central island
        set_treasure_chests()  # call procedure to set random treasure chests


# miscellaneous values
# create list of all game treasure names
treasures_list = ["The Sword of Blackbeard", "The Goblet of Avery", "The Sigil of Tew", "Barbarossa's Beard",
                  "Sparrow's coin", "The Cutlass of Morgan", "Kidd's Pistol"]
chests = pygame.sprite.Group()  # group for all chests in game
menu_obj = Menu()
island_obj = Island(300, 300, 0, 0, "sand")  # create first island object
island2_obj = Island(300, 300, 0, 0, "grass")  # create second island object
island3_obj = Island(300, 300, 0, 0, "rock")  # create third island object
island4_obj = Island(300, 300, 0, 0, "sand")  # create fourth island object
centre_island_obj = Island(400, 400, ((WIDTH / 2) - 50), ((HEIGHT / 2) - 50), "centre")
islands = pygame.sprite.Group()  # initialise list of islands
islands.add(island_obj, island2_obj, island3_obj, island4_obj)  # add island objects to list of islands
enemies = pygame.sprite.Group()  # create list of all enemies
enemies_hit = pygame.sprite.Group()  # create list of enemies hit by sword
swords = pygame.sprite.Group()  # create list of swords
bullets = pygame.sprite.Group()  # create list of bullets
font = pygame.font.SysFont('Freestyle Script', 24, False, False)  # font for use in messages, with size, bold, italic
paused = False  # boolean for if the game is paused
enemy_move_timer = 0  # timer for when enemy can calculate movement
curr_enemy_list = enemies  # current list for enemy collision
treasure_message_display = False  # boolean for if treasure chest message should be displayed
game_end = False  # boolean to check if game is done or not
doors = pygame.sprite.Group()  # create dungeon door sprite group
centre_pot_obj = BreakObject((WIDTH / 2) - 20, centre_island_obj.position_y_close + 45)
centre_island_obj.breakables.add(centre_pot_obj)
# create objects for tutorial messages and list of them
centre_sword_tutorial = TutorialRect(60, 60, (WIDTH / 2 - 30),
                                     centre_island_obj.position_y_close + 10 + centre_pot_obj.size, "Press SPACE.")
movement_tutorial = TutorialRect(30, 30, centre_island_obj.position_x_close + (centre_island_obj.width / 2) - 15,
                                 centre_island_obj.position_y_close + (centre_island_obj.height * 0.8),
                                 "Use WASD or arrow keys to move.")
pause_tutorial = TutorialRect(centre_island_obj.width, 60, centre_island_obj.position_x_close,
                              (centre_island_obj.position_y_close + centre_island_obj.height - 60), "Press P to pause.")
tutorials = pygame.sprite.Group()
tutorials.add(centre_sword_tutorial, movement_tutorial, pause_tutorial)
# create lists for enemy path-finding
available_spaces = []
unavailable_spaces = []
visited = []

# create list of all game locations
locations = pygame.sprite.Group()
locations.add(island_obj, island2_obj, island3_obj, island4_obj)
locations.add(centre_island_obj)
locations.add(dungeon_entrance_obj)
locations.add(dungeon_second_room_obj)

# procedure to spawn islands on map
def island_spawn():
    # generate list of island positions for use
    x_position_list = [25, 75, 100, 125, 150, 175, 200, 250, 275, 300, 350, 425, 450, 475, 500, 550, 525, 575]
    y_position_list = [25, 75, 100, 150, 175, 200, 225, 250, 275, 325]
    # assign island positions to each island, except for centre_island
    for island in islands:
        islands.remove(island)  # remove current island from island list
        while not island.island_location:
            # generate random positions
            index_x = random.choice(x_position_list)
            index_y = random.choice(y_position_list)
            island.rect.x = index_x
            island.rect.y = index_y
            # if there are no collisions ith other islands
            if not (pygame.sprite.spritecollideany(island, islands, pygame.sprite.collide_circle) or
                        pygame.sprite.collide_circle(island, centre_island_obj)):
                island.island_location = True
                islands.add(island)  # put island back in sprite group
                # remove x and y positions from list
                x_position_list.remove(index_x)
                y_position_list.remove(index_y)

    islands.add(centre_island_obj)  # add centre_island to list of islands


# procedure to spawn enemies on location (island, dungeon room, etc)
def island_moving_enemy_spawn(location, location_list, enemy_num, type):
    # for loop determining enemy spawn
    for index in range(enemy_num):
        enemy_obj = Ghost(0, 0)
        enemies.add(enemy_obj)
        location_list.add(enemy_obj)

    # random spawn location code
    for enemy in location_list:
        location_list.remove(enemy)  # remove enemy from sprite group
        while not enemy.found_location:
            # generate random enemy positions
            enemy.rect.x = random.randrange(location.position_x_close + 1,
                                            location.position_x_close + location.width - 21)
            enemy.rect.y = random.randrange(location.position_y_close + 1,
                                            location.position_y_close + location.height - 61)
            enemy_pos = location.graph.find_grid_position(enemy, location)
            location.place_in_graph(enemy, enemy_pos)
            # if no collision with other enemies, then the position is valid
            if not pygame.sprite.spritecollideany(enemy, location_list, pygame.sprite.collide_circle):
                enemy.found_location = True
                location_list.add(enemy)
                enemies.add(enemy)  # add enemy back into sprite group
                enemy.type = type


# procedure to spawn gun enemies on island
def island_gun_enemy_spawn(location, location_list, enemy_num):
    # access global variables
    global enemies
    # for loop determining enemy spawn
    for index in range(enemy_num):
        enemy_obj = Pirate(0, 0)
        location_list.add(enemy_obj)
        enemies.add(enemy_obj)
    # random spawn location code
    for enemy in location_list:
        location_list.remove(enemy)
        while not enemy.found_location:
            enemy.rect.x = random.randrange(location.position_x_close + 1,
                                            location.position_x_close + location.width - 21)
            enemy.rect.y = random.randrange(location.position_y_close + 1,
                                            location.position_y_close + location.height - 61)
            enemy_pos = location.graph.find_grid_position(enemy, location)
            location.place_in_graph(enemy, enemy_pos)
            if not pygame.sprite.spritecollideany(enemy, location_list, pygame.sprite.collide_circle):
                enemy.found_location = True
                location_list.add(enemy)
                enemies.add(enemy)


# procedure to spawn enemies in dungeon
def dungeon_enemy_spawn(location, location_list, moving_enemy_num, gun_enemy_num):
    # make variables global
    global enemies
    # for loop to determine moving enemy spawn
    for index in range(moving_enemy_num):
        enemy_obj = Ghost(0, 0)
        enemies.add(enemy_obj)
        location_list.add(enemy_obj)
    # for loop to determine gun enemy spawn
    for index in range(gun_enemy_num):
        enemy_obj = Pirate(0, 0)
        location_list.add(enemy_obj)
        enemies.add(enemy_obj)
    # random spawn location code
    for enemy in location_list:
        location_list.remove(enemy)
        while not enemy.found_location:
            enemy.rect.x = random.randrange(location.rect.x + 1, location.rect.x + location.width - 21)
            enemy.rect.y = random.randrange(location.rect.x + 1, location.rect.y + location.height - 61)
            enemy_pos = location.graph.find_grid_position(enemy, location)
            location.place_in_graph(enemy, enemy_pos)
            if not pygame.sprite.spritecollideany(enemy, location_list, pygame.sprite.collide_circle):
                enemy.found_location = True
                location_list.add(enemy)
                enemies.add(enemy)


# procedure to display end game screen
def end_game(screen):
    # make variables global
    global game_end
    # draw things to screen
    screen.fill(BLACK)
    while game_end:
        end_game_interaction()
        player_obj.message("Well done! You have finished the game. Press ESC to quit.")
        screen_update()


# procedure to set treasures in all chests
def set_treasure_chests():
    # for chest in chests:
    for island in islands:
        island.chest.set_treasure(random.choice(treasures_list))
        treasures_list.remove(island.chest.treasure)


# procedure to keep timers ticking over while paused
def timer_continue():
    # if sword object is drawn to screen, keep timer going
    if sword_obj.will_draw:
        sword_obj.delay += (pygame.time.get_ticks() - player_obj.pause_timer)
    # keep player invulnerable timer going
    player_obj.invulnerable_timer += (pygame.time.get_ticks() - player_obj.pause_timer)
    # keep enemy timers going
    for enemy in enemies:
        enemy.invulnerable_timer += (pygame.time.get_ticks() - player_obj.pause_timer)
    # keep island timers going if treasure message is being displayed
    for island in islands:
        if island.chest.treasure_message_display:
            island.chest.treasure_message_timer += (pygame.time.get_ticks() - player_obj.pause_timer)
    # record pause timers to keep timers ticking
    player_obj.pause_timer = pygame.time.get_ticks()


# procedure to update screen and framerate
def screen_update():
    # update screen and framerate
    pygame.display.flip()
    clock.tick(60)


# procedure to draw sword to screen
def draw_sword(location_list):
    # code to determine if sword is drawn to screen
    if sword_obj.will_draw:
        if player_obj.change_x == 0 and player_obj.change_y == 0 and player_obj.health > 0:
            sword_obj.draw(screen)
            sword_obj.attack_collision(location_list)
        else:
            sword_obj.will_draw = False
        if pygame.time.get_ticks() - sword_obj.delay >= 700:
            sword_obj.will_draw = False


# procedure to determine bullet movement
def draw_bullet():
    # access global variables
    global screen
    # iterate through list of bullets, and either draw and move, or remove from list
    for bullet_shot in bullets:
        if ((bullet_shot.rect.x < WIDTH and bullet_shot.rect.x > 0 - bullet_shot.size) and
                (bullet_shot.rect.y < HEIGHT and bullet_shot.rect.y > 0 - bullet_shot.size) and player_obj.health > 0):
            bullet_shot.move()
            bullet_shot.draw(screen)
        else:
            bullet_shot.kill()  # remove bullet from game logic


# procedure to determine whether enemies are dead or not, and if not make invulnerable
def enemy_health_check():
    for enemy in enemies_hit:  # all enemies hit by sword
        if enemy.health <= 0:
            enemy.kill()  # remove from game logic if enemy has no health left
        if pygame.time.get_ticks() - enemy.invulnerable_timer >= 500:
            enemy.invulnerable = False
            enemies_hit.remove(enemy)


# procedure to determine whether enemies attack
def enemy_draw_move(location, location_list, location_rect):
    for enemy in location_list:  # all enemies in that location
        enemy.draw(screen)  # draw to screen
        if player_obj.health > 0 and not enemy.move:
            enemy.attack()  # attack player for Ghost
        elif player_obj.health > 0 and enemy.move:
            enemy.move_attack(location_rect)  # attack player for Pirate


# procedure to determine the movement and actions of the enemies
def determine_enemy_behaviour(location_list):
    behaviour_list = ["default", "charge", "follow"]
    for enemy in location_list:
        if enemy.move:  # set enemy behaviour for Ghost
            behaviour = random.choice(behaviour_list)
            behaviour_list.remove(behaviour)
            enemy.type = behaviour


# procedure to determine if player should be moving or if they are dead
def player_draw_or_die():
    # display player movements to screen
    if player_obj.health > 0:
        player_obj.health_invulnerable_flicker(screen)
        player_obj.draw_player_health(screen)
        player_obj.draw(screen)
    else:
        # display death message upon failure
        player_obj.message("You died! Press ESC to quit.")


# procedure to determine what happens when player lands on island
def land_on_island(curr_island):
    # set player position
    player_obj.rect.y = curr_island.position_y_close + (curr_island.height * 0.8)
    player_obj.rect.x = curr_island.position_x_close + (curr_island.width / 2) - (player_obj.width / 2)
    player_obj.halt_speed()
    player_obj.invulnerable_timer = pygame.time.get_ticks()  # make player invincible
    player_obj.on_island = False


# procedure to make sure player is invincible upon entering location
def enemy_delay(location_enemies):
    for enemy in location_enemies:
        if not enemy.move:  # if gun enemy
            # set attack timer to random
            enemy.can_attack = False
            enemy.attack_timer = pygame.time.get_ticks() - random.randrange(1000)
        else:
            enemy.attack_timer = pygame.time.get_ticks() - 1500
    player_obj.on_island = False


# procedure for when player enters dungeon room from bottom
def enter_room_lower(curr_location, curr_door):
    # code to determine player location
    player_obj.rect.y = curr_location.rect.y + (5 * (curr_location.height / 6))
    player_obj.rect.x = curr_location.rect.x + (curr_location.width / 2) - (player_obj.size / 2)
    player_obj.halt_speed()
    player_obj.invulnerable_timer = pygame.time.get_ticks()
    curr_location.room_entry = False


# procedure to deal with attacking
def sword_attack(location_list):
    # code for attacking and bringing player to halt
    player_obj.halt_speed()
    sword_obj.will_draw = True
    sword_obj.attack()
    sword_obj.attack_collision(location_list)
    sword_obj.delay = pygame.time.get_ticks()  # amount of milliseconds before sword sprite disappears


# procedure to determine what happens when island is left
def check_leave_island(curr_island):
    # code to check if island is being left
    if player_obj.rect.y + player_obj.size >= curr_island.position_y_close + curr_island.height - player_obj.speed:
        curr_island.overview = False
        map.overview = True
        curr_island.off = True


# procedure to determine what happens if island is left
def leave_island(island):
    # set player position
    player_obj.rect.y = island.rect.y + island.height_map + 5
    player_obj.rect.x = island.rect.x + (island.width_map / 2) - (player_obj.size / 2)
    player_obj.halt_speed()
    island.off = False
    island.chest.treasure_message_display = False  # stop displaying treasure message
    bullets.empty()  # remove all bullets from group


# procedure to determine if player and chest have collided
def check_chest_collision(curr_location, curr_chest, curr_location_enemies):
    # access global variables
    global treasure_message_timer
    global treasure_message_display
    # check collision player-chest collision, output found treasure message, and add treasure to player inventory
    if pygame.sprite.collide_rect(player_obj,
                                  curr_chest) and not curr_location.chest_open and not curr_location_enemies:
        curr_chest.pick_treasure()
        curr_location.chest_open = True
        treasure_message_display = True
        treasure_message_timer = pygame.time.get_ticks()


# procedure to check if player can be hit
def check_player_invulnerable():
    # check if invulnerability timer has run out
    if pygame.time.get_ticks() - player_obj.invulnerable_timer >= 1000:
        player_obj.invulnerable = False


# procedure to check if enemies are invulnerable or not
def check_enemy_invulnerable():
    for enemy in enemies_hit:  # all enemies hit by sword
        if pygame.time.get_ticks() - enemy.invulnerable_timer >= 500:
            enemy.invulnerable = False
            enemies_hit.remove(enemy)


# procedure to check for collision between player and enemy
def check_player_enemy_collision(curr_enemy_list):
    # code to check collision between player and enemy
    take_damage = pygame.sprite.spritecollideany(player_obj, curr_enemy_list, False)
    if take_damage and not player_obj.invulnerable:
        player_obj.take_damage(1)
        player_obj.invulnerable = True
        player_obj.draw_health = False
        player_obj.health_flicker_timer = pygame.time.get_ticks()
        player_obj.invulnerable_timer = pygame.time.get_ticks()


# procedure to check for collision between bullets and sword
def check_sword_bullet_collision():
    # make variables global
    global bullets
    # code to check collision between sword and bullets
    pygame.sprite.spritecollide(sword_obj, bullets, True)

# procedure to check for collision between player and bullets
def check_player_bullet_collision():
    got_hit = pygame.sprite.spritecollideany(player_obj, bullets)
    if got_hit and not player_obj.invulnerable:
        player_obj.take_damage(1)
        player_obj.invulnerable = True
        player_obj.draw_health = False
        player_obj.health_flicker_timer = pygame.time.get_ticks()
        player_obj.invulnerable_timer = pygame.time.get_ticks()


# procedure to check for collision between player and door
def check_player_door_collision(curr_location, destination, destination_enemies_list):
    # collision code
    if pygame.sprite.collide_rect(player_obj, curr_location.door):
        curr_location.door.check_open(curr_location)
    if curr_location.door.can_open:
        curr_location.door.open_door(curr_location, destination, destination_enemies_list)


# procedure to take care of key presses while in locations like islands on dungeons
def location_movement(curr_location, location_list):
    # access global variables
    global done
    # code for key presses + movement
    for event in pygame.event.get():  # get events from Pygame event queue
        if event.type == pygame.QUIT:  # if the user clicks close, quit game
            done = True
            curr_location.overview = False
        if event.type == pygame.KEYDOWN:  # if a key is pressed, movement starts
            if event.key == pygame.K_ESCAPE:  # if the user presses escape, quit game
                done = True
                curr_location.overview = False
            # below code sets player speed, direction, image, and image_timer
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                player_obj.change_y = -player_obj.speed
                player_obj.last_y = -1
                player_obj.last_x = 0
                player_obj.curr_image = player_obj.up_image1
                player_obj.image_timer = pygame.time.get_ticks()
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                player_obj.change_y = player_obj.speed
                player_obj.last_y = 1
                player_obj.last_x = 0
                player_obj.curr_image = player_obj.down_image1
                player_obj.image_timer = pygame.time.get_ticks()
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player_obj.change_x = -player_obj.speed
                player_obj.last_y = 0
                player_obj.last_x = -1
                player_obj.curr_image = player_obj.left_image1
                player_obj.image_timer = pygame.time.get_ticks()
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player_obj.change_x = player_obj.speed
                player_obj.last_y = 0
                player_obj.last_x = 1
                player_obj.curr_image = player_obj.right_image1
                player_obj.image_timer = pygame.time.get_ticks()
            # below code pauses game when player presses p
            if event.key == pygame.K_p:
                player_obj.pause_timer = pygame.time.get_ticks()
                pause(curr_location)
            # below code lets the player attack when they press the space bar
            if event.key == pygame.K_SPACE:
                sword_attack(location_list)
        if event.type == pygame.KEYUP:  # if a key is released, movement stops
            if (event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_w or
                        event.key == pygame.K_s):
                player_obj.change_y = 0
            if (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or
                        event.key == pygame.K_d):
                player_obj.change_x = 0


# procedure for key presses while paused
def pause_interaction(curr_location):
    # access global variables
    global paused
    global done
    # code for key presses
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            paused = False
            curr_location.overview = False
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # if the user presses escape, quit game
                done = True
                curr_location.overview = False
            if event.key == pygame.K_p:
                paused = False


# procedure for key presses while on endgame screen
def end_game_interaction():
    # access global variables
    global done
    global game_end
    # code for key presses
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_end = False
            done = True
        if event.type == pygame.KEYDOWN:  # if key is pressed, movement starts
            if event.key == pygame.K_ESCAPE:  # if the user presses escape, quit game
                game_end = False
                done = True


# procedure for key presses in peaceful location
def peaceful_location_movement(curr_location):
    # access global variables
    global done
    # code for key presses + movement
    for event in pygame.event.get():  # if the user does something
        if event.type == pygame.QUIT:  # if the user clicks close, quit game
            done = True
            curr_location.overview = False
        if event.type == pygame.KEYDOWN:  # if key is pressed, movement starts
            if event.key == pygame.K_ESCAPE:  # if the user presses escape, quit game
                done = True
                curr_location.overview = False
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                player_obj.change_y = -player_obj.speed
                player_obj.last_y = -1
                player_obj.last_x = 0
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                player_obj.change_y = player_obj.speed
                player_obj.last_y = 1
                player_obj.last_x = 0
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player_obj.change_x = -player_obj.speed
                player_obj.last_y = 0
                player_obj.last_x = -1
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player_obj.change_x = player_obj.speed
                player_obj.last_y = 0
                player_obj.last_x = 1
            if event.key == pygame.K_p:
                player_obj.pause_timer = pygame.time.get_ticks()
                pause(curr_location)
        if event.type == pygame.KEYUP:  # if key is released, movement stops
            if (event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_w or
                        event.key == pygame.K_s):
                player_obj.change_y = 0
            if (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or
                        event.key == pygame.K_d):
                player_obj.change_x = 0


# procedure for key presses while on map
def map_movement():
    # access global variables
    global done
    # code for key presses and movement
    for event in pygame.event.get():  # if the user does something
        if event.type == pygame.QUIT:  # if the user clicks close or presses escape
            done = True
            map.overview = False
        if event.type == pygame.KEYDOWN:  # if key is pressed, movement starts
            if event.key == pygame.K_ESCAPE:  # if the user presses escape, quit game
                done = True
                map.overview = False
            # if pressing key, change player speed and ship sprite
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                player_obj.change_y = -(player_obj.speed - 1)
                player_obj.last_y = -1
                player_obj.last_x = 0
                player_obj.curr_image = player_obj.ship_up_spr
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                player_obj.change_y = (player_obj.speed - 1)
                player_obj.last_y = 1
                player_obj.last_x = 0
                player_obj.curr_image = player_obj.ship_down_spr
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player_obj.change_x = -(player_obj.speed - 1)
                player_obj.last_y = 0
                player_obj.last_x = -1
                player_obj.curr_image = player_obj.ship_left_spr
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player_obj.change_x = (player_obj.speed - 1)
                player_obj.last_y = 0
                player_obj.last_x = 1
                player_obj.curr_image = player_obj.ship_right_spr
            if event.key == pygame.K_p:
                player_obj.pause_timer = pygame.time.get_ticks()
                pause(map)
        if event.type == pygame.KEYUP:  # if key is released, movement stops
            if (event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_w or
                        event.key == pygame.K_s):
                player_obj.change_y = 0
            if (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or
                        event.key == pygame.K_d):
                player_obj.change_x = 0


# create chest objects and add them to chests list
end_chest = TreasureChest(40, (WIDTH / 2) - 20, (HEIGHT / 2) - 20, "Ultimate pirate treasure")
chests.add(end_chest)

# assign island spawn locations
island_spawn()

# create all default enemies for tutorial island 1
island_moving_enemy_spawn(island_obj, island_obj.enemies, 2, "default")

# create all enemy objects for use on island 2
island_gun_enemy_spawn(island2_obj, island2_obj.enemies, 2)

# create all charge enemies for tutorial island 3
island_moving_enemy_spawn(island3_obj, island3_obj.enemies, 1, "charge")

# create all follow enemies for tutorial island 4
island_moving_enemy_spawn(island4_obj, island4_obj.enemies, 1, "follow")

# create all enemy objects for use in dungeon entrance
dungeon_enemy_spawn(dungeon_entrance_obj, dungeon_entrance_obj.enemies, 2, 2)

# create all enemy objects for use in dungeon second room
dungeon_enemy_spawn(dungeon_second_room_obj, dungeon_second_room_obj.enemies, 2, 4)

# determine all enemy types in dungeons
for dungeon in dungeons:
    determine_enemy_behaviour(dungeon.enemies)

# main program loop setup
done = False
clock = pygame.time.Clock()


# create pause procedure, to be in effect while pausing
def pause(curr_location):
    # access global variables
    global paused

    # check that game will be paused
    paused = True

    # ensure that player speed does not carry over to after pause
    player_obj.halt_speed()

    # convert inventory text string to Surface
    inventory_text = font.render("Player inventory:", True, WHITE)

    # pause loop
    while paused:
        # code for key presses
        pause_interaction(curr_location)

        # code to make black screen with overlay message
        screen.fill(BLACK)
        text = font.render("Game paused. Press P to continue.", True, WHITE)
        screen.blit(text, [20, 10])

        # display player inventory to the screen
        screen.blit(inventory_text, [WIDTH // 2, HEIGHT // 5])
        if player_obj.inventory:
            for index in range(len(player_obj.inventory)):
                item_text = font.render(player_obj.inventory[index], True, WHITE)
                screen.blit(item_text, [(WIDTH // 2) + 20, (HEIGHT // 5) + ((index + 1) * 30)])
        else:
            empty_text = font.render("Empty - no treasures found.", True, WHITE)
            screen.blit(empty_text, [(WIDTH // 2) + 20, (HEIGHT // 5) + 30])

        # call timer continue function
        timer_continue()

        # remove pause tutorial message
        if not pause_tutorial.shown:
            pause_tutorial.end_tutorial()

        # update screen
        screen_update()


# main program loop
while not done:
    # if in an area, activate its' procedure for overview
    if menu_obj.menu:
        menu_obj.display_menu()

    if map.overview:
        map.world_map()

    for location in locations:
        if location.overview:
            location.location_loop()

    # display end game screen if game is ended
    if game_end:
        end_game(screen)

# closes window, exits game
pygame.quit()
