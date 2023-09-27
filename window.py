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

# Adding the font for score text
text_font = pygame.font.Font('./Fonts/Origin.ttf',60)
score_surface = text_font.render('Score: ', False, 'Black')
score_rect = score_surface.get_rect(center = (520, 160))


# Player Class
class Player (pygame.sprite.Sprite):
    # Setup all the player methods
    def __init__(self):
        super().__init__()
        self.player_walk1 = pygame.image.load('./Graphics/p1_walk02.png').convert_alpha()
        self.player_walk2 = pygame.image.load('./Graphics/p1_walk03.png').convert_alpha()
        self.player_walk = [self.player_walk1, self.player_walk2]
        self.player_jump = pygame.image.load('./Graphics/p1_jump.png').convert_alpha()
        self.player_index = 0

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (200,640))
        self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 640:
            self.gravity = -20


    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 640:
            self.rect.bottom = 640

    def animation(self):
        if self.rect.bottom < 640:
            self.image = self.player_jump 
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation()
#Creating the player's sprite
player = pygame.sprite.GroupSingle()
player.add(Player())
# Creating a clock to set the FPS
clock = pygame.time.Clock()
# While condintion
running = True

while running:
    # Getting all the pygame events
    for event in pygame.event.get():

        # Get the event to close the window
        if event.type == pygame.QUIT:
            running = False

    # Showing the bg image and the ground image
    screen.blit(bg_surface_trans, (0,0))
    screen.blit(gr_surface_trans,(0,370))

    # Showing the score text 
    screen.blit(score_surface, score_rect)

    # Setting the FPS to 60
    clock.tick(60)

    # Drawing the player
    player.draw(screen)
    player.update()
    # Updating the game 
    pygame.display.update()
# Closing the game 
pygame.quit()