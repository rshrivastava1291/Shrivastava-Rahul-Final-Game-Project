import pygame
import math
#import random so that zombies can spawn from all directions
import random

class Zombie:
    def __init__(self, screen_width, screen_height, wave):
        #set size and difficulty of zombie according to wave
        self.radius = 24
        self.speed = 2 + (wave * 0.2)
        self.health = 3 + (wave // 3)
        self.color = (50, 200, 50)  #green color

        self.wave = wave

        self.hit_timer = 0

        self.original_image = pygame.image.load("Zombie_Sprite.png").convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (86, 86))
        self.image = self.original_image

        self.angle = 0

        #pick a random edge of the game window and randomize the x/y location according to the side picked
        edge = random.choice(["top", "bottom", "left", "right"])
        if edge == "top":
            self.x = random.randint(0, screen_width)
            self.y = 0
        elif edge == "bottom":
            self.x = random.randint(0, screen_width)
            self.y = screen_height
        elif edge == "left":
            self.x = 0
            self.y = random.randint(0, screen_height)
        elif edge == "right":
            self.x = screen_width
            self.y = random.randint(0, screen_height)

    #will move the zombie toward the players direction each frame
    def go_toward_player(self, player_x, player_y):
        #will set a vector pointing the zombie at the player each frame
        dx = player_x - self.x
        dy = player_y - self.y
        #use hypot for the pythagorean theorem to find the actual distance
        distance = math.hypot(dx, dy)
        #will divide the dx and dy by distance, which will leave zombie only with direction
        #shrinks the vector down to 1
        #multiply by self.speed to set the movement speed
        #for example:
        #(300/360) * 2 = 1.67 pixels right
        #(200/360) * 2 = 1.11 pixels down
        #wont move the zombie for the rare case that it spawns right on top of the player
        if distance != 0:
            self.angle = math.atan2(dy, dx)
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed

    #will return true if the center of the bullet overlaps the zombie's radius
    def hit_by_bullet(self, bullet):
        distance = math.hypot(bullet.x - self.x, bullet.y - self.y)
        return distance < self.radius + 8
    
    #will return true if the zombie is overlapping the player
    def touching_player(self, player):
        distance = math.hypot(player.x - self.x, player.y - self.y)
        return distance < self.radius + player.radius
    
    def zombie_health_bar(self, screen):
        bar_width = 40
        bar_height = 5
        x = int(self.x) - bar_width // 2
        y = int(self.y) - self.radius - 10
        max_health = 3 + (self.wave // 3)
        fill_width = int((self.health / max_health) * bar_width)
        pygame.draw.rect(screen, (200, 50, 50), (x, y, bar_width, bar_height))
        pygame.draw.rect(screen, (50, 200, 50), (x, y, fill_width, bar_height))
        pygame.draw.rect(screen, (0, 0, 0), (x, y, bar_width, bar_height), 1)
    
    #will draw the zombie on the screen as a green circle
    def draw_on_screen(self, screen):
        angle_degrees = -math.degrees(self.angle)
        self.image = pygame.transform.rotate(self.original_image, angle_degrees)

        if self.hit_timer > 0:
            red_surface = self.image.copy()
            red_surface.fill((255, 0, 0, 100), special_flags=pygame.BLEND_RGBA_MULT)
            self.image.blit(red_surface, (0, 0))
            self.hit_timer -= 1
        rect = self.image.get_rect(center = (int(self.x), int(self.y)))
        screen.blit(self.image, rect)