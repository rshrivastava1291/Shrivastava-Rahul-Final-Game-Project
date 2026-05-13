import pygame
import math

class Player:
    def __init__(self, x, y, screen_width, screen_height):
        #radius for player (size)
        self.radius = 24

        #position of player on screen (x and y position)
        self.x = x
        self.y = y

        #speed player moves at
        self.speed = 5

        #used to ensure player doesnt go off screen
        self.screen_width = screen_width
        self.screen_height = screen_height

        #will set the starting angle for player in radians
        self.angle = 0

        self.hit_timer = 0

        self.original_image = pygame.image.load("Player_Sprite.png").convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (96, 96))
        self.image = self.original_image
    
    def player_movement(self):

        #will see if any key is pressed and will move the player according to either WASD or arrow keys
        keys = pygame.key.get_pressed()

        #up
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.y -= self.speed
        #down
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.y += self.speed
        #left
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.x -= self.speed
        #right
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.x += self.speed

    #will calculate the angle of the player depending on where cursor is in radians
    def angle_of_player(self, mouse_x, mouse_y):
        dx = mouse_x - self.x
        dy = mouse_y - self.y
        #atan2 is to handle all of the quadrants
        self.angle = math.atan2(dy, dx)

    #will not allow player to go off of the game window
    def stay_on_screen(self):
        self.x = max(self.radius, min(self.screen_width - self.radius, self.x))
        self.y = max(self.radius, min(self.screen_height - self.radius, self.y))

    #update players movement and see if their off the screen for each frame
    def update(self):
        self.player_movement()
        self.stay_on_screen()

    #draw the player as a circle and a line in the middle to indicate the direction which the player is facing
    def draw_on_screen(self, screen):
        angle_degrees = -math.degrees(self.angle)
        self.image = pygame.transform.rotate(self.original_image, angle_degrees)

        if self.hit_timer > 0:
            white_surface = self.image.copy()
            white_surface.fill((255, 255, 255, 100), special_flags = pygame.BLEND_RGBA_MULT)
            self.image.blit(white_surface, (0,0))
            self.hit_timer -= 1
        
        rect = self.image.get_rect(center = (self.x, self.y))
        screen.blit(self.image, rect)