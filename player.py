import pygame
import field
from settings import *

class Player(pygame.sprite.Sprite):
    iq = 0
    def __init__(self,x,y,groups,opening = False,id = 0):
        super().__init__(groups)
        self.id = id
        self.x = x
        self.y = y
        self.body = {}
        self.window = pygame.display.get_surface()
        self.decision = None
        self.image = pygame.image.load("C:\\Users\\Sidho\\OneDrive\\Desktop\\soccer\\graphics\\Johnny.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 100))
        if opening:
            self.rect = self.image.get_rect(topleft = (0,0))
        else:
            self.rect = self.image.get_rect(topleft = (x,y))
        self.direction = pygame.math.Vector2()
        self.done = opening
        self.d = 10
        #self.window.blit(self.player,(x, y+100))

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0
        
    def move(self):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.rect.y += self.direction.y * 1.2
        self.rect.x += self.direction.x * 1.2
        #self.rect.center += self.direction * 1.2
    def opening(self):

            #self.window.blit(self.image,(self.rect.x, self.rect.y))
            #print(self.rect.x,self.rect.y)
        self.rect.x += self.d


        if self.rect.x > 1150 and self.d == 10:
            self.rect.y += 100
            self.d = -10
            #print(1)
            self.rect.x = 1200
            pygame.display.update()
        if self.rect.x > 1200 and self.d == -10:
            self.rect.y += 100 
            self.d = 10  
            #print(2)
            pygame.display.update()
        if self.rect.x <= -10 and self.d == -10:
            self.rect.y += 100
            self.d = 10
            #print(4)
            pygame.display.update()
        if self.rect.y > 700:
            #print(3)
            self.done = False
            self.rect.x = self.x
            self.rect.y = self.y
            print(self.y,self.x)
            pygame.display.update()
            
            #print(5)
    def border(self):
        if self.rect.x > 1150: 
            self.rect.x = 1150
        if self.rect.x <0:
            self.rect.x = 0
        if self.rect.y > 700 :
            self.rect.y = 700
        if self.rect.y <0:
            self.rect.y = 0

    def update(self):
        if self.done:
            self.opening()
        else:
            if field.Field.FOCUS == self.id:
                self.input()
            self.move()
            self.border()
        # Player.iq += 1
        # #pygame.draw.circle(self.window, (RED), (x,y),30)
        # for i,v in self.body.items():
        #     if Player.iq < 5:
        #         print(self.body[i].x)
        #     self.body[i].x += x 
        #     self.body[i].y += y
        #     if self.body[i].x > 1:
        #         print(self.body[i].x)
        #         print(self.body)
        #     self.body[i] = pygame.draw.circle(self.window, (RED), (self.body[i].x,self.body[i].y),30)
        # if Player.iq < 5:
        #     print(self.body)    


            

         