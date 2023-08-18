import pygame
import random
import field

class Enemy(pygame.sprite.Sprite):
    game_started = False
    def __init__(self,x,y,groups,opening = False,id = 0,ball = None):
        super().__init__(groups)
        self.id = id
        self.x = x
        self.y = y
        self.speed = 60
        self.ai_action_allowed = True
        self.ai_action_allowed_time = pygame.time.get_ticks()
        self.instruction = None


        self.body = {}
        self.have_ball = None
        self.decision = None
        self.strike = False
        self.have_ball = None
        self.pass_allow = True
        self.shoot_allow = True
        self.passed_to = False
        self.change_pass = pygame.time.get_ticks()
        self.window = pygame.display.get_surface()
        self.decision = None
        self.image = pygame.image.load("C:\\Users\\Sidho\\OneDrive\\Desktop\\soccer\\graphics\\Messi_2.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (200, 100))
        if opening:
            self.rect = self.image.get_rect(topleft = (0,0))
        else:
            self.rect = self.image.get_rect(topleft = (x,y))
        self.direction = pygame.math.Vector2()
        self.done = opening
        self.d = 10
        self.strike = False
        self.passed_to = False
        self.shoot_allow = False
    def get_rect(self):
        return self.rect
    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0
        self.speed = 1.2
    def border(self):
        if self.rect.x > 1070: 
            self.rect.x = 1070
        if self.rect.x <-80:
            self.rect.x = -80

        if self.rect.y > 700 :
            self.rect.y = 700
        if self.rect.y <0:
            self.rect.y = 0


    def shooting(self):
        if self.have_ball:
            self.shoot_player = pygame.time.get_ticks()
            self.have_ball = False
            self.shoot_allow = False
            self.strike = True
    def move(self,x=0,y=0):
        if x != 0 or y != 0:
            self.rect.y = y
            self.rect.x = x
        #print(self.direction.x,self.direction.y)
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
            #print('ya zmeky')
        self.rect.y += self.direction.y * self.speed
        self.rect.x += self.direction.x * self.speed
        
        #self.rect.center += self.direction * 1.2
    def follow(self,x,y):
        try:
            self.speed = 60
            #print()
            if (x - self.rect.x) > 30:
                self.direction.x = 1
                self.move()
                self.direction.x = 0
            elif (y - self.rect.x) < -30:
                self.direction.x = -1
                self.move()
                self.direction.x = 0
            else:
                pass

            # y_plus_div = (y - self.rect.y)/self.speed
            # y_plus = (y - self.rect.y)/y_plus_div

            if (y - self.rect.y) > 30:
                self.direction.y = 1
                self.move()
                self.direction.y = 0
            elif (y - self.rect.y) < -30:
                self.direction.y = -1
                self.move()
                self.direction.y = 0
            else:
                pass

            # print(x_plus,x_plus_div,x - self.rect.x)
            # print(y_plus,y_plus_div,y - self.rect.y)
            
            

            
            #print("done")
            #print()
            #print(self.rect.y - y,(int(abs(self.rect.y - y)/self.speed)),self.rect.y - y/int((abs(self.rect.y - y)/self.speed)))
            
            
        except Exception as e:
            print(e)
    def know_team(self,p2,p3):
        self.teamates = [p2,p3]
    def pass_to_teammate(self,closer):
        self.change_pass = pygame.time.get_ticks()
        self.have_ball = False
        self.pass_allow = False
        self.passing_to = closer
        closer.passed_to = True
    def preform_move(self,action):
        
        if self.ai_action_allowed:
            self.ai_action_allowed_time = pygame.time.get_ticks()
            #print(9)
            self.ai_action_allowed = False
            #print(main.id)
            #print(main.rect.x,main.rect.y,'before')
            if self.have_ball:
                if action[0] == 1:
                    self.pass_to_teammate(self.teamates[0])
                elif action[1] == 1:
                    self.pass_to_teammate(self.teamates[1])
                elif action[2] == 1:
                    self.shooting()
            elif action[3] == 1:
                self.rect.x += 80
                #main.rect.x = 1
                #print("right")
            elif action[4] == 1:
                self.rect.x -= 80
                #main.rect.x = -1
                #print("left")
            elif action[5] == 1:
                self.rect.y += 60
                #main.rect.y = 1
                #print('down')
            elif action[6] == 1:
                
                self.rect.y -= 60
                
                #main.rect.y = -1
            pygame.display.update(self)
            #print(self.rect.x,self.rect.y)
            #print(self.rect.x,main.rect.y,'after')
    def update(self,final_move = False):
        
        if not Enemy.game_started:
            return
        if field.Field.FOCUS == self.id:
            self.input()
        self.move()
        self.border()
        if final_move:
            self.preform_move(final_move)
            #final_move)
        pygame.display.update()


