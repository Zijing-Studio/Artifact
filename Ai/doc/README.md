[TOC]

# ai运行流程

1、ai启动后，会获得自己的阵营。此后会根据己方阵营选取卡组。

> 阵营为0的玩家先手，阵营为1的玩家后手。

> 在chooseCards()/choose_cards()函数中，玩家可以根据阵营做出自己的卡牌选择

2、每位玩家的回合开始时，judger会向ai发送当前游戏局面信息(json格式)。updateGameInfo()/update_game_info()函数会处理相关的json串并将游戏局面信息存储在类属性中。

> 存储游戏局面信息的结构体/类的具体结构可见gameunit.hpp/gameunit.py

玩家根据当前游戏局面信息进行自己的处理，并调用相关的函数发送自己的操作。

> 目前相关的游戏操作函数包括summon、move、attack、use函数

每次操作后，judger会向ai发送操作后的当前游戏局面信息。

玩家可以不断发送自己的操作，直到发送结束回合的指令为止。

> 用于结束当前回合的函数是endRound()/self.end_round()函数

> 一些其它的状况也可能导致回合结束，比如超时/一回合内的操作数超出上限等。

2、非当前回合的ai将不会接收到任何信息，发出的信息也不会得到接收。

3、建议直接调用相关的函数进行消息的收发。您需要的做的仅仅是处理相关的数据。

> 不合法的信息发送可能导致回合结束/直接判负等后果。

注意AI的通信使用标准输入/输出流。除了直接使用sdk中相关的函数外，请不要在标准输出流中输出任何信息。

# 测试

## 使用judger启动游戏逻辑和ai

启动指令: python <judger路径> <启动逻辑command> <启动AI 1 command> <启动AI 2 command> <逻辑生成replay路径>

启动指令示例: python .\Judger\judger.py python+.\\logic.py python+.\\Ai\\ai_py\\ai-HL.py  python+.\\Ai\\ai_py\\ai-HL.py  record

AI可以是C++版本，也可以选择python版本。选择其一即可。

注意judger与AI的通信使用标准输入/输出流。除了直接使用sdk中相关的函数外，请不要在标准输出流中输出任何信息。

logic.py中有一个DEBUG参数，设置为True的时候会在当前目录下生成一个log.txt文件，记录收发的信息。



