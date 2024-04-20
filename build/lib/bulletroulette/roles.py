# 此文件用于定义角色类
from random import random

class Dealer: # 恶魔
    def __init__(self,health,prop = []) -> None: # 初始化
        self.__tophealth = health
        self.__health = health
        self.__prop = prop

    def gethealth(self) -> int:
        return self.__health

    def smoke(self) -> None:
        if self.__health < self.__tophealth:
            self.__health += 1

    def setprop(self,prop) -> None: # 抽取道具
        self.__prop.append(prop)

    def getprop(self) -> list:
        return self.__prop

    def shoot(self) -> int: # 开枪
        if random() >= 0.5:return 1 # 1：向玩家开枪，0：向自己开枪
        else:return 0

    def useprop(self) -> int: # 使用道具
        '''
        args:None
        return:
        （1：使用道具
            （
            0：不用）
        ）
        '''
        while True:
            rdm = random()
            if rdm <= 0.19: # 啤酒
                if 1 in self.__prop:
                    del self.__prop[self.__prop.index(1)]
                    return 1
            elif rdm <= 0.38: # 烟
                if 2 in self.__prop:
                    del self.__prop[self.__prop.index(2)]
                    return 2
            elif rdm <= 0.57: # 手铐
                if 3 in self.__prop:
                    del self.__prop[self.__prop.index(3)]
                    return 3
            elif rdm <= 0.76: # 小刀
                if 4 in self.__prop:
                    del self.__prop[self.__prop.index(4)]
                    return 4
            elif rdm <= 0.95: # 放大镜
                if 5 in self.__prop:
                    del self.__prop[self.__prop.index(5)]
                    return 5
            else:return 0

    def hurt(self):
        self.__health -= 1
        print("恶魔:啊！！！")
        if self.__health == 0: 
            print("恶魔死了！！！")

class Player: # 人（玩家）
    def __init__(self,health,name,prop = []) -> None: # 初始化（设置血量）
        self.__tophealth = health
        self.__health = health
        self.__name = name
        self.__prop = prop
    
    def smoke(self) -> None:
        if self.__health < self.__tophealth:
            self.__health += 1

    def shoot(self) -> int: # 打出
        return int(input(f"{self.__name}想射："))

    def gethealth(self) -> int:
        return self.__health

    def getprop(self) -> list:
        return self.__prop

    def useprop(self): # 抽取道具
        while True:
            using = int(input(f"使用道具："))
            if using in self.__prop:
                del self.__prop[self.__prop.index(using)]
                return using
            elif using == 0:
                return 0
            else:
                print("没有此道具")

    def setprop(self,prop) -> None: # 抽取道具
        self.__prop.append(prop)

    def hurt(self) -> int: # 受伤
        self.__health -= 1
        print(f"{self.__name}：啊！！！")
        if self.__health == 0:
            print(f"{self.__name}死了！！！")
            raise SystemExit

    def setname(self,name):
        self.__name = name