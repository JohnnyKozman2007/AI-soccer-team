import pygame
import random

class Mind(pygame.sprite.Sprite):
    def __init__(self,x,y,groups,opening = False,id = 0,ball = None):
        super().__init__(groups)
        self.id = id
        self.x = x
        self.y = y
        self.body = {}
        self.have_ball = None
        self.window = pygame.display.get_surface()
        self.decision = None
        self.image = pygame.image.load("C:\\Users\\Sidho\\OneDrive\\Desktop\\soccer\\graphics\\ronaldo.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (300, 200))
        if opening:
            self.rect = self.image.get_rect(topleft = (0,0))
        else:
            self.rect = self.image.get_rect(topleft = (x,y))
        self.direction = pygame.math.Vector2()
        self.done = opening
        self.d = 10
    def move(self):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.rect.y += self.direction.y * 1.2
        self.rect.x += self.direction.x * 1.2
        #self.rect.center += self.direction * 1.2
    
    def pick_move(self):
        pass
    def update(self):
        self.pick_move()
        self.move()
        pass
        #if self.done:
        #    self.opening()
        #else:
        #    if field.Field.FOCUS == self.id:
        #        self.input()
        #    self.move()
        #    self.border()
