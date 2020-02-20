[TOC]

# 游戏信息

## 概述

ai回合开始时/每次执行非结束回合的游戏操作时会收到一个表述游戏当前局面信息的json格式的字符串。对该字符串的解析已于updateGameInfo()函数中实现。updateGameInfo()函数会将相关的信息以结构体的形式存入类属性中。相关的结构体在gameunit.hpp中给出。结构体属性已于代码中给出一定注释。gameunit.hpp中的from_json()用于把json转化成相应对象，细节此处不表。

## 结构体信息

以下为gameunit.hpp相关结构体的具体参数的解释。

其中Pos类型表示三元整数tuple，表示位置。

### Unit

表示单个生物。

#### id

int。表示生物的id。

#### camp

int。表示生物所属阵营。

#### type

string。表示生物的种类。

#### name

string。表示生物的名字。

#### cost

int。表示生物的法力消耗。

#### atk

int。表示生物的攻击。

#### max_hp

int。表示生物的生命上限。

#### hp

int。表示生物的当前生命。

#### atk_range

二元int数组。表示生物攻击最小范围/最大范围。

>（攻击范围0表示不可攻击/反击，0-0表示可攻击与自身相同格子的生物）

#### max_move

int。表示生物的行动力。

#### cool_down

int。表示生物的冷却。

#### pos

Pos。表示生物的位置。

#### level

int。表示生物的等级。

#### flying

bool。表示生物是否飞行。

#### atk_flying

bool。表示生物能否攻击飞行生物。

#### agility

bool。表示生物是否迅捷。

#### holy_shield

bool。表示生物是否具有圣盾。

#### can_atk

bool。表示生物能否攻击。

#### can_move

bool。表示生物能否移动。

### Barrack

表示一个驻扎点。

#### pos

Pos。表示驻扎点的位置。

#### camp

int。表示驻扎点所属阵营。

#### summon_pos_list

Pos数组。表示驻扎点所控制的出兵点的位置。

### Miracle

表示一个神迹。

#### camp

int。表示神迹所属阵营。

#### max_hp

int。表示神迹生命上限。

#### hp

int。表示神迹生命值。

#### pos

Pos。表示神迹的位置。

#### summon_pos_list

Pos数组。表示神迹控制的初始出兵点的位置。

#### name

string。表示神迹的名字。

#### id

int。表示神迹的id。

### Obstacle

表示一个Obstacle

#### type

string。表示Obstacle的种类。

#### pos

Pos。表示Obstacle的位置。

#### allow_flying

bool。表示Obstacle是否允许飞行生物通过。

#### allow_ground

bool。表示Obstacle是否允许地面生物通过。

### Artifact

表示一个神器。

#### id

int。表示神器的id。

#### name

string。表示神器的名字。

#### camp

int。表示神器所属的阵营。

#### cost

int。表示神器的法力消耗。

#### max_cool_down

int。表示神器的最大冷却时间。

#### cool_down_time

int。表示神器的目前冷却时间。

#### state

string。表示神器的目前使用状态。

#### target_type

string。表示神器使用对象的种类（Unit或Pos）。

### CreatureCapacity

TODO

#### type

string。表示生物种类。

#### available_count

int。表示生物的生物槽容量。

#### cool_down_list

int数组。表示生物的冷却时间。

### Map

#### units

Unit数组。包括地图上所有生物。

#### barracks

Barrack数组。包括地图上所有驻扎点。

#### miracles

Miracle数组。包括地图上所有神迹。

#### obstacles

Obstacle数组。包括地图上所有Obstacle。

#### flying_obstacles

Obstacle数组。包括地图上所有飞行Obstacle。

#### ground_obstacles

Obstacle数组。包括地图上所有地面Obstacle。

### Player

表示一个玩家。

#### camp

int。表示玩家所处的阵营。

#### artifact

Artifact数组。表示玩家所拥有的神器的情况。

#### mana

int。表示玩家当前法力值。

#### max_mana

int。表示玩家最大法力值。

#### creature_capacity

TODO

#### newly_summoned_id_list

int数组。表示玩家最新召唤的生物的id。

## 类属性

### map

Map。

### players

Player数组。长度为2。Player在数组中的下标与其camp相同。
 
### round

int。当前游戏回合。

### my_camp

int。己方阵营。

### my_artifacts

string数组。用于确认己方神器。

### my_creatures

string数组。用于确认己方生物。

> 注：神器与生物已经确定后便无法在游戏中修改。但可以通过访问my_artifacts与my_creatures快速获取己方所选神器与生物。

## python版本的细微差异

python版本的gameunit与C++版本的gameunit大体相同。在此列出一些细微差异。

C++版本的Pos是std::tuple<int, int, int>，而python版本的Pos是list。

C++版本用的是结构体，而python版本用的是类。python版本的类属性有一些无关紧要的默认值。
