import pygame, random, time
from pygame.locals import *

# VARIABLES
cambioNivel = 2
SCREEN_WIDHT = 400
SCREEN_HEIGHT = 600
SPEED = 20
GRAVITY = 2.5
GAME_SPEED = 15

GROUND_WIDHT = 2 * SCREEN_WIDHT
GROUND_HEIGHT = 100

PIPE_WIDHT = 80
PIPE_HEIGHT = 500

PIPE_GAP = 150

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
background_day = pygame.image.load('assets/sprites/background-day.png').convert()
background_day = pygame.transform.scale(background_day, (SCREEN_WIDHT, SCREEN_HEIGHT))
background_night = pygame.image.load('assets/sprites/background-night.png').convert()
background_night = pygame.transform.scale(background_night, (SCREEN_WIDHT, SCREEN_HEIGHT))

# Load bird images
bluebird_images = [pygame.image.load('assets/sprites/bluebird-upflap.png').convert_alpha(),
                   pygame.image.load('assets/sprites/bluebird-midflap.png').convert_alpha(),
                   pygame.image.load('assets/sprites/bluebird-downflap.png').convert_alpha()]

redbird_images = [pygame.image.load('assets/sprites/redbird-upflap.png').convert_alpha(),
                  pygame.image.load('assets/sprites/redbird-midflap.png').convert_alpha(),
                  pygame.image.load('assets/sprites/redbird-downflap.png').convert_alpha()]

# Load pipe images
pipe_green = pygame.image.load('assets/sprites/pipe-green.png').convert_alpha()
pipe_red = pygame.image.load('assets/sprites/pipe-red.png').convert_alpha()
pipe_image = pipe_green  # Initialize pipe_image with the default pipe

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = bluebird_images
        self.speed = SPEED
        self.current_image = 0
        self.image = self.images[self.current_image]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect[0] = SCREEN_WIDHT / 6
        self.rect[1] = SCREEN_HEIGHT / 2

    def update(self):
        global score
        
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]

        self.speed += GRAVITY
        # UPDATE HEIGHT
        self.rect[1] += self.speed

        # Change to red bird when score reaches 2
        if score >= cambioNivel:
            self.images = redbird_images
        else:
            self.images = bluebird_images

    def bump(self):
        self.speed = -SPEED
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]

    def begin(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]

class Pipe(pygame.sprite.Sprite):
    def __init__(self, inverted, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)
        self.image = pipe_image
        self.image = pygame.transform.scale(self.image, (PIPE_WIDHT, PIPE_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = - (self.rect[3] - ysize)
        else:
            self.rect[1] = SCREEN_HEIGHT - ysize
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect[0] -= GAME_SPEED

class Ground(pygame.sprite.Sprite):
    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/sprites/base.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (GROUND_WIDHT, GROUND_HEIGHT))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT

    def update(self):
        self.rect[0] -= GAME_SPEED

def is_off_screen(sprite):
    return sprite.rect[0] < -(sprite.rect[2])

def get_random_pipes(xpos):
    size = random.randint(100, 300)
    pipe = Pipe(False, xpos, size)
    pipe_inverted = Pipe(True, xpos, SCREEN_HEIGHT - size - PIPE_GAP)
    return pipe, pipe_inverted

def draw_score(screen, score):
    score_str = str(score)
    for i, digit in enumerate(score_str):
        digit_image = score_images[int(digit)]
        screen.blit(digit_image, (SCREEN_WIDHT // 2 + i * digit_image.get_width(), 50))

BEGIN_IMAGE = pygame.image.load('assets/sprites/message.png').convert_alpha()

bird_group = pygame.sprite.Group()
bird = Bird()
bird_group.add(bird)

ground_group = pygame.sprite.Group()
for i in range(2):
    ground = Ground(GROUND_WIDHT * i)
    ground_group.add(ground)

pipe_group = pygame.sprite.Group()
for i in range(2):
    pipes = get_random_pipes(SCREEN_WIDHT * i + 800)
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
    screen.blit(BEGIN_IMAGE, (120, 150))
    if is_off_screen(ground_group.sprites()[0]):
        ground_group.remove(ground_group.sprites()[0])
        new_ground = Ground(GROUND_WIDHT - 20)
        ground_group.add(new_ground)

    bird.begin()
    ground_group.update()
    bird_group.draw(screen)
    ground_group.draw(screen)
    pygame.display.update()

# Main game loop
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
        new_ground = Ground(GROUND_WIDHT - 20)
        ground_group.add(new_ground)

    if is_off_screen(pipe_group.sprites()[0]):
        pipe_group.remove(pipe_group.sprites()[0])
        pipe_group.remove(pipe_group.sprites()[0])
        pipes = get_random_pipes(SCREEN_WIDHT * 2)
        pipe_group.add(pipes[0])
        pipe_group.add(pipes[1])
        score += 1  # Increment score each time the bird passes a set of pipes

    bird_group.update()
    ground_group.update()
    pipe_group.update()
    bird_group.draw(screen)
    pipe_group.draw(screen)
    ground_group.draw(screen)

    # Draw the score
    draw_score(screen, score)

    pygame.display.update()

    if (pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask) or
            pygame.sprite.groupcollide(bird_group, pipe_group, False, False, pygame.sprite.collide_mask)):
        pygame.mixer.music.load(hit)
        pygame.mixer.music.play()
        time.sleep(1)
        break