# Importing Pygame
import pygame

# Importing Random
import random

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
start_time = 0
score = 0
def display_score():
    current_time = int(pygame.time.get_ticks() / 1000)  - start_time
    score_surface = text_font.render(f'Score: {current_time}', False, 'Black')
    score_rect = score_surface.get_rect(center = (560, 160))
    
    # Showing the score text 
    screen.blit(score_surface, score_rect)
    return current_time

# Menu text
text_menu_font1 = pygame.font.Font('./Fonts/Origin.ttf',90)
text_menu_font2 = pygame.font.Font('./Fonts/Origin.ttf',50)
menu_surface = text_menu_font1.render('Pixel Game ', False, '#37ABA6')
menu_rect = menu_surface.get_rect(center = (560, 160))

start_surface = text_menu_font2.render('Press SPACE to start the game ', False, '#37ABA6')
start_rect = start_surface.get_rect(center = (560, 570))

# Menu Image
menuimg = pygame.image.load('./Graphics/p1_jump.png')
menuimg_surface = pygame.transform.scale2x(menuimg)
menuimg_rect = menuimg_surface.get_rect(center = (540, 400))


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
        mouse = pygame.mouse.get_pressed(num_buttons=3)
        if keys[pygame.K_SPACE] and self.rect.bottom >= 640:
            self.gravity = -20
        elif mouse[0] and self.rect.collidepoint(pygame.mouse.get_pos()) and self.rect.bottom >= 640:
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

# Creating the player's sprite
player = pygame.sprite.GroupSingle()
player.add(Player())

class Enemies(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == 'fly':
            self.fly1 = pygame.image.load('./Graphics/flyFly1.png')
            self.fly2 = pygame.image.load('./Graphics/flyFly2.png')
            self.frames = [self.fly1, self.fly2]
            y_pos = 535
        else:
            self.snail1 = self.fly1 = pygame.image.load('./Graphics/snailWalk1.png')
            self.snail2 = self.fly1 = pygame.image.load('./Graphics/snailWalk2.png')
            self.frames = [self.snail1, self.snail2]
            y_pos = 640
        self.index_animation = 0
        self.image = self.frames[self.index_animation]
        self.rect = self.image.get_rect(midbottom = (random.randint(900,1100), y_pos))

    def animation(self):
        self.index_animation += 0.1
        if self.index_animation >= len(self.frames):
            self.index_animation = 0
        self.image = self.frames[int(self.index_animation)]

    def destroy(self):
         if self.rect <= -100:
            self.kill()
    def update(self):
        self.animation()
        self.rect.x -= 6

# Creating the enemies group
enemies_group = pygame.sprite.Group()

# Collision detection
def collision():
    if pygame.sprite.spritecollide(player.sprite, enemies_group, False):
        enemies_group.empty()
        return False
    else: 
        return True
    

# Creating a timer
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 900)
# Creating a clock to set the FPS
clock = pygame.time.Clock()

# While condition
running = True
game_active = False
while running:
    # Getting all the pygame events
    for event in pygame.event.get():

        # Get the event to close the window
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000) 
        
        if event.type == enemy_timer and game_active == True:
            enemies_group.add(Enemies(random.choice(['fly', 'snail', 'snail', 'snail'])))
    if game_active:
        # Showing the bg image and the ground image
        screen.blit(bg_surface_trans, (0,0))
        screen.blit(gr_surface_trans,(0,370))

        # Saving the score
        score = display_score()

        # Setting the FPS to 60
        clock.tick(60)

        # Drawing the player
        player.draw(screen)
        player.update()

        # Drawing the enemies
        enemies_group.draw(screen)
        enemies_group.update()

        # Stopping the game
        game_active = collision()
    else:
        screen.fill('#212323')
        screen.blit(menu_surface, menu_rect)
        screen.blit(menuimg_surface, menuimg_rect)
        if score == 0:
            screen.blit(start_surface, start_rect)
        else:
            final_score_surface = text_menu_font2.render(f'Your score was: {score}', False, '#37ABA6')
            final_score_rect = final_score_surface.get_rect(center = (560, 570))
            screen.blit(final_score_surface, final_score_rect)
    
    # Updating the game 
    pygame.display.update()


# Closing the game 
pygame.quit()