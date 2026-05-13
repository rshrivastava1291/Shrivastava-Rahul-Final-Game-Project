#Rahul Shrivastava
#Period 2
#Zombie Survival


#IMPORTS
import pygame
import sys
import random
from player import Player
from bullet import Bullet
from zombie import Zombie

#will initialize all of the modules for pygame
pygame.init()

#SCREEN CONSTANTS
WIDTH = 800
HEIGHT = 600

#COLOR CONSTANTS
DIRT = (155, 118, 83)
GRAY = (100, 100, 100)
BLACK = (0, 0, 0)
RED = (200, 50, 50)
GREEN = (50, 200, 50)

#Will create the window for the game and set the caption for the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie Survival")

#control the frame rate
clock = pygame.time.Clock()

#font variables for different font sizes
font_large = pygame.font.SysFont(None, 72)
font_medium = pygame.font.SysFont(None, 48)
font_small = pygame.font.SysFont(None, 36)

#function to reset the game. will reset game to state it was in when it started.
def reset_game():
    player = Player(WIDTH // 2, HEIGHT // 2, WIDTH, HEIGHT)
    bullets = []   #remove all bullets from list
    zombies = []   #remove all zombies from list
    return player, bullets, zombies

#function to draw the start screen. will include the game name and "press any key to start" text
def draw_start_screen():
    screen.fill(GRAY)
    title = font_large.render("Zombie Survival", True, RED)
    prompt = font_medium.render("Press any key to start", True, BLACK)
    screen.blit(title, title.get_rect(center = (WIDTH // 2, HEIGHT // 2 - 50)))
    screen.blit(prompt, prompt.get_rect(center = (WIDTH // 2, HEIGHT // 2 + 30)))
    pygame.display.flip()

#function to draw the game over screen. will return the wave that the player reached
def draw_game_over_screen(wave):
    screen.fill(GRAY)
    title = font_large.render("Game Over", True, RED)
    prompt = font_medium.render(f"You reached wave {wave}", True, BLACK)
    restart = font_small.render("Press R to restart", True, BLACK)
    screen.blit(title, title.get_rect(center = (WIDTH // 2, HEIGHT // 2 - 80)))
    screen.blit(prompt, prompt.get_rect(center = (WIDTH // 2, HEIGHT // 2)))
    screen.blit(restart, restart.get_rect(center = (WIDTH // 2, HEIGHT // 2 + 70)))
    pygame.display.flip()

#function to draw the health bar. sets size and location for it
def draw_health_bar(screen, health, max_health):
    bar_width = 200
    bar_height = 20
    x = WIDTH // 2 - bar_width // 2
    y = 10
    
    #will color it and actually draw the rectangle
    pygame.draw.rect(screen, RED, (x, y, bar_width, bar_height))
    fill_width = int((health / max_health) * bar_width)
    pygame.draw.rect(screen, GREEN, (x, y, fill_width, bar_height))
    pygame.draw.rect(screen, BLACK, (x, y, bar_width, bar_height), 2)

#screen to signal a new wave
def draw_wave_transition(wave):
    screen.fill(GRAY)
    wave_incoming = font_large.render(f"Wave {wave}", True, RED)
    incoming_text = font_medium.render("Incoming!", True, BLACK)
    screen.blit(wave_incoming, wave_incoming.get_rect(center = (WIDTH // 2, HEIGHT // 2 - 50)))
    screen.blit(incoming_text, incoming_text.get_rect(center = (WIDTH // 2, HEIGHT // 2 + 30)))
    pygame.display.flip()

def shake_offset():
    if shake_timer > 0:
        return (random.randint(-shake_intensity, shake_intensity), random.randint(-shake_intensity, shake_intensity))
    return (0, 0)

#different states to switch between for different screens
START = "start" #start screen
PLAYING = "playing" #screen while playing
GAME_OVER = "game_over" #game over screen
WAVE_TRANSITION = "wave_transition" #screen during wave transition
state = START #sets the state when game is started to start screen

#will reset all aspects of game at the start
player, bullets, zombies = reset_game()

#will count the amount of frames as the wave transitions
transition_timer = 0

zombie_spawn_timer = 0  #counts the amount of frames between each zombie spawn
player_health = 10 #sets amount of health player starts with

#all variables to track the wave and difficulty
wave = 1
zombies_per_wave = 8
zombies_spawned = 0
zombies_killed = 0
zombie_spawn_rate = 90
wave_complete = False #start at not complete since game just started

shake_timer = 0
shake_intensity = 8

#still set the game as running to enter loop
running = True

#loop for whole game
while running:
    #60 frames per second
    clock.tick(60)

    #start screen for game
    if state == START:
        draw_start_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            #will start the game if any key is pressed
            if event.type == pygame.KEYDOWN:
                state = PLAYING

    #game over screen for game
    elif state == GAME_OVER:
        draw_game_over_screen(wave)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            #will restart the game and reset the player health and wave mechanics if 'r' is pressed
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
                    state = PLAYING   #will set the game to "playing" state to play game

    #screen for when player is transitioning to next wave
    elif state == WAVE_TRANSITION:
        draw_wave_transition(wave + 1)  #show wave player is now on
        transition_timer += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        #will start next wave after 3 seconds (180/60)
        if transition_timer >= 180:
            # will increase difficulty and reset zombies spawned and killed during wave
            wave += 1
            zombies_per_wave += 3
            zombie_spawn_rate = max(30, zombie_spawn_rate - 5)
            zombies_spawned = 0
            zombies_killed = 0
            state = PLAYING

    #screen when player is playing the game
    elif state == PLAYING:

        screen.fill(BLACK)
        offset_x, offset_y = shake_offset()
        dirt_floor = pygame.Surface((WIDTH, HEIGHT))
        dirt_floor.fill(DIRT)
        screen.blit(dirt_floor, (offset_x, offset_y))

        #will track where cursor is and will change angle of player to follow cursor
        mouse_x, mouse_y = pygame.mouse.get_pos()
        player.angle_of_player(mouse_x, mouse_y)

        if shake_timer > 0:
            shake_timer -= 1

        #will handle events from player
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            #will shoot a bullet when player clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    bullets.append(Bullet(player.x, player.y, player.angle))

        #will handle the movement and ensure player doesnt go outside of map
        player.update()

        #will spawn a zombie at 1 second intervals until the wave is complete
        if zombies_spawned < zombies_per_wave:
            zombie_spawn_timer += 1 #wait a second to spawn a zombie if more are left during wave
            if zombie_spawn_timer >= zombie_spawn_rate:
                #append zombis to list and increase amount of zombies spawned if one was spawned
                zombies.append(Zombie(WIDTH, HEIGHT, wave))
                zombies_spawned += 1
                zombie_spawn_timer = 0

        #will set the game to the wave transition screen if all zombies are killed
        if zombies_spawned >= zombies_per_wave and len(zombies) == 0:
            state = WAVE_TRANSITION
            transition_timer = 0

        #zombies will go towards player and reduce 1 health if they hit the player
        for zombie in zombies:
            zombie.go_toward_player(player.x, player.y)
            if zombie.touching_player(player):
                #will decrease health by 1 and remove zombie from list
                player_health -= 1

                player.hit_timer = 10

                shake_timer = 20

                zombies.remove(zombie)
                #will set the game to the game over screen if player loses all of their health
                if player_health <= 0:
                    state = GAME_OVER

        #will track the bullets and zombies that need to be removed during each frame
        bullets_to_remove = []
        zombies_to_remove = []

        #check if each bullet hits a zombie
        for bullet in bullets:
            for zombie in zombies:
                #decrease zombies health
                if zombie.hit_by_bullet(bullet):
                    zombie.health -= 1
                    zombie.hit_timer = 6
                    #deletes bullet from screen when it hits
                    bullets_to_remove.append(bullet)
                    #remove zombie from screen when its health reaches 0
                    if zombie.health <= 0:
                        zombies_to_remove.append(zombie)
                        zombies_killed += 1

        #for each bullet in list, if the bullet didnt hit a zombie and hasn't gone past the edge of the screen, keep it in the list
        bullets = [b for b in bullets if b not in bullets_to_remove and not b.if_off_screen(WIDTH, HEIGHT)]

        #for each zombie in list, keep it if it doesn't need to be removed
        zombies = [z for z in zombies if z not in zombies_to_remove]

        #update and draw all the bullets being shot
        for bullet in bullets:
            bullet.movement()
            bullet.draw_on_screen(screen)

        #update and draw all the zombies being spawned
        for zombie in zombies:
            zombie.draw_on_screen(screen)
            zombie.zombie_health_bar(screen)

        #draw player in the middle of the screen
        player.draw_on_screen(screen)

        #all UI/text on the top of the screen to show stats for current wave
        wave_text = font_small.render(f"Wave: {wave}", True, BLACK)
        zombies_left_text = font_small.render(f"Zombies: {zombies_killed}/{zombies_per_wave}", True, BLACK)
        draw_health_bar(screen, player_health, 10)
        screen.blit(wave_text, (10, 10))
        screen.blit(zombies_left_text, (WIDTH - 180, 10))

        #will push each finished frame onto the game window
        pygame.display.flip()

#will exit the game
pygame.quit()
sys.exit()