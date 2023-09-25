# Importing Pygame
import pygame

# Initializing Pygame
pygame.init()

# Creating the window of the game
screen = pygame.display.set_mode((1080,720))

# Setting the window title
pygame.display.set_caption("Pixel Game")

# Setting the window icon
icon = pygame.image.load('./Graphics/p1_jump.png')
pygame.display.set_icon(icon)

# Adding the Background image
bg_surface = pygame.image.load('./Graphics/bg.png').convert_alpha()
bg_surface_trans = pygame.transform.scale(bg_surface,(1080,720)).convert_alpha()

# Adding the Ground image
gr_surface = pygame.image.load('./Graphics/ground.png').convert_alpha()
gr_surface_trans = pygame.transform.scale(gr_surface,(1080,360)).convert_alpha()

# While condintion
running = True

while running:
    # Getting all the pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Showing the bg image and the ground image
    screen.blit(bg_surface_trans, (0,0))
    screen.blit(gr_surface_trans,(0,370))

    # Updating the game 
    pygame.display.update()
# Closing the game 
pygame.quit()