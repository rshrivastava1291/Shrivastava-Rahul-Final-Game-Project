import pygame
import math

class Bullet:
    def __init__(self, x, y, angle):
        self.radius = 8
        self.x = x
        self.y = y
        self.speed = 10
        self.color = (255, 50, 50)
        self.dx = math.cos(angle) * self.speed
        self.dy = math.sin(angle) * self.speed

    def movement(self):
        self.y += self.dy
        self.x += self.dx

    def draw_on_screen(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def if_off_screen(self, width, height):
        return self.x < 0 or self.x > width or self.y < 0 or self.y > height