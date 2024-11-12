import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Define constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

Display_Background= pygame.image.load('assets/darkPurple.png')
# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jumping Game")

# Define the character class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = SCREEN_HEIGHT - 70
        self.velocity_y = 0
        self.is_jumping = False

    def update(self):
        # Update the player's position (handle jumping)
        if self.is_jumping:
            self.velocity_y += 1  # Gravity effect
            self.rect.y += self.velocity_y
            
            # If the player hits the ground, stop jumping
            if self.rect.y >= SCREEN_HEIGHT - 70:
                self.rect.y = SCREEN_HEIGHT - 70
                self.is_jumping = False
                self.velocity_y = 0

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.velocity_y = -15  # Jump force

# Define the obstacle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = SCREEN_HEIGHT - 70  # Same ground level as player

    def update(self):
        # Move the obstacle leftwards
        self.rect.x -= 5
        if self.rect.x < -30:  # If the obstacle goes off screen, reset it
            self.rect.x = SCREEN_WIDTH + random.randint(100, 300)
            self.rect.y = SCREEN_HEIGHT - 70  # Reset obstacle to the ground level

# Initialize the player and obstacles
player = Player()
obstacles = pygame.sprite.Group()

# Create some obstacles
for _ in range(5):
    obstacle = Obstacle()
    obstacles.add(obstacle)

# Group to handle all sprites (player + obstacles)
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(obstacles)

# Set up the clock
clock = pygame.time.Clock()

# Game loop
while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Space bar to make the player jump
                player.jump()

    # Update game objects
    all_sprites.update()

    # Check for collisions
    if pygame.sprite.spritecollide(player, obstacles, False):
        print("Game Over!")
        pygame.quit()
        sys.exit()

    # Draw everything
    screen.fill(WHITE)  # Clear screen with white color
    all_sprites.draw(screen)  # Draw all sprites (player and obstacles)

    # Update the display
    pygame.display.flip()

    # Set the frame rate
    clock.tick(60)
     