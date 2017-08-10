# import modules
import pygame
import random
import math
from math import pi

# defining a few colours, using their RGB value
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BROWN = (102, 51, 0)
SEABLUE = (0, 191, 255)  # colour for sea
GRASSGREEN = (0, 204, 0)  # colour for green grassy islands
SAND = (204, 204, 0)  # colour for beach islands
ROCK = (128, 128, 128)  # colour for rock islands
ENEMY_PURPLE = (255, 51, 255)  # stand-in colour for enemies
island_material = (GRASSGREEN, SAND, ROCK)  # tuple for the island material

# initialise PI, for some ellipses and arcs
PI = pi

# initialise window height and width
WIDTH = 700
HEIGHT = 500

# initialising the engine
pygame.init()

# setting the borderless window
size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Comp Sci Project")  # sets the window title


# initialise player class, using rectangle for now
class Player(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y, player_size):
        super().__init__()
        self.change_x = 0  # player speed left and right, starts at 0
        self.change_y = 0  # player speed up and down, starts at 0
        self.size = player_size  # player rectangle size
        self.colour = RED  # set player colour
        self.image = pygame.Surface([self.size, self.size])
        self.image.fill(self.colour)
        self.rect = self.image.get_rect()
        self.rect.x = start_x  # player x position
        self.rect.y = start_y  # player y position
        self.enemies_killed = 0
        self.last_x = 0  # most recent x direction of player
        self.last_y = -1  # most recent y direction of player
        self.health = 5  # integer for player health
        self.max_health = 5  # integer for maximum player health
        self.invulnerable = False  # boolean for if player is invulnerable or not
        self.invulnerable_timer = pygame.time.get_ticks()  # create reference timer for invulnerability period
        self.inventory = []  # empty list for use in inventory

    def move_map(self):
        self.rect.x += self.change_x
        self.rect.y += self.change_y

    def move_close(self):
        self.rect.clamp_ip(island_rect)  # keep player on island
        self.rect.x += self.change_x
        self.rect.y += self.change_y

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, self.rect)

    def take_damage(self, damage_source):
        self.health -= damage_source.damage  # take away enemy damage from player health

    def message(self, text):
        output_text = font.render(text, True, WHITE)
        pygame.draw.rect(screen, BLACK, [0, 0, 700, 50])
        screen.blit(output_text, [20, 10])

    def halt_speed(self):
        player_obj.change_y = 0
        player_obj.change_x = 0


# initialise player object
player_obj = Player(350, 250, 20)


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
        self.image = pygame.Surface([self.width_map, self.height_map])
        self.image.fill(self.colour)
        self.rect = self.image.get_rect()
        self.rect.x = position_x
        self.rect.y = position_y
        self.rect_close = [self.position_x_close, self.position_y_close, self.height,
                           self.width]  # rectangle for displaying island up close
        self.boundary_rect = [self.position_x_close + 5, self.position_y_close + 5, self.height - 10,
                              self.width - 10]  # rectangle for keeping player in island
        # self.grid = [[0 for x in range(width // 10)] for y in range(height // 10)]
        # self.grid_margin = 10
        self.overview = False
        self.off = False  # boolean to check if player has left island
        self.chest_open = False  # boolean to check if island chest is open
        self.island_location = False # boolean to determine if island spawn location is all good (no collisions)

    def draw_close(self, screen):  # drawing code for when player is on island
        pygame.draw.rect(screen, self.colour, self.rect_close)

    def draw_map(self, screen):
        pygame.draw.rect(screen, self.colour, self.rect)

        # def find_player(self):
        #     self.player_x = (player_obj.rect.x - self.position_x_close)
        #     self.player_y = (player_obj.rect.y - self.position_y_close)
        #     self.grid_player_x = self.player_x // self.grid_margin
        #     self.grid_player_y = self.player_y // self.grid_margin
        #     return [self.grid_player_x, self.grid_player_y]


# create map class, for use
class Map():
    def __init__(self):
        self.overview = True

# create map object
map = Map()

# initialise moving enemy class, intended as parent class for future enemies
class MovingEnemy(pygame.sprite.Sprite):
    def __init__(self, size, colour, start_x, start_y, health, damage):
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
        self.health = 1  # integer for health value, each hit does damage of 1
        # self.dead = False  # boolean for if enemy is dead or not
        self.damage = 1  # boolean for damage enemy does to player health
        self.invulnerable = False  # boolean for if enemy can take damage or not
        self.invulnerable_timer = pygame.time.get_ticks()  # sets the current time as reference for invincibility
        self.move_timer = pygame.time.get_ticks()  # sets current time as reference for attack calculation
        # self.chest_collision = False  # boolean for if enemy has collided with a chest
        # self.aggressive = True #boolean for if enemy should be attacking or not
       # self.move_rect = (self.size, 45, self.rect.x + self.size,
                          # self.rect.y + self.size)  # set rectangle for checking movement path

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
        if pygame.time.get_ticks() - self.move_timer >= 500:
            if abs(player_obj.rect.x - self.rect.x) < abs(player_obj.rect.y - self.rect.y):
                if player_obj.rect.y > self.rect.y:
                    self.change_x = 0
                    self.change_y = 1.5
                    self.move_timer = pygame.time.get_ticks()
                else:
                    self.change_x = 0
                    self.change_y = -1.5
                    self.move_timer = pygame.time.get_ticks()
            elif abs(player_obj.rect.x - self.rect.x) > abs(player_obj.rect.y - self.rect.y):
                if player_obj.rect.x > self.rect.x:
                    self.change_x = 1.5
                    self.change_y = 0
                    self.move_timer = pygame.time.get_ticks()
                else:
                    self.change_x = -1.5
                    self.change_y = 0
                    self.move_timer = pygame.time.get_ticks()

    def attack(self):
        self.rect.clamp_ip(island_rect)  # keep enemy on island

        # #code to check how close player is to enemy
        # if abs(player_obj.rect.x - self.rect.x) <= 50 or abs(player_obj.rect.y - self.rect.y) <= 50:
        #      self.aggressive = True
        # else:
        #      self.aggressive = False

        # attack movement
        self.move_attack()

        # check movement
        # self.check_movement()

        # apply position changes
        self.rect.x += self.change_x
        self.rect.y += self.change_y

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, self.rect)


# class for stationary, shooting enemies
class GunEnemy(pygame.sprite.Sprite):
    def __init__(self, size, colour, start_x, start_y, health, damage):
        super().__init__()
        self.size = size
        self.colour = colour
        self.image = pygame.Surface([self.size, self.size])
        self.image.fill(self.colour)
        self.rect = self.image.get_rect()
        self.rect.x = start_x  # enemy x position
        self.rect.y = start_y  # enemy y position
        self.health = 2  # integer for health value, each hit does damage of 1
        # self.dead = False  # boolean for if enemy is dead or not
        self.invulnerable = False # boolean for if enemy can be hit
        self.invulnerable_timer = pygame.time.get_ticks() # sets the current time as reference for invincibility
        self.attack_timer = pygame.time.get_ticks() # sets the current time as reference for attacking
        self.can_attack = False # boolean for if the enemy can attack
        self.damage = 0 # integer for how much damage dealt to player health

    def attack(self):
        # make variables global
        global screen
        # check enemy can attack
        if pygame.time.get_ticks() - self.attack_timer >= 2000:
            self.can_attack = True
        if self.can_attack and not pygame.sprite.collide_rect(self, player_obj):
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
        self.image = pygame.Surface([self.size, self.size])
        self.image.fill(self.colour)
        self.rect = self.image.get_rect()
        self.rect.x = start_x
        self.rect.y = start_y
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.damage = 2 # integer for damage dealt to player health

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, self.rect)

    def move(self):
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed


# initialise sword class, for attacking
class Sword(pygame.sprite.Sprite):
    def __init__(self, size):
        super().__init__()
        self.size = size
        # self.colour = BLACK
        # load pygame image sprite
        self.image = pygame.image.load("Sword.png").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = player_obj.rect.x + player_obj.size
        self.rect.y = player_obj.rect.y + player_obj.size
        # create variables for sword image/sprite at different directions
        self.image_up = self.image
        self.image_down = pygame.transform.flip(self.image, False, True)
        self.image_left = pygame.transform.rotate(self.image, 90)
        self.image_right = pygame.transform.flip(self.image_left, True, False)
        self.curr_image = self.image_up

    def draw(self, screen):
        screen.blit(self.curr_image, [self.rect.x, self.rect.y])

    def attack(self):
        # code to put rectangle x value at area where character is facing
        if player_obj.last_x > 0:
            self.rect.x = player_obj.rect.x + player_obj.size
            self.curr_image = self.image_right
        elif player_obj.last_x < 0:
            self.rect.x = player_obj.rect.x - self.size
            self.curr_image = self.image_left
        elif player_obj.last_x == 0:
            self.rect.x = player_obj.rect.x + (player_obj.size / 2) - (self.size / 2)

        # code to put rectangle y value at area where character is facing
        if player_obj.last_y > 0:
            self.rect.y = player_obj.rect.y + player_obj.size
            self.curr_image = self.image_down
        elif player_obj.last_y < 0:
            self.rect.y = player_obj.rect.y - self.size
            self.curr_image = self.image_up
        elif player_obj.last_y == 0:
            self.rect.y = player_obj.rect.y + (player_obj.size / 2) - (self.size / 2)

    def attack_collision(self, enemy_list):
        # make variables global
        global enemies_island
        global enemies_island2
        # create list of enemies hit by player sword
        enemies_hit_list = pygame.sprite.spritecollide(self, enemy_list, False)
        for enemy in enemies_hit_list:
            if not enemy.invulnerable:
                enemy.health -= 1
                enemy.invulnerable = True
                enemies_hit.add(enemy)


# create sword object, for use during the game
sword_obj = Sword(15)


# initialise treasure chest class
class TreasureChest(pygame.sprite.Sprite):
    def __init__(self, size, position_x, position_y, treasure):
        super().__init__()
        self.colour = BROWN
        self.size = size
        # self.image = pygame.Surface([self.size, self.size])
        # self.image.fill(self.colour)
        self.image = pygame.image.load("Chest.png").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = position_x
        self.rect.y = position_y
        self.treasure = treasure
        self.text = "Congratulations! You found the " + self.treasure + "!"

    def pick_treasure(self):
        player_obj.message(self.text)
        player_obj.inventory.append(self.treasure)

    def draw(self, screen):
        screen.blit(self.image, [self.rect.x, self.rect.y])


# miscellaneous values
map.overview = True  # boolean for when player is in map
on_island = False  # boolean for when player gets onto island
island_obj = Island(300, 300, 0, 0)
island2_obj = Island(300, 300, 0, 0)
centre_island_obj = Island(400, 400, ((WIDTH / 2) - 50), ((HEIGHT / 2) - 50))
islands = pygame.sprite.Group()  # initialise list of islands
islands.add(island_obj)  # add first island object to list of islands
islands.add(island2_obj)  # add second island object to list of islands
enemies = pygame.sprite.Group()  # create list of all enemies
enemies_island2 = pygame.sprite.Group()  # create list of enemies for island 2
enemies_island = pygame.sprite.Group()  # create list of enemies for island 1
enemies_dungeon = pygame.sprite.Group()  # create list of enemies for dungeon
enemies_hit = pygame.sprite.Group()  # create list of enemies hit by sword
sword_draw = False  # boolean for if sword should be drawn
swords = pygame.sprite.Group()  # create list of swords
bullets = pygame.sprite.Group() # create list of bullets
font = pygame.font.SysFont('Arial Black', 18, True, False)  # created font for use in player messages
paused = False  # boolean for if the game is paused
enemy_move_timer = 0  # timer for when enemy can calculate movement
chests = pygame.sprite.Group()  # group for all chests in game
curr_enemy_list = enemies  # current list for enemy collision
treasure_message_display = False  # boolean for if treasure chest message should be displayed

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
            if not pygame.sprite.spritecollideany(island, islands) and not pygame.sprite.collide_rect(island, centre_island_obj):
                island.island_location = True
                islands.add(island)
                x_position_list.remove(index_x)
                y_position_list.remove(index_y)
    islands.add(centre_island_obj)  # add centre_island to list of islands


# function to spawn enemies on location (island, dungeon room, etc)
def island_moving_enemy_spawn(location_list):
    # make variables global
    global enemies_island
    global enemies_island2
    global enemies
    # for loop determining enemy spawn
    for index in range(3):
        enemy_obj = MovingEnemy(20, ENEMY_PURPLE, 300, 150, 1, 1)
        location_list.add(enemy_obj)
        enemies.add(enemy_obj)
        enemy_obj.rect.x += (index * 50)
        enemy_obj.rect.y += (index * 50)

def island_gun_enemy_spawn(location_list):
    # make variables global
    global enemies_island
    global enemies_island2
    global enemies
    # for loop determining enemy spawn
    for index in range(3):
        enemy_obj = GunEnemy(20, ENEMY_PURPLE, 300, 150, 1, 1)
        location_list.add(enemy_obj)
        enemies.add(enemy_obj)
        enemy_obj.rect.x += (index * 50)
        enemy_obj.rect.y += (index * 50)

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
    # iterate through list of bullets, and either draw and move, or remove from list
    for bullet_shot in bullets:
        if ((bullet_shot.rect.x < WIDTH and bullet_shot.rect.x > 0 - bullet_shot.size) and
                (bullet_shot.rect.y < HEIGHT and bullet_shot.rect.y > 0 - bullet_shot.size)):
            bullet_shot.move()
            bullet_shot.draw(screen)
        else:
            bullet_shot.kill()


# function to determine whether enemies are dead or not
def enemy_health_check():
    for enemy in enemies_hit:
        if enemy.health <= 0:
            enemy.kill()


# function to determine whether enemies are removed from groups (killed) or if they attack
def enemy_draw_move(location_list):
    for enemy in location_list:
        enemy.draw(screen)
        if player_obj.health > 0:
            enemy.attack()


def player_draw_or_move():
    # display player movements to screen
    if player_obj.health > 0:
        player_obj.draw(screen)
    else:
        # display death message upon failure
        player_obj.message("You died! Press ESC to quit.")


# function to determine what happens when player lands on island
def land_on_island(curr_island):
    # make variables global
    global on_island
    # code to determine what happens
    player_obj.rect.y = curr_island.position_y_close + (4 * (curr_island.height / 5))
    player_obj.rect.x = curr_island.position_x_close + (curr_island.width / 2) - (player_obj.size / 2)
    player_obj.change_x = 0
    player_obj.change_y = 0
    on_island = False


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
    if player_obj.rect.y + player_obj.size >= curr_island.position_y_close + curr_island.height:
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
    treasure_message_display = False # stop displaying treasure message
    bullets.empty() # remove all bullets from group


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
    if pygame.time.get_ticks() - player_obj.invulnerable_timer >= 2000:
        player_obj.invulnerable = False


# function to check if enemy can be hit
def check_enemy_invulnerable():
    for enemy in enemies_hit:
        if pygame.time.get_ticks() - enemy.invulnerable_timer >= 1000:
            enemy.invulnerable = False
            enemies_hit.remove(enemy)


# function to check for collision between player and enemy
def check_player_enemy_collision():
    # code to check collision between player and enemy
    enemy_damage_list = pygame.sprite.spritecollide(player_obj, enemies, False)
    for enemy in enemy_damage_list:
        if not player_obj.invulnerable:
            player_obj.take_damage(enemy)
            player_obj.invulnerable = True
            player_obj.invulnerable_timer = pygame.time.get_ticks()

# function to check for collision between player and bullets
def check_player_bullet_collision():
    # code to check collision between player and bullets
    bullet_hit_list = pygame.sprite.spritecollide(player_obj, bullets, True)
    for bullet_hit in bullet_hit_list:
        if not player_obj.invulnerable:
            player_obj.take_damage(bullet_hit)
            player_obj.invulnerable = True
            player_obj.invulnerable_timer = pygame.time.get_ticks()


# function to ensure map wrap around to keep player on screen
def map_wraparound():
    # if player is in map/sailing screen and they go off the edge, make them reappear on the opposite one
    if player_obj.rect.x + player_obj.size < 0:
        player_obj.rect.x = WIDTH + 5
    elif player_obj.rect.x > WIDTH:
        player_obj.rect.x = (0 - player_obj.size) - 5
    if player_obj.rect.y + player_obj.size < 0:
        player_obj.rect.y = HEIGHT + 5
    elif player_obj.rect.y > HEIGHT:
        player_obj.rect.y = (0 - player_obj.size) - 5

# function for island collision on map
def island_collision(island, island_enemies_list):
    # make variables global
    global on_island
    global island_rect
    global curr_enemy_list

    # code for collision
    map.overview = False
    island.overview = True
    on_island = True
    island_rect = island.boundary_rect
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
    # code for key presses + movement
    for event in pygame.event.get():  # if the user does something
        if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:  # if the user clicks close or presses escape
            done = True
            curr_location.overview = False
        if event.type == pygame.KEYDOWN:  # if key is pressed, movement starts
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                player_obj.change_y = -5
                player_obj.last_y = -1
                player_obj.last_x = 0
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                player_obj.change_y = 5
                player_obj.last_y = 1
                player_obj.last_x = 0
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player_obj.change_x = -5
                player_obj.last_y = 0
                player_obj.last_x = -1
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player_obj.change_x = 5
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
                player_obj.change_y = -5
                player_obj.last_y = -1
                player_obj.last_x = 0
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                player_obj.change_y = 5
                player_obj.last_y = 1
                player_obj.last_x = 0
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player_obj.change_x = -5
                player_obj.last_y = 0
                player_obj.last_x = -1
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player_obj.change_x = 5
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
                             island_obj.position_y_close + 40 - 20, "Shield of Litness")
chests.add(island_chest)

island_2_chest = TreasureChest(40, island2_obj.position_x_close + (island2_obj.width / 2) - 20,
                               island2_obj.position_y_close + 40 - 20, "Sword of Awesome")
chests.add(island_2_chest)

# assign island spawn locations
island_spawn()

# create all enemy objects for use on island 1
island_moving_enemy_spawn(enemies_island)

# create all enemy objects for use on island 2
island_gun_enemy_spawn(enemies_island2)

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

        # update screen
        screen_update()


# create island function, to be in effect while on first island
def island():
    # make variables global so they can be used
    global pause_timer
    global treasure_message_timer
    global done
    global on_island
    global island_rect
    global sword_draw
    global sword_delay
    global curr_enemy_list
    global treasure_message_display

    # ensure player speed does not carry over
    player_obj.halt_speed()

    while island_obj.overview:
        # code for key presses + movement
        location_movement(island_obj, enemies_island)

        # fill screen with background colour
        screen.fill(SEABLUE)

        # draw the island up close
        island_obj.draw_close(screen)

        # code to remove enemies from enemies_island list, draw them to screen, and have them attack
        enemy_draw_move(enemies_island)

        # code to spawn chest on island
        if not enemies_island:
            island_chest.draw(screen)

        # have player attack (on island)
        player_obj.move_close()

        # what happens when player spawns on island
        if on_island:
            land_on_island(island_obj)

        # make player leave if exit bottom of island
        check_leave_island(island_obj)

        # code to check collision between player and chest
        check_chest_collision(island_obj, island_chest, enemies_island)

        # code to keep treasure message on screen for set amount of time
        check_treasure_message(island_obj, island_chest)

        # code to check if enemies are dead or not
        enemy_health_check()

        # function to check for player death and draw to screen
        player_draw_or_move()

        # code to check if player can be hit
        check_player_invulnerable()

        # code to check if enemy can be hit
        check_enemy_invulnerable()

        # code to check collision between player and enemy
        check_player_enemy_collision()

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
    global island_rect
    global sword_draw
    global sword_delay
    global curr_enemy_list

    # ensure player speed does not carry over
    player_obj.halt_speed()

    while island2_obj.overview:
        # code for key presses + movement
        location_movement(island2_obj, enemies_island2)

        # fill screen with background colour
        screen.fill(SEABLUE)

        # draw the island up close
        island2_obj.draw_close(screen)

        # code to remove enemies from enemies_island list, draw them to screen, and have them attack
        enemy_draw_move(enemies_island2)

        # code to spawn chest on island
        if not enemies_island2:
            island_2_chest.draw(screen)

        # have player attack (on an island)
        player_obj.move_close()

        # what happens when player spawns on island
        if on_island:
            land_on_island(island2_obj)

        # make player leave if exit bottom of island
        check_leave_island(island2_obj)

        # code to check collision between player and chest
        check_chest_collision(island2_obj, island_2_chest, enemies_island2)

        # code to keep treasure message on screen for set amount of time
        check_treasure_message(island2_obj, island_2_chest)

        # code to check if enemies are dead or not
        enemy_health_check()

        # display player movements to screen
        player_draw_or_move()

        # code to check if player can be hit
        check_player_invulnerable()

        # code to check if enemy can be hit
        check_enemy_invulnerable()

        # code to check collision between player and enemy
        check_player_enemy_collision()

        # code to check bullet shooting
        if bullets:
            draw_bullet()

        # draw sword to screen
        draw_sword(enemies_island2)

        # update screen and framerate
        screen_update()


# create map function, to be used while on world map
def world_map():
    # make variables global so they can be used
    global on_island
    global island_rect
    global curr_enemy_list
    global pause_timer

    # ensure player speed does not carry over
    player_obj.halt_speed()

    # map loop
    while map.overview:
        # function for key presses and movement
        map_movement()

        # fill screen with background colour
        screen.fill(SEABLUE)

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

        # if player is in map/sailing screen and they go off the edge, make them reappear on the opposite one
        map_wraparound()

        # code for collision detection with islands
        if pygame.sprite.collide_rect(player_obj, island_obj):
            island_collision(island_obj, enemies_island)

        if pygame.sprite.collide_rect(player_obj, island2_obj):
            island_collision(island2_obj, enemies_island2)

        # display output and framerate
        screen_update()


# main program loop
while not done:
    # functions for different areas
    if map.overview:
        world_map()

    if island_obj.overview:
        island()

    if island2_obj.overview:
        island2()

    # display output and framerate
    screen_update()

# closes window, exits game
pygame.quit()
