import pygame
from settings import *

class Player:
    iq = 0
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.body = {}
        self.window = pygame.display.get_surface()
        self.decision = None
        self.body['body'] = pygame.draw.circle(self.window, (RED), (200,200),30)
    def draw(self,x,y):
        Player.iq += 1
        #pygame.draw.circle(self.window, (RED), (x,y),30)
        for i,v in self.body.items():
            if Player.iq < 5:
                print(self.body[i].x)
            self.body[i].x += x 
            self.body[i].y += y
            if self.body[i].x > 1:
                print(self.body[i].x)
                print(self.body)
            self.body[i] = pygame.draw.circle(self.window, (RED), (self.body[i].x,self.body[i].y),30)
        if Player.iq < 5:
            print(self.body)    


            

         