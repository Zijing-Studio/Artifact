# ai_cpp

## json.hpp

开源的json库。

需要调用该json库的地方已经给出相关代码，您不必关注相关细节。

## gameunit.hpp

包含若干结构体，用于表述游戏中各单位的信息。

> 结构体的结构取决于gameinfo的格式。具体可查看gameinfo.md。

## calculator.h

计算几何库

## card.h

包含生物、神器的基本属性。

## ai_sdk.hpp

包含以下函数。您可以调用以下函数来快速执行相关操作。


一部分为与游戏通信的函数。建议您不要修改它们。

为确认操作来源，部分函数包含player参数或round参数。

player参数均指代玩家阵营（0或1）

round参数均指代当前的回合数。如果round不等于实际当前回合数，则操作无效。




```cpp
void init(int player, std::vector<std::string> artifacts, std::vector<std::string> creatures)
```

​		选择初始神器(**artifacts**数组里包含其名字)和生物(**creatures**数组里包含其名字)



```cpp
void summon(int player, int round, int type, int star, int x, int y, int z)
```

​		在地图(**x**, **y**, **z**)处召唤一个本方类型为**type**，星级为**star**的单位



```cpp
void summon(int player, int round, int type, int star, std::vector<int> position)
```

​		在地图**position**处召唤一个本方类型为**type**，星级为**star**的单位



```cpp
void move(int player, int round, int mover, int x, int y, int z)
```

​		将地图上id为**mover**的单位移动到地图(**x**, **y**, **z**)处



```cpp
void move(int player, int round, int mover, std::vector<int> position)
```

​		将地图上id为**mover**的单位移动到地图**position**处



```cpp
void attack(int player, int round, int attacker, int target)
```

​		令地图上id为**attacker**的单位攻击地图上id为**target**的单位




```cpp
void use(int player, int round, int artifact, int target)
```

​		对id为**target**的单位使用id为**artifact**的神器



```cpp
void use(int player, int round, int artifact, std::vector<int> target)
```

​		对**target**位置使用id为**artifact**的神器



```cpp
void endRound(int player, int round)
```

​		结束当前回合。



除了以上与游戏通信相关的函数外，ai_sdk还包含以下可能有助于快速写AI的函数。这些函数仅在本地进行相关的查询操作。



```cpp
int getDistanceOnGround(gameunit::Map map, gameunit::Pos pos_a, gameunit::Pos pos_b, int camp)
```

​		获取地图map上camp阵营单位从位置pos_a到位置pos_b的地面距离(不经过地面障碍或敌方地面单位)。



```cpp
int getDistanceInSky(gameunit::Map map, gameunit::Pos pos_a, gameunit::Pos pos_b, int camp)

```

​		获取地图map上camp阵营单位从位置pos_a到位置pos_b的飞行距离(不经过飞行障碍或敌方飞行单位)。






```cpp
int checkBarrack(gameunit::Map map, gameunit::Pos pos)
```

​		对于指定位置pos,判断其驻扎情况。不是驻扎点返回-2,中立返回-1,否则返回占领该驻扎点的阵营(0或1)。




```cpp
bool canAttack(gameunit::Unit attacker, gameunit::Unit target)
```

​		判断生物attacker能否攻击到生物target(只考虑攻击力、攻击范围)。



```cpp
bool canUseArtifact(gameunit::Map map, gameunit::Artifact artifact, gameunit::Pos pos, int camp)
```

​		判断能否对位置pos使用神器artifact(不考虑消耗、冷却)。



```cpp
bool canUseArtifact(gameunit::Artifact artifact, gameunit::Unit unit)
```

​		判断能否对生物pos使用神器artifact(不考虑消耗、冷却)。


```cpp
gameunit::Unit getUnitsByPos(gameunit::Map map, gameunit::Pos pos, bool flying)

```

​		获取地图map上位置pos上的生物。


```cpp
gameunit::Unit getUnitById(gameunit::Map map, int unit_id)
```

​		获取地图map上id为unit_id的unit。



```cpp
std::vector<gameunit::Unit> getUnitsByCamp(gameunit::Map map, int unit_camp)
```

​		获取地图map上所有阵营为unit_camp的unit。



```cpp
std::vector<gameunit::Pos> getSummonPosByCamp(gameunit::Map map, int camp)
```

​		获取地图上所有属于阵营camp的出兵点(初始出兵点+额外出兵点)。

## ai.cpp

包含类AI。该类包含的类方法如下

```cpp
void chooseCards()
```

​		(获取阵营后)选择初始卡组。




```cpp
void update_game_info()
```

​		更新游戏局面信息，并存入类属性中。



```cpp
void play()
```

​		您需要在此处结合游戏当前局面信息，做出自己的处理，并调用ai_sdk.hpp中的接口，实现自己的操作。



同时该文件中也包含main()函数，用于启动AI。

