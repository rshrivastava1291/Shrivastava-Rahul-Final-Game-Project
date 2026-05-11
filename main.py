import pygame
import sys
from player import Player
from bullet import Bullet
from zombie import Zombie

pygame.init()

WIDTH = 800
HEIGHT = 600
DIRT = (155, 118, 83)
GRAY = (100, 100, 100)
BLACK = (0, 0, 0)
RED = (200, 50, 50)
GREEN = (50, 200, 50)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie Survival")

clock = pygame.time.Clock()
font_large = pygame.font.SysFont(None, 72)
font_medium = pygame.font.SysFont(None, 48)
font_small = pygame.font.SysFont(None, 36)

def reset_game():
    player = Player(WIDTH // 2, HEIGHT // 2, WIDTH, HEIGHT)
    bullets = []
    zombies = []
    return player, bullets, zombies

def draw_start_screen():
    screen.fill(GRAY)
    title = font_large.render("Zombie Survival", True, RED)
    prompt = font_medium.render("Press any key to start", True, BLACK)
    screen.blit(title, title.get_rect(center = (WIDTH // 2, HEIGHT // 2 - 50)))
    screen.blit(prompt, prompt.get_rect(center = (WIDTH // 2, HEIGHT // 2 + 30)))
    pygame.display.flip()

def draw_game_over_screen(wave):
    screen.fill(GRAY)
    title = font_large.render("Game Over", True, RED)
    prompt = font_medium.render(f"You reached wave {wave}", True, BLACK)
    restart = font_small.render("Press R to restart", True, BLACK)
    screen.blit(title, title.get_rect(center = (WIDTH // 2, HEIGHT // 2 - 80)))
    screen.blit(prompt, prompt.get_rect(center = (WIDTH // 2, HEIGHT // 2)))
    screen.blit(restart, restart.get_rect(center = (WIDTH // 2, HEIGHT // 2 + 70)))
    pygame.display.flip()

def draw_health_bar(screen, health, max_health):
    bar_width = 200
    bar_height = 20
    x = WIDTH // 2 - bar_width // 2
    y = 10
    
    pygame.draw.rect(screen, RED, (x, y, bar_width, bar_height))
    fill_width = int((health / max_health) * bar_width)
    pygame.draw.rect(screen, GREEN, (x, y, fill_width, bar_height))
    pygame.draw.rect(screen, BLACK, (x, y, bar_width, bar_height), 2)

def draw_wave_transition(wave):
    screen.fill(GRAY)
    wave_incoming = font_large.render(f"Wave {wave}", True, RED)
    incoming_text = font_medium.render("Incoming!", True, BLACK)
    screen.blit(wave_incoming, wave_incoming.get_rect(center = (WIDTH // 2, HEIGHT // 2 - 50)))
    screen.blit(incoming_text, incoming_text.get_rect(center = (WIDTH // 2, HEIGHT // 2 + 30)))
    pygame.display.flip()

START = "start"
PLAYING = "playing"
GAME_OVER = "game_over"
WAVE_TRANSITION = "wave_transition"
state = START

player, bullets, zombies = reset_game()

transition_timer = 0

zombie_spawn_timer = 0
player_health = 10

wave = 1
zombies_per_wave = 8
zombies_spawned = 0
zombies_killed = 0
zombie_spawn_rate = 90
wave_complete = False

running = True

while running:
    clock.tick(60)

    if state == START:
        draw_start_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                state = PLAYING

    elif state == GAME_OVER:
        draw_game_over_screen(wave)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    player, bullets, zombies = reset_game()
                    zombie_spawn_timer = 0
                    player_health = 10
                    wave = 1
                    zombies_per_wave = 8
                    zombies_spawned = 0
                    zombies_killed = 0
                    zombies_spawn_rate = 90
                    transition_timer = 0
                    state = PLAYING

    elif state == WAVE_TRANSITION:
        draw_wave_transition(wave + 1)
        transition_timer += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if transition_timer >= 180:
            wave += 1
            zombies_per_wave += 3
            zombie_spawn_rate = max(30, zombie_spawn_rate - 5)
            zombies_spawned = 0
            zombies_killed = 0
            state = PLAYING

    elif state == PLAYING:

        screen.fill(DIRT)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        player.angle_of_player(mouse_x, mouse_y)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    bullets.append(Bullet(player.x, player.y, player.angle))

        player.update()

        if zombies_spawned < zombies_per_wave:
            zombie_spawn_timer += 1
            if zombie_spawn_timer >= zombie_spawn_rate:
                zombies.append(Zombie(WIDTH, HEIGHT, wave))
                zombies_spawned += 1
                zombie_spawn_timer = 0

        if zombies_spawned >= zombies_per_wave and len(zombies) == 0:
            state = WAVE_TRANSITION
            transition_timer = 0

        for zombie in zombies:
            zombie.go_toward_player(player.x, player.y)
            if zombie.touching_player(player):
                player_health -= 1
                zombies.remove(zombie)
                if player_health <= 0:
                    state = GAME_OVER

        bullets_to_remove = []
        zombies_to_remove = []

        for bullet in bullets:
            for zombie in zombies:
                if zombie.hit_by_bullet(bullet):
                    zombie.health -= 1
                    bullets_to_remove.append(bullet)
                    if zombie.health <= 0:
                        zombies_to_remove.append(zombie)
                        zombies_killed += 1

        bullets = [b for b in bullets if b not in bullets_to_remove and not b.if_off_screen(WIDTH, HEIGHT)]
        zombies = [z for z in zombies if z not in zombies_to_remove]

        for bullet in bullets:
            bullet.movement()
            bullet.draw_on_screen(screen)

        for zombie in zombies:
            zombie.draw_on_screen(screen)

        player.draw_on_screen(screen)

        wave_text = font_small.render(f"Wave: {wave}", True, BLACK)
        zombies_left_text = font_small.render(f"Zombies: {zombies_killed}/{zombies_per_wave}", True, BLACK)
        draw_health_bar(screen, player_health, 10)
        screen.blit(wave_text, (10, 10))
        screen.blit(zombies_left_text, (WIDTH - 180, 10))

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
