# 播放器协议

| 播放器协议   | 版本0        |      |       |     |     |      |
| ------------ | ------------ | ---- | ----- | --- | --- | :--- |
| 0(游戏开始)  |              |      |       |     |     |      |
| round        | 1(回合开始)  | camp | 0     | 0   | 0   | 0    |
| round        | 2(回合结束)  | camp | 0     | 0   | 0   | 0    |
| round        | 3(召唤)      | type | level | x   | y   | id0  |
| round        | 4(移动)      | id0  | x     | y   | 0   | 0    |
| round        | 5(攻击)      | id1  | id2   | 0   | 0   | 0    |
| round        | 6(伤害)      | id2  | id1   | d   | 0   | 0    |
| round        | 7(死亡)      | id0  | 0     | 0   | 0   | 0    |
| round        | 8(治疗)      | id2  | id1   | h   | 0   | 0    |
| round        | 9(使用神器)  | camp | type  | x   | y   | id0  |
| round        | 10(游戏结束) | camp | 0     | 0   | 0   | 0    |
| round        | 11(配置卡组) | camp | a0    | c1  | c2  | c3   |
| round        | 12(圣盾加持) | id0  | 0     | 0   | 0   | 0    |
| round        | 13(圣盾击破) | id0  | 0     | 0   | 0   | 0    |
| round        | 14(攻击前)   | id1  | id2   | 0   | 0   | 0    |
| round        | 15(攻击后)   | id1  | id2   | 0   | 0   | 0    |
| round        | 16(离开)     | id0  | x     | y   | 0   | 0    |
| round        | 17(抵达)     | id0  | x     | y   | 0   | 0    |
| round        | 18(开始召唤) | type | level | x   | y   | 0    |
| -1(录像结束) |              |      |       |     |     |      |

第一个数字表示版本号，同时也表示游戏（录像文件）开始

1: camp(0/1)方玩家开始回合round

2: camp(0/1)方玩家结束回合round （不一定意味着下个回合开始）

3: round回合在x y处召唤类型为type等级为level的单位 其id为id0

4: round回合id为id0的单位移动到x y处

5: round回合id为id1的单位攻击id为id2的单位（不结算伤害）

6: round回合id为id2的单位受到来自id为id1的单位d点伤害

7: round回合id为id0的单位死亡

8: round回合id为id2的单位受到来自id为id1的单位h点治疗

9: round回合camp(0/1)方玩家使用神器 (神器还没完全设计完毕，参数待定)

10: round回合camp(0/1/2)方玩家获胜 其中2表示平局

11: round(一般为0)回合camp(0/1)方玩家初始化神器a0和卡组c1,c2,c3

12: round回合id为id0的单位加上圣盾

13: round回合id为id0的单位圣盾被击破

14: round回合id为id1的单位对id为id2的单位的攻击开始

15: round回合id为id1的单位对id为id2的单位的攻击结束

16: round回合id为id0的单位离开x y处

17: round回合id为id0的单位抵达x y处

18: round回合在x y处开始召唤类型为type等级为level的单位

最后一个数字固定为-1，表示游戏（录像文件）结束

0方玩家神迹id暂定为0 1方玩家神迹id暂定为1

其中Summon命令对应的type（暂定）:

1:  0方剑士
2: 0方弓箭手
3:  0方黑蝙蝠
4:  0方牧师
5:  0方火山龙
11:  1方剑士
12:  1方弓箭手
13:  1方黑蝙蝠
14:  1方牧师
15:  1方火山龙

神器的使用方式待定（可先看看当前的策划案）