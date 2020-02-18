# ai_cpp

## json.hpp

开源的json库。

需要调用该json库的地方已经给出相关代码，您不必关注相关细节。

## gameunit.hpp

包含若干结构体，用于表述游戏中各单位的信息。

> 具体的游戏信息、结构体的结构可查看gameinfo.md。

## card.h

包含生物、神器的基本属性。

## calculator.h

计算几何库。包含以下函数。您可以调用以下函数来进行相关的位置计算。
```cpp
std::vector<Point> search_path(Point start, Point to,
    std::vector<Point> obstacles={}, std::vector<Point> obstructs={})
```
通过起点、终点、阻挡列表、拦截列表寻找路径，obstacles代表不能停留也不能经过的点，obstructs代表可以停留但不能经过的点。

```cpp
std::vector<Point> path(gameunit::Unit unit, Point dest, gameunit::Map _map)
```
A*算法，给出从单位unit到dest点的路径（包含起点），不行就返回空数组, _map为地图系统。

```cpp
int cube_distance(Point a, Point b)
```
给出两个位置之间的距离。

```cpp
std::vector<std::vector<Point>> reachable(gameunit::Unit unit, gameunit::Map _map)
```
给出单位unit在其最大步数内可达的位置，结果为列表，列表中的元素为经过等于下标的步数可达的位置的列表（例如result[1]为经过1步能到达的位置的列表）。

```cpp
std::vector<gameunit::Unit> units_in_range(Point pos, int dist, gameunit::Map _map, int camp=-1,
                                bool flyingIncluded=true, bool onlandIncluded=true)
```
给出某点pos在给定范围内存在的单位,dist为给定的范围（步数），camp默认为-1，将会返回所有阵营的单位，0为先手阵营，1为后手阵营；flyingIncluded表示将飞行单位包含其中，onlandIncluded为将地面单位包含其中，默认两者都包含。

```cpp
bool in_map(Point pos)
```
判断某个点pos是否在地图范围之内，返回布尔值。


```cpp
std::vector<Point> all_pos_in_map()
```
给出地图内的所有点。


## ai_client.h

包含ai基类。封装好了部分通信函数和查找函数。


前一部分为与游戏通信的函数。建议您不要修改它们。



```cpp
void init(std::vector<std::string> artifacts, std::vector<std::string> creatures)
```

​		选择初始神器(**artifacts**数组里包含其名字)和生物(**creatures**数组里包含其名字)



```cpp
void summon(int type, int star, int x, int y, int z)
```

​		在地图(**x**, **y**, **z**)处召唤一个本方类型为**type**，星级为**star**的单位



```cpp
void summon(int type, int star, std::vector<int> position)
```

​		在地图**position**处召唤一个本方类型为**type**，星级为**star**的单位



```cpp
void move(int mover, int x, int y, int z)
```

​		将地图上id为**mover**的单位移动到地图(**x**, **y**, **z**)处



```cpp
void move(int mover, std::vector<int> position)
```

​		将地图上id为**mover**的单位移动到地图**position**处



```cpp
void attack(int attacker, int target)
```

​		令地图上id为**attacker**的单位攻击地图上id为**target**的单位




```cpp
void use(int artifact, int target)
```

​		对id为**target**的单位使用id为**artifact**的神器



```cpp
void use(int artifact, std::vector<int> target)
```

​		对**target**位置使用id为**artifact**的神器



```cpp
void endRound()
```

​		结束当前回合。



除了以上与游戏通信相关的函数外，ai_client还包含以下可能有助于快速写AI的函数。这些函数仅在本地进行相关的查询操作。



```cpp
int getDistanceOnGround(gameunit::Pos pos_a, gameunit::Pos pos_b, int camp)
```

​		获取地图上camp阵营单位从位置pos_a到位置pos_b的地面距离(不经过地面障碍或敌方地面单位)。



```cpp
int getDistanceInSky(gameunit::Pos pos_a, gameunit::Pos pos_b, int camp)

```

​		获取地图map上camp阵营单位从位置pos_a到位置pos_b的飞行距离(不经过飞行障碍或敌方飞行单位)。






```cpp
int checkBarrack(gameunit::Pos pos)
```

​		对于指定位置pos,判断其驻扎情况。不是驻扎点返回-2,中立返回-1,否则返回占领该驻扎点的阵营(0或1)。




```cpp
bool canAttack(gameunit::Unit attacker, gameunit::Unit target)
```

​		判断生物attacker能否攻击到生物target(只考虑攻击力、攻击范围)。



```cpp
bool canUseArtifact(gameunit::Artifact artifact, gameunit::Pos pos, int camp)
```

​		判断能否对位置pos使用神器artifact(不考虑消耗、冷却)。



```cpp
bool canUseArtifact(gameunit::Artifact artifact, gameunit::Unit unit)
```

​		判断能否对生物pos使用神器artifact(不考虑消耗、冷却)。


```cpp
gameunit::Unit getUnitsByPos(gameunit::Pos pos, bool flying)

```

​		获取地图map上位置pos上的生物。


```cpp
gameunit::Unit getUnitById(int unit_id)
```

​		获取地图map上id为unit_id的unit。



```cpp
std::vector<gameunit::Unit> getUnitsByCamp(int unit_camp)
```

​		获取地图map上所有阵营为unit_camp的unit。



```cpp
std::vector<gameunit::Pos> getSummonPosByCamp(int camp)
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

