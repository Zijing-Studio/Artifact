[TOC]

# 简述

每次接收到的信息都是一个json字符串

该json有四个键:"map"， "players"， "round"， "camp"。

"map"对应的值为一个json对象，包含键"units"，"barracks"，"relics"，"obstacles"。

"players"对应的值为一个二元json对象数组，每一个包含键"camp"，"artifact"，"mana"，"max_mana"，"creature_capacity"，"newly_summoned_id_list"。


"round"对应的值为一个整数，表示当前回合数。

"camp"对应的值为一个整数（0或1），表示你所处的阵营。

以下给出具体解释。


# 结构

## map

### units

json对象（称其为生物）的数组。下面对生物进行解释。

#### id

整数。表示生物的id。

#### camp

整数。表示生物所属阵营。

#### name

字符串。表示生物的名字。

#### cost

整数。表示生物的费用。

#### atk

整数。表示生物的攻击。

#### max_hp

整数。表示生物的生命上限。

#### hp

整数。表示生物的当前生命。

#### atk_range

二元整数数组。表示生物攻击最小范围/最大范围。

>（攻击范围0表示不可攻击/反击，0-0表示可攻击与自身相同格子的生物）

#### max_move

整数。表示生物的行动力。

#### cool_down

整数。表示生物的冷却。

#### pos

三元整数数组。表示生物的位置。

#### level

整数。表示生物的等级。

#### flying

布尔值。表示生物是否是飞行生物。

#### atk_flying

布尔值。表示生物是否能攻击飞行生物。

### barracks

json对象（称其为驻扎点）的数组。下面对驻扎点进行解释。

#### pos

三元整数数组。表示驻扎点的位置。

#### camp

整数。表示驻扎点所属阵营。

#### summon_pos_list

三元整数数组的数组。表示驻扎点所控制的出兵点的位置。

### relics

json对象（称其为神迹）的数组。下面对神迹进行解释。

#### camp

整数。表示神迹所属阵营。

#### max_hp

整数。表示神迹生命上限。

#### hp

整数。表示神迹生命值。

#### pos

三元整数数组。表示神迹的位置。

#### name

字符串。表示神迹的名字。

#### id

整数。表示神迹的id。

### obstacles

json对象（称其为obstacle）的数组。下面对obstacle进行解释。

#### type

字符串。表示obstacle的种类。

#### pos

三元整数数组。表示obstacle的位置。

#### allow_flying

布尔值。表示obstacle是否允许飞行单位通过。

## players

json对象（称其为玩家）的二元数组。下面对玩家进行解释。

### camp

0或1。表示该玩家所处的阵营。（与下标相同）

### artifact

json对象（称其为神器）的数组。下面对神器进行解释。

#### id

整数。表示神器的id。

#### name

字符串。表示神器的名字。

#### camp

整数。表示神器所属的阵营。

#### cost

整数。表示神器的法力消耗。

#### max_cool_down

整数。表示神器的最大冷却时间。

#### cool_down_time

整数。表示神器的目前冷却时间。

#### state

字符串。表示神器的目前使用状态。

#### target_type

字符串。表示神器的使用方式。

### mana

整数。表示玩家当前法力值。

### max_mana

整数。表示玩家最大法力值。

### creature_capacity

#### type

字符串。表示生物种类。

#### available_count

整数。表示生物的生物槽容量。

### newly_summoned_id_list

整数数组。表示玩家最新召唤的生物的id。

## round

整数。表示当前回合数。

## camp

整数。表示你所属阵营。

# 示例

```json
{
    "map":
    {
        "units":
        [
            {
                "id": 3，
                "camp": 1，
                "name": "BlackBat (Level 1)"，
                "cost": 2，
                "atk": 1，
                "max_hp": 1，
                "hp": 1，
                "atk_range":
                [
                    0，
                    1
                ]，
                "max_move": 5，
                "cool_down": 2，
                "pos":
                [
                    0，
                    0，
                    0
                ]，
                "level": 1，
                "flying": true，
                "atk_flying": true
            }，
            {
                "id": 4，
                "camp": 0，
                "name": "Priest (Level 1)"，
                "cost": 2，
                "atk": 0，
                "max_hp": 2，
                "hp": 2，
                "atk_range":
                [
                    0，
                    0
                ]，
                "max_move": 3，
                "cool_down": 4，
                "pos":
                [
                    0，
                    1，
                    -1
                ]，
                "level": 1，
                "flying": false，
                "atk_flying": false
            }，
            {
                "id": 5，
                "camp": 0，
                "name": "Priest (Level 1)"，
                "cost": 2，
                "atk": 0，
                "max_hp": 2，
                "hp": 2，
                "atk_range":
                [
                    0，
                    0
                ]，
                "max_move": 3，
                "cool_down": 4，
                "pos":
                [
                    0，
                    -2，
                    2
                ]，
                "level": 1，
                "flying": false，
                "atk_flying": false
            }，
            {
                "id": 6，
                "camp": 0，
                "name": "Priest (Level 1)"，
                "cost": 2，
                "atk": 0，
                "max_hp": 2，
                "hp": 2，
                "atk_range":
                [
                    0，
                    0
                ]，
                "max_move": 3，
                "cool_down": 4，
                "pos":
                [
                    0，
                    0，
                    0
                ]，
                "level": 1，
                "flying": false，
                "atk_flying": false
            }
        ]，
        "barracks":
        [
            {
                "pos":
                [
                    0，
                    0，
                    0
                ]，
                "camp": null，
                "summon_pos_list": []
            }
        ]，
        "relics":
        [
            {
                "camp": 0，
                "max_hp": 30，
                "hp": 30，
                "pos":
                [
                    0，
                    0，
                    0
                ]，
                "name": "Relic (belongs to Player 0)"，
                "id": 0
            }，
            {
                "camp": 1，
                "max_hp": 30，
                "hp": 30，
                "pos":
                [
                    1，
                    1，
                    -2
                ]，
                "name": "Relic (belongs to Player 1)"，
                "id": 1
            }
        ]，
        "obstacles": []
    }，
    "players":
    [
        {
            "camp": 0，
            "artifact":
            [
                {
                    "id": 0，
                    "name": "HolyLight"，
                    "camp": 0，
                    "cost": 6，
                    "max_cool_down": 6，
                    "cool_down_time": 0，
                    "state": "Ready"，
                    "target_type": "Pos"
                }
            ]，
            "mana": 9，
            "max_mana": 9，
            "creature_capacity":
            [
                {
                    "type": "Archer"，
                    "available_count": 3，
                    "cool_down_list": []
                }
            ]，
            "newly_summoned_id_list": []
        }，
        {
            "camp": 1，
            "artifact":
            [
                {
                    "id": 1，
                    "name": "HolyLight"，
                    "camp": 1，
                    "cost": 6，
                    "max_cool_down": 6，
                    "cool_down_time": 0，
                    "state": "Ready"，
                    "target_type": "Pos"
                }
            ]，
            "mana": 0，
            "max_mana": 2，
            "creature_capacity":
            [
                {
                    "type": "Archer"，
                    "available_count": 3，
                    "cool_down_list": []
                }
            ]，
            "newly_summoned_id_list":
            [
                3
            ]
        }
    ]，
    "round": 0，
    "camp": 0
}
```