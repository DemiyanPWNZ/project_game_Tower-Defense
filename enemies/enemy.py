import os.path

import pygame
import math



class Enemy:

    def __init__(self):

        self.width = 64
        self. height = 64
        self.animation_count = 0
        self.health = 1
        self.vel = 3
        self.path = [(546, 700),(546, 644),  (460, 553),  (660, 366), (737, 310),    (637, 183),  (785, 164),  (623, 135) ,(623, -10)]
        self.x = self.path[0][0]
        self.y = self.path[0][1]
        self.img = None
        self.path_pos = 0
        self.move_count = 0
        self.move_dis = 0
        self.dis  = 0
        self.imgs = []
        self.flipped = False
        self.max_health = 0

    def draw(self, win):
        """
        Draw the enemy with the given image
        :param win: surface
        :return: None
        """

        self.img = self.imgs[self.animation_count]



        win.blit(self.img, (self.x - self.img.get_width()/2, self.y-self.img.get_height()/2))
        self.draw_health_bar(win)

    def draw_health_bar(self, win):
        """
        draw health bar above enemy
        :param win: surface
        :return: None
        """
        length = 50
        move_by = round(length / self.max_health)
        health_bar = move_by * self.health

        pygame.draw.rect(win, (255, 0, 0), (self.x-30, self.y - 35, length, 10), 0)
        pygame.draw.rect(win, (0, 255, 0), (self.x-30, self.y - 35, health_bar, 10), 0)

    def collide(self,X,Y):
        """
        Returns if position has hit enemy
        :param x: int
        :param y:  int
        :return:  BoOl
        """
        if X <= self.x + self.width and X >=self.x:
            if Y <= self.y + self.height and Y >= self.y:
                return True
        return False

    def move(self):
        """
        Move enemy
        :return: None
        """
        self.animation_count += 1
        if self.animation_count >= len(self.imgs):
            self.animation_count = 0
        x1, y1 = self.path[self.path_pos]

        if self.path_pos + 1  >= len(self.path):
            x2, y2 = (613, 125)
        else :
            x2, y2 = self.path[self.path_pos+1]



        dirn = ((x2-x1)*2, (y2-y1)*2)

        length = math.sqrt(((dirn[0]**2) + (dirn[1]**2)))
        dirn = ((dirn[0])/length, (dirn[1])/length)
        if dirn[0] < 0 and not (self.flipped):
            self.flipped = True
            for x, img in enumerate(self.imgs):
                 self.imgs[x] = pygame.transform.flip(img, True, False)
        # else:
        #     if dirn[0] >= 0 and not (self.flipped):
        #         self.flipped = True
        #         for x, img in enumerate(self.imgs):
        #             self.imgs[x] = pygame.transform.flip(img, False, False)

        move_x, move_y = ((self.x + dirn[0]), (self.y + dirn[1] ))

        self.x = move_x
        self.y = move_y

        # Go to next point
        if dirn[0]>=0 :# moving right
            if dirn[1] >=0 :# moving down
                if self.x>= x2 and self.y >= y2:
                    self.path_pos +=1
            else:
                if self.x >= x2 and self.y <= y2:
                    self.path_pos += 1
        else : #moving left
            if dirn[1] >= 0:  # moving down
                if self.x <= x2 and self.y >= y2:
                    self.path_pos += 1
            else:
                if self.x <= x2 and self.y <= y2:
                    self.path_pos += 1
    def hit(self, damage):
        """
        Returns if an enemy has died and removes one health
        each call
        :return: Bool
        """
        self.health -= damage
        if self.health <= 0:
            return True
        return False