from distutils.command.build_ext import show_compilers
import pygame
from settings import *
import random

class Ball(pygame.sprite.Sprite):
    def __init__(self,x,y,groups,players,enemy):
        super().__init__(groups)
        self.window = pygame.display.get_surface()
        self.image = pygame.image.load("C:\\Users\\Sidho\\OneDrive\\Desktop\\soccer\\graphics\\ball.png").convert_alpha()
        self.ball = pygame.transform.scale(self.image, (200, 100))
        self.rect = self.image.get_rect(topleft = (x,y))
        self.players = players
        self.enemy = enemy
        self.shoot_allow = False
        self.passed_to = False
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
            if player in self.enemy:
                shoot_x = -200
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
        if self.rect.colliderect(player.rect.inflate(-180,-80)):
            #print(player,"has ball")
            if player.direction.x == 1:
                self.shift = 60
            elif player.direction.x == -1:
                self.shift = 0
            self.rect.y = player.rect.y+40
            self.rect.x = player.rect.x+40+self.shift
            player.have_ball = True
        else:
            player.have_ball = False
        #print(self.rect.x,player.rect.x,self.rect.y,player.rect.y)
        # if self.rect.y <= player.rect.y+55 and self.rect.y >= player.rect.y-55:
        #     #print('kkkkkkkkk',self.rect.x,player.rect.x,self.rect.y,player.rect.y)
        #     #print(self.rect.x ,player.rect.x,self.rect.x <= player.rect.x+100,self.rect.x >= player.rect.x-300)
        #     if self.rect.x <= player.rect.x+105 and self.rect.x >= player.rect.x-105 and player.direction.x != 0:# and not player in self.enemy:
        #         player.have_ball = True
        #         #print(player.id,player.have_ball,player)
        #         if not player.done:
        #             if player.direction.x == 1:
        #                 self.shift = 60
        #             elif player.direction.x == -1:
        #                 self.shift = 0
        #             self.rect.y = player.rect.y+40
        #             self.rect.x = player.rect.x+40+self.shift
        #             #if player.direction.x == 1:
        #             #    self.rect.x = self.rect.x + 60
        #     else:
        #         player.have_ball = False
        #     if self.rect.x <= player.rect.x+105 and self.rect.x >= player.rect.x-105:

        #         player.have_ball = True
        #         #print(player.id,player.have_ball,player)
        #         if not player.done:
        #             if player.direction.x == 1:
        #                 self.shift = 60
        #             elif player.direction.x == -1:
        #                 self.shift = 0
        #             self.rect.y = player.rect.y+40
        #             self.rect.x = player.rect.x+40+self.shift 
        #             #if player.direction.x == 1:
        #             #    self.rect.x = self.rect.x + 60
        #     else:
        #         player.have_ball = False
        #         #print(1)
        # else:
        #         player.have_ball = False
        #         #print(2)
    def move(self,player):
        #if player.direction.y > 0:
            #print('entered',player.direction.y * 0.5,player.direction.x * 0.5)

        #if player.direction.y < 0:
            #print(self.rect.y,player.y,self.have_ball,player.direction.y)
        self.rect.y += player.direction.y * player.speed
        self.rect.x += player.direction.x * player.speed
            
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
        for player2 in self.enemy:
            #if player.have_ball and player.passed_to == True:
            #    print("hi")
            #    continue
            self.check_ball(player2)
            # if player2.have_ball:
            #     print(player2.id,player2.have_ball)
            #     print()
            #     print()
            if player2.have_ball:     
                self.move(player2)
            else:
                self.check_ball(player2)

            self.border()            

        
        
            
