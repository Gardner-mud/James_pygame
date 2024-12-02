import pygame
import math

# pygame setup
pygame.init()

# Set game dimensions
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

# Blitting background and initializing the player
Display_Background = pygame.image.load('assets/tiles/Moon_Space.png')


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()  # Call the parent class's __init__ to initialize the Sprite properly
        self.image = pygame.image.load('assets/kenney_space-shooter-extension/PNG/Sprites/Ships/spaceShips_007.png')  # Path to the astronaut image
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.image = pygame.transform.rotozoom(self.image, 270,1)  # Scale to appropriate size
        self.orig_image = self.image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5
        self.angle = 0

    def controls(self, keys):
        if keys[pygame.K_LEFT]:
            self.angle+=3
        if keys[pygame.K_RIGHT]:
            self.angle-=3
        if keys[pygame.K_UP]:
            radians = math.radians(self.angle)
            self.rect.centery -= self.speed * math.sin(radians)
            self.rect.centerx += self.speed * math.cos(radians)
        if keys[pygame.K_DOWN]:
            radians = math.radians(self.angle)
            self.rect.centery += self.speed * math.sin(radians)
            self.rect.centerx -= self.speed * math.cos(radians)

        # Keep the player within the screen bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        self.rect = self.image.get_rect(center=self.rect.center) 

    def update(self):
        #Update method to handle the controls and movement
        keys = pygame.key.get_pressed()  # Get the current state of all keys
        self.controls(keys)

        self.image= pygame.transform.rotozoom(self.orig_image, self.angle, 1)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, player):
        super().__init__()
        self.image = pygame.image.load('assets/kenney_space-shooter-extension/PNG/Sprites/Ships/spaceShips_001.png')  # Path to the enemy image
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.orig_image = self.image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 2  # Slow speed for the enemy
        self.player = player  # The player instance that the enemy will track

    def update(self):
        # Calculate direction vector from enemy to player
        direction = pygame.math.Vector2(self.player.rect.centerx - self.rect.centerx, self.player.rect.centery - self.rect.centery)
        direction_length = direction.length()  # Get the length of the direction vector

        # Normalize the direction vector (convert it to a unit vector)
        if direction_length != 0:
            direction.normalize_ip()

        # Move the enemy towards the player
        self.rect.centerx += direction.x * self.speed
        self.rect.centery += direction.y * self.speed

        # Rotate the enemy to face the player
        angle = math.degrees(math.atan2(direction.y, direction.x))
        self.image = pygame.transform.rotate(self.orig_image, -angle)  # Invert angle for correct rotation
        self.rect = self.image.get_rect(center=self.rect.center)


player = Player(1280/2, 720/2)
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

while running:
    # Poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update game logic here
    all_sprites.update()  # This will call the update method of all sprites, including the player

    # Clear screen with a background color or image
    screen.fill((0, 0, 255))  # Fill the screen with blue as the background (optional)

    # Draw the background
    screen.blit(Display_Background, (0, 0))  # Draw the background image

    # Draw all sprites
    all_sprites.draw(screen)  # Draw all sprites (player and obstacles)

    # Update the display
    pygame.display.update()

    # Set the frame rate (60 FPS)
    clock.tick(60)

# Quit pygame when the loop is done
pygame.quit()
