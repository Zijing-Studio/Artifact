# ai_py

## gameunit.py

包含若干类，用于表述游戏中各单位的信息。

> 具体的类的结构可查看gameinfo.md。

## card.py

包含生物、神器的基本属性。

## calculator.py

计算几何库。包含以下函数。您可以调用以下函数来进行相关的位置计算。

```python
search_path(start, end, obstacles, obstructs)
```

​		通过起点、终点、阻挡列表、拦截列表寻找路径，obstacles代表不能停留也不能经过的点，obstructs代表可以停留但不能经过的点。



```python
path(unit, dest, _map)
```

​		用A*算法给出生物unit到位置dest的路径（包含起点）。无法给出路径时返回False。



```python
cube_distance(pos1, pos2)
```

​		给出两个位置之间的距离。



```python
reachable(unit, _map)
```

​		给出生物unit在其最大步数内可达的位置，结果为列表，列表中的元素为经过等于下标的步数可达的位置的列表（例如result[1]为经过1步能到达的位置的列表）。



```python
units_in_range(pos, dist, _map, camp=-1, flyingIncluded=True, onlandIncluded=True)
```

​		给出某点pos在给定范围内存在的生物,dist为给定的范围（步数），camp默认为-1，将会返回所有阵营的生物，0为先手阵营，1为后手阵营；flyingIncluded表示将飞行生物包含其中，onlandIncluded为将地面生物包含其中，默认两者都包含。



```python
in_map(pos)
```

​		判断某个点pos是否在地图范围之内，返回布尔值。



```python
all_pos_in_map()
```

​		给出地图内的所有点。



## ai_client.py

包含ai基类。封装好了部分通信函数和查找函数。



前一部分为与游戏通信的函数。建议您不要修改它们。


```python
update_game_info()
```
​		读入游戏信息并更新相关数据。



```python
choose_cards()
```
​	设置卡组，并调用init()函数确定初始卡组。



```python
play()
```
​	结合当前局面信息做出操作。




```python
 init()
```
​		选择初始神器(my_artifacts)和生物(my_creatures)。




```python
 summon(_type, star, position)
```
​		在**position**处召唤一个本方类型为**\_type**，星级为**star**的生物。



```python
move(mover, position)
```
​		将id为**mover**的生物移动到**position**处。




```python
attack(attacker, target)
```
​		令id为**attacker**的生物攻击id为**target**的生物或神迹。



```python
use(artifact, target)
```
​		对id为**target**的生物/**target**位置使用id为**artifact**的神器。




```python
end_round()
```
​		结束当前回合。




除了以上与游戏通信相关的函数外，ai_client还包含以下可能有助于快速写AI的函数。这些函数仅在本地进行相关的查询操作。

```python
get_distance_on_ground(pos_a, pos_b, camp)
```
​		获取**camp**阵营生物从位置**pos_a**到位置**pos_b**的地面距离(不经过地面障碍或敌方地面生物)。




```python
get_distance_in_sky(pos_a, pos_b, camp)
```
​		获取**camp**阵营生物从位置**pos_a**到位置**pos_b**的飞行距离(不经过飞行障碍或敌方飞行生物)。






```python
check_barrack(pos)
```
​		判定位置**pos**的驻扎情况。不是驻扎点返回-2,中立返回-1,否则返回占领该驻扎点的阵营(0或1)。




```python
can_attack(attacker, target)
```
​		判断生物**attacker**能否攻击到生物**target**(只考虑攻击力、攻击范围)。




```python
can_use_artifact(artifact, target, camp)
```
​		判断阵营**camp**的玩家能否对目标**target**使用神器**artifact**(不考虑消耗、冷却)。



```python
get_unit_by_pos(_map, pos, flying)
```
​		获取位置**pos**上的生物。无生物时返回None。



```python
get_unit_by_id(unit_id)
```
​		获取id为**unit_id**的生物。无生物时返回None。



```python
get_units_by_camp(_map, unit_camp)
```
​		获取所有阵营为**unit_camp**的生物。无生物时返回空数组。




```python
get_summon_pos_by_camp(camp)
```
​		获取所有属于阵营**camp**的出兵点(初始出兵点+额外出兵点)。

## ai.py

包含类AI。该类继承自AiClient类。玩家需要在AiClient类的基础上，重写play()函数及其它函数，完成自己的AI。


同时该文件中也包含main()函数，用于启动AI。

## ai-HL.py

一个样例AI，玩家可以用于参考。
