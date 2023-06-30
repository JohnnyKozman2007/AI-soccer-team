from tkinter import Place
import pygame
import field
from settings import *
import random
import math 

class Player(pygame.sprite.Sprite):
    iq = 0
    i = 0
    def __init__(self,x,y,groups,opening = False,id = 0):
        super().__init__(groups)
        self.id = id
        self.x = x
        self.y = y
        self.body = {}
        self.window = pygame.display.get_surface()
        self.decision = None
        self.strike = False
        self.have_ball = None
        self.pass_allow = True
        self.shoot_allow = True
        self.passed_to = False
        self.change_pass = pygame.time.get_ticks()
        self.shoot_player = pygame.time.get_ticks()
        self.image = pygame.image.load("C:\\Users\\Sidho\\OneDrive\\Desktop\\soccer\\graphics\\messi.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (200, 100))
        self.passing_to = None
        if opening:
            self.rect = self.image.get_rect(topleft = (0,0))
        else:
            self.rect = self.image.get_rect(topleft = (x,y))
        self.direction = pygame.math.Vector2()
        self.done = opening
        self.d = 10
        #self.window.blit(self.player,(x, y+100))
    def get_rect(self):
        return self.rect
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
    def know_team(self,p2,p3):
        self.teamates = [p2,p3]
    def shooting(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.shoot_allow:
            if self.have_ball :
                self.shoot_player = pygame.time.get_ticks()
                self.have_ball = False
                self.shoot_allow = False
                self.strike = True
                
                #self.ball.shot(shoot_x,shoot_y)
                
                      
    def passing(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_p] and self.have_ball:
            self.change_pass = pygame.time.get_ticks()
            self.pass_allow = False

            distance_1 = pygame.math.Vector2 (self.teamates[0].rect.x, self.teamates[0].rect.y).distance_to ((self.rect.x, self.rect.y))    
            #distance_1 = math.sqrt(abs(((self.teamates[0].rect.x + self.rect.x)*2)+((self.teamates[0].rect.y - self.rect.y)*2)))
            distance_2 = pygame.math.Vector2 (self.teamates[1].rect.x, self.teamates[1].rect.y).distance_to ((self.rect.x, self.rect.y))
            if distance_1 > distance_2:  
                
                closer = self.teamates[1]
            elif distance_1 < distance_2:
                
                closer = self.teamates[0]
            else:
                 
                closer = self.teamates[random.randint(0,1)]
            
            self.have_ball = False
            self.pass_allow = False
            self.passing_to = closer
            #closer.have_ball = True
            closer.passed_to = True    
        return
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
            self.rect.x = 1200
        if self.rect.x > 1200 and self.d == -10:
            self.rect.y += 100 
            self.d = 10  
            
        if self.rect.x <= -10 and self.d == -10:
            self.rect.y += 100
            self.d = 10
        if self.rect.y > 700:
            self.done = False
            self.rect.x = self.x
            self.rect.y = self.y

            


    def border(self):
        if self.rect.x > 1070: 
            self.rect.x = 1070
        if self.rect.x <-80:
            self.rect.x = -80

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
            self.passing()
            self.shooting()


            

         