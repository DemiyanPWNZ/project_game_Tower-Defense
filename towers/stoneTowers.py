import pygame
from .tower import Tower
import os
import math
from menu.menu import Menu

import time

menu_bg = pygame.transform.scale(pygame.image.load(os.path.join("game_assets","Menu.png")),(200,100))
upgrade_btn = pygame.transform.scale(pygame.image.load(os.path.join("game_assets/menu","upgrade.png")),(50, 50))



tower_imgs1 = []
stone_imgs1 = []
# load stone1 tower1 images
for x in range(7, 9):
    tower_imgs1.append(pygame.transform.scale(
        pygame.image.load(os.path.join("game_assets/stonetower/tower1", str(x) + ".png")),
        (90, 90)))
# load stone1 images
for x in range(9, 11):
    stone_imgs1.append(pygame.transform.scale(
        pygame.image.load(os.path.join("game_assets/stonetower/stone1", str(x) + ".png")),(60,32)))


class StoneTower(Tower):
    def __init__(self, x, y):

        super().__init__(x, y)

        self.tower_imgs = tower_imgs1[:]
        self.stone_imgs = stone_imgs1[:]
        self.stone_count = 0
        self.range = 200
        self.original_range = self.range
        self.original_damage = self.damage
        self.inRange = False
        self.left = True
        self.hit_timer = 0
        self.width = self.height = 90
        self.damage = 1
        self.moving = False
        self.name = "stone1"

        self.menu = Menu(self, self.x, self.y, menu_bg, [2000, "MAX"])
        self.menu.add_btn(upgrade_btn, "Upgrade")

    def get_upgrade_cost(self):
        """
        gets the upgrade cost
        :return:int
        """
        return self.menu.get_item_cost()

    def draw(self, win):
        """
        draw the stone tower and animated stone
        :param win:surface
        :return:int
        """
        super().draw_radius(win)
        super().draw(win)
        if self.inRange and not self.moving:
            self.stone_count += 1
            if self.stone_count >= len(self.stone_imgs) * 10:
                self.stone_count = 0
        else:
            self.stone_count = 0

        stone = self.stone_imgs[self.stone_count // 10]
        if self.left == True:
            add = -25
        else:
            add = -stone.get_width()+10
        win.blit(stone, ((self.x  + add), (self.y - 25)))



    def change_range(self,r):
        """
        change range of stone1 tower1
        :param r: int
        :return: None
        """
        self.range = r

    def attack(self, enemies):
        """
        attacks an anemy in the enemy list, modifies the list

        :param enemies: list of enemies
        :return: None
        """
        money = 0
        self.inRange = False
        enemy_closest = []

        for enemy in enemies:
            x = enemy.x
            y = enemy.y

            dis = math.sqrt((self.x - x)**2 +(self.y- y)**2)
            if dis < self.range:
                self.inRange = True
                enemy_closest.append(enemy)

        enemy_closest.sort(key=lambda x : x.path_pos)
        enemy_closest = enemy_closest[::-1]
        if len(enemy_closest)>0:
            first_enemy = enemy_closest[0]
            if self.stone_count == 2:

                if first_enemy.hit(self.damage) == True:
                    money = first_enemy.money
                    enemies.remove(first_enemy)

            if first_enemy.x > self.x and not (self.left):
                self.left = True
                for x, img in enumerate(self.stone_imgs):
                    self.stone_imgs[x] = pygame.transform.flip(img, True, False)
            elif self.left and first_enemy.x < self.x:
                self.left = False
                for x, img in enumerate(self.stone_imgs):
                    self.stone_imgs[x] = pygame.transform.flip(img, True, False)

        return money

tower_imgs = []
stone_imgs = []
# load stone1 tower1 images
for x in range(15, 18):
    tower_imgs.append(pygame.transform.scale(
        pygame.image.load(os.path.join("game_assets/stonetower/tower2", str(x) + ".png")),
        (90, 90)))
# load stone1 images
for x in range(18, 20):
    stone_imgs.append(pygame.transform.scale(
        pygame.image.load(os.path.join("game_assets/stonetower/stone2", str(x) + ".png")), (60,32)))

class StoneTowerShort(StoneTower):
    def __init__(self, x, y):

        super().__init__(x, y)

        self.tower_imgs = tower_imgs[:]
        self.stone_imgs = stone_imgs[:]
        self.stone_count = 0
        self.range = 150
        self.original_range = self.range
        self.original_damage = self.damage
        self.inRange = False
        self.left = True
        self.hit_timer = 0
        self.width = self.height = 90
        self.damage = 2
        self.name = "stone2"
        self.menu = Menu(self, self.x, self.y, menu_bg, [3000, "MAX"])
        self.menu.add_btn(upgrade_btn, "Upgrade")

