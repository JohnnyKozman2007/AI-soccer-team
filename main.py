import pygame
import field
from player import Player

pygame.init()
pygame.display.set_mode([1200,800])
pygame.display.set_caption("World cup !")


field = field.Field()
done = False

while not done:
    pygame.display.update()
    #events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            
    field.run()
    

    