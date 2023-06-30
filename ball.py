from distutils.command.build_ext import show_compilers
import pygame
from settings import *
import random

class Ball(pygame.sprite.Sprite):
    def __init__(self,x,y,groups,players):
        super().__init__(groups)
        self.window = pygame.display.get_surface()
        self.image = pygame.image.load("C:\\Users\\Sidho\\OneDrive\\Desktop\\soccer\\graphics\\ball.png").convert_alpha()
        self.ball = pygame.transform.scale(self.image, (200, 100))
        self.rect = self.image.get_rect(topleft = (x,y))
        self.players = players
        # self.pass_allow = True
        # self.have_ball = None
        self.shift = 0
    def border(self):
        if self.rect.x > 1150: 
            self.rect.x = 1150
        if self.rect.x <-10:
            self.rect.x = -10

        if self.rect.y > 770 :
            self.rect.y = 770
        if self.rect.y <0:
            self.rect.y = 0

    def check_ball(self,player):
        if player.strike:
            shoot_y = random.randrange(360,390)
            shoot_x =  200
            self.rect.x += shoot_x*1
            self.rect.y = shoot_y
            player.strike = False


        if player.passed_to:
            

            if player.direction.x == 1:
                self.shift = 60
            elif player.direction.x == -1:
                self.shift = 0
            self.rect.y = player.rect.y+40
            self.rect.x = player.rect.x+40+self.shift
            return
        if self.rect.x >= player.rect.x or self.rect.x <= player.rect.x:
            #print(self.rect.x,player.rect.x,self.rect.y,player.rect.y)
            if self.rect.y <= player.rect.y+55 and self.rect.y >= player.rect.y-55:
                #print('kkkkkkkkk',self.rect.x,player.rect.x,self.rect.y,player.rect.y)
                #print(self.rect.x ,player.rect.x,self.rect.x <= player.rect.x+100,self.rect.x >= player.rect.x-300)
                if self.rect.x <= player.rect.x+135 and self.rect.x >= player.rect.x-135 and player.direction.x == 1:
                    player.have_ball = True
                    if not player.done:
                        if player.direction.x == 1:
                            self.shift = 60
                        elif player.direction.x == -1:
                            self.shift = 0
                        self.rect.y = player.rect.y+40
                        self.rect.x = player.rect.x+40+self.shift
                        #if player.direction.x == 1:
                        #    self.rect.x = self.rect.x + 60

                elif self.rect.x <= player.rect.x+105 and self.rect.x >= player.rect.x-105:

                    player.have_ball = True
                    if not player.done:
                        if player.direction.x == 1:
                            self.shift = 60
                        elif player.direction.x == -1:
                            self.shift = 0
                        self.rect.y = player.rect.y+40
                        self.rect.x = player.rect.x+40+self.shift 
                        #if player.direction.x == 1:
                        #    self.rect.x = self.rect.x + 60
                else:
                    player.have_ball = False
            else:
                    player.have_ball = False


        #if self.rect.x -250 <= player.rect.x:
         #   print(3)
          #  if self.rect.y <= player.rect.y+60 and self.rect.y >= player.rect.y-60:
                #print('kkkkkkkkk',self.rect.x,player.rect.x,self.rect.y,player.rect.y)
                

        
        #print(self.rect.y,player.y,self.have_ball)
    def move(self,player):
        #if player.direction.y > 0:
            #print('entered',player.direction.y * 0.5,player.direction.x * 0.5)

        #if player.direction.y < 0:
            #print(self.rect.y,player.y,self.have_ball,player.direction.y)
        self.rect.y += player.direction.y * 1.2
        self.rect.x += player.direction.x * 1.2
            
    def update(self):
        for player in self.players:
            #if player.have_ball and player.passed_to == True:
            #    print("hi")
            #    continue
            
            self.check_ball(player)

            if player.have_ball:     
                self.move(player)
            else:
                self.check_ball(player)
            self.border()


        
        
            
