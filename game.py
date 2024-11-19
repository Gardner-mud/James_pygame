import pygame

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
        self.image = pygame.transform.scale(self.image, (50, 50))  # Scale to appropriate size
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5
        self.angle = 0

    def controls(self, keys):
        """Handles movement controls"""
        if keys[pygame.K_LEFT]:
            self.angle-=2
            self.image= pygame.transform.rotozoom(self.image, self.angle, 1)
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

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
        """Update method to handle the controls and movement"""
        keys = pygame.key.get_pressed()  # Get the current state of all keys
        self.controls(keys)


player = Player(5, 5)
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
