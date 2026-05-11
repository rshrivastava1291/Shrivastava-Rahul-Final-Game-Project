import pygame
import math

class Player:
    def __init__(self, x, y, screen_width, screen_height):
        self.radius = 20
        self.size = 40
        self.x = x
        self.y = y
        self.speed = 5
        self.color = (255, 203, 131)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.angle = 0
    
    def player_movement(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.y += self.speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.x += self.speed

    def angle_of_player(self, mouse_x, mouse_y):
        dx = mouse_x - self.x
        dy = mouse_y - self.y
        self.angle = math.atan2(dy, dx)

    def stay_on_screen(self):
        self.x = max(self.radius, min(self.screen_width - self.radius, self.x))
        self.y = max(self.radius, min(self.screen_height - self.radius, self.y))

    def update(self):
        self.player_movement()
        self.stay_on_screen()

    def draw_on_screen(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        end_x = self.x + math.cos(self.angle) * (self.radius + 8)
        end_y = self.y + math.sin(self.angle) * (self.radius + 8)
        pygame.draw.line(screen, (180, 100, 50), (self.x, self.y), (int(end_x), int(end_y)), 4)