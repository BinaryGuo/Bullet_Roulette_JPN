# 主程序（没错，运行它！）
__version__ = "1.0" # 版本说明（没什么用）

# 外部导入
cannotuseGUI = False
from random import shuffle
from time import sleep
import pygame
from os import chdir,path
from traceback import print_exc
# 模块导入
from bulletroulette.roles import *
from bulletroulette.data import *
from bulletroulette.sprites import *
# 以下是主程序
chdir(path.dirname(__file__))
health = [2,4,6]
buckshots = [ # 子弹（1代表实，0代表空）
        [
            [1,0,0],
            [1,1,0,0]
        ],
        [
            [1,0],
            [1,1,0,0,0],
            [1,1,1,0,0,0],
            [1,1,1,1,0,0,0,0]
        ],
        [
            [1,1,1,1,1,0,0,0],
            [1,1,1,1,0,0,0,0],
            [1,1,1,0],
            [1,1,1,1,0,0,0,0]
        ]
    ]
def run():
    try:
        if cannotuseGUI:
            mode = 2
        else:
            mode = int(input("请选择模式（壳程序按0（更为稳定）,窗口按1（游戏体验更好））:"))
        if mode:
            FPS = int(input("请设置帧率（如果设的太高您的计算机可能运行不了，区间：1～200）："))
            assert FPS >= 1 and FPS <= 200,"FPS out of range"
            pygame.init()
            # 以下是一些关于pygame的一些常量声明
            # 以下是初始化
            clock = pygame.time.Clock() # 初始化时钟
            screen = pygame.display.set_mode((1400,850)) # 屏幕（窗口）初始化
            pygame.display.set_caption("Buckshot Roulette") # 设置标题
            background = pygame.image.load(BACKGROUND) # 加载背景图
            gunimage = pygame.image.load(GUN) # 加载霰弹枪图片
            charge = pygame.image.load(CHARGE) # 加载血量图片
            blank = pygame.image.load(BLANK) # 加载空弹图片
            liveround = pygame.image.load(LIVEROUND) # 加载实弹图片
            dealershootself = pygame.image.load(SHOOTSELF) # 加载恶魔射击自己时的图片
            dealershootplayer = pygame.image.load(SHOOTPLAYER) # 加载恶魔射击玩家时的图片
            buckshotlocation = blank.get_rect() # 获取子弹显示位置
            shootlocation = dealershootself.get_rect() # 获取恶魔射击时的位置
            chargelocation = charge.get_rect() # 获取血量显示位置
            gunimage.set_alpha(0) # 完全透明（此图是为了绘制边框）
            gun = Button(675,300,gunimage,1) # 加载按钮（Button类的定义在sprites.py)
            pygame.mixer.music.load(BGM) # 加载背景音乐（BGM）
            liveplayermusic = pygame.mixer.Sound(LIVEPLAYER) # 玩家被击中时的音效
            livedealermusic = pygame.mixer.Sound(LIVEDEALER) # 恶魔被击中时的音效
            blankmusic = pygame.mixer.Sound(BLANKMUSIC) # 空弹发射时的音效
            shootlocation.center = (700,300) # 设置恶魔射击时的位置
            text = pygame.font.Font(FONT,75) # 设定字体
            nametext = text.render("Enter name:",False,WHITE) # 用字体生成文字
            playerlose = text.render("dealer win!",False,WHITE) # 用字体生成文字
            loseorwinlocation = playerlose.get_rect()
            loseorwinlocation.center = (700,425)
            nametextlocation = nametext.get_rect()
            nametextlocation.center = (700,100)
            shootdealer = Button(700,75,text.render("DEALER",False,WHITE),1)
            dealerturntext = text.render("dealer's turn",False,WHITE)
            buttons = []
            name = ""
            for i in range(26):buttons.append(Button(50*(i+1),700,pygame.image.load(f"assets/{LETTERS[i]}.png")))
            delete = Button(350,760,pygame.image.load(DELETE))
            enter = Button(800,760,pygame.image.load(ENTER))
            # 以下是一些控制变量
            naming = True # 正在命名
            playerturn = False # 玩家回合
            dealerturn = False # 恶魔回合
            choosing = False
            drawingbuckshots = False
            wasd = int(0)
            turn = [0,0]
            dealer = Dealer(2)
            player = Player(2,name)
            # 以下是游戏主循环
            pygame.mixer.music.play(-1)
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        raise SystemExit
                screen.blit(background,(0,0))
                if not player.gethealth():
                    screen.blit(playerlose,loseorwinlocation)
                    pygame.display.update()
                    sleep(3)
                    raise SystemExit
                if not dealer.gethealth():
                    turn[1] = 0
                    turn[0] += 1
                    del buckshot
                    screen.blit(playerwin,loseorwinlocation)
                    pygame.display.update()
                    sleep(3)
                    if turn[0] == 3:
                        raise SystemExit
                    else:
                        dealer = Dealer(health[turn[0]])
                        player = Player(health[turn[0]],name)
                try:buckshot[0]
                except:
                    if turn[0] < 3:
                        buckshot = buckshots[turn[0]][turn[1]]
                        turn[1] += 1
                    if not naming:
                        playerturn = dealerturn = False
                        drawingbuckshots = True
                if naming:
                    screen.blit(nametext,nametextlocation)
                    for i in buttons: 
                        if i.run(screen):
                            name += (LETTERS[buttons.index(i)])
                    if delete.run(screen):
                        name = name[:-1]
                    if enter.run(screen):
                        naming = False
                        drawingbuckshots = True
                        shootyou = Button(700,700,text.render(name,False,WHITE),1)
                        playerwin = text.render(f"{name} win!",False,WHITE)
                        player.setname(name)
                    tmpnametext = text.render(name,False,WHITE)
                    tmpnametextlocation = tmpnametext.get_rect()
                    tmpnametextlocation.center = (700,400)
                    screen.blit(tmpnametext,tmpnametextlocation)
                elif playerturn:
                    for i in range(player.gethealth()):
                        chargelocation.bottomleft = (0,850-50*i)
                        screen.blit(charge,chargelocation)
                    for i in range(dealer.gethealth()):
                        chargelocation.topleft = (0,0+50*i)
                        screen.blit(charge,chargelocation)
                    if gun.run(screen):
                        playerturn = False
                        choosing = True
                elif dealerturn:
                    screen.blit(dealerturntext,nametextlocation)
                    for i in range(player.gethealth()):
                        chargelocation.bottomleft = (0,850-50*i)
                        screen.blit(charge,chargelocation)
                    for i in range(dealer.gethealth()):
                        chargelocation.topleft = (0,0+50*i)
                        screen.blit(charge,chargelocation)
                    if dealer.shoot() == 0:
                        print("dealer shooting himself!")
                        screen.blit(dealershootself,shootlocation)
                        if buckshot[0]:
                            livedealermusic.play()
                            dealer.hurt()
                            dealerturn = False
                            playerturn = True
                        else:
                            blankmusic.play()
                    else:
                        print(f"dealer shooting {name}")
                        screen.blit(dealershootplayer,shootlocation)
                        if buckshot[0]:
                            liveplayermusic.play()
                            player.hurt()
                        else:
                            blankmusic.play()
                        dealerturn = False
                        playerturn = True
                    del buckshot[0]
                    pygame.display.update()
                    sleep(2)
                elif choosing:
                    for i in range(player.gethealth()):
                        chargelocation.bottomleft = (0,850-50*i)
                        screen.blit(charge,chargelocation)
                    for i in range(dealer.gethealth()):
                        chargelocation.topleft = (0,0+50*i)
                        screen.blit(charge,chargelocation)
                    if shootdealer.run(screen):
                        print(f"{name} shooting dealer!")
                        choosing = False
                        dealerturn = True
                        if buckshot[0] == 0:
                            blankmusic.play()
                        else:
                            livedealermusic.play()
                            dealer.hurt()
                        del buckshot[0]
                        sleep(2)
                    elif shootyou.run(screen):
                        print(f"{name} shooting himself!")
                        choosing = False
                        if buckshot[0] == 0:
                            blankmusic.play()
                            playerturn = True
                        else:
                            liveplayermusic.play()
                            player.hurt()
                            dealerturn = True
                        del buckshot[0]
                        sleep(2)
                elif drawingbuckshots:
                    for en,b in enumerate(buckshot):
                        buckshotlocation.topleft = (400+80 * en,400)
                        if b:
                            screen.blit(liveround,buckshotlocation)
                        else:
                            screen.blit(blank,buckshotlocation)
                    pygame.display.update()
                    sleep(2)
                    drawingbuckshots = False
                    playerturn = True
                    shuffle(buckshot)
                else:
                    raise TypeError("Nothing is Running!!!")
                pygame.display.update()
                clock.tick(FPS)
        else:
            name = input("你的名字：") # 输入名字
            for j in range(3): # 三个回合
                dealer = Dealer(health[j]) # 恶魔初始化
                player = Player(health[j],name) # 玩家初始化
                for i in range(len(buckshots[j])): # 每一小轮
                    buckshot = buckshots[j][i] # 初始化本轮子弹
                    buckshotcount = [0,0] #子弹计数
                    for k in buckshot: # 实弹
                        if k:buckshotcount[0]+=1
                    for k in buckshot: # 空弹
                        if k == 0:buckshotcount[1]+=1
                    next = 0 # 下一轮
                    shuffle(buckshot) # 打乱子弹顺序
                    print(f"{buckshotcount[0]}发实弹，{buckshotcount[1]}发空弹") # 打印子弹提示
                    for i in range(len(buckshot)): #
                        print(f"恶魔血量:{dealer.gethealth()} {name}的血量:{player.gethealth()}")
                        if next == 0:
                            if player.shoot():
                                if buckshot[i]:
                                    print("砰！！！")
                                    dealer.hurt() # 受伤
                                else:
                                    print("咔......")
                                next = 1
                            else:
                                if buckshot[i]:
                                    print("砰！！！")
                                    player.hurt()
                                    next = 1
                                else:
                                    print("咔......")
                        else:
                            if dealer.shoot():
                                print(f"恶魔选择向{name}开枪！！！")
                                if buckshot[i]:
                                    print("砰！！！")
                                    player.hurt()
                                else:
                                    print("咔......")
                                next = 0
                            else:
                                print("恶魔选择向自己开枪......")
                                if buckshot[i]:
                                    print("砰！！！")
                                    dealer.hurt()
                                    next = 0
                                else:
                                    print("咔......")
                        if dealer.gethealth() == 0 or player.gethealth() == 0:exit()
                        sleep(1.5)
                del dealer
                del player
    except KeyboardInterrupt:
        print("\n检测到^C")
        exit()
    except SystemExit:pass
    except:
        print("抱歉，我们检测到了一个错误，这可能不是您造成的，但您无法继续进行游戏了")
        print("错误信息：")
        print_exc()
    print("游戏结束!")
    print("感谢您的游玩!")
    print("名称:Buckshot Roulette（恶魔轮盘赌）")
    print("版本：1.0")
    print("LevoLet Inc.")