import pygame
import field
from player import Player

pygame.init()
pygame.display.set_mode([1200,800])
pygame.display.set_caption("World cup !")


field = field.Field(Player(200,400))
done = False
while not done:
    #events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    
    field.input()
    pygame.display.update()