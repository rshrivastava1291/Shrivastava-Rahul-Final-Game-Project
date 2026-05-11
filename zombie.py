import pygame
import math
import random

class Zombie:
    def __init__(self, screen_width, screen_height, wave):
        self.radius = 20
        self.speed = 2 + (wave * 0.2)
        self.health = 3 + (wave // 3)
        self.color = (50, 200, 50)

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

    def go_toward_player(self, player_x, player_y):
        dx = player_x - self.x
        dy = player_y - self.y
        distance = math.hypot(dx, dy)
        if distance != 0:
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed

    def hit_by_bullet(self, bullet):
        distance = math.hypot(bullet.x - self.x, bullet.y - self.y)
        return distance < self.radius + 8
    
    def touching_player(self, player):
        distance = math.hypot(player.x - self.x, player.y - self.y)
        return distance < self.radius + player.radius
    
    def draw_on_screen(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
