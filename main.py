
import pygame
from pygame.locals import *

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
pygame.display.set_caption("Greed Island YNC Arc")
running = True

####Player Movement#######
walkingRight = False
walkingLeft = False

jumpingUp = False

class backGroundText():
    def __init__(self) :
        self.font = pygame.font.Font("texts/retganon.ttf",64 )
        self.openingText = self.font.render("York New City",True,(255,255,255))
        self.openingTextRect = self.openingText.get_rect()
        self.openingTextRect.center = (1280//2,720//6)
    def draw(self):
        screen.blit(self.openingText,self.openingTextRect)

class Protag(pygame.sprite.Sprite):
    def __init__(self,x,y,displacement) :
        pygame.sprite.Sprite.__init__(self)
        self.animationList = []
        self.animationCooldown = 0
        self.flip_image = False
        self.displacement = displacement
        self.direction = pygame.math.Vector2(0, 0)
        self.gravityValue = 0.7
        self.jumpSpeed = -15
        self.current_choice = 0
        self.list_choice = 0
        self.update_time = pygame.time.get_ticks()

        character_list = []
        for i in range(5):
                character = pygame.image.load(f"Protags\Kurapika\Stance\k_stance{i}.png").convert_alpha()
                character = pygame.transform.scale(character, (100, 150))
                character_list.append(character)
                # the list  is appended into a greater animation list
        self.animationList.append(character_list)

        character_list = []
        for i in range(4):
                character = pygame.image.load(f"Protags\Kurapika\Run\k_run{i}.png").convert_alpha()
                character = pygame.transform.scale(character, (100, 150))
                character_list.append(character)
                # the list  is appended into a greater animation list
        self.animationList.append(character_list)

        # the characters image is set to the index of the animation list and the list choice. This will allow for the image to constantly change depending on the character's actions
        self.image = self.animationList[self.current_choice][self.list_choice]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update_animation(self):
        # i have two different animation cooldowns for my character when he has collected an upgrade
            self.animationCooldown = 100 # here its 100
            self.image = self.animationList[self.current_choice][self.list_choice]
            if pygame.time.get_ticks() - self.update_time > self.animationCooldown:
                self.update_time = pygame.time.get_ticks()
                self.list_choice += 1
            if self.list_choice >= len(self.animationList[self.current_choice]):
                self.list_choice = 0
            

    def override_currentAction(self, new_action):
        if new_action != self.current_choice:
            self.current_choice = new_action
            self.list_choice = 0
            self.update_time = pygame.time.get_ticks()

    def movement(self,Right,Left):
        if Right:
            self.rect.x +=5
            self.flip_image = False
        if Left:
            self.rect.x -=5
            self.flip_image = True
    
    def gravity(self):
        self.direction.y += self.gravityValue
        self.rect.y += self.direction.y
        if self.rect.bottom >= 720:
            self.rect.bottom = 720

    def jump(self,jump):
        if jump:
            self.direction.y = self.jumpSpeed

    

    def draw(self):
          screen.blit(pygame.transform.flip(self.image, self.flip_image, False), self.rect)




gameText = backGroundText()
chrollo = Protag(600,300,400)


while True:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                walkingLeft = True
            if event.key == pygame.K_d:
                walkingRight = True
            if event.key == pygame.K_w:
                jumpingUp = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                walkingLeft = False
            if event.key == pygame.K_d:
                walkingRight = False
            if event.key == pygame.K_w:
                jumpingUp = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("light blue")

    # RENDER YOUR GAME HERE
    
    gameText.draw()


    chrollo.draw()
    chrollo.update_animation()
    chrollo.gravity()
    chrollo.jump(jumpingUp)
    chrollo.movement(walkingRight,walkingLeft)
    

    if walkingRight or  walkingLeft:
        chrollo.override_currentAction(1)
    else:
        chrollo.override_currentAction(0)
    
    
    

    # flip() the display to put your work on screen
    pygame.display.update()

      # limits FPS to 60

