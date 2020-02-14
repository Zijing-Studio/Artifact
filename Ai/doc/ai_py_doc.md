# ai_py

## calculator.py

计算几何库

## card.py

包含生物、神器的基本属性。


## ai_sdk.py

包含以下函数。您可以调用以下函数来快速执行相关操作。



一部分为与游戏通信的函数。建议您不要修改它们。

为确认操作来源，部分函数包含player参数或\_round参数。

player参数均指代玩家阵营（0或1）

\_round参数均指代当前的回合数。如果\_round不等于实际当前回合数，则操作无效。




```python
 init(player, artifacts, creatures):
```
​		选择初始神器(**artifacts**数组里包含其名字)和生物(**creatures**数组里包含其名字)




```python
 summon(player, _round, _type, star, position)
```
​		在地图**position**处召唤一个本方类型为**\_type**，星级为**star**的单位



```python
move(player, _round, mover, position)
```
​		将id为**mover**的单位移动到地图**position**处




```python
attack(player, _round, attacker, target)
```
​		令id为**attacker**的单位攻击id为**target**的单位



```python
use(player, _round, artifact, target)
```
​		对id为**target**的单位/**target**位置使用id为**artifact**的神器




```python
end_round(player, _round)
```
​		结束当前回合。




除了以上与游戏通信相关的函数外，ai_sdk还包含以下可能有助于快速写AI的函数。这些函数仅在本地进行相关的查询操作。

```python
get_distance_on_ground(_map, pos_a, pos_b, camp)
```
​		获取地图_map上camp阵营单位从位置pos_a到位置pos_b的地面距离(不经过地面障碍或敌方地面单位)。




```python
get_distance_in_sky(_map, pos_a, pos_b, camp)
```
​		获取地图_map上camp阵营单位从位置pos_a到位置pos_b的飞行距离(不经过飞行障碍或敌方飞行单位)。






```python
check_barrack(_map, pos)
```
​		对于指定位置pos,判断其驻扎情况。不是驻扎点返回-2,中立返回-1,否则返回占领该驻扎点的阵营(0或1)。




```python
can_attack(attacker, target)
```
​		判断生物attacker能否攻击到生物target(只考虑攻击力、攻击范围)。




```python
can_use_artifact(_map, artifact, target, camp)
```
​		判断阵营camp能否对目标target使用神器artifact(不考虑消耗、冷却)



```python
get_unit_by_pos(_map, pos, flying)
```
​		获取地图_map上位置pos上的生物

```python
get_unit_by_id(_map, unit_id)
```
​		获取地图_map上id为unit_id的unit



```python
get_units_by_camp(_map, unit_camp)
```
​		获取地图_map上所有阵营为unit_camp的unit




```python
get_summon_pos_by_camp(_map, camp)
```
​		获取地图上所有属于阵营camp的出兵点(初始出兵点+额外出兵点)

## ai.py

包含类AI。该类包含的类方法如下

```python
__inti__(self)
```

​		初始化游戏局面信息相关的变量。




```python
choose_cards(self)
```

​		(获取阵营后)选择初始卡组。



```python
update_game_info(self)
```

​		更新游戏局面信息，并存入类属性中。




```python
play(self)
```

​		您需要在此处结合游戏当前局面信息，做出自己的处理，并调用ai_sdk.py中的接口，实现自己的操作。



同时该文件中也包含main()函数，用于启动AI。
