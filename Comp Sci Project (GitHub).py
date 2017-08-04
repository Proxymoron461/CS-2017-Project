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
         self.health = 30 #integer for player health
         self.max_health = 30 #integer for maximum player health (when healing, etc, want to be able to return player health to max efficiently)
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
island_obj = Island(400, 400, 400, 100)
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
          self.move_timer = pygame.time.get_ticks() #sets current time as reference for move calculation
          self.chest_collision = False #boolean for if enemy has collided with a chest
          self.move_x_plane = False #boolean for change of direction upon collision with obstacle
          self.move_y_plane = False #boolean for change of direction upon collision with obstacle
     def move(self):
          self.rect.clamp_ip(island_rect) #keep enemy on island
                    
          #code to move enemy towards player
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
              elif abs(player_obj.rect.x - self.rect.x) > abs(player_obj.rect.y - self.rect.y) or self.move_x_plane:
                  if player_obj.rect.x > self.rect.x:
                      self.change_x = 1.5
                      self.change_y = 0
                      self.move_timer = pygame.time.get_ticks()
                  else:
                      self.change_x = -1.5
                      self.change_y = 0
                      self.move_timer = pygame.time.get_ticks()
               
          self.rect.x += self.change_x
          self.rect.y += self.change_y
     def draw(self, screen):
          if not self.dead:
               pygame.draw.rect(screen, self.colour, self.rect)

#initialise sword class, for attacking
class Sword(pygame.sprite.Sprite):
     def __init__(self, size):
          super().__init__()
          self.size = size
          self.colour = BLACK
          #self.image = pygame.Surface([self.size, self.size])
          #self.image.fill(self.colour)
          self.image = pygame.image.load("Sword.png").convert()
          self.image.set_colorkey(BLACK)
          self.rect = self.image.get_rect()
          self.rect.x = player_obj.rect.x + player_obj.size
          self.rect.y = player_obj.rect.y + player_obj.size
          #create variables for sword image/sprite at different directions
          self.image_up = self.image
          self.image_down = pygame.transform.flip(self.image, False, True)
          self.image_left = pygame.transform.rotate(self.image, 90)
          self.image_right = pygame.transform.flip(self.image_left, True, False)
          self.curr_image = self.image_up
     def draw(self, screen):
          screen.blit(self.curr_image, [self.rect.x, self.rect.y])
     def attack(self):
          #code to put rectangle x value at area where character is facing
          if player_obj.last_x > 0:
              self.rect.x = player_obj.rect.x + player_obj.size
              self.curr_image = self.image_right
          elif player_obj.last_x < 0:
              self.rect.x = player_obj.rect.x - self.size
              self.curr_image = self.image_left
          elif player_obj.last_x == 0:
              self.rect.x = player_obj.rect.x + (player_obj.size / 2) - (self.size / 2)

          #code to put rectangle y value at area where character is facing     
          if player_obj.last_y > 0:
              self.rect.y = player_obj.rect.y + player_obj.size
              self.curr_image = self.image_down
          elif player_obj.last_y < 0:
              self.rect.y = player_obj.rect.y - self.size
              self.curr_image = self.image_up
          elif player_obj.last_y == 0:
              self.rect.y = player_obj.rect.y + (player_obj.size / 2) - (self.size / 2)
     def attack_collision(self):
          #create list of enemies hit by player sword
          enemies_hit_list = pygame.sprite.spritecollide(self, enemies, False)
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
          #self.image = pygame.Surface([self.size, self.size])
          #self.image.fill(self.colour)
          self.image = pygame.image.load("Chest.png").convert()
          self.image.set_colorkey(BLACK)
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
enemies = pygame.sprite.Group() #create list of all enemies
enemies_island2 = pygame.sprite.Group() #create list of enemies for island 2
enemies_island = pygame.sprite.Group() #create list of enemies for island 1
enemies_dungeon = pygame.sprite.Group() #create list of enemies for dungeon
sword_draw = False #boolean for if sword should be drawn
swords = pygame.sprite.Group() #create list of swords
font = pygame.font.SysFont('Arial Black', 18, True, False) #created font for use in player messages
island_chest_open = False #boolean for if the chest on island 1 has been opened
island_2_chest_open = False #boolean for if the chest on island 2 has been opened
paused = False #boolean for if the game is paused
enemy_move_timer = 0 #timer for when enemy can calculate movement
chests = pygame.sprite.Group() #group for all chests in game

#create chest objects
island_chest = Treasure_Chest(40, island_obj.position_x_close + (island_obj.width / 2) - 20, island_obj.position_y_close + 40 - 20, "Shield of Litness")
chests.add(island_chest)
island_2_chest = Treasure_Chest(40, island2_obj.position_x_close + (island2_obj.width / 2) - 20, island2_obj.position_y_close + 40 - 20, "Sword of Awesome")
chests.add(island_2_chest)

#create all enemy objects for use on island 1
for index in range(3):
     enemy_obj = Enemy(20, ENEMY_PURPLE, 300, 150, 1, 1)
     enemies_island.add(enemy_obj)
     enemies.add(enemy_obj)
     enemy_obj.rect.x += (index * 50)
     enemy_obj.rect.y += (index * 50)
         
#create all enemy objects for use on island 2
for index in range(3):
     enemy_obj = Enemy(20, ENEMY_PURPLE, 300, 150, 1, 1)
     enemies_island2.add(enemy_obj)
     enemies.add(enemy_obj)
     enemy_obj.rect.x += (index * 50)
     enemy_obj.rect.y += (index * 50)

#main program loop setup
done = False
clock = pygame.time.Clock()

#create pause function, to be in effect while pausing
def pause():
     paused = True
     #make variables global so they can be changed
     global treasure_message_timer
     global pause_timer
     global done
     global sword_delay

     #pause loop
     while paused:
        #code for key presses
        for event in pygame.event.get():
             if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
                  paused = False
                  done = True
             if event.type == pygame.KEYDOWN:
                  if event.key == pygame.K_p:
                       paused = False
                       
        #code to make black screen with overlay message
        screen.fill(BLACK)
        text = font.render("Game paused. Press P to continue.", True, WHITE)
        screen.blit(text, [20, 10])
        
        #code to keep timers ticking over
        if sword_draw:
            sword_delay += (pygame.time.get_ticks() - pause_timer)
        player_obj.invulnerable_timer += (pygame.time.get_ticks() - pause_timer)
        for enemy_obj in enemies:
            enemy_obj.invulnerable_timer += (pygame.time.get_ticks() - pause_timer)
        if island_2_chest_open or island_chest_open:
            treasure_message_timer += (pygame.time.get_ticks() - pause_timer)
        pause_timer = pygame.time.get_ticks()

        #update screen and framerate
        pygame.display.flip()
        clock.tick(60)

#create island function, to be in effect while on first island
def island():
     #make variables global so they can be used
     global pause_timer
     global treasure_message_timer
     global done
     global island_overview
     global on_island
     global map_overview
     global island_rect
     global island_chest_open
     global off_island
     global sword_draw
     global sword_delay
     
     while island_overview:
          #code for key presses + movement
          for event in pygame.event.get(): #if the user does something
              if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE: #if the user clicks close or presses escape
                  done = True
                  island_overview = False
              if event.type == pygame.KEYDOWN: #if key is pressed, movement starts
                  if (event.key == pygame.K_UP or event.key == pygame.K_w):
                      player_obj.change_y = -5
                      player_obj.last_y = -1
                      player_obj.last_x = 0
                  if (event.key == pygame.K_DOWN or event.key == pygame.K_s):
                      player_obj.change_y = 5
                      player_obj.last_y = 1
                      player_obj.last_x = 0
                  if (event.key == pygame.K_LEFT or event.key == pygame.K_a):
                      player_obj.change_x = -5
                      player_obj.last_y = 0
                      player_obj.last_x = -1
                  if (event.key == pygame.K_RIGHT or event.key == pygame.K_d):
                      player_obj.change_x = 5
                      player_obj.last_y = 0
                      player_obj.last_x = 1
                  if event.key == pygame.K_j:
                      print(player_obj.inventory)
                  if event.key == pygame.K_p:
                      pause_timer = pygame.time.get_ticks()
                      pause()
                  if event.key == pygame.K_SPACE:
                      if (player_obj.change_x == 0 and player_obj.change_y == 0):
                           sword_draw = True
                           sword_obj.attack()
                           sword_obj.attack_collision()
                           sword_delay = pygame.time.get_ticks() #amount of milliseconds before sword sprite disappears
              if event.type == pygame.KEYUP: #if key is released, movement stops
                  if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_w or event.key == pygame.K_s:
                      player_obj.change_y = 0
                  if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                      player_obj.change_x = 0
                      
          #fill screen with background colour
          screen.fill(SEABLUE)

          #draw the island up close
          island_obj.draw_close(screen)

          #code to remove enemies from enemies_island list, draw them to screen, and have them move
          for enemy_obj in enemies_island:
              if enemy_obj.dead:
                   enemies_island.remove(enemy_obj)
              else:
                   enemy_obj.draw(screen)
              if player_obj.health > 0:
                   enemy_obj.move()

          #code to spawn chest on island
          if not enemies_island:
              island_chest.draw(screen)

          #have player move (on island)
          player_obj.move_close()
        
          #what happens when player spawns on island
          if on_island:
              player_obj.rect.y = island_obj.position_y_close + (4 * (island_obj.height / 5))
              player_obj.rect.x = island_obj.position_x_close + (island_obj.width / 2) - (player_obj.size / 2)
              player_obj.change_x = 0
              player_obj.change_y = 0
              on_island = False
              #pygame.time.delay(200)

          #make player leave if exit bottom of island
          if player_obj.rect.y + player_obj.size >= island_obj.position_y_close + island_obj.height:
               island_overview = False
               map_overview = True
               off_island = True

          #code to check collision between player and chest, output a found treasure message, and add that treasure to player inventory
          if pygame.sprite.collide_rect(player_obj, island_chest) and not island_chest_open and not enemies_island:
               island_chest.pick_treasure()
               island_chest_open = True
               treasure_message_timer = pygame.time.get_ticks()

          #code to keep treasure message on screen for set amount of time
          if island_chest_open:
               if pygame.time.get_ticks() - treasure_message_timer <= 2000:
                    player_obj.message(island_chest.text)

          #code to check if enemies are dead or not
          for enemy_obj in enemies:
              if enemy_obj.health <= 0:
                  enemy_obj.dead = True

          #display player movements to screen
          if player_obj.health > 0:
              player_obj.draw(screen)
          else:
              #display death message upon failure
              player_obj.message("You died! Press ESC to quit.")

          #code to check if player can be hit
          if pygame.time.get_ticks() - player_obj.invulnerable_timer >= 2000:
              player_obj.invulnerable = False

          #code to check if enemy can be hit
          for enemy_obj in enemies:
              if pygame.time.get_ticks() - enemy_obj.invulnerable_timer >= 1000:
                  enemy_obj.invulnerable = False

          #code to check collision between player and enemy
          enemy_damage_list = pygame.sprite.spritecollide(player_obj, enemies, False)
          for enemy_obj in enemy_damage_list:
              if (not enemy_obj.dead) and (not player_obj.invulnerable):
                  player_obj.take_damage()
                  player_obj.invulnerable = True
                  player_obj.invulnerable_timer = pygame.time.get_ticks()
    
          #draw sword to screen
          if sword_draw:
              if player_obj.change_x == 0 and player_obj.change_y == 0 and player_obj.health > 0:
                  sword_obj.draw(screen)
                  sword_obj.attack_collision()
              else:
                  sword_draw = False
              if pygame.time.get_ticks() - sword_delay >= 700:
                  sword_draw = False

          #update screen and framerate
          pygame.display.flip()
          clock.tick(60)

#create island 2 function, to be in effect while on second island
def island2():
     #make variables global so they can be used
     global pause_timer
     global treasure_message_timer
     global done
     global island2_overview
     global on_island
     global map_overview
     global island_rect
     global island_2_chest_open
     global off_island2
     global sword_draw
     global sword_delay
     
     while island2_overview:
          #code for key presses + movement
          for event in pygame.event.get(): #if the user does something
              if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE: #if the user clicks close or presses escape
                  done = True
                  island2_overview = False
              if event.type == pygame.KEYDOWN: #if key is pressed, movement starts
                  if (event.key == pygame.K_UP or event.key == pygame.K_w):
                      player_obj.change_y = -5
                      player_obj.last_y = -1
                      player_obj.last_x = 0
                  if (event.key == pygame.K_DOWN or event.key == pygame.K_s):
                      player_obj.change_y = 5
                      player_obj.last_y = 1
                      player_obj.last_x = 0
                  if (event.key == pygame.K_LEFT or event.key == pygame.K_a):
                      player_obj.change_x = -5
                      player_obj.last_y = 0
                      player_obj.last_x = -1
                  if (event.key == pygame.K_RIGHT or event.key == pygame.K_d):
                      player_obj.change_x = 5
                      player_obj.last_y = 0
                      player_obj.last_x = 1
                  if event.key == pygame.K_j:
                      print(player_obj.inventory)
                  if event.key == pygame.K_p:
                      pause_timer = pygame.time.get_ticks()
                      pause()
                  if event.key == pygame.K_SPACE:
                      if (player_obj.change_x == 0 and player_obj.change_y == 0):
                           sword_draw = True
                           sword_obj.attack()
                           sword_obj.attack_collision()
                           sword_delay = pygame.time.get_ticks() #amount of milliseconds before sword sprite disappears
              if event.type == pygame.KEYUP: #if key is released, movement stops
                  if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_w or event.key == pygame.K_s:
                      player_obj.change_y = 0
                  if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                      player_obj.change_x = 0
                      
          #fill screen with background colour
          screen.fill(SEABLUE)

          #draw the island up close
          island2_obj.draw_close(screen)

          #code to remove enemies from enemies_island list, draw them to screen, and have them move
          for enemy_obj in enemies_island2:
              if enemy_obj.dead:
                   enemies_island2.remove(enemy_obj)
              else:
                   enemy_obj.draw(screen)
              if player_obj.health > 0:
                   enemy_obj.move()

          #code to spawn chest on island
          if not enemies_island2:
              island_2_chest.draw(screen)

          #have player move (on an island)
          player_obj.move_close()
        
          #what happens when player spawns on island
          if on_island:
              player_obj.rect.y = island2_obj.position_y_close + (4 * (island2_obj.height / 5))
              player_obj.rect.x = island2_obj.position_x_close + (island2_obj.width / 2) - (player_obj.size / 2)
              player_obj.change_x = 0
              player_obj.change_y = 0
              on_island = False
              #pygame.time.delay(200)

          #make player leave if exit bottom of island
          if player_obj.rect.y + player_obj.size >= island2_obj.position_y_close + island2_obj.height:
               island2_overview = False
               map_overview = True
               off_island2 = True

          #code to check collision between player and chest, output a found treasure message, and add that treasure to player inventory
          if pygame.sprite.collide_rect(player_obj, island_2_chest) and not island_2_chest_open and not enemies_island2:
               island_2_chest.pick_treasure()
               island_2_chest_open = True
               treasure_message_timer = pygame.time.get_ticks()

          #code to keep treasure message on screen for set amount of time
          if island_2_chest_open:
               if pygame.time.get_ticks() - treasure_message_timer <= 2000:
                    player_obj.message(island_2_chest.text)

          #code to check if enemies are dead or not
          for enemy_obj in enemies:
              if enemy_obj.health <= 0:
                  enemy_obj.dead = True

          #display player movements to screen
          if player_obj.health > 0:
              player_obj.draw(screen)
          else:
              #display death message upon failure
              player_obj.message("You died! Press ESC to quit.")

          #code to check if player can be hit
          if pygame.time.get_ticks() - player_obj.invulnerable_timer >= 2000:
              player_obj.invulnerable = False

          #code to check if enemy can be hit
          for enemy_obj in enemies:
              if pygame.time.get_ticks() - enemy_obj.invulnerable_timer >= 1000:
                  enemy_obj.invulnerable = False

          #code to check collision between player and enemy
          enemy_damage_list = pygame.sprite.spritecollide(player_obj, enemies, False)
          for enemy_obj in enemy_damage_list:
              if (not enemy_obj.dead) and (not player_obj.invulnerable):
                  player_obj.take_damage()
                  player_obj.invulnerable = True
                  player_obj.invulnerable_timer = pygame.time.get_ticks()
    
          #draw sword to screen
          if sword_draw:
              if player_obj.change_x == 0 and player_obj.change_y == 0 and player_obj.health > 0:
                  sword_obj.draw(screen)
                  sword_obj.attack_collision()
              else:
                  sword_draw = False
              if pygame.time.get_ticks() - sword_delay >= 700:
                  sword_draw = False

          #update screen and framerate
          pygame.display.flip()
          clock.tick(60)

#create map function, to be used while on world map
def world_map():
     #make variables global so they can be used
     global map_overview
     global island_overview
     global island2_overview
     global on_island
     global off_island
     global off_island2
     global island_rect
     
     #map loop
     while map_overview:
          #code for key presses and movement
          for event in pygame.event.get(): #if the user does something
              if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE: #if the user clicks close or presses escape
                  done = True
                  map_overview = False
              if event.type == pygame.KEYDOWN: #if key is pressed, movement starts
                  if (event.key == pygame.K_UP or event.key == pygame.K_w):
                      player_obj.change_y = -5
                      player_obj.last_y = -1
                      player_obj.last_x = 0
                  if (event.key == pygame.K_DOWN or event.key == pygame.K_s):
                      player_obj.change_y = 5
                      player_obj.last_y = 1
                      player_obj.last_x = 0
                  if (event.key == pygame.K_LEFT or event.key == pygame.K_a):
                      player_obj.change_x = -5
                      player_obj.last_y = 0
                      player_obj.last_x = -1
                  if (event.key == pygame.K_RIGHT or event.key == pygame.K_d):
                      player_obj.change_x = 5
                      player_obj.last_y = 0
                      player_obj.last_x = 1
                  if event.key == pygame.K_j:
                      print(player_obj.inventory)
                  if event.key == pygame.K_p:
                      pause_timer = pygame.time.get_ticks()
                      pause()
              if event.type == pygame.KEYUP: #if key is released, movement stops
                  if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_w or event.key == pygame.K_s:
                      player_obj.change_y = 0
                  if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                      player_obj.change_x = 0
                    
          #fill screen with background colour
          screen.fill(SEABLUE)

          #draw all islands on map
          island_obj.draw_map(screen)
          island2_obj.draw_map(screen)

          #have player move (map overview) and draw it to screen
          player_obj.move_map()
          player_obj.draw(screen)
         
          #what happens when player leaves first island
          if off_island:
              player_obj.rect.y = island_obj.rect.y + island_obj.height_map + 5
              player_obj.rect.x = island_obj.rect.x + (island_obj.width_map / 2) - (player_obj.size / 2)
              player_obj.change_x = 0
              player_obj.change_y = 0
              off_island = False
              #pygame.time.delay(200)

          #what happens when player leaves second island
          if off_island2:
              player_obj.rect.y = island2_obj.rect.y + island2_obj.height_map + 5
              player_obj.rect.x = island2_obj.rect.x + (island2_obj.width_map / 2) - (player_obj.size / 2)
              player_obj.change_x = 0
              player_obj.change_y = 0
              off_island2 = False
              #pygame.time.delay(200)

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

          #display output and framerate
          pygame.display.flip() #updates screen with what's drawn
          clock.tick(60) #limits to 60 frames per second

#main program loop
while not done:
    for event in pygame.event.get(): #if the user does something
        if event.type == (pygame.QUIT or pygame.K_ESCAPE): #if the user clicks close or presses escape
            done = True
        if event.type == pygame.KEYDOWN: #if key is pressed, movement starts
            if (event.key == pygame.K_UP or event.key == pygame.K_w):
                player_obj.change_y = -5
                player_obj.last_y = -1
                player_obj.last_x = 0
            if (event.key == pygame.K_DOWN or event.key == pygame.K_s):
                player_obj.change_y = 5
                player_obj.last_y = 1
                player_obj.last_x = 0
            if (event.key == pygame.K_LEFT or event.key == pygame.K_a):
                player_obj.change_x = -5
                player_obj.last_y = 0
                player_obj.last_x = -1
            if (event.key == pygame.K_RIGHT or event.key == pygame.K_d):
                player_obj.change_x = 5
                player_obj.last_y = 0
                player_obj.last_x = 1
            if event.key == pygame.K_j:
                print(player_obj.inventory)
            if event.key == pygame.K_p:
                pause_timer = pygame.time.get_ticks()
                pause()
            if event.key == pygame.K_SPACE:
                if (player_obj.change_x == 0 and player_obj.change_y == 0):
                     sword_draw = True
                     sword_obj.attack()
                     sword_obj.attack_collision()
                     sword_delay = pygame.time.get_ticks() #amount of milliseconds before sword sprite disappears
        if event.type == pygame.KEYUP: #if key is released, movement stops
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_w or event.key == pygame.K_s:
                player_obj.change_y = 0
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                player_obj.change_x = 0

    #functions for different areas                            
    if map_overview:
        world_map()

    if island_overview:
        island()

    if island2_overview:
        island2()


    
    #display output and framerate
    pygame.display.flip() #updates screen with what's drawn
    clock.tick(60) #limits to 60 frames per second

#closes window, exits game
pygame.quit()
