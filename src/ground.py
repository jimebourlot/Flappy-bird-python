import pygame

class Ground(pygame.sprite.Sprite):
    def __init__(self, xpos, SCREEN_HEIGHT, GROUND_WIDHT, GROUND_HEIGHT, GAME_SPEED):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/sprites/base.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (GROUND_WIDHT, GROUND_HEIGHT))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT
        self.GAME_SPEED = GAME_SPEED

    def update(self):
        self.rect[0] -= self.GAME_SPEED