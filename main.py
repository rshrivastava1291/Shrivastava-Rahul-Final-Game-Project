import pygame
import sys
from player import Player
from bullet import Bullet

pygame.init()

WIDTH = 800
HEIGHT = 600
WHITE = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie Survival")

clock = pygame.time.Clock()

player = Player(WIDTH // 2, HEIGHT // 2, WIDTH, HEIGHT)

bullets = []

running = True

while running:
    clock.tick(60)
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                bullet_x = player.x + player.size // 2
                bullet_y = player.y
                bullets.append(Bullet(bullet_x, bullet_y))

    player.update()

    bullets = [b for b in bullets if not b.stay_on_screen()]

    player.draw_on_screen(screen)

    for bullet in bullets:
        bullet.draw_on_screen(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()

#core variables:
# player_x, player_y
# player_speed

# bullets = []   # store active bullets
# # zombies = []   # store active zombies

# wave = 1
# spawn_rate = initial value
# game_state = "start"  # "start", "game", "game_over"


#Player movement logic
# if key pressed:
#   update player_x / player_y
# make sure player stays inside screen bounds


#Bullet logic
# when player presses shoot:
#   create new bullet object
#   append to bullets list

#each frame:
#   update bullet position
#   remove bullet if off screen


#Zombie spawning
# spawn zombies at random positions along screen edges

# each zombie:
#   move toward player position using direction vector


#Collision logic
# for each bullet:
#   check distance to each zombie
#   if collision:
#       remove zombie
#       remove bullet

# for each zombie:
#   check distance to player
#   if collision:
#       set game_state = "game_over"


#Wave system
# track time or number of zombies killed

# every X seconds or after clearing zombies:
#   increase wave number
#   increase spawn rate


#Main game loop structure
# while running:
#   handle input
#   update player
#   update bullets
#   update zombies
#   check collisions
#   render everything


#Rendering
# draw player
# draw bullets
# draw zombies
# display wave number
# display start screen with start option and game title
