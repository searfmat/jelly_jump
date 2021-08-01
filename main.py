import pygame
import sys
import random

def draw_ground():
    screen.blit(ground, (ground_x, 450))
    screen.blit(ground, (ground_x + 512 ,450))

def draw_bg():
    screen.blit(background, (bg_x, 0))
    screen.blit(background, (bg_x + 512, 0))

def create_obs():
    random_obs_pos = random.choice(obs_hgt)
    bottom_obs = obs.get_rect(midtop = (513,random_obs_pos))
    top_obs = obs.get_rect(midbottom = (513,random_obs_pos - 150))
    return bottom_obs, top_obs

def move_obs(obsList):
    for obs1 in obsList:
        obs1.centerx -= 2.5
    return obsList

def draw_obs(obsList):
    for obs1 in obsList:
        if obs1.bottom >= 512:
            screen.blit(obs, obs1)
        else:
            flip_obs = pygame.transform.flip(obs, False, True)
            screen.blit(flip_obs, obs1)

def check_collision(obsList):
    for obs1 in obsList:
        if slime_box.colliderect(obs1):
            failed.play()
            return False
    if slime_box.top <= -100 or slime_box.bottom >= 450:
        failed.play()
        return False
    return True

def check_score():
    if obs_list:
        for obs1 in obs_list:
            if 98 <= obs1.centerx <=100:
                cleared.play()
                return 1
    return 0

def score_display(point):
    score = game_font.render(str(point), False, (255,255,255))
    score_box = score.get_rect(center = (256, 40))
    screen.blit(score, score_box)

def title_display():
    title = title_font.render("Jelly Jump", False, (255,255,255))
    title_box = title.get_rect(center = (285, 256))
    screen.blit(title, title_box)

pygame.init()

# Establish canvas (W/H) - display surface
screen = pygame.display.set_mode((512,512))
clock = pygame.time.Clock()

# Music
music = pygame.mixer.Sound('sounds/soundtrack.wav')
cleared = pygame.mixer.Sound('sounds/pass.wav')
failed = pygame.mixer.Sound('sounds/fail.wav')

music.set_volume(.3)
music.play(-1)

# Font
game_font = pygame.font.Font('PressStart2P-Regular.ttf',20)
title_font = pygame.font.Font('PressStart2P-Regular.ttf',32)

# Tiles
background = pygame.image.load('assets/bgr.png').convert()
background = pygame.transform.scale(background, (512, 512))

ground = pygame.image.load('assets/ground.png').convert()
ground = pygame.transform.scale(ground, (512, 100))

ground_x = 0
bg_x = 0

slime = pygame.image.load('assets/slime1.png').convert_alpha()
slime = pygame.transform.flip(slime, True, False)
slime = pygame.transform.scale(slime, (40 , 40))
slime_box = slime.get_rect(center = (75, 256))

obs = pygame.image.load('assets/obs.png').convert_alpha()
obs_list = []
SPAWNOBS = pygame.USEREVENT
obs_hgt = [400, 350 , 250 ,200]

# Game Variables
gravity = 0
slime_movement = 0
game_active = True
points = 0 
show_title =True

# Game loop
while True:
    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                slime_movement = 0
                slime_movement -= 6
                # On first SPACE
                if gravity == 0:
                    pygame.time.set_timer(SPAWNOBS, 1200)
                    gravity = 0.25
                    show_title = False
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                obs_list.clear()
                points = 0
                score_display(0)
                slime_movement = 0
        if event.type == SPAWNOBS:
            obs_list.extend(create_obs())

    # Adds surface onto background surface
    screen.blit(background, (0,0))
    ground_x -= 1
    bg_x -= 0.5
    draw_bg()
    
    if show_title:
        title_display()

    if game_active:
        slime_movement += gravity
        slime_box.centery += slime_movement
        screen.blit(slime, slime_box)
        game_active = check_collision(obs_list)
        obs_list = move_obs(obs_list)
        draw_obs(obs_list)
    else:
        screen.blit(slime, slime_box)
        slime_box.center = (75, 256)
        title_display()

    draw_ground()
    points += check_score()
    score_display(points)

    # Resets the ground 
    if ground_x <= -512:
        ground_x = 0
    if bg_x <= -512:
        bg_x = 0

    # Draw the screen (display surface)
    pygame.display.update()
    # Max FPS
    clock.tick(120)