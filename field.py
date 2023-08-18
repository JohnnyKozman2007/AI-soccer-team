import pygame
import copy
from settings import *
from player import Player
from enemy import Enemy
from tkinter import messagebox
import ball
import time
from control_AI import Agent
from helper import plot
import random

class Field:
    FOCUS = 2   
    def __init__(self,background =None):
        self.done = False  
        self.record = 0 
        self.goal = 0
        
        self.plot_scores = []
        self.plot_mean_scores = []
        self.total_score = 0
        self.enemy_score = 0 
        self.player_score = 0
        self.team = None
        self.background = background
        self.change_allow = True
        self.switch_duration_cooldown = 200
        #window
        self.window = pygame.Surface((1200, 800))
        self.visible_sprites = pygame.sprite.Group()
        self.ai_action_allowed_time = pygame.time.get_ticks()
        self.ai_action_allowed = True


        self.a = pygame.draw.rect(self.window, (GREEN),(0,0,1200,800))
        self.outline = pygame.draw.rect(self.window, (WHITE),(5,5,1190,790),10)


        
        self.goal_ai_area = pygame.draw.rect(self.window, (WHITE),(1115,295,80,200),10)


        self.goal_player_area = pygame.draw.rect(self.window, (WHITE),(5,295,80,200),10)



        self.goal_ai = pygame.draw.rect(self.window, (WHITE),(1155,350,40,100),10)
        self.goal_player = pygame.draw.rect(self.window, (WHITE),(5,350,40,100),10)
        
        self.e = pygame.draw.line(self.window, (WHITE), (600, 5), (600, 794),10)
        self.r = pygame.draw.circle(self.window, (WHITE), (600,400), 30)
        self.r2 = pygame.draw.circle(self.window, (GREEN), (600,400), 20)
        
        
        self.make_team()
        self.make_enemy()
        
        self.players_enemies = self.team + self.enemy
        self.ball = ball.Ball(570,370,self.visible_sprites,self.team,self.enemy)#pygame.draw.circle(self.window, (BLUE), (600,400), 12)
        self.objects = [self.ball,self.team,self.enemy]
        self.ai_action_allowed_time = pygame.time.get_ticks()
        self.ai_action_allowed = True
        #
        #self.ai = Agent(self.enemy,self.ball,self.team)

        #self.ai = Control(self.enemy,self.team,self.ball) 
        self.agent = Agent(self.enemy,self.ball,self.team)
        self.last_moved = self.team[0]
        #self.game = main.field
    # def preform_move(self,action,main):
    #     main.ai_action_allowed_time = pygame.time.get_ticks()
    #     if main.ai_action_allowed:
    #         print(9)
    #         main.ai_action_allowed = False
    #         #print(main.id)
    #         #print(main.rect.x,main.rect.y,'before')
    #         if main.have_ball:
    #             if action[0] == 1:
    #                 main.pass_to_teammate(main.teamates[0])
    #             elif action[1] == 1:
    #                 main.pass_to_teammate(main.teamates[1])
    #             elif action[2] == 1:
    #                 main.shooting()
    #         elif action[3] == 1:
    #             main.rect.x += 80
    #             #main.rect.x = 1
    #             #print("right")
    #         elif action[4] == 1:
    #             main.rect.x -= 80
    #             #main.rect.x = -1
    #             #print("left")
    #         elif action[5] == 1:
    #             main.rect.y += 60
    #             #main.rect.y = 1
    #             #print('down')
    #         elif action[6] == 1:
                
    #             main.rect.y -= 60
                
    #             #main.rect.y = -1
    #         print(main.rect.x,main.rect.y,'after')
    def make_team(self):
        self.p1 = Player(200,100,self.visible_sprites,id = 1)
        self.p2 = Player(0,350,self.visible_sprites,opening = True,id = 2)
        self.p3 = Player(200,600,self.visible_sprites,id = 3)
        self.team = [self.p1,self.p2,self.p3]
        self.p1.know_team(self.p2,self.p3)
        self.p2.know_team(self.p1,self.p3)
        self.p3.know_team(self.p1,self.p2)

        for player in self.team:
            self.visible_sprites.add(player)
    def make_enemy(self):
        self.e1 = Enemy(740,100,self.visible_sprites,id = 1)
        self.e2 = Enemy(940,350,self.visible_sprites,id = 2)
        self.e3 = Enemy(740,600,self.visible_sprites,id = 3)
        self.enemy = [self.e1,self.e2,self.e3]

        self.e1.know_team(self.e2,self.e3)
        self.e2.know_team(self.e1,self.e3)
        self.e3.know_team(self.e1,self.e2)
        for player in self.enemy:
            self.visible_sprites.add(player)
            
        #print(self.visible_sprites)
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
                current_time = pygame.time.get_ticks()
        if not self.ai_action_allowed:
            if current_time - self.ai_action_allowed_time >= self.switch_duration_cooldown:
                self.change_allow = True
                current_time = pygame.time.get_ticks()
        for player in self.enemy:
            if not player.ai_action_allowed:
                if current_time - player.ai_action_allowed_time>= 600:
                    player.ai_action_allowed = True
                    current_time = pygame.time.get_ticks()                
        # if not self.ai.run_allow:
        #     if current_time - self.ai.run_cooldown >= self.switch_duration_cooldown+1000:
        #         self.ai.run_allow = True
        for player in self.team:                
            if not player.shoot_allow:
                if current_time - player.shoot_player >= self.switch_duration_cooldown:
                    player.shoot_allow = True 
                               
                
        for player in self.team:
            
            if current_time - player.change_pass > self.switch_duration_cooldown:
                # self.last_have_ball()
                #player.passed_to = False
                #player.pass_allow = True
                if not player.pass_allow:
                    player.pass_allow = True
                    player.have_ball = False
                    player.passing_to.passed_to = False
                    


        for player2 in self.enemy:
            
            if current_time - player2.change_pass > self.switch_duration_cooldown+800:
                #player.passed_to = False
                #player.pass_allow = True
                if not player2.pass_allow:
                    player2.pass_allow = True
                    player2.have_ball = False
                    player2.passing_to.passed_to = False    
                    #print('cooldown')  
        # for player in self.team:
        #     if player.passing_to != None:
        #         player.passing_to.have_ball = True
            #print(i.id,i.have_ball)          
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
    # def ball_owner(self):
    #     x = 1
    #     self.all_players = self.team + self.enemy
    #     for i in self.all_players:
            
    #         if i.have_ball:
    #             return x
    #         x += 1
    def reset(self,on = False):
        if not on:
           self.enemy_score = 0
           self.player_score = 0
           
        self.p1.rect.x = 200
        self.p1.friendly_start = True
        self.p1.rect.y = 100
        self.p2.rect.x = 0 
        self.p2.rect.y = 350 
        self.p3.rect.x = 200
        self.p3.rect.y = 600 

        self.e1.rect.x = 740
        self.e1.rect.y = 100
        self.e2.rect.x = 940
        self.e2.rect.y = 350 
        self.e3.rect.x = 740
        self.e3.rect.y = 600 
        self.ball.rect.x = 570 
        self.ball.rect.y = 370
    def enemy_ball_owner(self):
        for player in self.enemy:
            if player.have_ball:
                return player
    def evaluate_move(self):
        player = self.enemy_ball_owner()
        if player != None:
            d1 = pygame.math.Vector2 (player.rect.x, player.rect.y).distance_to ((self.team[0].rect.x, self.team[0].rect.y))
            d2 = pygame.math.Vector2 (player.rect.x, player.rect.y).distance_to ((self.team[1].rect.x, self.team[1].rect.y))
            d3 = pygame.math.Vector2 (player.rect.x, player.rect.y).distance_to ((self.team[2].rect.x, self.team[2].rect.y))
            x = min(d1,d2,d3)
            goal = copy.deepcopy(self.goal)
            self.goal = 0


            if x < 1:
                x = 1
            #print(((1200/self.ball.rect.x)*100)*2 + (x/100)*100 + goal)
            return ((1200/self.ball.rect.x)*100)*2 + (100/x)*100 + goal 
        else:
            d1 = pygame.math.Vector2 (self.enemy[0].rect.x, self.enemy[0].rect.y).distance_to ((self.team[0].rect.x, self.team[0].rect.y))
            d2 = pygame.math.Vector2 (self.enemy[0].rect.x, self.enemy[0].rect.y).distance_to ((self.team[1].rect.x, self.team[1].rect.y))
            d3 = pygame.math.Vector2 (self.enemy[0].rect.x, self.enemy[0].rect.y).distance_to ((self.team[2].rect.x, self.team[2].rect.y))
            x = min(d1,d2,d3)

            d1 = pygame.math.Vector2 (self.enemy[1].rect.x, self.enemy[1].rect.y).distance_to ((self.team[0].rect.x, self.team[0].rect.y))
            d2 = pygame.math.Vector2 (self.enemy[1].rect.x, self.enemy[1].rect.y).distance_to ((self.team[1].rect.x, self.team[1].rect.y))
            d3 = pygame.math.Vector2 (self.enemy[1].rect.x, self.enemy[1].rect.y).distance_to ((self.team[2].rect.x, self.team[2].rect.y))
            y = min(d1,d2,d3)

            d1 = pygame.math.Vector2 (self.enemy[2].rect.x, self.enemy[2].rect.y).distance_to ((self.team[0].rect.x, self.team[0].rect.y))
            d2 = pygame.math.Vector2 (self.enemy[2].rect.x, self.enemy[2].rect.y).distance_to ((self.team[1].rect.x, self.team[1].rect.y))
            d3 = pygame.math.Vector2 (self.enemy[2].rect.x, self.enemy[2].rect.y).distance_to ((self.team[2].rect.x, self.team[2].rect.y))
            z = min(d1,d2,d3)
            try:
                #print(((1000/x) * (1000/y) * (1000/z)))
                return (((1000/x) * (1000/y) * (1000/z)))
            except:
                return 0


    def score(self):
        if self.player_score >= 3 or self.enemy_score >= 3:
            self.reset(on = True)
            self.done = True
            if self.player_score >= 3:
                messagebox.showinfo("showinfo", "Human wins !")
            else:
                messagebox.showinfo("showinfo", "AI wins !")
        if self.ball.rect.x > 1148 and self.ball.rect.y > 290 and self.ball.rect.y < 390:
            self.player_score += 1
            self.goal = 500
            self.reset(on = True)
            #print(self.player_score,":",self.enemy_score)
            my_font = pygame.font.SysFont('Comic Sans MS', 80)
            score_board = str(self.player_score) + ':' + str(self.enemy_score)
            text_surface = my_font.render(score_board, True, (250, 250, 250))
            
            messagebox.showinfo("showinfo", score_board)
            #print(1111111)
        if self.ball.rect.x < 10 and self.ball.rect.y > 290 and self.ball.rect.y < 390 :
            self.enemy_score += 1
            self.goal = 500
            #print(self.player_score,":",self.enemy_score,2)
            self.reset(on = True)
            my_font = pygame.font.SysFont('Comic Sans MS', 80)
            score_board = str(self.player_score) + ':' + str(self.enemy_score)
            #text_surface = my_font.render(score_board, True, (250, 250, 250))
            messagebox.showinfo("showinfo", score_board)
            #print(2222222)
            #self.window.blit(text_surface, (540,0))
            pygame.display.update()
#This creates a new surface with text already drawn onto it. At the end you can just blit the text surface onto your main screen.

#screen.blit(text_surface, (0,0))
    def make_decision(self):
        score = 0
        for player in self.agent.team:
            
            #print('entered yasta el zkaa el sna3y')
            state_old = self.agent.get_state()
            #print(state_old)
            # get move
            final_move = self.agent.get_action(state_old)

            # perform move and get new state
           
            
            #self.preform_move(final_move,player)
            player.update(final_move)
            
            reward, done, score = self.evaluate_move(),self.done,self.enemy_score  # evaluate move
            state_new = self.agent.get_state()

            # train short memory
            self.agent.train_short_memory(state_old, final_move, reward, state_new, done)

            # remember
            self.agent.remember(state_old, final_move, reward, state_new, done)

            
            if self.done:
                # train long memory, plot result
                score = copy.deepcopy(self.enemy_score)

                self.reset()
                self.agent.n_games += 1
                self.agent.train_long_memory()
                self.done = False

                
                record = score
                self.agent.model.train()
                self.agent.model.save(self.agent.model)
                    

                # print('Game', self.agent.n_games, 'Score', score, 'Record:', self.record)

                # self.plot_scores.append(score)
                # self.total_score += score
                # mean_score = self.total_score / self.agent.n_games
                # self.plot_mean_scores.append(mean_score)
                # plot(self.plot_scores, self.plot_mean_scores)
        self.score()
        self.run(False)
        pygame.display.update()
        

    def run(self,display_only = True):
        
        
        self.get_focus()
        
        self.cooldown()
        
        # 
        #self.draw_background()

        
        self.visible_sprites.clear(pygame.display.get_surface(),self.window)
        self.visible_sprites.draw(pygame.display.get_surface())
        self.visible_sprites.update()
        if display_only:
            #for i in self.enemy:
                #print(i.rect.x,i.rect.y,"before")
            self.make_decision()
                #print(i.rect.x,i.rect.y,"after")
        else:
            self.visible_sprites.clear(pygame.display.get_surface(),self.window)    
            self.visible_sprites.draw(pygame.display.get_surface())
            self.visible_sprites.update()
            
            #print("graphics only")
            
        # self.ai.update()
        
        

        
        
        
        
        