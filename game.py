import os.path
from enemies.club import Club
from enemies.ork import Ork
from enemies.wizard import Wizard
import pygame
from towers.stoneTowers import StoneTower, StoneTowerShort
from towers.supportTower import DamageTower, RangeTower
import os
import time
import math
import numpy as np
import matplotlib.pyplot as plt
from menu.menu import VerticalMenu, PlayPauseButton
import random


pygame.font.init()
pygame.init()

path = [(546, 700),(546, 644),  (460, 553),  (660, 366), (737, 310),    (637, 183),  (785, 164),  (623, 135) ,(623, -10)]


lifes_img = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "heart.png")), (48, 48))
star_img = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "star.png")), (50, 50))
side_img = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "side.png")), (200, 500))


buy_stone1 = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "stone1.png")), (50, 50))
buy_stone2 = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "stone2.png")), (50, 50))
buy_damage = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "buy_damage.png")), (50, 50))
buy_range = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "buy_range.png")), (50, 50))

play_btn = pygame.transform.scale(pygame.image.load(os.path.join("game_assets/menu", "play_button.png")), (150, 50))
pause_btn = pygame.transform.scale(pygame.image.load(os.path.join("game_assets/menu", "pause_button.png")), (150, 50))

wave_bg = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "wave_bg.png")), (250, 100))


attack_tower_names = ["stone1", "stone2"]
support_tower_names = ["damage", "range"]

#load music
#pygame.mixer.music.load(os.path.join("game_assets", "music.mp3"))

#waves are in form
#frequency of enemies
# (#ork, #wizard, #clubs)

waves = [
    [20, 0, 0],
    [50, 0, 0],
    [100, 0, 0],
    [0, 20, 0],
    [0, 50, 0],
    [0, 100, 0],
    [20, 100, 0],
    [50, 100, 0],
    [100, 100, 0],
    [0, 0, 50],
    [20, 0, 100],
    [20, 0, 150],
    [200, 100, 200],
]

class Game:

    def __init__(self):
        self.width = 1350
        self.height = 700
        self.win = pygame.display.set_mode((self.width, self.height))
        self.enemys = []
        self.attack_towers = []
        self.support_towers = []
        self.lives = 10
        self.money = 1000
        self.bg = pygame.image.load(os.path.join("game_assets", "bg.png"))
        self.bg = pygame.transform.scale(self.bg, (self.width, self.height))
        self.clicks = [] # remove
        self.timer = time.time()
        self.life_font = pygame.font.SysFont("comicsans", 50)
        self.selected_tower = None
        self.menu = VerticalMenu(self.width - side_img.get_width() + 100, 150, side_img)
        self.menu.add_btn(buy_stone1, "buy_stone1", 300)
        self.menu.add_btn(buy_stone2, "buy_stone2", 500)
        self.menu.add_btn(buy_damage, "buy_damage", 200)
        self.menu.add_btn(buy_range, "buy_range", 400)
        self.wave = 0
        self.current_wave = waves[self.wave][:]
        self.pause = True
        self.playPauseButton = PlayPauseButton(play_btn, pause_btn, 10, self.height - 85)

        self.moving_object = None


    def gen_enemies(self):
        """
        generate the next enemy or enemies to show
        :return: enemy
        """
        if sum(self.current_wave)== 0 :
            if len(self.enemys) == 0:
                self.wave +=1
                self.current_wave = waves[self.wave]
                self.pause = True
                self.playPauseButton.paused = self.pause
        else:
            wave_enemies = [Ork(), Wizard(), Club()]
            for x in range(len(self.current_wave)):
                if self.current_wave[x] != 0:
                    self.enemys.append(wave_enemies[x])
                    self.current_wave[x] = self.current_wave[x] - 1
                    break



    def run(self):
       # pygame.mixer.music.play(1)
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(100)

            if self.pause == False:
                #gen monsters
                if time.time() - self.timer >= random.randrange(1,5)/2:
                    self.timer = time.time()
                    self.gen_enemies()

            pos = pygame.mouse.get_pos()

            #check for moving object
            if self.moving_object:
                self.moving_object.move(pos[0], pos[1])
                tower_list = self.attack_towers[:] + self.support_towers[:]
                collide = False
                for tower in tower_list:
                    if tower.collide(self.moving_object):
                        collide = True
                        tower.place_color = (255, 0, 0, 100)
                        self.moving_object.place_color = (255, 0, 0, 100)
                    else:
                        tower.place_color = (0, 0, 255, 100)
                        if not collide:
                            self.moving_object.place_color = (0, 0, 0, 100)

            # main event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False


                if event.type == pygame.MOUSEBUTTONUP:
                    #if you'ra moving an object and click

                    if self.moving_object:
                        not_allowed = False
                        tower_list = self.attack_towers[:] + self.support_towers[:]
                        for tower in tower_list:
                            if tower.collide(self.moving_object) :
                                not_allowed = True


                        if not not_allowed and self.point_to_line(self.moving_object):

                            if self.moving_object.name in attack_tower_names:
                                self.attack_towers.append(self.moving_object)
                            elif self.moving_object.name in support_tower_names:
                                self.support_towers.append(self.moving_object)

                            self.moving_object.moving = False
                            self.moving_object = None
                    else:
                        #check for plar or pause
                        if self.playPauseButton.click(pos[0],pos[1]):
                            self.pause = not(self.pause)
                            self.playPauseButton.paused = self.pause



                        #look if you click on side menu
                        side_menu_button = self.menu.get_clicked(pos[0],pos[1])
                        if side_menu_button:
                            cost = self.menu.get_item_cost(side_menu_button)
                            if self.money >= cost:
                                self.money -= cost
                                self.add_tower(side_menu_button)

                        #look if you clicked on btn
                        btn_clicked = None
                        if self.selected_tower :
                            btn_clicked = self.selected_tower.menu.get_clicked(pos[0],pos[1])
                            if btn_clicked :
                                print(btn_clicked)
                                if btn_clicked == "Upgrade":
                                    cost = self.selected_tower.get_upgrade_cost()
                                    if self.money >= cost:
                                        self.money -= cost
                                        self.selected_tower.upgrade()


                        if not (btn_clicked):
                            #look if you click on attack towers
                            for tw in self.attack_towers:
                                if tw.click(pos[0],pos[1]):
                                    tw.selected = True
                                    self.selected_tower = tw
                                else:
                                    tw.selected = False
                            # look if you click on support towers
                            for tw in self.support_towers:
                                if tw.click(pos[0], pos[1]):
                                    tw.selected = True
                                    self.selected_tower = tw
                                else:
                                    tw.selected = False

            if not(self.pause):
                # loop  throught enemoes
                to_del = []
                for en in self.enemys:
                    en.move()
                    if en.y < -5:
                        to_del.append(en)

                # delete all enemies off the screen
                for d in to_del:
                    self.lives -= 1
                    self.enemys.remove(d)


                # loop through  attack_towers
                for tw in self.attack_towers:
                    self.money += tw.attack(self.enemys)

                # loop through  support _towers
                for tw in self.support_towers:
                    tw.support(self.attack_towers)
                #if you lose
                if self.lives <= 0:
                    print("You lose")
                    run = False

            self.draw()



        pygame.quit()

    def point_to_line(self, tower):
        """
        returns if you can place tower based on distance from path
        :param tower: Tower
        :return: Bool
        """

        # find two closest points
        return True

    def draw(self):
        self.win.blit(self.bg, (0, 0))
        # draw pacement rings
        if self.moving_object:
            for tower in self.attack_towers:
                tower.draw_placement(self.win)

            for tower in self.support_towers:
                tower.draw_placement(self.win)

            self.moving_object.draw_placement(self.win)


        # draw attack_towers

        for tw in self.attack_towers:
            tw.draw(self.win)

        # draw support_towers

        for tw in self.support_towers:
            tw.draw(self.win)
        # draw enemies

        for en in self.enemys:
            en.draw(self.win)

        #redraw selected tower
        if self.selected_tower:
            self.selected_tower.draw(self.win)


        #draw moving object
        if self.moving_object:
            self.moving_object.draw(self.win)


        #draw menu
        self.menu.draw(self.win)
        #draw play pause button
        self.playPauseButton.draw(self.win)

        #draw lives
        text = self.life_font.render(str(self.lives),1,(255, 255, 255))
        life = lifes_img
        start_x = self.width - life.get_width() -10

        self.win.blit(text, (start_x-text.get_width()-5, 5))
        self.win.blit(life, (start_x, 10))

        # draw money
        text = self.life_font.render(str(self.money), 1, (255, 255, 255))
        money = star_img
        start_x = self.width - life.get_width() - 10

        self.win.blit(text, (start_x - text.get_width() - 5, 70))
        self.win.blit(money, (start_x, 75))

        #draw wave
        self.win.blit(wave_bg, (10, 10))
        text = self.life_font.render("Wave #" + str(self.wave),1, (255,255,255))
        self.win.blit(text, (10+ wave_bg.get_width()/2 - text.get_width()/2, 20))

        pygame.display.update()



    def add_tower(self, name):
        x, y = pygame.mouse.get_pos()
        name_list = ["buy_stone1","buy_stone2", "buy_damage", "buy_range"]
        object_list = [StoneTower(x,y), StoneTowerShort(x,y), DamageTower(x,y), RangeTower(x,y)]
        try:
            obj = object_list[name_list.index(name)]
            self.moving_object = obj
            obj.moving = True
        except Exception as e:
            print(str(e) + "NOT VALID NAME")


# win = pygame.display.set_mode((1350, 700))
# g = Game()
# g.run()
