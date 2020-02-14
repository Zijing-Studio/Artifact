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

json对象（生物）的数组。下面对生物进行解释。

#### id

整数。表示生物的id。

#### camp

整数。表示生物所属阵营。

#### type

字符串。表示生物的种类。

#### name

字符串。表示生物的名字。

#### cost

整数。表示生物的法力消耗。

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

布尔值。表示生物是否飞行。

#### atk_flying

布尔值。表示生物能否攻击飞行生物。

#### agility

布尔值。表示生物是否迅捷。

#### holy_shield

布尔值。表示生物是否具有圣盾。

#### can_atk

布尔值。表示生物能否攻击。

#### can_move

布尔值。表示生物能否移动。

### barracks

json对象（驻扎点）的数组。下面对驻扎点进行解释。

#### pos

三元整数数组。表示驻扎点的位置。

#### camp

整数。表示驻扎点所属阵营。

#### summon_pos_list

三元整数数组的数组。表示驻扎点所控制的出兵点的位置。

### relics

json对象（神迹）的数组。下面对神迹进行解释。

#### camp

整数。表示神迹所属阵营。

#### max_hp

整数。表示神迹生命上限。

#### hp

整数。表示神迹生命值。

#### pos

三元整数数组。表示神迹的位置。

#### summon_pos_list

三元整数数组的数组。表示神迹控制的初始出兵点的位置。

#### name

字符串。表示神迹的名字。

#### id

整数。表示神迹的id。

### obstacles

json对象（Obstacle）的数组。下面对Obstacle进行解释。

#### type

字符串。表示Obstacle的种类。

#### pos

三元整数数组。表示Obstacle的位置。

#### allow_flying

布尔值。表示Obstacle是否允许飞行单位通过。

#### allow_ground

布尔值。表示Obstacle是否允许地面单位通过。

## players

json对象（玩家）的二元数组。下面对玩家进行解释。

### camp

0或1。表示该玩家所处的阵营。（与下标相同）

### artifact

json对象（神器）的数组。下面对神器进行解释。

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

字符串。表示神器使用对象的种类（Unit或Pos）。

### mana

整数。表示玩家当前法力值。

### max_mana

整数。表示玩家最大法力值。

### creature_capacity

#### type

字符串。表示生物种类。

#### available_count

整数。表示生物的生物槽容量。

#### cool_down_list

整数数组。表示生物的冷却时间。

### newly_summoned_id_list

整数数组。表示玩家最新召唤的生物的id。

## round

整数。表示当前回合数。

## camp

整数。表示你所属阵营。

# 示例

```json
{
	"map": {
		"units": [{
			"id": 4,
			"camp": 0,
			"name": "BlackBat (Level 1)",
			"cost": 2,
			"atk": 1,
			"max_hp": 1,
			"hp": 1,
			"atk_range": [0, 1],
			"max_move": 5,
			"cool_down": 2,
			"pos": [0, 1, -1],
			"level": 1,
			"flying": true,
			"atk_flying": true,
			"agility": false,
			"holy_shield": false
		}, {
			"id": 5,
			"camp": 0,
			"name": "Inferno (Level 1)",
			"cost": 8,
			"atk": 8,
			"max_hp": 8,
			"hp": 8,
			"atk_range": [1, 1],
			"max_move": 3,
			"cool_down": 999,
			"pos": [0, 1, 0],
			"level": 1,
			"flying": false,
			"atk_flying": false,
			"agility": false,
			"holy_shield": false
		}],
		"barracks": [{
			"pos": [-6, -6, 12],
			"camp": null,
			"summon_pos_list": [
				[-7, -5, 12],
				[-5, -7, 12],
				[-5, -6, 11]
			]
		}, {
			"pos": [6, 6, -12],
			"camp": null,
			"summon_pos_list": [
				[7, 5, -12],
				[5, 7, -12],
				[5, 6, -11]
			]
		}, {
			"pos": [0, -5, 5],
			"camp": null,
			"summon_pos_list": [
				[0, -4, 4],
				[-1, -4, 5],
				[-1, -5, 6]
			]
		}, {
			"pos": [0, 5, -5],
			"camp": null,
			"summon_pos_list": [
				[0,
					4, -4
				],
				[1, 4, -5],
				[1, 5, -6]
			]
		}],
		"relics": [{
			"camp": 0,
			"max_hp": 30,
			"hp": 30,
			"pos": [-7, 7, 0],
			"name": "Relic (belongs to Player 0)",
			"id": 0
		}, {
			"camp": 1,
			"max_hp": 30,
			"hp": 30,
			"pos": [7, -7, 0],
			"name": "Relic (belongs to Player 1)",
			"id": 1
		}],
		"obstacles": [{
			"type": "Abyss",
			"pos": [0, 0, 0],
			"allow_flying": true,
			"allow_ground": false
		}, {
			"type": "Abyss",
			"pos": [-1, 0, 1],
			"allow_flying": true,
			"allow_ground": false
		}, {
			"type": "Abyss",
			"pos": [0, -1, 1],
			"allow_flying": true,
			"allow_ground": false
		}, {
			"type": "Abyss",
			"pos": [1, -1, 0],
			"allow_flying": true,
			"allow_ground": false
		}, {
			"type": "Abyss",
			"pos": [1, 0, -1],
			"allow_flying": true,
			"allow_ground": false
		}, {
			"type": "Abyss",
			"pos": [0, 1, -1],
			"allow_flying": true,
			"allow_ground": false
		}, {
			"type": "Abyss",
			"pos": [-1, 1, 0],
			"allow_flying": true,
			"allow_ground": false
		}, {
			"type": "Abyss",
			"pos": [-2, -1, 3],
			"allow_flying": true,
			"allow_ground": false
		}, {
			"type": "Abyss",
			"pos": [-1, -2, 3],
			"allow_flying": true,
			"allow_ground": false
		}, {
			"type": "Abyss",
			"pos": [-2, -2, 4],
			"allow_flying": true,
			"allow_ground": false
		}, {
			"type": "Abyss",
			"pos": [-3, -2, 5],
			"allow_flying": true,
			"allow_ground": false
		}, {
			"type": "Abyss",
			"pos": [-4, -4, 8],
			"allow_flying": true,
			"allow_ground": false
		}, {
			"type": "Abyss",
			"pos": [-5, -4, 9],
			"allow_flying": true,
			"allow_ground": false
		}, {
			"type": "Abyss",
			"pos": [-4, -5, 9],
			"allow_flying": true,
			"allow_ground": false
		}, {
			"type": "Abyss",
			"pos": [-5, -5, 10],
			"allow_flying": true,
			"allow_ground": false
		}, {
			"type": "Abyss",
			"pos": [-6, -5, 11],
			"allow_flying": true,
			"allow_ground": false
		}, {
			"type": "Abyss",
			"pos": [1, 2, -3],
			"allow_flying": true,
			"allow_ground": false
		}, {
			"type": "Abyss",
			"pos": [2, 1, -3],
			"allow_flying": true,
			"allow_ground": false
		}, {
			"type": "Abyss",
			"pos": [2, 2, -4],
			"allow_flying": true,
			"allow_ground": false
		}, {
			"type": "Abyss",
			"pos": [3, 2, -5],
			"allow_flying": true,
			"allow_ground": false
		}, {
			"type": "Abyss",
			"pos": [4, 4, -8],
			"allow_flying": true,
			"allow_ground": false
		}, {
			"type": "Abyss",
			"pos": [5, 4, -9],
			"allow_flying": true,
			"allow_ground": false
		}, {
			"type": "Abyss",
			"pos": [4, 5, -9],
			"allow_flying": true,
			"allow_ground": false
		}, {
			"type": "Abyss",
			"pos": [5, 5, -10],
			"allow_flying": true,
			"allow_ground": false
		}, {
			"type": "Abyss",
			"pos": [6, 5, -11],
			"allow_flying": true,
			"allow_ground": false
		}],
		"ground_obstacles": [{
				"type": "Abyss",
				"pos": [0, 0, 0],
				"allow_flying": true,
				"allow_ground": false
			}, {
				"type": "Abyss",
				"pos": [-1, 0, 1],
				"allow_flying": true,
				"allow_ground": false
			}, {
				"type": "Abyss",
				"pos": [0, -1, 1],
				"allow_flying": true,
				"allow_ground": false
			}, {
				"type": "Abyss",
				"pos": [1, -1, 0],
				"allow_flying": true,
				"allow_ground": false
			}, {
				"type": "Abyss",
				"pos": [1, 0, -1],
				"allow_flying": true,
				"allow_ground": false
			}, {
				"type": "Abyss",
				"pos": [0, 1, -1],
				"allow_flying": true,
				"allow_ground": false
			}, {
				"type": "Abyss",
				"pos": [-1, 1, 0],
				"allow_flying": true,
				"allow_ground": false
			}, {
				"type": "Abyss",
				"pos": [-2, -1, 3],
				"allow_flying": true,
				"allow_ground": false
			}, {
				"type": "Abyss",
				"pos": [-1, -2, 3],
				"allow_flying": true,
				"allow_ground": false
			}, {
				"type": "Abyss",
				"pos": [-2, -2, 4],
				"allow_flying": true,
				"allow_ground": false
			}, {
				"type": "Abyss",
				"pos": [-3, -2, 5],
				"allow_flying": true,
				"allow_ground": false
			}, {
				"type": "Abyss",
				"pos": [-4, -4, 8],
				"allow_flying": true,
				"allow_ground": false
			}, {
				"type": "Abyss",
				"pos": [-5, -4, 9],
				"allow_flying": true,
				"allow_ground": false
			}, {
				"type": "Abyss",
				"pos": [-4, -5, 9],
				"allow_flying": true,
				"allow_ground": false
			}, {
				"type": "Abyss",
				"pos": [-5, -5, 10],
				"allow_flying": true,
				"allow_ground": false
			}, {
				"type": "Abyss",
				"pos": [-6, -5, 11],
				"allow_flying": true,
				"allow_ground": false
			}, {
				"type": "Abyss",
				"pos": [1, 2, -3],
				"allow_flying": true,
				"allow_ground": false
			}, {
				"type": "Abyss",
				"pos": [2, 1, -3],
				"allow_flying": true,
				"allow_ground": false
			}, {
				"type": "Abyss",
				"pos": [2, 2, -4],
				"allow_flying": true,
				"allow_ground": false
			}, {
				"type": "Abyss",
				"pos": [3, 2, -5],
				"allow_flying": true,
				"allow_ground": false
			}, {
				"type": "Abyss",
				"pos": [4, 4, -8],
				"allow_flying": true,
				"allow_ground": false
			},
			{
				"type": "Abyss",
				"pos": [5, 4, -9],
				"allow_flying": true,
				"allow_ground": false
			}, {
				"type": "Abyss",
				"pos": [4, 5, -9],
				"allow_flying": true,
				"allow_ground": false
			}, {
				"type": "Abyss",
				"pos": [5, 5, -10],
				"allow_flying": true,
				"allow_ground": false
			}, {
				"type": "Abyss",
				"pos": [6, 5, -11],
				"allow_flying": true,
				"allow_ground": false
			}
		],
		"flying_obstacles": []
	},
	"players": [{
		"camp": 0,
		"artifact": [{
			"id": 0,
			"name": "SalamanderShield",
			"camp": 0,
			"cost": 6,
			"max_cool_down": 6,
			"cool_down_time": 0,
			"state": "Ready",
			"target_type": "Unit"
		}, {
			"id": 1,
			"name": "InfernoFlame",
			"camp": 0,
			"cost": 6,
			"max_cool_down": 6,
			"cool_down_time": 0,
			"state": "In Use",
			"target_type": "Pos"
		}],
		"mana": -15,
		"max_mana": 1,
		"creature_capacity": [{
			"type": "BlackBat",
			"available_count": 3,
			"cool_down_list": []
		}, {
			"type": "Priest",
			"available_count": 4,
			"cool_down_list": []
		}, {
			"type": "Archer",
			"available_count": 3,
			"cool_down_list": []
		}],
		"newly_summoned_id_list": [4, 5]
	}, {
		"camp": 1,
		"artifact": [{
			"id": 2,
			"name": "SalamanderShield",
			"camp": 1,
			"cost": 6,
			"max_cool_down": 6,
			"cool_down_time": 0,
			"state": "Ready",
			"target_type": "Unit"
		}, {
			"id": 3,
			"name": "HolyLight",
			"camp": 1,
			"cost": 6,
			"max_cool_down": 6,
			"cool_down_time": 0,
			"state": "Ready",
			"target_type": "Pos"
		}],
		"mana": 0,
		"max_mana": 2,
		"creature_capacity": [{
			"type": "BlackBat",
			"available_count": 3,
			"cool_down_list": [2]
		}, {
			"type": "Priest",
			"available_count": 4,
			"cool_down_list": []
		}, {
			"type": "Archer",
			"available_count": 3,
			"cool_down_list": []
		}],
		"newly_summoned_id_list": [3]
	}]
}
```