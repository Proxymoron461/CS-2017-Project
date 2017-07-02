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
SEABLUE = (0, 191, 255)
GRASSGREEN = (0, 204, 0) #colour for green grassy islands
SAND = (204, 204, 0) #colour for beach islands
ROCK = (128, 128, 128) #colour for rock islands
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
         self.image = pygame.Surface([self.size, self.size])
         self.image.fill(self.colour)
         self.rect = self.image.get_rect()
         self.rect.x = start_x #player x position
         self.rect.y = start_y #player y position
     def move_map(self):
         self.rect.x += self.change_x
         self.rect.y += self.change_y
     def move_close(self):
         self.rect.clamp_ip(island_obj.boundary_rect)
         self.rect.x += self.change_x
         self.rect.y += self.change_y
     def draw(self, screen):
         pygame.draw.rect(screen, self.colour, self.rect)

#initialise player object
player_obj = Player(250, 250, 20)

#initialise island class
class Island(pygame.sprite.Sprite):
     def __init__(self, height, width, position_x, position_y):
          super().__init__()
          self.height = height
          self.width = width
          self.width_map = width / 5
          self.height_map = height / 5
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
     def draw_close(self, screen): #drawing code for when player is on island
          pygame.draw.rect(screen, self.colour, self.rect_close)
     def draw_map(self, screen):
          pygame.draw.rect(screen, self.colour, self.rect)

#initialise island object
island_obj = Island(300, 300, 400, 100)

#initialise enemy class, intended as parent class for future enemies
class Enemy(pygame.sprite.Sprite):
     def __init__(self, size, colour,start_x, start_y):
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
     def move(self):
          self.rect.x += self.change_x
          self.rect.y += self.change_y
     def draw(self, screen):
          pygame.draw.rect(screen, self.colour, self.rect)

#miscellaneous values
map_overview = True #boolean for when player is in map
island_overview = False #boolean for when player is on island
dungeon_overview = False #boolean for when player is in dungeon
on_island = False #boolean for when player gets onto island
off_island = False #boolean for when player gets off island
islands = pygame.sprite.Group() #initialise list of islands
islands.add(island_obj) #add island object to list of islands

#main program loop setup
done = False
clock = pygame.time.Clock()

#main program loop
while not done:
    for event in pygame.event.get(): #if the user does something
        if event.type == pygame.QUIT: #if the user clicks close
            done = True
        if event.type == pygame.KEYDOWN: #if key is pressed, movement starts
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                player_obj.change_y = -5
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                player_obj.change_y = 5
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player_obj.change_x = -5
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player_obj.change_x = 5
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
    if dungeon_overview:
         screen.fill(ROCK)

    #screen drawing code, like shapes and text, goes here
    #x and y start from TOP LEFT

    #while on map screen
    if map_overview:
         #have player move (map overview) and draw it to screen
         player_obj.move_map()
         
         island_obj.draw_map(screen)
         #what happens when player leaves island
         if off_island:
              player_obj.rect.y = island_obj.rect.y + island_obj.height_map + 5
              player_obj.rect.x = island_obj.rect.x + (island_obj.width_map / 2) - (player_obj.size / 2)
              island_boundary_north = False
              island_boundary_west = False
              island_boundary_east = False
              player_obj.change_x = 0
              player_obj.change_y = 0
              off_island = False
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

         #collision code for if player lands on island in map overview
         if pygame.sprite.spritecollide(player_obj, islands, False):
              map_overview = False
              island_overview = True
              on_island = True

    #while on island screen
    if island_overview:
        #have player move (island overview) within island boundaries
        player_obj.move_close()
        
        island_obj.draw_close(screen)
        #what happens when player spawns on island
        if on_island:
            player_obj.rect.y = island_obj.position_y_close + (4 * (island_obj.height / 5))
            player_obj.rect.x = island_obj.position_x_close + (island_obj.width / 2) - (player_obj.size / 2)
            island_boundary_north = True
            island_boundary_west = True
            island_boundary_east = True
            player_obj.change_x = 0
            player_obj.change_y = 0
            on_island = False
            pygame.time.delay(200)

        #make player leave if exit bottom of island
        if player_obj.rect.y + player_obj.size >= island_obj.position_y_close + island_obj.height:
             island_overview = False
             map_overview = True
             off_island = True

    #display player movements to screen
    player_obj.draw(screen)
    
    #display output and framerate
    pygame.display.flip() #updates screen with what's drawn
    if island_overview:
         pygame.display.update(island_obj.rect)
    clock.tick(60) #limits to 60 frames per second

#closes window, exits game
pygame.quit()
