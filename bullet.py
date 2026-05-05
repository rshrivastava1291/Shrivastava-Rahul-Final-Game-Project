import pygame

print("E")
class Bullet:
    def __init__(self, x, y):
        self.width = 6
        self.height = 12
        self.x = x
        self.y = y
        self.speed = 10
        self.color = (255, 50, 50)

    def movement(self):
        self.y -= self.speed

    def draw_on_screen(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def stay_on_screen(self):
        return self.y < 0