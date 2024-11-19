import pygame 
import random 

#making the player and choosing space ship as skin
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.image = pygame.image.load('assets/kenney_space-shooter-extension/PNG/Sprites/Ships/spaceShips_007.png')  # Path to the astronaut image
        self.image = pygame.transform.scale(self.image, (50, 50))  # Scale to appropriate size
        self.rect = self.image.get_rect(center=(x, y))
        self.speed= 5
# using up down left right as controls 
    def controls(self, keys):
        
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
    def draw(self, surface):
        surface.blit(self.image, self.rect)
