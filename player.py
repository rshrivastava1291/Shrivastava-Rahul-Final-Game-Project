import pygame

class Player:
    def __init__(self, x, y, width, height):
        self.size = 40
        self.x = x
        self.y = y
        self.speed = 5
        self.color = (255, 203, 131)
        self.width = width
        self.height = height
    
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

    def stay_on_screen(self):
        self.x = max(0, min(self.width - self.size, self.x))
        self.y = max(0, min(self.height - self.size, self.y))

    def update(self):
        self.player_movement()
        self.stay_on_screen()

    def draw_on_screen(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))