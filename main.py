import pygame, random, time
from pygame.locals import *
from src.bird import Bird
from src.pipe import Pipe, get_random_pipes
from src.ground import Ground
from src.utils import is_off_screen, draw_score

# VARIABLES
SCREEN_WIDHT = 400*1.3
SCREEN_HEIGHT = 600*1.3
SPEED = 20
GRAVITY = 2.5
GAME_SPEED = 15
GROUND_WIDHT = 2 * SCREEN_WIDHT
GROUND_HEIGHT = 100
PIPE_WIDHT = 80
PIPE_HEIGHT = 500
PIPE_GAP = 150
cambioNivel = 2

wing = 'assets/audio/wing.wav'
hit = 'assets/audio/hit.wav'

pygame.mixer.init()

# Score variable
score = 0

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDHT, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')

# Load number images for score display after initializing display
score_images = [pygame.image.load(f'assets/sprites/{i}.png').convert_alpha() for i in range(10)]

# Load background images
background_day = pygame.image.load('assets/sprites_taller/background-day.jpeg').convert()
background_day = pygame.transform.scale(background_day, (SCREEN_WIDHT, SCREEN_HEIGHT))
background_night = pygame.image.load('assets/sprites_taller/background-night.jpeg').convert()
background_night = pygame.transform.scale(background_night, (SCREEN_WIDHT, SCREEN_HEIGHT))

# Load bird images
hornero_images = []
for i in range(1, 9):
    image = pygame.image.load(f'assets/sprites_taller/hornero/hornero{i}.png').convert_alpha()
    hornero_images.append(image)

redbird_images = [pygame.image.load('assets/sprites/redbird-upflap.png').convert_alpha(),
                  pygame.image.load('assets/sprites/redbird-midflap.png').convert_alpha(),
                  pygame.image.load('assets/sprites/redbird-downflap.png').convert_alpha()]

# Load pipe images
pipe_green = pygame.image.load('assets/sprites/pipe-green.png').convert_alpha()
pipe_red = pygame.image.load('assets/sprites/pipe-red.png').convert_alpha()
pipe_image = pipe_green  # Initialize pipe_image with the default pipe

BEGIN_IMAGE = pygame.image.load('assets/sprites_taller/message.png').convert_alpha()

bird_group = pygame.sprite.Group()
bird = Bird(hornero_images, hornero_images, SCREEN_WIDHT, SCREEN_HEIGHT, SPEED, GRAVITY, cambioNivel)
bird_group.add(bird)

ground_group = pygame.sprite.Group()
for i in range(2):
    ground = Ground(GROUND_WIDHT * i, SCREEN_HEIGHT, GROUND_WIDHT, GROUND_HEIGHT, GAME_SPEED)
    ground_group.add(ground)

pipe_group = pygame.sprite.Group()
for i in range(2):
    pipes = get_random_pipes(SCREEN_WIDHT * i + 800, SCREEN_HEIGHT, PIPE_WIDHT, PIPE_HEIGHT, PIPE_GAP, pipe_image, GAME_SPEED)
    pipe_group.add(pipes[0])
    pipe_group.add(pipes[1])

clock = pygame.time.Clock()
begin = True

while begin:
    clock.tick(15)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE or event.key == K_UP:
                bird.bump()
                pygame.mixer.music.load(wing)
                pygame.mixer.music.play()
                begin = False

    screen.blit(background_day, (0, 0))
    screen.blit(BEGIN_IMAGE, ((SCREEN_WIDHT/2) - (BEGIN_IMAGE.get_width()/2), (SCREEN_HEIGHT/2) - (BEGIN_IMAGE.get_height()/2)))

    if is_off_screen(ground_group.sprites()[0]):
        ground_group.remove(ground_group.sprites()[0])
        new_ground = Ground(GROUND_WIDHT - 20, SCREEN_HEIGHT, GROUND_WIDHT, GROUND_HEIGHT, GAME_SPEED)
        ground_group.add(new_ground)

    bird.begin()
    ground_group.update()
    bird_group.update(0)  # Pass 0 as score to avoid changing bird color
    bird_group.draw(screen)
    ground_group.draw(screen)
    pipe_group.draw(screen)  # Ensure pipes are drawn on the screen
    pygame.display.update()

#MAIN LOOP
while True:
    clock.tick(15)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE or event.key == K_UP:
                bird.bump()
                pygame.mixer.music.load(wing)
                pygame.mixer.music.play()

    # Change background and pipe image based on score
    if score >= cambioNivel:
        screen.blit(background_night, (0, 0))
        pipe_image = pipe_red
    else:
        screen.blit(background_day, (0, 0))
        pipe_image = pipe_green

    if is_off_screen(ground_group.sprites()[0]):
        ground_group.remove(ground_group.sprites()[0])
        new_ground = Ground(GROUND_WIDHT - 20, SCREEN_HEIGHT, GROUND_WIDHT, GROUND_HEIGHT, GAME_SPEED)
        ground_group.add(new_ground)

    if is_off_screen(pipe_group.sprites()[0]):
        pipe_group.remove(pipe_group.sprites()[0])
        pipe_group.remove(pipe_group.sprites()[0])
        pipes = get_random_pipes(SCREEN_WIDHT * 2, SCREEN_HEIGHT, PIPE_WIDHT, PIPE_HEIGHT, PIPE_GAP, pipe_image, GAME_SPEED)
        pipe_group.add(pipes[0])
        pipe_group.add(pipes[1])
        score += 1  # Increment score each time the bird passes a set of pipes

    bird_group.update(score)
    ground_group.update()
    pipe_group.update()
    bird_group.draw(screen)
    pipe_group.draw(screen)
    ground_group.draw(screen)

    # Draw the score
    draw_score(screen, score, score_images, SCREEN_WIDHT)

    pygame.display.update()

    if (pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask) or
            pygame.sprite.groupcollide(bird_group, pipe_group, False, False, pygame.sprite.collide_mask)):
        pygame.mixer.music.load(hit)
        pygame.mixer.music.play()
        time.sleep(1)
        break