import pygame
import random

class Pipe(pygame.sprite.Sprite):
    def __init__(self, inverted, xpos, ysize, pipe_image, PIPE_WIDHT, PIPE_HEIGHT, GAME_SPEED, SCREEN_HEIGHT):
        pygame.sprite.Sprite.__init__(self)
        self.inverted = inverted
        self.xpos = xpos
        self.ysize = ysize
        self.pipe_image = pipe_image
        self.PIPE_WIDHT = PIPE_WIDHT
        self.PIPE_HEIGHT = PIPE_HEIGHT
        self.GAME_SPEED = GAME_SPEED
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.update_image()

    def update_image(self, pipe_image=None):
        if pipe_image:
            self.pipe_image = pipe_image
        self.image = self.pipe_image
        self.image = pygame.transform.scale(self.image, (self.PIPE_WIDHT, self.PIPE_HEIGHT))
        if self.inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect = self.image.get_rect()
            self.rect[0] = self.xpos
            self.rect[1] = - (self.rect[3] - self.ysize)
        else:
            self.rect = self.image.get_rect()
            self.rect[0] = self.xpos
            self.rect[1] = self.SCREEN_HEIGHT - self.ysize
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect[0] -= self.GAME_SPEED

def get_random_pipes(xpos, SCREEN_HEIGHT, PIPE_WIDHT, PIPE_HEIGHT, PIPE_GAP, pipe_image, GAME_SPEED):
    size = random.randint(130, 500)
    print(size)
    pipe = Pipe(False, xpos, size, pipe_image, PIPE_WIDHT, PIPE_HEIGHT, GAME_SPEED, SCREEN_HEIGHT)
    pipe_inverted = Pipe(True, xpos, SCREEN_HEIGHT - size - PIPE_GAP, pipe_image, PIPE_WIDHT, PIPE_HEIGHT, GAME_SPEED, SCREEN_HEIGHT)
    return pipe, pipe_inverted