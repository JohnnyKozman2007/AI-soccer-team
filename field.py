import pygame
from settings import *

class Field:
    def __init__(self,team):
        
        self.team = [team] 
        
        #window
        self.window = pygame.display.get_surface()

        pygame.draw.rect(self.window, (GREEN),(0,0,1200,800))
        pygame.draw.rect(self.window, (WHITE),(5,5,1190,790),10)


        
        pygame.draw.rect(self.window, (WHITE),(1115,295,80,200),10)


        pygame.draw.rect(self.window, (WHITE),(5,295,80,200),10)



        self.net_r = pygame.draw.rect(self.window, (WHITE),(1155,350,40,100),10)
        self.net_l = pygame.draw.rect(self.window, (WHITE),(5,350,40,100),10)
        pygame.draw.line(self.window, (WHITE), (600, 5), (600, 794),10)
        pygame.draw.circle(self.window, (WHITE), (600,400), 30)
        self.ball = pygame.draw.circle(self.window, (BLUE), (600,400), 15)

        self.objects = [self.ball,self.team]
    
    def input(self):
        keys = pygame.key.get_pressed()

        # movement input
        x,y = 0,0
        if keys[pygame.K_UP]:
            y = -30
        elif keys[pygame.K_DOWN]:
            y = 30
        else:
            y = 0
        if keys[pygame.K_RIGHT]:
            x = 30
        elif keys[pygame.K_LEFT]:
            x = -30
        else:
            x = 0
        self.update(x,y)
    def update(self,x,y):
        for i in self.objects:
            if type(i) == list:
                for player in i:
                    player.draw(x,y)
            else:
                pass
        #pygame.draw.rect(self.window, (GREEN),(0,0,1200,800))
        #pygame.draw.rect(self.window, (WHITE),(0,500,119,79),10)
