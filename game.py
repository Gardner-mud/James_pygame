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
        super().__init__()
        self.image = pygame.image.load('assets/kenney_space-shooter-extension/PNG/Sprites/Ships/spaceShips_007.png')  # Path to the astronaut image
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.image = pygame.transform.rotozoom(self.image, 270, 1)  # Scale to appropriate size
        self.orig_image = self.image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5
        self.angle = 0

    def controls(self, keys):
        if keys[pygame.K_LEFT]:
            self.angle += 3
        if keys[pygame.K_RIGHT]:
            self.angle -= 3
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
        self.rect = self.image.get_rect(center=self.rect.center)  # Update the rect position

    def update(self):
        # Update method to handle the controls and movement
        keys = pygame.key.get_pressed()  # Get the current state of all keys
        self.controls(keys)

        # Rotate 
        self.image = pygame.transform.rotozoom(self.orig_image, self.angle, 1)

    def shoot(self):
    # Offset the bullet spawn position slightly in the direction of the player's current angle
        radians = math.radians(self.angle)
        bullet_x = self.rect.centerx + math.cos(radians) * 30  # Spawn 30 pixels ahead
        bullet_y = self.rect.centery - math.sin(radians) * 30
        bullet = Bullet(bullet_x, bullet_y, self.angle, self)  # Pass the player reference
        all_sprites.add(bullet)  # Add bullet to all sprites
        bullets.add(bullet)      # Add bullet to bullets group



class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, player):
        super().__init__()
        self.image = pygame.image.load('assets/kenney_space-shooter-extension/PNG/Sprites/Ships/spaceShips_001.png')  # Path to the enemy image
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.orig_image = self.image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 2  
        self.player = player  # The player instance that the enemy will track

    def update(self):
        # Calculate direction towards the player, this sucked to figure out
        dx = self.player.rect.centerx - self.rect.centerx
        dy = self.player.rect.centery - self.rect.centery
        angle = math.atan2(dy, dx)

        # Move the enemy towards the player
        self.rect.centerx += math.cos(angle) * self.speed
        self.rect.centery += math.sin(angle) * self.speed

        # Rotate the enemy to face the player
        self.image = pygame.transform.rotate(self.orig_image, -math.degrees(angle))  # Rotate the enemy to face the player
        self.rect = self.image.get_rect(center=self.rect.center)  # Update the rect after rotation

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, player):
        super().__init__()
        self.image = pygame.image.load('assets/kenney_space-shooter-extension/PNG/Sprites/Missiles/spaceMissiles_022.png')
        self.image = pygame.transform.scale(self.image, (10, 30))
        self.orig_image = self.image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 10
        self.angle = angle
        self.do_not_collide = True  # Initially avoid collisions with the player
        self.player = player  # Reference to the player to check distance

    def update(self):
        # Move the bullet in the direction it is facing
        radians = math.radians(self.angle)
        self.rect.centery -= self.speed * math.sin(radians)
        self.rect.centerx += self.speed * math.cos(radians)

        # Allow collisions after the bullet is far enough from the player
        if self.do_not_collide and self.rect.center != self.player.rect.center:
            distance = math.hypot(self.rect.centerx - self.player.rect.centerx,
                                  self.rect.centery - self.player.rect.centery)
            if distance > 50:  # Safe distance threshold (50 pixels)
                self.do_not_collide = False

        # Remove the bullet if it goes off-screen
        if self.rect.bottom < 0 or self.rect.top > HEIGHT or self.rect.right < 0 or self.rect.left > WIDTH:
            self.kill()

        # Check for collisions with enemies only if do_not_collide is False
        if not self.do_not_collide:
            enemy_hit = pygame.sprite.spritecollideany(self, enemies)
            if enemy_hit:
                self.kill()
                enemy_hit.kill()
                print("Enemy destroyed!")

    




# Initialize player, enemies, and bullets
player = Player(WIDTH / 2, HEIGHT / 2)
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()  # Initialize bullets group

# Add an enemy for testing
enemy = Enemy(100, 100, player)
enemies.add(enemy)

# Add all sprites to a single group for easier updates and drawing
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(enemy)


all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(enemy)

while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                try:
                    player.shoot()  # Attempt to shoot a bullet
                except Exception as e:
                    print(f"Error when shooting: {e}")
                    running = False  # Stop the game for debugging
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