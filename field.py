import pygame
from settings import *
from player import Player
from mind import Mind
import ball

class Field:
    FOCUS = 2   
    def __init__(self,background =None):
        
        self.team = None
        self.background = background
        self.change_allow = True
        self.switch_duration_cooldown = 200
        #window
        self.window = pygame.Surface((1200, 800))
        self.visible_sprites = pygame.sprite.Group()
        


        self.a = pygame.draw.rect(self.window, (GREEN),(0,0,1200,800))
        self.b = pygame.draw.rect(self.window, (WHITE),(5,5,1190,790),10)


        
        self.c = pygame.draw.rect(self.window, (WHITE),(1115,295,80,200),10)


        self.d = pygame.draw.rect(self.window, (WHITE),(5,295,80,200),10)



        self.net_r = pygame.draw.rect(self.window, (WHITE),(1155,350,40,100),10)
        self.net_l = pygame.draw.rect(self.window, (WHITE),(5,350,40,100),10)
        
        self.e = pygame.draw.line(self.window, (WHITE), (600, 5), (600, 794),10)
        self.r = pygame.draw.circle(self.window, (WHITE), (600,400), 30)
        self.r2 = pygame.draw.circle(self.window, (GREEN), (600,400), 20)
        
        
        self.make_team()
        self.make_enemy()
         
        self.ball = ball.Ball(600,400,self.visible_sprites,self.team)#pygame.draw.circle(self.window, (BLUE), (600,400), 12)
        self.objects = [self.ball,self.team]
        #
    def make_team(self):
        self.p1 = Player(200,100,self.visible_sprites,id = 1)
        self.p2 = Player(0,350,self.visible_sprites,opening = True,id = 2)
        self.p3 = Player(200,600,self.visible_sprites,id = 3)
        self.team = [self.p1,self.p2,self.p3]
        self.p1.know_team(self.p2,self.p3)
        self.p2.know_team(self.p1,self.p3)
        self.p3.know_team(self.p1,self.p2)

        for player in self.team:
            self.visible_sprites.add(self.p1)
    def make_enemy(self):
        self.e1 = Mind(740,70,self.visible_sprites,id = 1)
        self.e2 = Mind(940,280,self.visible_sprites,id = 2)
        self.e3 = Mind(740,530,self.visible_sprites,id = 3)
        self.enemy = [self.e1,self.e2,self.e3]

        for player in self.team:
            self.visible_sprites.add(self.p1)
    def get_focus(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LCTRL]:
            self.change_player = pygame.time.get_ticks()
            if self.change_allow:
                self.change_allow = False
                Field.FOCUS += 1 
            if Field.FOCUS == 4:
                Field.FOCUS  = 1 
    def cooldown(self):
        current_time = pygame.time.get_ticks()
        if not self.change_allow:
            if current_time - self.change_player >= self.switch_duration_cooldown:
                self.change_allow = True
        for player in self.team:                
            if not player.shoot_allow:
                if current_time - player.shoot_player >= self.switch_duration_cooldown:
                    player.shoot_allow = True 
                               
                
        for player in self.team:
            
            if current_time - player.change_pass > self.switch_duration_cooldown:
                #player.passed_to = False
                #player.pass_allow = True
                if not player.pass_allow:
                    player.pass_allow = True
                    player.have_ball = False
                    player.passing_to.passed_to = False
                    Player.i += 1
        
        # for player in self.team:
        #     if player.passing_to != None:
        #         player.passing_to.have_ball = True
    def draw_background(self):
        self.a = pygame.draw.rect(self.window, (GREEN),(0,0,1200,800))
        self.b = pygame.draw.rect(self.window, (WHITE),(5,5,1190,790),10)


        
        self.c = pygame.draw.rect(self.window, (WHITE),(1115,295,80,200),10)


        self.d = pygame.draw.rect(self.window, (WHITE),(5,295,80,200),10)



        self.net_r = pygame.draw.rect(self.window, (WHITE),(1155,350,40,100),10)
        self.net_l = pygame.draw.rect(self.window, (WHITE),(5,350,40,100),10)
        self.e = pygame.draw.line(self.window, (WHITE), (600, 5), (600, 794),10)
        self.r = pygame.draw.circle(self.window, (WHITE), (600,400), 30)
        #self.ball = pygame.draw.circle(self.window, (BLUE), (700,400), 5)
    def run(self):
        self.get_focus()
        self.cooldown()
        #
        #self.draw_background()
        self.visible_sprites.clear(pygame.display.get_surface(),self.window)
        self.visible_sprites.draw(pygame.display.get_surface())
        self.visible_sprites.update()
        
        