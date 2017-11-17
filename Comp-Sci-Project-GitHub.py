# import modules
import pygame
import random
import math
# import pi from math
import grid_class
import queue

# defining a few colours, using their RGB value
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BROWN = (102, 51, 0)
SEA_BLUE = (0, 191, 255)  # colour for sea
GRASS_GREEN = (0, 204, 0)  # colour for green grassy islands
SAND = (204, 204, 0)  # colour for beach islands
ROCK = (128, 128, 128)  # colour for rock islands
MOVING_ENEMY_PURPLE = (255, 51, 255)  # stand-in colour for moving enemies
GUN_ENEMY_BLUE = (0, 0, 255)  # stand-in colour for projectile enemies
island_material = (GRASS_GREEN, SAND, ROCK)  # tuple for the island material

# initialise PI, for some ellipses and arcs
# PI = pi

# initialise window height and width
WIDTH = 700
HEIGHT = 500

# initialising the engine
pygame.init()

# setting the borderless window
size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pirate Game")  # sets the window title


# initialise player class, using rectangle for now
class Player(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y, player_size):
        super().__init__()
        self.change_x = 0  # player speed left and right, starts at 0
        self.change_y = 0  # player speed up and down, starts at 0
        self.speed = 4  # player speed variable
        self.size = player_size  # player rectangle size
        self.colour = RED  # set player colour
        self.image = pygame.Surface([self.size, self.size])
        self.image.fill(self.colour)
        self.rect = self.image.get_rect()
        self.health_image = pygame.image.load("Health.png").convert()
        self.health_image.set_colorkey(WHITE)
        self.health_rect = self.image.get_rect()
        self.rect.x = start_x  # player x position
        self.rect.y = start_y  # player y position
        self.enemies_killed = 0
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

    def move_map(self):
        self.rect.x += self.change_x
        self.rect.y += self.change_y

    def move_close(self, location_rect):
        self.rect.clamp_ip(location_rect)  # keep player on island
        self.rect.x += self.change_x
        self.rect.y += self.change_y

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, self.rect)

    def take_damage(self, damage_source):
        self.health -= damage_source.damage  # take away enemy damage from player health

    def message(self, text):
        output_text = font.render(text, True, BLACK)
        # pygame.draw.rect(screen, BLACK, [0, 0, WIDTH - 50, 50])
        screen.blit(self.banner, [0, 0])
        screen.blit(output_text, [20, 10])

    def halt_speed(self):
        player_obj.change_y = 0
        player_obj.change_x = 0

    def draw_player_health(self, screen):
        if self.draw_health:
            for hp in range(self.health):
                screen.blit(self.health_image, [WIDTH - 40, (20 + hp * 35)])

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
player_obj = Player(350, 250, 15)


# initialise island class
class Island(pygame.sprite.Sprite):
    def __init__(self, height, width, position_x, position_y):
        super().__init__()
        self.height = height
        self.width = width
        self.width_map = width / 4
        self.height_map = height / 4
        self.position_x_close = (WIDTH / 2) - (self.width / 2)
        self.position_y_close = (HEIGHT / 2) - (self.height / 2)
        self.colour = random.choice(island_material)
        self.image = pygame.image.load("SandIslandClose.png").convert()
        self.image.set_colorkey(WHITE)
        self.image_map = pygame.image.load("SandIslandMap.png").convert()
        self.image_map.set_colorkey(WHITE)
        # self.rect = [position_x, position_y, self.height_map, self.width_map]
        # self.image = pygame.Surface([self.width_map, self.height_map])
        # self.image.fill(self.colour)
        self.rect = self.image_map.get_rect()
        self.rect.x = position_x
        self.rect.y = position_y
        # self.rect_close = [self.position_x_close, self.position_y_close, self.height, self.width]
        self.rect_close = self.image.get_rect()
        self.rect_close.x = self.position_x_close
        self.rect_close.y = self.position_y_close
        self.boundary_rect = [self.position_x_close + 5, self.position_y_close + 5, self.height - 10,
                              self.width - 10]  # rectangle for keeping player in island
        self.overview = False
        self.off = False  # boolean to check if player has left island
        self.chest_open = False  # boolean to check if island chest is open
        self.island_location = False  # boolean to determine if island spawn location is all good (no collisions)
        self.breakables = pygame.sprite.Group()  # create list of breakable items per location
##        # create island graph, in dictionary as list
##        self.graph = {
##            'A1': ['A2', 'B1'],
##            'A2': ['A1', 'B2', 'A3'],
##            'A3': ['A2', 'B3', 'A4'],
##            'A4': ['A3', 'B4', 'A5'],
##            'A5': ['A4', 'B5'],
##            'B1': ['A1', 'C1', 'B2'],
##            'B2': ['B1', 'A2', 'C2', 'B3'],
##            'B3': ['B2', 'A3', 'C3', 'B4'],
##            'B4': ['B3', 'A4', 'C4', 'B5'],
##            'B5': ['B4', 'A5', 'C5'],
##            'C1': ['B1', 'D1', 'C2'],
##            'C2': ['C1', 'B2', 'D2', 'C3'],
##            'C3': ['C2', 'B3', 'D3', 'C4'],
##            'C4': ['C3', 'B4', 'D4', 'C5'],
##            'C5': ['C4', 'B5', 'D5'],
##            'D1': ['C1', 'E1', 'D2'],
##            'D2': ['D1', 'C2', 'E2', 'D3'],
##            'D3': ['D2', 'C3', 'E3', 'D4'],
##            'D4': ['D3', 'C4', 'E4', 'D5'],
##            'D5': ['D4', 'C5', 'E5'],
##            'E1': ['D1', 'E2'],
##            'E2': ['E1', 'D2', 'E3'],
##            'E3': ['E2', 'D3', 'E4'],
##            'E4': ['E3', 'D4', 'E5'],
##            'E5': ['E4', 'D5']
##        }
##        # create dictionary to transform numbers into graph letters, and back again
##        self.graph_transfer = {
##            1: 'A',
##            2: 'B',
##            3: 'C',
##            4: 'D',
##            5: 'E',
##            'A': 1,
##            'B': 2,
##            'C': 3,
##            'D': 4,
##            'E': 5
##        }
##        self.graph_height = self.height / 5
##        self.graph_width = self.width / 5
        # create graph with grid_class script
        self.graph = grid_class.Grid(self.height, self.width)

    def draw_close(self, screen):  # drawing code for when player is on island
        # pygame.draw.rect(screen, self.colour, self.rect_close)
        screen.blit(self.image, [self.rect_close.x, self.rect_close.y])

    def draw_map(self, screen):
        # pygame.draw.rect(screen, self.colour, self.rect)
        screen.blit(self.image_map, [self.rect.x, self.rect.y])

    def get_graph_position(self, item):
        # method to find item position
        self.graph.find_grid_position(item, self)
##        x_position = item_x - self.rect.x
##        y_position = item_y - self.rect.y
##        graph_x = (x_position // self.graph_width) + 1
##        graph_y = (y_position // self.graph_height) + 1
##        graph_y = self.graph_transfer[graph_y]
##        return (graph_x, graph_y)

    def place_in_graph(self, item, item_pos):
        # method to place item in centre of graph
        # print(item_pos)
        self.graph.place_in_position(item_pos, item, self)
##        graph_x = item_pos[0]
##        graph_y = item_pos[1]
##        graph_x = (graph_x - 1) * self.graph_width
##        graph_y = self.graph_transfer[graph_y]
##        graph_y = (graph_y - 1) * self.graph_height
##        graph_x += (self.graph_width / 2)
##        graph_y += (self.graph_height / 2)
##        graph_x -= (item.size / 2)
##        graph_y -= (item.size / 2)
##        graph_x += self.rect.x
##        graph_y += self.rect.y
##        item.rect.x = graph_x
##        item.rect.y = graph_y

    def find_neighbours(self, position):
        # method to find all neighbouring positions
        self.graph.find_neighbours(position)


# create dungeon class, for use
class Dungeon():
    def __init__(self):
        self.overview = False  # boolean for if dungeon level is on screen
        self.height = HEIGHT - 100
        self.width = WIDTH - 100
        self.colour = ROCK  # stand-in colour for dungeon floor
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(self.colour)
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 50
        self.chest_open = False  # boolean for if chest is open
        self.breakables = pygame.sprite.Group()  # create list of breakable items per location
        # create dungeon graph, in dictionary as list
##        self.graph = {
##            'A1': ['A2', 'B1'],
##            'A2': ['A1', 'B2', 'A3'],
##            'A3': ['A2', 'B3', 'A4'],
##            'A4': ['A3', 'B4', 'A5'],
##            'A5': ['A4', 'B5'],
##            'B1': ['A1', 'C1', 'B2'],
##            'B2': ['B1', 'A2', 'C2', 'B3'],
##            'B3': ['B2', 'A3', 'C3', 'B4'],
##            'B4': ['B3', 'A4', 'C4', 'B5'],
##            'B5': ['B4', 'A5', 'C5'],
##            'C1': ['B1', 'D1', 'C2'],
##            'C2': ['C1', 'B2', 'D2', 'C3'],
##            'C3': ['C2', 'B3', 'D3', 'C4'],
##            'C4': ['C3', 'B4', 'D4', 'C5'],
##            'C5': ['C4', 'B5', 'D5'],
##            'D1': ['C1', 'E1', 'D2'],
##            'D2': ['D1', 'C2', 'E2', 'D3'],
##            'D3': ['D2', 'C3', 'E3', 'D4'],
##            'D4': ['D3', 'C4', 'E4', 'D5'],
##            'D5': ['D4', 'C5', 'E5'],
##            'E1': ['D1', 'E2'],
##            'E2': ['E1', 'D2', 'E3'],
##            'E3': ['E2', 'D3', 'E4'],
##            'E4': ['E3', 'D4', 'E5'],
##            'E5': ['E4', 'D5']
##        }
##        # create dictionary to transform numbers into graph letters, and back again
##        self.graph_transfer = {
##            1: 'A',
##            2: 'B',
##            3: 'C',
##            4: 'D',
##            5: 'E',
##            'A': 1,
##            'B': 2,
##            'C': 3,
##            'D': 4,
##            'E': 5
##        }
##        self.graph_height = self.height / 5
##        self.graph_width = self.width / 5
        # create graph with grid_class script
        self.graph = grid_class.Grid(self.height, self.width)

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, self.rect)

    def get_graph_position(self, item):
        # method to find item position
        position = self.graph.find_grid_position(item, self)
        return position
##        x_position = item_x - self.rect.x
##        y_position = item_y - self.rect.y
##        graph_x = (x_position // self.graph_width) + 1
##        graph_y = (y_position // self.graph_height) + 1
##        graph_y = self.graph_transfer[graph_y]
##        return (graph_x, graph_y)

    def place_in_graph(self, item, item_pos):
        # method to place item in centre of graph
        self.graph.place_in_position(item_pos, item, self)
##        graph_x = item_pos[0]
##        graph_y = item_pos[1]
##        graph_x = (graph_x - 1) * self.graph_width
##        graph_y = self.graph_transfer[graph_y]
##        graph_y = (graph_y - 1) * self.graph_height
##        graph_x += (self.graph_width / 2)
##        graph_y += (self.graph_height / 2)
##        graph_x -= (item.size / 2)
##        graph_y -= (item.size / 2)
##        graph_x += self.rect.x
##        graph_y += self.rect.y
##        item.rect.x = graph_x
##        item.rect.y = graph_y

    def find_neighbours(self, position):
        # method to find all neighbouring positions
        self.graph.find_neighbours(position)


# create dungeon objects
dungeon_entrance_obj = Dungeon()
dungeon_second_room_obj = Dungeon()


# create dungeon door class, for use
class DungeonDoor(pygame.sprite.Sprite):
    def __init__(self, position_x, position_y):
        super().__init__()
        self.height = 40
        self.width = 30
        self.image = pygame.image.load("Door.png").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = position_x
        self.rect.y = position_y
        self.can_open = False  # boolean to check if door can be opened

    def draw(self, screen):
        screen.blit(self.image, [self.rect.x, self.rect.y])

    def open_door(self, curr_location, destination, destination_enemies_list):
        # make variables global
        global curr_enemy_list
        global location_rect
        global room_entry

        # code for collision
        curr_location.overview = False
        destination.overview = True
        room_entry = True
        curr_enemy_list = destination_enemies_list
        location_rect = destination.rect

    def check_open(self, curr_location):
        if curr_location == centre_island_obj:
            if len(player_obj.inventory) == len(islands) - 1 and centre_pot_obj.broken:
                self.can_open = True
            else:
                if centre_pot_obj.broken:
                    player_obj.message("Leave this island, trespasser.")
        elif curr_location == dungeon_entrance_obj:
            if not enemies_dungeon_entrance:
                self.can_open = True
        else:
            self.can_open = True


# create map class, for use
class Map():
    def __init__(self):
        self.overview = False  # boolean for if map level is on screen


# create map object
map = Map()


# initialise moving enemy class, intended as parent class for future enemies
class MovingEnemy(pygame.sprite.Sprite):
    def __init__(self, size, colour, start_x, start_y):
        super().__init__()
        self.change_x = 0  # initial x speed
        self.change_y = 0  # initial y speed
        self.size = size  # set size
        self.colour = colour  # set colour, may delegate to enemy sub-class in future
        self.image = pygame.Surface([self.size, self.size])
        self.image.fill(self.colour)
        self.rect = self.image.get_rect()
        self.rect.x = start_x  # enemy x position
        self.rect.y = start_y  # enemy y position
        self.health = 2  # integer for health value, each hit does damage of 2
        # self.dead = False  # boolean for if enemy is dead or not
        self.damage = 1  # boolean for damage enemy does to player health
        self.invulnerable = False  # boolean for if enemy can take damage or not
        self.invulnerable_timer = pygame.time.get_ticks()  # sets the current time as reference for invincibility
        self.move_timer = pygame.time.get_ticks()  # sets current time as reference for attack calculation
        self.found_location = False  # boolean to check if position is correct
        self.available_spaces = []  # list for places that can be moved to
        self.unavailable_spaces = []  # list for places that cannot be moved to
        self.position = [0, 0]  # list to contain position of enemy
        self.player_position = [0, 0]  # list to contain position of player
        # self.chest_collision = False  # boolean for if enemy has collided with a chest
        # self.aggressive = True #boolean for if enemy should be attacking or not
        # self.move_rect = self.rect.copy()
        # self.rect.y + self.size)  # set rectangle for checking movement path
        self.move = True
        self.path = []

    # def check_movement(self):
    #     # code to stop enemies merging
    #     curr_enemy_list.remove(self)
    #     for enemy_sprite in curr_enemy_list:
    #         if pygame.sprite.collide_circle(self, enemy_sprite):
    #             if self.change_x == 0:
    #                 self.change_y *= -1
    #             else:
    #                 self.change_x *= -1
    #             if enemy_sprite.change_x == 0:
    #                 enemy_sprite.change_y *= -1
    #             else:
    #                 enemy_sprite.change_x *= -1
    #     curr_enemy_list.add(self)

    def move_attack(self):
        # code to attack enemy towards player aggressively
        # if pygame.time.get_ticks() - self.move_timer >= 500:
        if abs(player_obj.rect.x - self.rect.x) < abs(player_obj.rect.y - self.rect.y):
            if player_obj.rect.y > self.rect.y:
                self.change_x = 0
                self.change_y = 1.5
                # self.move_timer = pygame.time.get_ticks()
            else:
                self.change_x = 0
                self.change_y = -1.5
                # self.move_timer = pygame.time.get_ticks()
        elif abs(player_obj.rect.x - self.rect.x) > abs(player_obj.rect.y - self.rect.y):
            if player_obj.rect.x > self.rect.x:
                self.change_x = 1.5
                self.change_y = 0
                # self.move_timer = pygame.time.get_ticks()
            else:
                self.change_x = -1.5
                self.change_y = 0
                # self.move_timer = pygame.time.get_ticks()

        # apply position changes and keep enemy on island
        self.rect.clamp_ip(location_rect)
        self.rect.x += self.change_x
        self.rect.y += self.change_y

    # def find_path(self, location, location_enemies):
        # # code to implement searching algorithm
        # self.available_spaces.clear()
        # self.unavailable_spaces.clear()
        # self.position = [self.rect.x, self.rect.y]
        # self.player_position = [player_obj.rect.x, player_obj.rect.y]
        # # if enemy position and player position are equal, in the x or y plane
        # if self.position[0] == self.player_position[0]:
        #     self.change_x = 0
        #     if self.position[1] >= self.player_position[1]:
        #         self.change_y = -1.5
        #     else:
        #         self.change_y = 1.5
        # elif self.position[1] == self.player_position[1]:
        #     self.change_y = 0
        #     if self.position[0] >= self.player_position[0]:
        #         self.change_x = -1.5
        #     else:
        #         self.change_x = 1.5
        #         # code to actually find a path
        #         # else:

##        # self.available_spaces.clear()
##        self.unavailable_spaces.clear()
##        # add all enemy positions as unavailable spaces, should not be any duplicates
##        for enemy in location_enemies:
##            enemy_pos = location.get_graph_position(enemy)
##            enemy_pos = graph_tuple_to_str(enemy_pos)
##            self.unavailable_spaces.append(enemy_pos)
##        # TODO - add breakable objects to this part
##        # add player position as end goal
##        end_vertex = location.get_graph_position(player_obj, player_obj.rect.x, player_obj.rect.y)
##        end_vertex = graph_tuple_to_str(end_vertex)
##
##        # actual pathfinding algorithm (depth-first search?)
##        self.path.clear()
##        location_enemies.remove(self)
##        current_vertex = location.get_graph_position(self, self.rect.x, self.rect.y)
##        current_vertex = graph_tuple_to_str(current_vertex)
##        self.path.append(current_vertex)
##        print(current_vertex)
##        print(end_vertex)
##
##        # while not at player vertex, with upper limit
##        while current_vertex != end_vertex:
##            print(location.graph[current_vertex])
##            vertex = location.graph[current_vertex].pop()
##            print(vertex)
##            if (vertex not in self.path) and (vertex not in self.unavailable_spaces):
##                self.path.append(vertex)
##                # self.available_spaces.remove(vertex)
##                self.unavailable_spaces.append(vertex)
##            # for next_vertex in location.graph[vertex]:
##            #     if next_vertex not in self.unavailable_spaces:
##            #         self.available_spaces.append(next_vertex)
##                current_vertex = vertex
##            else:
##                current_vertex = location.graph[current_vertex].pop()
##        location_enemies.add(self)
##        print(self.path)
##        print(unavailable_spaces)
##        return self.path

    def attack(self):
        self.rect.clamp_ip(location_rect)  # keep enemy on island

        # #code to check how close player is to enemy
        # if abs(player_obj.rect.x - self.rect.x) <= 50 or abs(player_obj.rect.y - self.rect.y) <= 50:
        #      self.aggressive = True
        # else:
        #      self.aggressive = False

        # attack movement
        # self.move_attack()

        # check movement
        # self.check_movement()

        # apply position changes
        # self.rect.x += self.change_x
        # self.rect.y += self.change_y

        # attack player

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, self.rect)


# class for stationary, shooting enemies
class GunEnemy(pygame.sprite.Sprite):
    def __init__(self, size, colour, start_x, start_y):
        super().__init__()
        self.size = size
        self.colour = colour
        self.image = pygame.Surface([self.size, self.size])
        self.image.fill(self.colour)
        self.rect = self.image.get_rect()
        self.rect.x = start_x  # enemy x position
        self.rect.y = start_y  # enemy y position
        self.health = 2  # integer for health value, each hit does damage of 2
        # self.dead = False  # boolean for if enemy is dead or not
        self.invulnerable = False  # boolean for if enemy can be hit
        self.invulnerable_timer = pygame.time.get_ticks()  # sets the current time as reference for invincibility
        self.attack_timer = pygame.time.get_ticks()  # sets the current time as reference for attacking
        self.can_attack = False  # boolean for if the enemy can attack
        self.damage = 0  # integer for how much damage dealt to player health
        self.found_location = False  # boolean to check if position is correct
        self.move = False

    def attack(self):
        # make variables global
        global screen
        global bullets
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
            bullet = Bullet(15, BLACK, self.rect.x, self.rect.y, bullet_x_speed, bullet_y_speed)
            bullets.add(bullet)
            bullet.move()
            bullet.draw(screen)
            self.can_attack = False
            self.attack_timer = pygame.time.get_ticks()

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, self.rect)


# initialise bullet class, for enemy attacks
class Bullet(pygame.sprite.Sprite):
    def __init__(self, size, colour, start_x, start_y, x_speed, y_speed):
        super().__init__()
        self.size = size
        self.colour = colour
        self.image = pygame.image.load("Bullet.png").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = start_x
        self.rect.y = start_y
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.damage = 1  # integer for damage dealt to player health
        self.deflected = False  # boolean for if it has been deflected by player sword

    def draw(self, screen):
        screen.blit(self.image, [self.rect.x, self.rect.y])

    def move(self):
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed


# create class of breakable objects
class BreakObject(pygame.sprite.Sprite):
    def __init__(self, size, x_position, y_position):
        super().__init__()
        self.size = size
        self.colour = BROWN
        self.image = pygame.Surface([self.size, self.size])
        self.image.fill(self.colour)
        self.rect = self.image.get_rect()
        self.rect.x = x_position
        self.rect.y = y_position
        self.broken = False

    def draw(self, screen):
        if not self.broken:
            pygame.draw.rect(screen, self.colour, self.rect)


# initialise sword class, for attacking
class Sword(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 15
        self.height = 15
        # load pygame image sprite
        self.image = pygame.image.load("Sword.png").convert()
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

    def draw(self, screen):
        screen.blit(self.curr_image, [self.rect.x, self.rect.y])

    def attack(self):
        # code to put rectangle x value at area where character is facing
        if player_obj.last_x > 0:
            self.curr_image = self.image_right
            self.rect = self.image.get_rect()
            self.rect.x = player_obj.rect.x + player_obj.size
        elif player_obj.last_x < 0:
            self.curr_image = self.image_left
            self.rect = self.image.get_rect()
            self.rect.x = player_obj.rect.x - self.height

        # code to put rectangle y value at area where character is facing
        if player_obj.last_y > 0:
            self.curr_image = self.image_down
            self.rect = self.image.get_rect()
            self.rect.y = player_obj.rect.y + player_obj.size
        elif player_obj.last_y < 0:
            self.curr_image = self.image_up
            self.rect = self.image.get_rect()
            self.rect.y = player_obj.rect.y - self.height

        # code to set sword position if character facing opposite plane
        if player_obj.last_x == 0:
            self.rect.x = player_obj.rect.x + (player_obj.size / 2) - (self.width / 2)
        if player_obj.last_y == 0:
            self.rect.y = player_obj.rect.y + (player_obj.size / 2) - (self.width / 2)

    def attack_collision(self, enemy_list):
        # make variables global
        global enemies_island
        global enemies_island2
        global enemies_dungeon_second_room
        global enemies_dungeon_entrance
        # create list of enemies hit by player sword
        enemies_hit_list = pygame.sprite.spritecollide(self, enemy_list, False)
        for enemy in enemies_hit_list:
            if not enemy.invulnerable:
                enemy.health -= 2
                enemy.invulnerable = True
                enemies_hit.add(enemy)

    def check_break(self, location, location_breakables):
        # create list of objects broken by player sword
        broken_obj_list = pygame.sprite.spritecollide(self, location_breakables, False)
        for break_obj in broken_obj_list:
            if location.overview:
                break_obj.broken = True


# create sword object, for use during the game
sword_obj = Sword()


# initialise treasure chest class
class TreasureChest(pygame.sprite.Sprite):
    def __init__(self, size, position_x, position_y, treasure):
        super().__init__()
        self.size = size
        self.image = pygame.image.load("Chest.png").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.open_image = pygame.image.load("ChestOpen.png").convert()
        self.open_image.set_colorkey(WHITE)
        self.rect.x = position_x
        self.rect.y = position_y
        self.treasure = treasure
        self.text = "You found the " + self.treasure + "!"
        self.game_end = False  # boolean for if game is ended

    def pick_treasure(self):
        self.image = self.open_image
        player_obj.message(self.text)
        player_obj.inventory.append(self.treasure)

    def draw(self, screen):
        screen.blit(self.image, [self.rect.x, self.rect.y])

    def check_end_game(self, curr_location):
        # make variables global
        global game_end
        # code to check if game is finished
        if pygame.sprite.collide_rect(player_obj, self):
            game_end = True
            curr_location.overview = False


# create class for tutorial rectangles
class TutorialRect(pygame.sprite.Sprite):
    def __init__(self, width, height, x_position, y_position, message):
        super().__init__()
        self.width = width
        self.height = height
        self.colour = BLACK
        self.image = pygame.Surface([self.width, self.height])
        self.rect = self.image.get_rect()
        self.rect.x = x_position
        self.rect.y = y_position
        self.message = message
        self.shown = False

    def show_tutorial(self, location):
        if self.rect.colliderect(player_obj) and location.overview and not self.shown:
            player_obj.message(self.message)

    def end_tutorial(self):
        self.shown = True


# miscellaneous values
map.overview = True  # boolean for when player is in map
on_island = False  # boolean for when player gets onto island
island_obj = Island(300, 300, 0, 0)  # create first island object
island2_obj = Island(300, 300, 0, 0)  # create second island object
centre_island_obj = Island(400, 400, ((WIDTH / 2) - 50), ((HEIGHT / 2) - 50))
islands = pygame.sprite.Group()  # initialise list of islands
islands.add(island_obj)  # add first island object to list of islands
islands.add(island2_obj)  # add second island object to list of islands
enemies = pygame.sprite.Group()  # create list of all enemies
enemies_island2 = pygame.sprite.Group()  # create list of enemies for island 2
enemies_island = pygame.sprite.Group()  # create list of enemies for island 1
enemies_dungeon = pygame.sprite.Group()  # create list of enemies for dungeon
enemies_centre_island = pygame.sprite.Group()  # create list of enemies for centre island
enemies_hit = pygame.sprite.Group()  # create list of enemies hit by sword
# centre_island_breakables = pygame.sprite.Group()  # create list of breakable items
sword_draw = False  # boolean for if sword should be drawn
swords = pygame.sprite.Group()  # create list of swords
bullets = pygame.sprite.Group()  # create list of bullets
bullets_deflected = pygame.sprite.Group()
font = pygame.font.SysFont('Freestyle Script', 24, False, False)  # font for use in messages, with size, bold, italic
paused = False  # boolean for if the game is paused
enemy_move_timer = 0  # timer for when enemy can calculate movement
chests = pygame.sprite.Group()  # group for all chests in game
enemies_dungeon_entrance = pygame.sprite.Group()
enemies_dungeon_second_room = pygame.sprite.Group()
curr_enemy_list = enemies  # current list for enemy collision
treasure_message_display = False  # boolean for if treasure chest message should be displayed
centre_island_obj.overview = True  # make sure player spawns on central island
game_end = False  # boolean to check if game is done or not
# create dungeon door objects and list
central_island_door = DungeonDoor((WIDTH / 2) - 15,
                                  centre_island_obj.position_y_close + 40)
dungeon_entrance_door = DungeonDoor(dungeon_entrance_obj.rect.x + ((dungeon_entrance_obj.width / 2) - 15),
                                    dungeon_entrance_obj.rect.y + 40)
doors = pygame.sprite.Group()
doors.add(central_island_door, dungeon_entrance_door)
# create breakable object objects
centre_pot_obj = BreakObject(40, (WIDTH / 2) - 20, centre_island_obj.position_y_close + 40)
centre_island_obj.breakables.add(centre_pot_obj)
# create objects for tutorial messages and list of them
centre_sword_tutorial = TutorialRect(30, 30, (WIDTH / 2 - 15),
                                     centre_island_obj.position_y_close + 40 + centre_pot_obj.size, "Press SPACE.")
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
# locations = pygame.sprite.Group()
# locations.add(island_obj)
# locations.add(island2_obj)
# locations.add(centre_island_obj)
# locations.add(dungeon_entrance_obj)
# locations.add(dungeon_second_room_obj)
# locations.add(map)

# function to spawn islands on map
def island_spawn():
    # generate list of island positions for use
    x_position_list = [25, 75, 100, 125, 150, 175, 200, 250, 275, 300, 325, 350, 375, 425, 450, 475, 500, 550, 525, 575]
    y_position_list = [25, 75, 100, 150, 175, 200, 225, 250, 275, 325, 375]
    # assign island positions to each island, except for centre_island
    for island in islands:
        islands.remove(island)
        while not island.island_location:
            index_x = random.choice(x_position_list)
            index_y = random.choice(y_position_list)
            island.rect.x = index_x
            island.rect.y = index_y
            if not (pygame.sprite.spritecollideany(island, islands, pygame.sprite.collide_circle) or
                        pygame.sprite.collide_circle(island, centre_island_obj)):
                island.island_location = True
                islands.add(island)
                x_position_list.remove(index_x)
                y_position_list.remove(index_y)
    islands.add(centre_island_obj)  # add centre_island to list of islands


# function to spawn enemies on location (island, dungeon room, etc)
def island_moving_enemy_spawn(location, location_list, enemy_num):
    # make variables global
    global enemies_island
    global enemies_island2
    global enemies
    # for loop determining enemy spawn
    for index in range(enemy_num):
        enemy_obj = MovingEnemy(20, MOVING_ENEMY_PURPLE, 0, 0)
        enemies.add(enemy_obj)
        location_list.add(enemy_obj)
    # random spawn location code
    for enemy in location_list:
        location_list.remove(enemy)
        while not enemy.found_location:
            enemy.rect.x = random.randrange(location.position_x_close + 1, location.position_x_close + location.width - 21)
            enemy.rect.y = random.randrange(location.position_y_close + 1, location.position_y_close + location.height - 61)
            enemy_pos = location.graph.find_grid_position(enemy, location)
            # print(enemy_pos)
            # location.place_in_graph(enemy, location.get_graph_position(enemy))
            location.place_in_graph(enemy, enemy_pos)
            # enemy.rect.x = enemy_x
            # enemy.rect.y = enemy_y
            if not pygame.sprite.spritecollideany(enemy, location_list, pygame.sprite.collide_circle):
                enemy.found_location = True
                location_list.add(enemy)
                enemies.add(enemy)


def island_gun_enemy_spawn(location, location_list, enemy_num):
    # make variables global
    global enemies_island
    global enemies_island2
    global enemies
    # for loop determining enemy spawn
    for index in range(enemy_num):
        enemy_obj = GunEnemy(20, GUN_ENEMY_BLUE, 0, 0)
        location_list.add(enemy_obj)
        enemies.add(enemy_obj)
    # random spawn location code
    for enemy in location_list:
        location_list.remove(enemy)
        while not enemy.found_location:
            enemy.rect.x = random.randrange(location.position_x_close + 1, location.position_x_close + location.width - 21)
            enemy.rect.y = random.randrange(location.position_y_close + 1, location.position_y_close + location.height - 61)
            # enemy_pos = location.get_graph_position(enemy)
            enemy_pos = location.graph.find_grid_position(enemy, location)
            location.place_in_graph(enemy, enemy_pos)
            # enemy.rect.x = enemy_x
            # enemy.rect.y = enemy_y
            if not pygame.sprite.spritecollideany(enemy, location_list, pygame.sprite.collide_circle):
                enemy.found_location = True
                location_list.add(enemy)
                enemies.add(enemy)


# function to spawn enemies in dungeon
def dungeon_enemy_spawn(location, location_list, moving_enemy_num, gun_enemy_num):
    # make variables global
    global enemies_dungeon_entrance
    global enemies
    # for loop to determine moving enemy spawn
    for index in range(moving_enemy_num):
        enemy_obj = MovingEnemy(20, MOVING_ENEMY_PURPLE, 0, 0)
        enemies.add(enemy_obj)
        location_list.add(enemy_obj)
    # for loop to determine gun enemy spawn
    for index in range(gun_enemy_num):
        enemy_obj = GunEnemy(20, GUN_ENEMY_BLUE, 0, 0)
        location_list.add(enemy_obj)
        enemies.add(enemy_obj)
    # random spawn location code
    for enemy in location_list:
        location_list.remove(enemy)
        while not enemy.found_location:
            enemy.rect.x = random.randrange(location.rect.x + 1, location.rect.x + location.width - 21)
            enemy.rect.y = random.randrange(location.rect.x + 1, location.rect.y + location.height - 61)
            # enemy_pos = location.get_graph_position(enemy)
            enemy_pos = location.graph.find_grid_position(enemy, location)
            location.place_in_graph(enemy, enemy_pos)
            # enemy.rect.x = enemy_x
            # enemy.rect.y = enemy_y
            if not pygame.sprite.spritecollideany(enemy, location_list, pygame.sprite.collide_circle):
                enemy.found_location = True
                location_list.add(enemy)
                enemies.add(enemy)


def end_game(screen):
    # make variables global
    global game_end
    # draw things to screen
    screen.fill(BLACK)
    while game_end:
        end_game_interaction()
        player_obj.message("Well done! You have finished the game. Press ESC to quit.")
        screen_update()


# function to keep timers ticking over while paused
def timer_continue():
    # make variables global
    global treasure_message_timer
    global pause_timer
    global done
    global sword_delay
    # code to keep timers ticking over
    if sword_draw:
        sword_delay += (pygame.time.get_ticks() - pause_timer)
    player_obj.invulnerable_timer += (pygame.time.get_ticks() - pause_timer)
    for enemy_obj in enemies:
        enemy_obj.invulnerable_timer += (pygame.time.get_ticks() - pause_timer)
    for island_obj in islands:
        if island_obj.chest_open:
            treasure_message_timer += (pygame.time.get_ticks() - pause_timer)
    pause_timer = pygame.time.get_ticks()


# function to update screen and framerate
def screen_update():
    # update screen and framerate
    pygame.display.flip()
    clock.tick(60)


# function to draw sword to screen
def draw_sword(location_list):
    # make variables global
    global sword_draw
    # code to determine if sword is drawn to screen
    if sword_draw:
        if player_obj.change_x == 0 and player_obj.change_y == 0 and player_obj.health > 0:
            sword_obj.draw(screen)
            sword_obj.attack_collision(location_list)
        else:
            sword_draw = False
        if pygame.time.get_ticks() - sword_delay >= 700:
            sword_draw = False


# function to determine bullet movement
def draw_bullet():
    # make variables global
    global screen
    global bullets
    # iterate through list of bullets, and either draw and move, or remove from list
    for bullet_shot in bullets:
        if ((bullet_shot.rect.x < WIDTH and bullet_shot.rect.x > 0 - bullet_shot.size) and
                (bullet_shot.rect.y < HEIGHT and bullet_shot.rect.y > 0 - bullet_shot.size) and player_obj.health > 0):
            bullet_shot.move()
            bullet_shot.draw(screen)
        else:
            bullet_shot.kill()


# function to determine whether enemies are dead or not
def enemy_health_check():
    for enemy in enemies_hit:
        if enemy.health <= 0:
            enemy.kill()


# # procedure to find paths for enemies within a location
# def enemies_find_path(location, location_enemies):
#     available_spaces.clear()
#     unavailable_spaces.clear()
#     # add all enemy positions as unavailable spaces, should not be any duplicates
#     for enemy in location_enemies:
#         enemy_pos = location.get_graph_position(enemy, enemy.rect.x, enemy.rect.y)
#         enemy_pos = graph_tuple_to_str(enemy_pos)
#         unavailable_spaces.append(enemy_pos)
#     # TODO - add breakable objects to this part
#     # add player position as end goal
#     end_vertex = location.get_graph_position(player_obj, player_obj.rect.x, player_obj.rect.y)
#     end_vertex = graph_tuple_to_str(end_vertex)
#     # actual pathfinding algorithm (depth-first search?)
#     for enemy in location_enemies:
#         if enemy.move:  # if enemy is moving enemy
#             visited.clear()
#             enemy.path.clear()
#             location_enemies.remove(enemy)
#             current_vertex = location.get_graph_position(enemy, enemy.rect.x, enemy.rect.y)
#             current_vertex = graph_tuple_to_str(current_vertex)
#             visited.append(current_vertex)
#             enemy.path.append(current_vertex)
#             print(current_vertex)
#             print(end_vertex)
#
#             # while not at player vertex, with upper limit
#             while current_vertex != end_vertex:
#                 print(location.graph[current_vertex])
#                 vertex = location.graph[current_vertex].pop()
#                 print(vertex)
#                 if (vertex not in visited) and (vertex in available_spaces):
#                     visited.append(vertex)
#                     enemy.path.append(vertex)
#                     available_spaces.remove(vertex)
#                     unavailable_spaces.append(vertex)
#                 for next_vertex in location.graph[vertex]:
#                     available_spaces.append(next_vertex)
#                 current_vertex = vertex
#             location_enemies.add(enemy)
#             print(visited)
#             print(enemy.path)
#             print(unavailable_spaces)
#             return visited



            # # reposition enemies if they are colliding with one another
            # colliding_enemies_list = pygame.sprite.spritecollide(enemy, location_enemies, False)
            # if colliding_enemies_list:
            #     for coll_enemy in colliding_enemies_list:
            #         # get the amounts with which the enemies are colliding
            #         x_overlap = abs(enemy.rect.x - coll_enemy.rect.x)
            #         y_overlap = abs(enemy.rect.y - coll_enemy.rect.y)
            #         # rectify enemy position based on how much that collision is
            #         if x_overlap > y_overlap:
            #             enemy.rect.y -= (y_overlap + 1)
            #         elif x_overlap < y_overlap:
            #             enemy.rect.x -= (x_overlap + 1)
            #         elif x_overlap == y_overlap:
            #             enemy.rect.x -= (x_overlap + 1)
            #             enemy.rect.y -= (y_overlap + 1)
            #
            # # calculate enemy position relative to player position
            # if abs(player_obj.rect.x - enemy.rect.x) < abs(player_obj.rect.y - enemy.rect.y):
            #     if player_obj.rect.y > enemy.rect.y:
            #         # reposition enemy, if not colliding with another enemy
            #         enemy.rect.y += 1.5
            #         if pygame.sprite.spritecollideany(enemy, location_enemies):
            #             enemy.rect.y -= 1.5
            #     else:
            #         enemy.rect.y -= 1.5
            #         if pygame.sprite.spritecollideany(enemy, location_enemies):
            #             enemy.rect.y += 1.5
            # elif abs(player_obj.rect.x - enemy.rect.x) > abs(player_obj.rect.y - enemy.rect.y):
            #     if player_obj.rect.x > enemy.rect.x:
            #         enemy.rect.x += 1.5
            #         if pygame.sprite.spritecollideany(enemy, location_enemies):
            #             enemy.rect.x -= 1.5
            #     else:
            #         enemy.rect.x -= 1.5
            #         if pygame.sprite.spritecollideany(enemy, location_enemies):
            #             enemy.rect.x += 1.5
            # enemy.rect.clamp_ip(location_rect)  # keep enemy on island


# procedure to find paths to player for enemies within location, returns list of squares
def find_path(location, location_enemies, location_breakables):
    # create queues for unavailable/available positions
    # unavailable_positions = []
    # visited_positions = []
    # positions_to_visit = queue.Queue()
    graph = location.graph
    # TODO - remove breakable objects from available locations
    for breakable in location_breakables:
        breakable_pos = graph.find_grid_position(breakable, location)
        graph.remove_position(breakable_pos)
    # remove enemy positions from available locations
    for enemy in location_enemies:
        enemy_pos = graph.find_grid_position(enemy, location)
        # unavailable_positions.append(enemy_pos)
        if enemy_pos in graph.position_list:
            graph.remove_position(enemy_pos)
    # add player position as end goal
    end_vertex = graph.find_grid_position(player_obj, location)
    # go through list of enemies and find path
    for enemy in location_enemies:
        # enqueue enemy positions
        enemy_pos = graph.find_grid_position(enemy, location)
        graph.add_position(enemy_pos)
        # positions_to_visit.put(enemy_pos)
        # enemy_neighbours = location.graph.find_neighbours(enemy_pos)
        # function to find optimal path
        path = a_star_search(enemy_pos, graph, end_vertex)
        print(path)
        # while not positions_to_visit.empty():
        #     current_position = positions_to_visit.get()
        #     if current_position == end_vertex:
        #         # TODO - sort code for when path is found, return something
        #         x = 10
        #     else:
        #         for next_pos in enemy_neighbours:
        #             if next_pos not in unavailable_positions:
        #                 # find best next position towards goal
        #                 x = 10


# function to conduct a* search and return list of nodes with cost
def a_star_search(start, graph, goal):
    # create front queue for node order, and lists for visited lists and cost
    # front = queue.PriorityQueue()
    front = grid_class.Priority_Queue()
    front.put(start, 0)
    visited = {}
    cost_so_far = {}
    path = []
    visited[start] = None
    cost_so_far[start] = 0
    print(start, goal)

    while not front.empty():
        current = front.get()

        # check if position is same as player position
        if current == goal:
            break

        for next in graph.define_neighbours(current):
            new_cost = cost_so_far[current] + 1

            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + find_heuristic(goal, next)
                front.put(next, priority)
                visited[next] = current

        for item in visited:
            path.append(item)
        path.append(goal)


        # return visited
        print(visited)
        return path


# function to return the heuristic between two points, using manhattan system
def find_heuristic(position_1, position_2):
    # take in two lists of [x, y] and return integer heuristic
    x_heuristic = abs(position_1[0] - position_2[0])
    y_heuristic = abs(position_1[1] - position_2[1])
    return x_heuristic + y_heuristic


# # function to transform graph position tuple into string
# def graph_tuple_to_str(item=()):
#     new_item = item[1] + str(int(item[0]))
#     return new_item


# function to determine whether enemies are removed from groups (killed) or if they attack
def enemy_draw_move(location, location_list):
    # find_path(location, location_list, location.breakables)
    for enemy in location_list:
        enemy.draw(screen)
        if player_obj.health > 0 and not enemy.move:
            enemy.attack()
        elif player_obj.health > 0 and enemy.move:
            enemy.move_attack()


def player_draw_or_die():
    # display player movements to screen
    if player_obj.health > 0:
        player_obj.health_invulnerable_flicker(screen)
        player_obj.draw_player_health(screen)
        player_obj.draw(screen)
    else:
        # display death message upon failure
        player_obj.message("You died! Press ESC to quit.")


# function to determine what happens when player lands on island
def land_on_island(curr_island):
    # make variables global
    global on_island
    # code to determine what happens
    player_obj.rect.y = curr_island.position_y_close + (curr_island.height * 0.8)
    player_obj.rect.x = curr_island.position_x_close + (curr_island.width / 2) - (player_obj.size / 2)
    player_obj.halt_speed()
    player_obj.invulnerable_timer = pygame.time.get_ticks()
    on_island = False


# procedure to make sure gun enemies do not fire as soon as you enter a location
def gun_enemy_delay(location_enemies):
    for enemy in location_enemies:
        if not enemy.move:  # if gun enemy
            # set attack timer to random
            enemy.can_attack = False
            enemy.attack_timer = pygame.time.get_ticks() - random.randrange(1000)


# function for when player enters dungeon room from bottom
def enter_room_lower(curr_location):
    # make variables global
    global room_entry
    # code to determine player location
    player_obj.rect.y = curr_location.rect.y + (5 * (curr_location.height / 6))
    player_obj.rect.x = curr_location.rect.x + (curr_location.width / 2) - (player_obj.size / 2)
    player_obj.halt_speed()
    player_obj.invulnerable_timer = pygame.time.get_ticks()
    room_entry = False


# function to deal with attacking
def sword_attack(location_list):
    # make variables global
    global sword_delay
    global sword_draw
    global enemies_island
    global enemies_island2
    # code for attacking and bringing player to halt
    player_obj.halt_speed()
    sword_draw = True
    sword_obj.attack()
    sword_obj.attack_collision(location_list)
    sword_delay = pygame.time.get_ticks()  # amount of milliseconds before sword sprite disappears


# function to determine what happens when island is left
def check_leave_island(curr_island):
    # code to check if island is being left
    if player_obj.rect.y + player_obj.size >= curr_island.position_y_close + curr_island.height - player_obj.speed:
        curr_island.overview = False
        map.overview = True
        curr_island.off = True


# function to determine what happens if island is left
def leave_island(island):
    # make variables global
    global treasure_message_display
    # code to determine player position
    player_obj.rect.y = island.rect.y + island.height_map + 5
    player_obj.rect.x = island.rect.x + (island.width_map / 2) - (player_obj.size / 2)
    player_obj.change_x = 0
    player_obj.change_y = 0
    island.off = False
    treasure_message_display = False  # stop displaying treasure message
    bullets.empty()  # remove all bullets from group


# function to determine if player and chest have collided
def check_chest_collision(curr_location, curr_chest, curr_location_enemies):
    # make variables global
    global treasure_message_timer
    global treasure_message_display
    # check collision player-chest collision, output found treasure message, and add treasure to player inventory
    if pygame.sprite.collide_rect(player_obj,
                                  curr_chest) and not curr_location.chest_open and not curr_location_enemies:
        curr_chest.pick_treasure()
        curr_location.chest_open = True
        treasure_message_display = True
        treasure_message_timer = pygame.time.get_ticks()


# function to keep treasure message on screen for set amount of time
def check_treasure_message(curr_location, curr_chest):
    # make variables global
    global treasure_message_display
    global treasure_message_timer

    # code to check if treasure message should be displayed
    if curr_location.chest_open:
        if pygame.time.get_ticks() - treasure_message_timer <= 2000 and treasure_message_display:
            player_obj.message(curr_chest.text)


# function to check if player can be hit
def check_player_invulnerable():
    # check invulnerability timer has not run out
    if pygame.time.get_ticks() - player_obj.invulnerable_timer >= 1000:
        player_obj.invulnerable = False


# function to check if enemy can be hit
def check_enemy_invulnerable():
    for enemy in enemies_hit:
        if pygame.time.get_ticks() - enemy.invulnerable_timer >= 500:
            enemy.invulnerable = False
            enemies_hit.remove(enemy)


# function to check for collision between player and enemy
def check_player_enemy_collision(curr_enemy_list):
    # make variables global
    global enemies_island
    global enemies_island2
    global enemies_dungeon_second_room
    global enemies_dungeon_entrance
    # code to check collision between player and enemy
    enemy_damage_list = pygame.sprite.spritecollide(player_obj, curr_enemy_list, False)
    for enemy in enemy_damage_list:
        if not player_obj.invulnerable and enemy.damage != 0:
            player_obj.take_damage(enemy)
            player_obj.invulnerable = True
            player_obj.draw_health = False
            player_obj.health_flicker_timer = pygame.time.get_ticks()
            player_obj.invulnerable_timer = pygame.time.get_ticks()


# function to check for collision between bullets and sword
def check_sword_bullet_collision():
    # make variables global
    global bullets
    # code to check collision between sword and bullets
    pygame.sprite.spritecollide(sword_obj, bullets, True)


# function to check for collision between player and bullets
def check_player_bullet_collision():
    # make variables global
    global bullets
    # code to check collision between player and bullets
    bullet_hit_list = pygame.sprite.spritecollide(player_obj, bullets, True)
    for bullet_hit in bullet_hit_list:
        if not player_obj.invulnerable:
            player_obj.take_damage(bullet_hit)
            player_obj.invulnerable = True
            player_obj.invulnerable_timer = pygame.time.get_ticks()


# function to check for collision between player and door
def check_player_door_collision(curr_location, destination, destination_enemies_list):
    # make variables global
    global doors
    # collision code
    door_hit_list = pygame.sprite.spritecollide(player_obj, doors, False)
    for door in door_hit_list:
        door.check_open(curr_location)
        if door.can_open:
            door.open_door(curr_location, destination, destination_enemies_list)


# function to ensure map wrap around to keep player on screen
def map_wraparound():
    # if player is in map/sailing screen and they go off the edge, make them reappear on the opposite one
    if player_obj.rect.x + player_obj.size < 0:
        player_obj.rect.x = WIDTH + player_obj.speed
    elif player_obj.rect.x > WIDTH:
        player_obj.rect.x = (0 - player_obj.size) - player_obj.speed
    if player_obj.rect.y + player_obj.size < 0:
        player_obj.rect.y = HEIGHT + player_obj.speed
    elif player_obj.rect.y > HEIGHT:
        player_obj.rect.y = (0 - player_obj.size) - player_obj.speed


# function for island collision on map
def island_collision(island, island_enemies_list):
    # make variables global
    global on_island
    global location_rect
    global curr_enemy_list

    # code for collision
    map.overview = False
    island.overview = True
    on_island = True
    location_rect = island.boundary_rect
    curr_enemy_list = island_enemies_list


# function to take care of key presses while in locations like islands on dungeons
def location_movement(curr_location, location_list):
    # make variables global
    global done
    global pause_timer
    global sword_draw
    global sword_delay
    global enemies_island
    global enemies_island2
    global enemies_dungeon_entrance
    # code for key presses + movement
    for event in pygame.event.get():  # if the user does something
        if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:  # if the user clicks close or presses escape
            done = True
            curr_location.overview = False
        if event.type == pygame.KEYDOWN:  # if key is pressed, movement starts
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
                pause_timer = pygame.time.get_ticks()
                pause(curr_location)
            if event.key == pygame.K_SPACE:
                sword_attack(location_list)
        if event.type == pygame.KEYUP:  # if key is released, movement stops
            if (event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_w or
                        event.key == pygame.K_s):
                player_obj.change_y = 0
            if (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or
                        event.key == pygame.K_d):
                player_obj.change_x = 0


# function for key presses while paused
def pause_interaction(curr_location):
    # make variables global
    global paused
    global done
    # code for key presses
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
            paused = False
            curr_location.overview = False
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = False


# function for key presses while on endgame screen
def end_game_interaction():
    # make variables global
    global done
    global game_end
    # code for key presses
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
            game_end = False
            done = True


# function for key presses in peaceful location
def peaceful_location_movement(curr_location):
    # make variables global
    global pause_timer
    global done
    # code for key presses + movement
    for event in pygame.event.get():  # if the user does something
        if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:  # if the user clicks close or presses escape
            done = True
            curr_location.overview = False
        if event.type == pygame.KEYDOWN:  # if key is pressed, movement starts
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
                pause_timer = pygame.time.get_ticks()
                pause(curr_location)
        if event.type == pygame.KEYUP:  # if key is released, movement stops
            if (event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_w or
                        event.key == pygame.K_s):
                player_obj.change_y = 0
            if (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or
                        event.key == pygame.K_d):
                player_obj.change_x = 0


# function for key presses while on map
def map_movement():
    # make variables global
    global done
    global pause_timer
    # code for key presses and movement
    for event in pygame.event.get():  # if the user does something
        if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:  # if the user clicks close or presses escape
            done = True
            map.overview = False
        if event.type == pygame.KEYDOWN:  # if key is pressed, movement starts
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
                pause_timer = pygame.time.get_ticks()
                pause(map)
        if event.type == pygame.KEYUP:  # if key is released, movement stops
            if (event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_w or
                        event.key == pygame.K_s):
                player_obj.change_y = 0
            if (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or
                        event.key == pygame.K_d):
                player_obj.change_x = 0


# create chest objects and add them to chests list
island_chest = TreasureChest(40, island_obj.position_x_close + (island_obj.width / 2) - 20,
                             island_obj.position_y_close + 40 - 20, "Goblet of Blackbeard")
chests.add(island_chest)

island_2_chest = TreasureChest(40, island2_obj.position_x_close + (island2_obj.width / 2) - 20,
                               island2_obj.position_y_close + 40 - 20, "Coin of Avery")
chests.add(island_2_chest)
end_chest = TreasureChest(40, (WIDTH / 2) - 20, (HEIGHT / 2) - 20, "Ultimate pirate treasure")
chests.add(end_chest)

# assign island spawn locations
island_spawn()

# create all enemy objects for use on island 1
island_moving_enemy_spawn(island_obj, enemies_island, 3)

# create all enemy objects for use on island 2
island_gun_enemy_spawn(island2_obj, enemies_island2, 3)

# create all enemy objects for use in dungeon entrance
dungeon_enemy_spawn(dungeon_entrance_obj, enemies_dungeon_entrance, 2, 2)

# create all enemy objects for use in dungeon second room
dungeon_enemy_spawn(dungeon_second_room_obj, enemies_dungeon_second_room, 2, 4)

# main program loop setup
done = False
clock = pygame.time.Clock()


# create pause function, to be in effect while pausing
def pause(curr_location):
    # make variables global
    global paused

    # check that game should be paused
    paused = True

    # ensure that player speed does not carry over to after pause
    player_obj.halt_speed()

    # pause loop
    while paused:
        # code for key presses
        pause_interaction(curr_location)

        # code to make black screen with overlay message
        screen.fill(BLACK)
        text = font.render("Game paused. Press P to continue.", True, WHITE)
        screen.blit(text, [20, 10])

        # call timer continue function
        timer_continue()

        # remove pause tutorial message
        if not pause_tutorial.shown:
            pause_tutorial.end_tutorial()

        # update screen
        screen_update()


# create island function, to be in effect while on first island
def island():
    # make variables global so they can be used
    global treasure_message_timer
    global done
    global on_island
    global sword_draw
    global sword_delay
    global curr_enemy_list
    global treasure_message_display
    global bullets
    global enemies_island

    # ensure player speed does not carry over
    player_obj.halt_speed()

    while island_obj.overview:
        # code for key presses + movement
        location_movement(island_obj, enemies_island)

        # fill screen with background colour
        screen.fill(SEA_BLUE)

        # draw the island up close
        island_obj.draw_close(screen)

        # what happens when player spawns on island
        if on_island:
            land_on_island(island_obj)
            gun_enemy_delay(enemies_island)

        # code to remove enemies from enemies_island list, draw them to screen, and have them attack
        enemy_draw_move(island_obj, enemies_island)

        # code to spawn chest on island
        if not enemies_island:
            island_chest.draw(screen)

        # have player attack (on island)
        player_obj.move_close(island_obj.boundary_rect)

        # make player leave if exit bottom of island
        check_leave_island(island_obj)

        # code to check collision between player and chest
        check_chest_collision(island_obj, island_chest, enemies_island)

        # code to keep treasure message on screen for set amount of time
        check_treasure_message(island_obj, island_chest)

        # code to check if enemies are dead or not
        enemy_health_check()

        # function to check for player death and draw to screen
        player_draw_or_die()

        # code to check if player can be hit
        check_player_invulnerable()

        # code to check if enemy can be hit
        check_enemy_invulnerable()

        # code to check collision between player and enemy
        check_player_enemy_collision(enemies_island)

        # code to check collision between bullet and sword
        if sword_draw:
            # check sword-bullet collision
            check_sword_bullet_collision()

        # code to check collision between bullet and enemy
        # check_bullet_enemy_collision(enemies_island)

        # code to check collision between player and bullet
        check_player_bullet_collision()

        # code to check bullet shooting
        if bullets:
            draw_bullet()

        # draw sword to screen
        draw_sword(enemies_island)

        # update screen and framerate
        screen_update()


# create island 2 function, to be in effect while on second island
def island2():
    # make variables global so they can be used
    global pause_timer
    global treasure_message_timer
    global done
    global on_island
    global sword_draw
    global sword_delay
    global curr_enemy_list
    global bullets
    global enemies_island2

    # ensure player speed does not carry over
    player_obj.halt_speed()

    while island2_obj.overview:
        # code for key presses + movement
        location_movement(island2_obj, enemies_island2)

        # fill screen with background colour
        screen.fill(SEA_BLUE)

        # draw the island up close
        island2_obj.draw_close(screen)

        # what happens when player spawns on island
        if on_island:
            land_on_island(island2_obj)
            gun_enemy_delay(enemies_island2)

        # code to remove enemies from enemies_island list, draw them to screen, and have them attack
        enemy_draw_move(island2_obj, enemies_island2)

        # code to spawn chest on island
        if not enemies_island2:
            island_2_chest.draw(screen)

        # have player move (on an island)
        player_obj.move_close(island2_obj.boundary_rect)

        # make player leave if exit bottom of island
        check_leave_island(island2_obj)

        # code to check collision between player and chest
        check_chest_collision(island2_obj, island_2_chest, enemies_island2)

        # code to keep treasure message on screen for set amount of time
        check_treasure_message(island2_obj, island_2_chest)

        # code to check if enemies are dead or not
        enemy_health_check()

        # display player movements to screen
        player_draw_or_die()

        # code to check if player can be hit
        check_player_invulnerable()

        # code to check if enemy can be hit
        check_enemy_invulnerable()

        # code to check collision between player and enemy
        check_player_enemy_collision(enemies_island2)

        # code to check collision between bullet and sword
        if sword_draw:
            # check sword-bullet collision
            check_sword_bullet_collision()

        # code to check collision between bullet and enemy
        # check_bullet_enemy_collision(enemies_island2)

        # code to check collision between player and bullet
        check_player_bullet_collision()

        # code to check bullet shooting
        if bullets:
            draw_bullet()

        # draw sword to screen
        draw_sword(enemies_island2)

        # update screen and framerate
        screen_update()


# create island function, for centre island
def centre_island():
    # make variables global so they can be used
    global pause_timer
    global treasure_message_timer
    global done
    global on_island
    global sword_draw
    global sword_delay
    global curr_enemy_list
    global enemies_centre_island
    global tutorials

    # ensure player speed does not carry over
    player_obj.halt_speed()

    # loop for island
    while centre_island_obj.overview:
        # code for key presses + movement
        # peaceful_location_movement(centre_island_obj)
        location_movement(centre_island_obj, enemies_centre_island)

        # fill screen with background colour
        screen.fill(SEA_BLUE)

        # draw the island up close
        centre_island_obj.draw_close(screen)

        # have player move (on an island)
        player_obj.move_close(centre_island_obj.boundary_rect)

        # draw the door on the island
        central_island_door.draw(screen)

        # draw the breakable object on the island
        centre_pot_obj.draw(screen)

        # check if breakable object is broken
        sword_obj.check_break(centre_island_obj, centre_island_obj.breakables)

        # what happens when player spawns on island
        if on_island:
            land_on_island(centre_island_obj)

        # check collision with door on island
        if pygame.sprite.collide_rect(player_obj, central_island_door):
            check_player_door_collision(centre_island_obj, dungeon_entrance_obj, enemies_dungeon_entrance)

        # make player leave if exit bottom of island
        if centre_pot_obj.broken:
            check_leave_island(centre_island_obj)

        # display player movements to screen
        player_draw_or_die()

        # display tutorial messages
        for tutorial in tutorials:
            tutorial.show_tutorial(centre_island_obj)

        # remove tutorial messages
        if centre_pot_obj.broken:
            centre_sword_tutorial.end_tutorial()
        if player_obj.change_x != 0 or player_obj.change_y != 0:
            movement_tutorial.end_tutorial()
        if player_obj.rect.y + player_obj.size >= centre_island_obj.position_y_close + centre_island_obj.height - (
            player_obj.speed * 2):
            pause_tutorial.end_tutorial()

        # draw sword to screen
        draw_sword(enemies_centre_island)

        # update screen and framerate
        screen_update()


# create map function, to be used while on world map
def world_map():
    # make variables global so they can be used
    global on_island
    global curr_enemy_list
    global pause_timer

    # ensure player speed does not carry over
    player_obj.halt_speed()

    # map loop
    while map.overview:
        # function for key presses and movement
        map_movement()

        # fill screen with background colour
        screen.fill(SEA_BLUE)

        # draw all islands on map
        island_obj.draw_map(screen)
        island2_obj.draw_map(screen)
        centre_island_obj.draw_map(screen)

        # have player attack (map overview) and draw it to screen
        player_obj.move_map()
        player_obj.draw(screen)

        # what happens when player leaves first island
        if island_obj.off:
            leave_island(island_obj)

        # what happens when player leaves second island
        if island2_obj.off:
            leave_island(island2_obj)

        # what happens when player leaves central island
        if centre_island_obj.off:
            leave_island(centre_island_obj)

        # if player is in map/sailing screen and they go off the edge, make them reappear on the opposite one
        map_wraparound()

        # code for collision detection with islands
        if pygame.sprite.collide_rect(player_obj, island_obj):
            island_collision(island_obj, enemies_island)

        if pygame.sprite.collide_rect(player_obj, island2_obj):
            island_collision(island2_obj, enemies_island2)

        if pygame.sprite.collide_rect(player_obj, centre_island_obj):
            island_collision(centre_island_obj, enemies)

        # display output and framerate
        screen_update()


# create function for dungeon entrance
def dungeon_entrance():
    # make variables global so they can be used
    global pause_timer
    global treasure_message_timer
    global done
    global sword_draw
    global sword_delay
    global curr_enemy_list
    global enemies_dungeon_entrance
    global room_entry
    global bullets

    # ensure player speed does not carry over
    player_obj.halt_speed()

    # while in dungeon entrance
    while dungeon_entrance_obj.overview:

        # code for key presses + movement
        location_movement(dungeon_entrance_obj, enemies_dungeon_entrance)

        # fill screen background
        screen.fill(BLACK)

        # draw dungeon entrance floor
        dungeon_entrance_obj.draw(screen)

        # code to check if player has entered room from bottom
        if room_entry:
            enter_room_lower(dungeon_entrance_obj)
            gun_enemy_delay(enemies_dungeon_entrance)

        # code to draw enemies to screen
        enemy_draw_move(dungeon_entrance_obj, enemies_dungeon_entrance)

        # have player move (within dungeon bounds)
        player_obj.move_close(dungeon_entrance_obj)

        # code to check if enemies are dead or not
        enemy_health_check()

        # display player movements to screen
        player_draw_or_die()

        # code to check if player can be hit
        check_player_invulnerable()

        # code to check if enemy can be hit
        check_enemy_invulnerable()

        # code to check collision between player and enemy
        check_player_enemy_collision(enemies_dungeon_entrance)

        # code to check collision between bullet and sword
        if sword_draw:
            # check sword-bullet collision
            check_sword_bullet_collision()

        # code to check collision between bullet and enemy
        # check_bullet_enemy_collision(enemies_dungeon_entrance)

        # code to check collision between player and bullet
        check_player_bullet_collision()

        # code to check bullet shooting
        if bullets:
            draw_bullet()

        # draw sword to screen
        draw_sword(enemies_dungeon_entrance)

        # check if door can spawn
        if not enemies_dungeon_entrance:
            dungeon_entrance_door.draw(screen)
            # check player-door collision
            if pygame.sprite.collide_rect(player_obj, dungeon_entrance_door):
                check_player_door_collision(dungeon_entrance_obj, dungeon_second_room_obj, enemies_dungeon_second_room)

        # update screen and framerate
        screen_update()


# create function for dungeon entrance
def second_dungeon_room():
    # make variables global so they can be used
    global pause_timer
    global treasure_message_timer
    global done
    global sword_draw
    global sword_delay
    global curr_enemy_list
    global enemies_dungeon_second_room
    global room_entry
    global bullets

    # ensure player speed does not carry over
    player_obj.halt_speed()

    # while in dungeon entrance
    while dungeon_second_room_obj.overview:

        # code for key presses + movement
        location_movement(dungeon_second_room_obj, enemies_dungeon_second_room)

        # fill screen background
        screen.fill(BLACK)

        # draw dungeon entrance floor
        dungeon_second_room_obj.draw(screen)

        # code to check if player has entered room from bottom
        if room_entry:
            enter_room_lower(dungeon_second_room_obj)
            gun_enemy_delay(enemies_dungeon_second_room)

        # code to draw enemies to screen
        enemy_draw_move(dungeon_second_room_obj, enemies_dungeon_second_room)

        # have player move (within dungeon bounds)
        player_obj.move_close(dungeon_second_room_obj)

        # code to check if enemies are dead or not
        enemy_health_check()

        # display player movements to screen
        player_draw_or_die()

        # code to check if player can be hit
        check_player_invulnerable()

        # code to check if enemy can be hit
        check_enemy_invulnerable()

        # code to check collision between player and enemy
        check_player_enemy_collision(enemies_dungeon_second_room)

        # code to check collision between bullet and sword
        if sword_draw:
            # check sword-bullet collision
            check_sword_bullet_collision()

        # code to check collision between bullet and enemy
        # check_bullet_enemy_collision(enemies_dungeon_second_room)

        # code to check collision between player and bullet
        check_player_bullet_collision()

        # code to check bullet shooting
        if bullets:
            draw_bullet()

        # draw sword to screen
        draw_sword(enemies_dungeon_second_room)

        # check all enemies are dead, and display dungeon treasure (end of game)
        if not enemies_dungeon_second_room:
            end_chest.draw(screen)
            end_chest.check_end_game(dungeon_second_room_obj)

        # update screen and framerate
        screen_update()


# main program loop
while not done:
    # if in an area, activate its' function for overview
    if map.overview:
        world_map()

    if island_obj.overview:
        island()

    if island2_obj.overview:
        island2()

    if centre_island_obj.overview:
        centre_island()

    if dungeon_entrance_obj.overview:
        dungeon_entrance()

    if dungeon_second_room_obj.overview:
        second_dungeon_room()

    # display end game screen if game is ended
    if game_end:
        end_game(screen)

    # display output and framerate
    screen_update()

# closes window, exits game
pygame.quit()