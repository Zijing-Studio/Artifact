# 播放器协议

| 播放器协议   | 版本0        |      |       |     |      |      |
| ------------ | ------------ | ---- | ----- | --- | ---- | :--- |
| 0(游戏开始)  |              |      |       |     |      |      |
| round        | 1(回合开始)  | camp | 0     | 0   | 0    | 0    |
| round        | 2(回合结束)  | camp | 0     | 0   | 0    | 0    |
| round        | 3(召唤)      | type | level | x   | y    | id0  |
| round        | 4(移动)      | id0  | x     | y   | 0    | 0    |
| round        | 5(攻击前)    | id1  | id2   | 0   | 0    | 0    |
| round        | 6(伤害)      | id2  | id1   | d   | type | 0    |
| round        | 7(死亡)      | id0  | 0     | 0   | 0    | 0    |
| round        | 8(治疗)      | id2  | id1   | h   | 0    | 0    |
| round        | 9(使用神器)  | camp | type  | x   | y    | id0  |
| round        | 10(游戏结束) | camp | 0     | 0   | 0    | 0    |
| round        | 11(配置卡组) | camp | a0    | c1  | c2   | c3   |
| round        | 12(添加buff) | id0  | type  | 0   | 0    | 0    |
| round        | 13(移除buff) | id0  | type  | 0   | 0    | 0    |
| round        | 14(攻击中)   | id1  | id2   | 0   | 0    | 0    |
| round        | 15(受到攻击) | id1  | id2   | 0   | 0    | 0    |
| round        | 16(离开)     | id0  | x     | y   | 0    | 0    |
| round        | 17(抵达)     | id0  | x     | y   | 0    | 0    |
| round        | 18(开始召唤) | type | level | x   | y    | 0    |
| -1(录像结束) |              |      |       |     |      |      |

第一个数字表示版本号，同时也表示游戏（录像文件）开始

1: camp(0/1)方玩家开始回合round

2: camp(0/1)方玩家结束回合round （不一定意味着下个回合开始）

3: round回合在x y处召唤类型为type等级为level的单位 其id为id0

4: round回合id为id0的单位移动到x y处

5: round回合id为id1的单位攻击id为id2的单位（不结算伤害）

6: round回合id为id2的单位受到来自id为id1的单位d点伤害,伤害种类为type

7: round回合id为id0的单位死亡

8: round回合id为id2的单位受到来自id为id1的单位h点治疗

9: round回合camp(0/1)方玩家使用神器 (神器还没完全设计完毕，参数待定)

10: round回合camp(0/1/2)方玩家获胜 其中2表示平局

11: round(一般为0)回合camp(0/1)方玩家初始化神器a0和卡组c1,c2,c3

12: round回合id为id0的单位加上种类为type的buff

13: round回合id为id0的单位移除种类为type的buff

14: round回合id为id1的单位对id为id2的单位的攻击开始

15: round回合id为id2的单位受到id为id1的单位的攻击

16: round回合id为id0的单位离开x y处

17: round回合id为id0的单位抵达x y处

18: round回合在x y处开始召唤类型为type等级为level的单位

最后一个数字固定为-1，表示游戏（录像文件）结束

0方玩家神迹id为0 1方玩家神迹id为1

生物对应的数字(3中的type 18中的type 11中的c):

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

神器对应的数字(11中的a):
1: 0方圣光之耀
2: 0方阳炎之盾
3: 0方地狱之火
11: 1方圣光之耀
12: 1方阳炎之盾
13: 1方地狱之火
其中圣光之耀和地狱之火的后续是 x y 0
阳炎之盾的后续是 0 0 id

伤害类型对应的数字:
1: 攻击
2: 反击
3: 火山龙的溅射
4: 地狱之火

buff类型对应的数字:
0: BaseBuff
1: PriestAtkBuff 牧师光环
2: HolyShield 圣盾
3: HolyLightAtkBuff 圣光之耀
4: SalamanderShieldBuff 阳炎之盾
