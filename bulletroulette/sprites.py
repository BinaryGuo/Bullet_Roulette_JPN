# 此文件用于声明用于pygame的类
import pygame
from bulletroulette.data import *

class Button:
    def __init__(self,x,y,image,mode = 0):
        self.image = image
        self.location = self.image.get_rect()
        if mode == 0:
            self.location.topleft = (x,y)
        else:
            self.location.center = (x,y)
            x = self.location.topleft[0]
            y = self.location.topleft[1]
        self.framelocation = pygame.Rect(x-5, y-5, self.image.get_width()+10, self.image.get_height()+10)
        self.clicked = False
    
    def run(self,screen):
        screen.blit(self.image,self.location)
        mouselocation = pygame.mouse.get_pos()
        if self.location.collidepoint(mouselocation):
            pygame.draw.rect(screen,RED,self.framelocation,5)
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                return 1
            else:
                self.clicked = False
                return 0