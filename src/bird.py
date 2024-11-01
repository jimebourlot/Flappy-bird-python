import pygame

class Bird(pygame.sprite.Sprite):
    def __init__(self, bluebird_images, redbird_images, SCREEN_WIDHT, SCREEN_HEIGHT, SPEED, GRAVITY, cambioNivel):
        pygame.sprite.Sprite.__init__(self)
        self.bluebird_images = bluebird_images
        self.redbird_images = redbird_images
        self.images = bluebird_images
        self.speed = SPEED
        self.SPEED = SPEED  # Store SPEED as an instance attribute
        self.GRAVITY = GRAVITY
        self.cambioNivel = cambioNivel
        self.current_image = 0
        self.image = self.images[self.current_image]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect[0] = SCREEN_WIDHT / 6
        self.rect[1] = SCREEN_HEIGHT / 2
        self.screenheight = SCREEN_HEIGHT

    def update(self, score):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]
        self.speed += self.GRAVITY
        # UPDATE HEIGHT
        self.rect[1] += self.speed

        # Change to red bird when score reaches cambioNivel
        if score >= self.cambioNivel:
            self.images = self.redbird_images
        else:
            self.images = self.bluebird_images

    def bump(self):
        self.speed = -self.SPEED
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]

    def begin(self):
        self.rect[1] = self.screenheight / 2  # Reset position
        self.speed = 0  # Reset speed
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]