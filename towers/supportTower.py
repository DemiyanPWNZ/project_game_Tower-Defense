import pygame
from .tower import Tower
import os
import math
import time

range_imgs = []
for x in range(91):
    add_str = str(x)
    if x < 10:
        add_str = "0" + add_str
    range_imgs.append(pygame.transform.scale(
        pygame.image.load(os.path.join("game_assets/supportTowerRadius", "00" + add_str + ".png")),
        (64, 64)))


class RangeTower(Tower):
    """
    Add extra range to each surrounding tower
    """
    def __init__(self,x ,y):
        super().__init__(x,y)
        self.range = 300
        self.effect = [0.2, 0.4]
        self.tower_imgs = range_imgs[:]
        self.width = self.height = 90
        self.name = "range"

    def draw(self, win):
        super().draw_radius(win)
        super().draw(win)

    def support(self, towers):
        """
        will modify  towers according to abillity
        :param towers: list
        :return:None
        """
        effected = []
        for tower in towers:
            x = tower.x
            y = tower.y

            dis = math.sqrt((self.x-x) ** 2 + (self.y - y) ** 2)

            if dis  <= self.range +  tower.width/2:
                effected.append(tower)

        for tower in effected:
            tower.range = tower.original_range + round(tower.range * self.effect[self.level-1])


damage_imgs = [pygame.transform.scale(pygame.image.load(os.path.join("game_assets","supportTower1.png")),(64,64)),
               pygame.transform.scale(pygame.image.load(os.path.join("game_assets","supportTower2.png")),(64,64))]

class DamageTower(RangeTower):
    """
    add damage to surrounding towers
    """
    def __init__(self, x, y):
        super().__init__(x, y)
        self.range = 300
        self.effect = [0.5, 1]
        self.tower_imgs = damage_imgs[:]
        self.width = self.height = 90
        self.name = "damage"

    def support(self, towers):
        """
        will modify  towers according to ability
        :param towers: list
        :return:None
        """
        effected = []
        for tower in towers:
            x = tower.x
            y = tower.y

            dis = math.sqrt((self.x-x) ** 2 + (self.y - y) ** 2)

            if dis <= self.range + tower.width/2:
                effected.append(tower)

        for tower in effected:
            tower.damage = tower.original_damage + round(tower.damage * self.effect[self.level-1])



