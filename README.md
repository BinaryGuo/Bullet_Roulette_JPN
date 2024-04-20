# Bullet Roulette 说明

## 项目说明
- 此项目旨在将游戏“恶魔轮盘”的玩法移植到Python3.x上
- github：https://github.com/BinaryGuo/Bullet_Roulette/
- 问题反馈：https://github.com/BinaryGuo/Bullet_Roulette/issues
- 联系邮箱（GQX）：kill114514251@outlook.com
- testPyPI：同名

## 版本
- 1.1

## 开发环境
- linux ubuntu 22.04（主要开发环境，负责运行代码等等）
- apple mac 14.0（主要是使用mac上自带的“预览”来测量图片并使用PIL.Image进行切割、缩放等操作）
其实ubuntu在网上也有测像素的工具，但我懒得找了......
正好家里有台mac，就选择用mac完成。

## 改动说明

### 0.1（测试版，未发布）
- 使用类初步实现了游戏
- 可玩性不高

### 1.0（上个版本）
- 增加两个回合
- 增加图形界面（pygame）

### 1.1（此版本）
- 增加道具
- 增加开发者模式

### 1.2（计划）
- 增加开场
- 增加无尽模式

### 1.3（计划）
- 增加PVP

### 1.4（计划）
- 增加远程连接

### 1.5（计划）
- 增加多人模式

### 问题修复
- BUG1 降低在高帧率下的高灵敏度问题
- BUG2 增加获取屏幕尺寸功能 
- BUG3 兼容windows系统 # 已解决（1.0.4）
- BUG4 IDLE无法自动关闭 # 已解决（1.1.1）
- BUG5 shuffle,make prop beset 复制
- BUG6 道具摆放位置
- METHOD1 视角抬头
- METHOD2 血量

## 程序说明
- 你可以看到在每个.py文件开头简短的说明
### 安装方法
在shell(Terminal(Mac/Linux)或cmd(Windows))
> python3 -m pip install bulletroulette

或（前者更为保险）
> pip3 install bulletroulette

### 运行方法
启动IDLE(shell输入python)
> \>>> from bulletroulette.run import run
> \>>> run()

(终止时需在shell上按下^C ^D)

### 目录结构（在bulletroulette下）
```
/
    __init__.py  
    run.py  
    data.py  
    roles.py  
    sprites.py  
    assets/
        A.png  
        B.png
        C.png  
        .  
        .  
        .  
        X.png  
        Y.png  
        Z.png  
        bgmsc.ogg  
        blank.wav  
        .  
        .  
        .  
        (素材若干)
```

### 游戏规则
- 在运行程序后，程序会让您指定游戏模式，建议选择窗口（如果是开发人员请忽略此建议）。

#### 窗口模式
1. 在选择窗口模式后，会让您设置帧率（建议设置为25以下，见BUG1）。
2. 设置好帧率后会弹出一个窗口，让您输入名称（鼠标）
3. 设置好名称后正式进入游戏，游戏分为三轮，每轮结束后会弹出 <您的名字> WIN!（在您赢的情况下）（第三轮结束后需手动终止（shell按下^C ^D），见BUG4），每一轮有若干发子弹，显示一次子弹为一小轮
4. 每一轮会先显示子弹（红色为实弹，灰色为空弹），显示后子弹顺序会被打乱
5. 每一小轮都是玩家先手，用鼠标选择枪后可点击DEALER射击对面，点击自己名字射击自己（左边为您和对面的血量）
6. 如果您选择射击对面，不管是空弹还是实弹，下一回合都是对面开枪。如果您选择射击自己，如果是实弹下一回合就该对面开枪，如果是空弹，下一回合还是您射击。（如果是实弹会听到“砰！”，如果是空弹会听到“咔...”）

#### 壳程序模式
1. 在选择壳程序模式后，会提示您输入名称
2. 在名称输入完成后正式进入游戏，游戏分为三轮，每轮结束后会弹出“恶魔死了！！！”（在您赢的情况下），每一轮有若干发子弹，显示一次子弹为一小轮
4. 每一轮会先显示枪膛里有几发子弹，显示后子弹顺序会被打乱。
5. 每一小轮都是玩家先手，输入一射击对面，点击自己名字射击自己（左边为您和对面的血量）
6. 如果您选择射击对面，不管是空弹还是实弹，下一回合都是对面开枪。如果您选择射击自己，如果是实弹下一回合就该对面开枪，如果是空弹，下一回合还是您射击。（如果是实弹会听到“砰！”，如果是空弹会听到“咔...”）

## 道歉
- 不好意思，此版本没有提供开发接口，README也写的不多，请见凉！
- 不好意思，由于之前upload比较匆忙，没来得及改README上的协议，assets目录下还有个临时存放的二维码没有删，请见凉。

## 问题解决

### 找不到版本（安装问题）
> ERROR: Could not find a version that satisfies the requirement bulletroulette (from versions: none)  
> ERROR: No matching distribution found for bulletroulette

原因：Python版本小于3.8  
解决办法：重装一个Python3.8以上的版本

### 如果您的版本为1.0开头，并不是1.0.4的话请立即更新（1.0.4解决了很多问题）（如果不是WINDOWS，1.0.3也行）

## 鸣谢

### 测试人员

- 言邵阳（真名）
- 陈晨（真名）

### 开发人员

- 