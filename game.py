
# Example file showing a basic pygame "game loop"
import pygame
# pygame setup
pygame.init()
pygame.init.mixer()

#set game dimensions 
WIDTH =1280
HEIGHT =720
screen = pygame.display.set_mode((WIDTH, HEIGHT))


pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

#blitting background and whatnot
background=build_background(WIDTH, HEIGHT)
background = pygame.image.load('assests/tiles/Moon_Space.png')

while running:
    # poll for events

    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("blue")

    # RENDER YOUR GAME HERE
    screen.blit(background, (0,0))


    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
