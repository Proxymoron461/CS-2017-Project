#initialising pygame
import pygame
import random
from math import pi

#defining a few colours, using their RGB value
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BROWN = (102, 51, 0)
SEABLUE = (0, 191, 255) #colour for sea
GRASSGREEN = (0, 204, 0) #colour for green grassy islands
SAND = (204, 204, 0) #colour for beach islands
ROCK = (128, 128, 128) #colour for rock islands
ENEMY_PURPLE = (255, 51, 255) # stand-in colour for enemies
island_material = (GRASSGREEN, SAND, ROCK) #tuple for the island material

#initialise PI, for some ellipses and arcs
PI = pi

#initialise window height and width
WIDTH = 700
HEIGHT = 500

#initialising the engine
pygame.init()

#setting the borderless window
size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Comp Sci Project") #sets the window title

#initialise player class, using rectangle for now
class Player(pygame.sprite.Sprite):
     def __init__(self, start_x, start_y, size):
         super().__init__() 
         self.change_x = 0 #player speed left and right, starts at 0
         self.change_y = 0 #player speed up and down, starts at 0
         self.size = size #player rectangle size
         self.colour = RED #set player colour
         self.damage_colour = BLACK #set colour to be displayed when damage taken
         self.image = pygame.Surface([self.size, self.size])
         self.image.fill(self.colour)
         self.rect = self.image.get_rect()
         self.rect.x = start_x #player x position
         self.rect.y = start_y #player y position
         self.enemies_killed = 0
         self.last_x = 0 #most recent x direction of player
         self.last_y = -1 #most recent y direction of player
         self.health = 5 #integer for player health
         self.invulnerable = False #boolean for if player is invulnerable or not
         self.invulnerable_timer = pygame.time.get_ticks() #create reference timer for invulnerability period
         self.inventory = []
     def move_map(self):
         self.rect.x += self.change_x
         self.rect.y += self.change_y
     def move_close(self):
         self.rect.clamp_ip(island_rect) #keep player on island
         self.rect.x += self.change_x
         self.rect.y += self.change_y
     def draw(self, screen):
         pygame.draw.rect(screen, self.colour, self.rect)
     def draw_damage(self, screen):
         pygame.draw.rect(screen, self.damage_colour, self.rect)
     def take_damage(self):
         self.health -= enemy_obj.damage #take away enemy damage from player health
     def message(self, text):
         output_text = font.render(text, True, WHITE)
         pygame.draw.rect(screen, BLACK, [0, 0, 700, 50])
         screen.blit(output_text, [20, 10])
                                          
#initialise player object
player_obj = Player(250, 250, 20)

#initialise island class
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
          self.rect_close = [self.position_x_close, self.position_y_close, self.height, self.width] #rectangle for displaying island up close
          self.boundary_rect = [self.position_x_close + 5, self.position_y_close + 5, self.height - 10, self.width - 10] #rectangle for keeping player in island
          self.grid = [[0 for x in range(width // 10)] for y in range(height // 10)]
          self.grid_margin = 10
     def draw_close(self, screen): #drawing code for when player is on island
          pygame.draw.rect(screen, self.colour, self.rect_close)
     def draw_map(self, screen):
          pygame.draw.rect(screen, self.colour, self.rect)
     def find_player(self):
          self.player_x = (player_obj.rect.x - self.position_x_close)
          self.player_y = (player_obj.rect.y - self.position_y_close)
          self.grid_player_x = self.player_x // self.grid_margin
          self.grid_player_y = self.player_y // self.grid_margin
          return [self.grid_player_x, self.grid_player_y]

#initialise island objects
island_obj = Island(200, 200, 400, 100)
island2_obj = Island(300, 300, 200, 300)

#initialise enemy class, intended as parent class for future enemies
class Enemy(pygame.sprite.Sprite):
     def __init__(self, size, colour, start_x, start_y, health, damage):
          super().__init__()
          self.change_x = 0 #initial x speed
          self.change_y = 0 #initial y speed
          self.size = size #set size
          self.colour = colour #set colour, may delegate to enemy sub-class in future
          self.image = pygame.Surface([self.size, self.size])
          self.image.fill(self.colour)
          self.rect = self.image.get_rect()
          self.rect.x = start_x #enemy x position
          self.rect.y = start_y #enemy y position
          self.health = 1 #integer for health value, each hit does damage of 1
          self.dead = False #boolean for if enemy is dead or not
          self.damage = 1 #boolean for damage enemy does to player health
          self.invulnerable = False #boolean for if enemy can take damage or not
          self.invulnerable_timer = pygame.time.get_ticks() #sets the current time as reference for invincibility
     def move(self):
          self.rect.clamp_ip(island_rect) #keep enemy on island
          #code to move enemy towards player, facing them
          if player_obj.rect.x > self.rect.x:
               self.change_x = 1.5
          elif player_obj.rect.x < self.rect.x:
               self.change_x = -1.5
          if player_obj.rect.y > self.rect.y:
               self.change_y = 1.5
          elif player_obj.rect.y < self.rect.y:
               self.change_y = -1.5
          self.rect.x += self.change_x
          self.rect.y += self.change_y
     def draw(self, screen):
          if not self.dead:
               pygame.draw.rect(screen, self.colour, self.rect)

#initialise enemy object
enemy_obj = Enemy(20, ENEMY_PURPLE, 350, 250, 1, 1)

#initialise sword class, for attacking
class Sword(pygame.sprite.Sprite):
     def __init__(self, size):
          super().__init__()
          self.size = size
          self.colour = BLACK
          self.image = pygame.Surface([self.size, self.size])
          self.image.fill(self.colour)
          self.rect = self.image.get_rect()
          self.rect.x = player_obj.rect.x + player_obj.size
          self.rect.y = player_obj.rect.y + player_obj.size
     def draw(self, screen):
          pygame.draw.rect(screen, self.colour, self.rect)
     def attack(self):
          #code to put rectangle x value at area where character is facing
          if player_obj.last_x > 0:
              self.rect.x = player_obj.rect.x + player_obj.size
          elif player_obj.last_x < 0:
              self.rect.x = player_obj.rect.x - self.size
          elif player_obj.last_x == 0:
              self.rect.x = player_obj.rect.x + (player_obj.size / 2) - (self.size / 2)

          #code to put rectangle y value at area where character is facing     
          if player_obj.last_y > 0:
              self.rect.y = player_obj.rect.y + player_obj.size
          elif player_obj.last_y < 0:
              self.rect.y = player_obj.rect.y - self.size
          elif player_obj.last_y == 0:
              self.rect.y = player_obj.rect.y + (player_obj.size / 2) - (self.size / 2)
              
          #create list of enemies hit by player sword
          enemies_hit_list = pygame.sprite.spritecollide(self, enemies_island2, False)
          for enemy_obj in enemies_hit_list:
               if not enemy_obj.invulnerable:
                   enemy_obj.health -= 1
                   enemy_obj.invulnerable = True

#create sword object, for use during the game
sword_obj = Sword(15)

#initialise treasure chest class
class Treasure_Chest(pygame.sprite.Sprite):
     def __init__(self, size, position_x, position_y, treasure):
          super().__init__()
          self.colour = BROWN
          self.size = size
          self.image = pygame.Surface([self.size, self.size])
          self.image.fill(self.colour)
          self.rect = self.image.get_rect()
          self.rect.x = position_x
          self.rect.y = position_y
          self.treasure = treasure
          self.text = "Congratulations! You found the " + self.treasure + "!"
     def pick_treasure(self):
          player_obj.message(self.text)
          player_obj.inventory.append(self.treasure)
     def draw(self, screen):
          pygame.draw.rect(screen, self.colour, self.rect)

#miscellaneous values
map_overview = True #boolean for when player is in map
island_overview = False #boolean for when player is on first island
island2_overview = False #boolean for when player is on second island
dungeon_overview = False #boolean for when player is in dungeon
on_island = False #boolean for when player gets onto island
off_island = False #boolean for when player gets off first island
off_island2 = False #boolean for when player gets off second island
islands = pygame.sprite.Group() #initialise list of islands
islands.add(island_obj) #add first island object to list of islands
islands.add(island2_obj) #add second island object to list of islands
enemies_island2 = pygame.sprite.Group() #create list of enemies for island 2
enemies_island2.add(enemy_obj) #add enemy to list of enemies
sword_draw = False #boolean for if sword should be drawn
swords = pygame.sprite.Group() #create list of swords
font = pygame.font.SysFont('Arial Black', 18, True, False) #created font for use in player messages
island_2_chest_open = False #boolean for if the chest on island 2 has been opened
pause = False #boolean for if the game is paused

#main program loop setup
done = False
clock = pygame.time.Clock()

#main program loop
while not done:
    for event in pygame.event.get(): #if the user does something
        if event.type == pygame.QUIT: #if the user clicks close
            done = True
        if event.type == pygame.KEYDOWN: #if key is pressed, movement starts
            if (event.key == pygame.K_UP or event.key == pygame.K_w) and not pause:
                player_obj.change_y = -5
                player_obj.last_y = -1
                player_obj.last_x = 0
            if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and not pause:
                player_obj.change_y = 5
                player_obj.last_y = 1
                player_obj.last_x = 0
            if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and not pause:
                player_obj.change_x = -5
                player_obj.last_y = 0
                player_obj.last_x = -1
            if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and not pause:
                player_obj.change_x = 5
                player_obj.last_y = 0
                player_obj.last_x = 1
            if event.key == pygame.K_j and not pause:
                print(player_obj.inventory)
            if event.key == pygame.K_p:
                if not pause:
                     pause = True
                     pause_timer = pygame.time.get_ticks()
                else:
                     pause = False
            if event.key == pygame.K_SPACE and not pause:
                if (player_obj.change_x == 0 and player_obj.change_y == 0) and (island_overview or island2_overview or dungeon_overview):
                     sword_draw = True
                     sword_obj.attack()
                     sword_delay = pygame.time.get_ticks() #amount of milliseconds before sword sprite disappears
        if event.type == pygame.KEYUP: #if key is released, movement stops
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_w or event.key == pygame.K_s:
                player_obj.change_y = 0
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                player_obj.change_x = 0
                            
    #makes sure the screen is blank, drawing code goes AFTER
    #fill in background depending on where the player is
    if map_overview:
         screen.fill(SEABLUE)
    if island_overview:
         screen.fill(SEABLUE)
    if island2_overview:
         screen.fill(SEABLUE)
    if dungeon_overview:
         screen.fill(ROCK)

    #screen drawing code, like shapes and text, goes here
    #x and y start from TOP LEFT

    #while on map screen
    if map_overview:
         #have player move (map overview) and draw it to screen
         player_obj.move_map()

         island_obj.draw_map(screen)
         island2_obj.draw_map(screen)
         
         #what happens when player leaves first island
         if off_island:
              player_obj.rect.y = island_obj.rect.y + island_obj.height_map + 5
              player_obj.rect.x = island_obj.rect.x + (island_obj.width_map / 2) - (player_obj.size / 2)
              player_obj.change_x = 0
              player_obj.change_y = 0
              off_island = False
              pygame.time.delay(200)

         #what happens when player leaves second island
         if off_island2:
              player_obj.rect.y = island2_obj.rect.y + island2_obj.height_map + 5
              player_obj.rect.x = island2_obj.rect.x + (island2_obj.width_map / 2) - (player_obj.size / 2)
              player_obj.change_x = 0
              player_obj.change_y = 0
              off_island2 = False
              pygame.time.delay(200)

         #if player is in map/sailing screen and they go off the edge, make them reappear on the opposite one
         if player_obj.rect.x + player_obj.size < 0:
              player_obj.rect.x = WIDTH + 5
         elif player_obj.rect.x > WIDTH:
              player_obj.rect.x = (0 - player_obj.size) - 5
         if player_obj.rect.y + player_obj.size < 0:
              player_obj.rect.y = HEIGHT + 5
         elif player_obj.rect.y > HEIGHT:
              player_obj.rect.y = (0 - player_obj.size) - 5

         #code for collision detection with islands
         if pygame.sprite.collide_rect(player_obj, island_obj):
              map_overview = False
              island_overview = True
              on_island = True
              island_rect = island_obj.boundary_rect

         if pygame.sprite.collide_rect(player_obj, island2_obj):
              map_overview = False
              island2_overview = True
              on_island = True
              island_rect = island2_obj.boundary_rect

    #while on first island screen
    if island_overview:
        #have player move (island overview) within island boundaries
        player_obj.move_close()
        
        island_obj.draw_close(screen)
        
        #what happens when player spawns on island
        if on_island:
            player_obj.rect.y = island_obj.position_y_close + (4 * (island_obj.height / 5))
            player_obj.rect.x = island_obj.position_x_close + (island_obj.width / 2) - (player_obj.size / 2)
            player_obj.change_x = 0
            player_obj.change_y = 0
            on_island = False
            pygame.time.delay(200)

        #make player leave if exit bottom of island
        if player_obj.rect.y + player_obj.size >= island_obj.position_y_close + island_obj.height:
             island_overview = False
             map_overview = True
             off_island = True

    #while on second island screen
    if island2_overview:
        #draw island
        island2_obj.draw_close(screen)

        #create chest object
        island_2_chest = Treasure_Chest(40, island2_obj.position_x_close + (island2_obj.width / 2) - 20, island2_obj.position_y_close + 40 - 20, "Sword of Awesome")
                
        #code to spawn enemies on island
        for enemy_obj in enemies_island2:
             enemy_obj.draw(screen)

        #code to spawn chest on island
        island_2_chest.draw(screen)

        #have player move (on an island)
        player_obj.move_close()
        
        #have enemy move
        if not pause:
             enemy_obj.move()
        
        #what happens when player spawns on island
        if on_island:
            player_obj.rect.y = island2_obj.position_y_close + (4 * (island2_obj.height / 5))
            player_obj.rect.x = island2_obj.position_x_close + (island2_obj.width / 2) - (player_obj.size / 2)
            player_obj.change_x = 0
            player_obj.change_y = 0
            on_island = False
            pygame.time.delay(200)

        #make player leave if exit bottom of island
        if player_obj.rect.y + player_obj.size >= island2_obj.position_y_close + island2_obj.height:
             island2_overview = False
             map_overview = True
             off_island2 = True

        #code to check collision between player and chest, output a found treasure message, and add that treasure to player inventory
        if pygame.sprite.collide_rect(player_obj, island_2_chest) and not island_2_chest_open:
             island_2_chest.pick_treasure()
             island_2_chest_open = True
             treasure_message_timer = pygame.time.get_ticks()

        #code to keep treasure message on screen for set amount of time
        if island_2_chest_open:
             if pygame.time.get_ticks() - treasure_message_timer <= 2000:
                  player_obj.message(island_2_chest.text)

    #code to check if enemies are dead or not
    for enemy_obj in enemies_island2:
        if enemy_obj.health <= 0:
            enemy_obj.dead = True

    #display player movements to screen
    player_obj.draw(screen)

    #code to check if player can be hit
    if pygame.time.get_ticks() - player_obj.invulnerable_timer >= 1000:
        player_obj.invulnerable = False

    #code to check if enemy can be hit
    if pygame.time.get_ticks() - enemy_obj.invulnerable_timer >= 500:
        enemy_obj.invulnerable = False

    #code to check collision between player and enemy
    if pygame.sprite.collide_rect(player_obj, enemy_obj) and not enemy_obj.dead and not player_obj.invulnerable:
        player_obj.take_damage()
        player_obj.invulnerable = True
        player_obj.invulnerable_timer = pygame.time.get_ticks()
    
    #draw sword to screen
    if sword_draw:
        if player_obj.change_x == 0 and player_obj.change_y == 0:
            sword_obj.draw(screen)
        else:
            sword_draw = False
        if pygame.time.get_ticks() - sword_delay >= 700:
            sword_draw = False

    #clear screen and ignore if paused
    if pause:
        screen.fill(BLACK)
        text = font.render("Game paused. Press P to continue.", True, WHITE)
        screen.blit(text, [20, 10])
        if sword_draw:
            sword_delay += (pygame.time.get_ticks() - pause_timer)
        player_obj.invulnerable_timer += (pygame.time.get_ticks() - pause_timer)
        enemy_obj.invulnerable_timer += (pygame.time.get_ticks() - pause_timer)
        if island_2_chest_open:
            treasure_message_timer += (pygame.time.get_ticks() - pause_timer)
        pause_timer = pygame.time.get_ticks()
    
    #display output and framerate
    pygame.display.flip() #updates screen with what's drawn
    if island_overview:
         pygame.display.update(island_obj.rect) #if player on an island, the screen will only update what is on the island to save memory
    if island2_overview:
         pygame.display.update(island2_obj.rect)
    clock.tick(60) #limits to 60 frames per second

#closes window, exits game
pygame.quit()
