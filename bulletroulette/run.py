# 主程序（没错，运行它！）
__version__ = "1.1" # 版本说明（没什么用）

# 外部导入
cannotuseGUI = False
from random import shuffle
from time import sleep
import pygame
from traceback import print_exc
from os import chdir,path
from copy import copy
# 模块导入
from bulletroulette.roles import *
from bulletroulette.data import *
from bulletroulette.sprites import *
chdir(path.dirname(__file__))
with open("../README.md", "r", encoding="utf-8") as fh:
    readmetxt = fh.read()
with open("../LICENSE", "r", encoding="utf-8") as fh:
    licensetxt = fh.read()
# 以下是主程序
def printprop(prop):
    for p in prop:
        if p == 1:
            print("啤酒")
        elif p == 2:
            print("烟")
        elif p == 3:
            print("手铐")
        elif p == 4:
            print("小刀")
        else:
            print("放大镜")

def setprop(beset,value,prop):
    beset.setprop(value)
    prop.append(value)
    return prop

def makeprop(beset,value):
    print("value",value)
    prp = []
    for _ in range(value):
        rdm = random()
        if rdm <= 0.2: # 啤酒
            prp = setprop(beset,"beer",prp)
        elif rdm <= 0.4: # 烟
            prp = setprop(beset,"smoke",prp)
        elif rdm <= 0.6: # 手铐
            prp = setprop(beset,"handcuff",prp)
        elif rdm <= 0.8: # 小刀
            prp = setprop(beset,"knife",prp)
        else:
            prp = setprop(beset,"magnifier",prp)
        print("prop",prp)
    return prp

def run():
    playerknife = False
    dealerknife = False
    health = (2,4,6)
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
                [1,1,1,1,1,1,0,0],
                [1,1,1,1,0,0,0,0],
                [1,1,0,0,0,0,0,0]
            ]
        ]
    try:
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
            background   = pygame.image.load(BACKGROUND) # 加载背景图
            gunimage     = pygame.image.load(GUN) # 加载霰弹枪图片
            charge       = pygame.image.load(CHARGE) # 加载血量图片
            blank        = pygame.image.load(BLANK) # 加载空弹图片
            liveround    = pygame.image.load(LIVEROUND) # 加载实弹图片
            shootself    = pygame.image.load(SHOOTSELF) # 加载恶魔射击自己时的图片
            shootplayer  = pygame.image.load(SHOOTPLAYER) # 加载恶魔射击玩家时的图片
            smoke        = pygame.image.load(SMOKE) # 加载烟的图片
            magnifier    = pygame.image.load(MAGNIFIER) # 加载放大镜图片
            knife        = pygame.image.load(KNIFE) # 加载刀的图片
            handcuff     = pygame.image.load(HANDCUFF) # 加载手铐图片
            beer         = pygame.image.load(BEER) # 加载啤酒图片
            propbox      = pygame.image.load(PROPBOX) # 加载道具盒图片
            usesmoke     = pygame.image.load(USESMOKE) # 加载玩家使用烟时的图片
            usemagnifier = pygame.image.load(USEMAGNIFIER) # 加载玩家使用放大镜时的图片
            usehandcuff  = pygame.image.load(USEHANDCUFF) # 加载玩家使用手铐时的图片
            usebeer      = pygame.image.load(USEBEER) # 加载玩家使用啤酒时的图片
            useknife     = pygame.image.load(USEKNIFE) # 加载玩家使用刀时的图片
            seeblank     = pygame.image.load(SEEBLANK) # 加载玩家使用放大镜看到空弹时的图片
            seeliveround = pygame.image.load(SEELIVEROUND) # 加载玩家使用放大镜看到实弹时的图片
            uselocation = usebeer.get_rect() # 获取使用道具的图片的位置
            uselocation.bottom = (700,850) # 将使用道具的图片的位置的底边修改为700,850
            propboxbutton = Button(700,700,propbox,1)
            noneprop     = copy(knife)
            noneprop.set_alpha(0)
            proplocation = []
            propbuttons = []
            for i in range(8):
                proplocation.append(pygame.Rect((100*(i+1),425,50,100)))
            for i in range(8):
                propbuttons.append(Button(100*(i+1),425,noneprop))
            propboxlocation = propbox.get_rect()
            propboxlocation.center = (700,700)
            buckshotlocation = blank.get_rect() # 获取子弹显示位置
            shootlocation = shootself.get_rect() # 获取恶魔射击时的位置
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
            playerlose = text.render("Dealer win!",False,WHITE) # 用字体生成文字
            loseorwinlocation = playerlose.get_rect()
            loseorwinlocation.center = (700,425)
            nametextlocation = nametext.get_rect()
            nametextlocation.center = (700,100)
            shootdealer = Button(700,75,text.render("DEALER",False,WHITE),1)
            dealerturntext = text.render("Dealer's turn",False,WHITE)
            buckshottext = text.render("Bullets:",False,WHITE)
            buckshottextlocation = buckshottext.get_rect()
            buckshottextlocation.topleft = (100,75)
            buttons = []
            name = ""
            for i in range(26):buttons.append(Button(50*(i+1),700,pygame.image.load(f"assets/{LETTERS[i]}.png")))
            delete = Button(350,760,pygame.image.load(DELETE))
            enter = Button(800,760,pygame.image.load(ENTER))
            pygame.mixer.music.play(-1) # 循环播放音乐
            # 以下是一些控制变量
            first = True
            naming = True # 正在命名
            playerturn = False # 玩家回合
            dealerturn = False # 恶魔回合
            choosing = False # 玩家正在选择射击谁
            drawingbullets = False # 正在显示子弹和抽取道具
            selectingprop = True # 隶属于drawingbullets，正在选择道具（还没有点击道具盒）
            tmppropplayer = [] # 玩家当前将要抽取的道具
            propplayer = [None,None,None,None,None,None,None,None] # 玩家已经抽取的道具
            buckshot = [] # 当前小轮的子弹
            turn = [0,0] # 记录回合[大轮，小轮]
            dealer = Dealer(2) # 初始化Dealer类
            player = Player(2,name) # 初始化Player类
            while True: # 游戏主循环
                for event in pygame.event.get(): # 事件处理循环
                    if event.type == pygame.QUIT: # QUIT处理
                        raise SystemExit # 退出(等同于exit())
                screen.blit(background,(0,0)) # 粘贴背景图片
                if not player.gethealth(): # 玩家死亡
                    screen.blit(playerlose,loseorwinlocation) # 打印玩家死亡提示
                    pygame.display.update() # 更新画面
                    sleep(2) # 停留2秒
                    raise SystemExit # 退出
                if not dealer.gethealth(): # 恶魔死亡
                    turn[1] = 0 # 初始化小轮
                    turn[0] += 1 # 大轮+1
                    buckshot = [] # 初始化子弹
                    screen.blit(playerwin,loseorwinlocation) # 打印恶魔死亡提示
                    pygame.display.update() # 更新画面
                    sleep(2) # 停留2秒
                    screen.blit(background,(0,0))
                    pygame.display.update()
                    if turn[0] == 3: # 超出3轮
                        raise SystemExit # 退出
                    else:
                        dealer = Dealer(health[turn[0]]) # 初始化Dealer类
                        player = Player(health[turn[0]],name) # 初始化Player类
                if not len(buckshot):
                    if turn[0] < 3:
                        buckshot = buckshots[turn[0]][turn[1]]
                        turn[1] += 1
                        print("wc",buckshot)
                        if turn[0]:
                            makeprop(dealer,health[turn[0] - 1])
                            tmppropplayer = makeprop(player,health[turn[0] - 1])
                            print("tmp",tmppropplayer)
                    if not naming:
                        playerturn = dealerturn = False
                        drawingbullets = True
                if naming:
                    screen.blit(nametext,nametextlocation)
                    for i in buttons: 
                        if i.run(screen):
                            name += (LETTERS[buttons.index(i)])
                    if delete.run(screen):
                        name = name[:-1]
                    if enter.run(screen):
                        naming = False
                        drawingbullets = True
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
                    for en,i in enumerate(propplayer):
                        if i:
                            if propbuttons[en].run():
                                screen.blit(eval("use" + i),uselocation)
                                pygame.update()
                                if i == "beer":
                                elif i == "knife":
                                elif i == "smoke":
                                elif i == "handcuff":
                                else:
                                    if buckshot[0]:
                                        screen.blit(seelive,)
                                sleep(2)
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
                        screen.blit(shootself,shootlocation)
                        if buckshot[0]:
                            livedealermusic.play()
                            dealer.hurt()
                            dealerturn = False
                            playerturn = True
                        else:
                            blankmusic.play()
                    else:
                        print(f"dealer shooting {name}")
                        screen.blit(shootplayer,shootlocation)
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
                elif drawingbullets:
                    pygame.draw.rect(screen,RED,(0,0,1400,250))
                    screen.blit(buckshottext,buckshottextlocation)
                    for en,b in enumerate(buckshot):
                        buckshotlocation.topleft = (600+80 * en,75)
                        if b:
                            screen.blit(liveround,buckshotlocation)
                        else:
                            screen.blit(blank,buckshotlocation)
                    for en,p in enumerate(propplayer):
                        if p:
                            screen.blit(eval(p),proplocation[en])
                    if tmppropplayer:
                        screen.blit(propbox,propboxlocation)
                        print(tmppropplayer)
                        first = False
                        if selectingprop:
                            if propboxbutton.run(screen):
                                selectingprop = False
                        else:
                            print("in")
                            screen.blit(eval(tmppropplayer[0]),propboxlocation)
                            for en,p in enumerate(propbuttons):
                                if not propplayer[en] and p.run(screen):
                                    selectingprop = True
                                    propplayer[en] = tmppropplayer[0]
                                    del tmppropplayer[0]
                    else:
                        if first:
                            pygame.display.update()
                            sleep(2)
                        else:
                            first = True
                        drawingbullets = False
                        playerturn = True
                else:
                    raise TypeError("Nothing is Running!!!")
                pygame.display.update()
                clock.tick(FPS)
        else:
            name = input("你的名字：") # 输入名字
            for j in range(3): # 三个回合
                brk = False
                dealer = Dealer(health[j]) # 恶魔初始化
                player = Player(health[j],name) # 玩家初始化
                for i in range(len(buckshots[j])): # 每一小轮
                    if brk:
                        brk = False
                        break
                    buckshot = buckshots[j][i] # 初始化本轮子弹
                    buckshotcount = [0,0] #子弹计数
                    for k in buckshot: # 实弹
                        if k:buckshotcount[0]+=1
                    for k in buckshot: # 空弹
                        if k == 0:buckshotcount[1]+=1
                    shuffle(buckshot) # 打乱子弹顺序
                    print(f"{buckshotcount[0]}发实弹，{buckshotcount[1]}发空弹") # 打印子弹提示
                    if j:
                        for k in range(health[j-1]):
                            rdm = random()
                            if rdm <= 0.2: # 啤酒
                                dealer.setprop(1)
                            elif rdm <= 0.4: # 烟
                                dealer.setprop(2)
                            elif rdm <= 0.6: # 手铐
                                dealer.setprop(3)
                            elif rdm <= 0.8: # 小刀
                                dealer.setprop(4)
                            else:
                                dealer.setprop(5)
                        for k in range(health[j-1]):
                            rdm = random()
                            if rdm <= 0.2: # 啤酒
                                player.setprop(1)
                            elif rdm <= 0.4: # 烟
                                player.setprop(2)
                            elif rdm <= 0.6: # 手铐
                                player.setprop(3)
                            elif rdm <= 0.8: # 小刀
                                player.setprop(4)
                            else:
                                player.setprop(5)
                    print("恶魔的道具：")
                    printprop(dealer.getprop())
                    print("你的道具：")
                    printprop(player.getprop())
                    next = 0 # 下一轮
                    brk = False
                    ctn = False
                    ctnl = False
                    playercuff = False
                    dealercuff = False
                    for b in buckshot:
                        print(f"恶魔血量:{dealer.gethealth()} {name}的血量:{player.gethealth()}")
                        if next == 0:
                            if j:
                                while True:
                                    useprop = player.useprop()
                                    if useprop == 0:
                                        break
                                    elif useprop == 1: # 啤酒
                                        print("正在使用：啤酒")
                                        if b:
                                            print("下一发是：实弹")
                                        else:
                                            print("下一发是：空弹")
                                        ctnl = True
                                        break
                                    elif useprop == 2: # 烟
                                        print("正在使用：烟")
                                        player.smoke()
                                    elif useprop == 3:
                                        print("正在使用：手铐")
                                        dealercuff = True
                                    elif useprop == 4:
                                        print("正在使用：小刀")
                                        playerknife = True
                                    else:
                                        print("正在使用：放大镜")
                                        if buckshot[0]:
                                            print("下一发是：实弹")
                                        else:
                                            print("下一发是：空弹")
                                if ctnl:
                                    ctnl = False
                                    continue
                            if player.shoot():
                                if b:
                                    print("砰！！！")
                                    dealer.hurt() # 受伤
                                    if playerknife:
                                        dealer.hurt() # 受伤
                                else:
                                    print("咔......")
                                if not dealercuff:next = 1
                                else:dealercuff = False
                            else:
                                if b:
                                    print("砰！！！")
                                    player.hurt()
                                    if playerknife:
                                        player.hurt()
                                    if not dealercuff:next = 1
                                    else:dealercuff = False
                                else:
                                    print("咔......")
                        else:
                            if j:
                                while True:
                                    useprop = dealer.useprop()
                                    if useprop == 0:
                                        break
                                    elif useprop == 1: # 啤酒
                                        print("恶魔正在使用：啤酒")
                                        if b:
                                            print("下一发是：实弹")
                                        else:
                                            print("下一发是：空弹")
                                        ctnl = True
                                        break
                                    elif useprop == 2: # 烟
                                        print("恶魔正在使用：烟")
                                        dealer.smoke()
                                    elif useprop == 3:
                                        print("恶魔正在使用：手铐")
                                        playercuff = True
                                    elif useprop == 4:
                                        print("恶魔正在使用：小刀")
                                        dealerknife = True
                                    else:
                                        print("正在使用：放大镜") # TODO
                                        print("恶魔:非常有趣。。。")
                                if ctnl:
                                    ctnl = False
                                    continue
                            if dealerknife:
                                print(f"恶魔选择向{name}开枪！！！")
                                if b:
                                    print("砰！！！")
                                    player.hurt()
                                    player.hurt()
                                else:
                                    print("咔......")
                                if not playercuff:next = 0
                                else:playercuff = False
                                dealerknife = False
                            else:
                                if dealer.shoot():
                                    print(f"恶魔选择向{name}开枪！！！")
                                    if b:
                                        print("砰！！！")
                                        player.hurt()
                                    else:
                                        print("咔......")
                                    if not playercuff:next = 0
                                    else:playercuff = False
                                else:
                                    print("恶魔选择向自己开枪......")
                                    if b:
                                        print("砰！！！")
                                        dealer.hurt()
                                        if not playercuff:next = 0
                                        else:playercuff = False
                                    else:
                                        print("咔......")
                        playerknife = False
                        sleep(1)
                        if dealer.gethealth() == 0:
                            brk = True
                            break
                del dealer
                del player
    except KeyboardInterrupt:print("\n检测到^C")
    except SystemExit:pass
    except:
        print("抱歉，我们检测到了一个错误，这可能不是您造成的，但您无法继续进行游戏了")
        print("错误信息：")
        print_exc()
    print("游戏结束!")
    print("感谢您的游玩!")
    pygame.quit()

def dev():
    def readme():print(readmetxt)
    def license():print(licensetxt)
    while True:
        exec(input("(roulette)>>> "))

run()