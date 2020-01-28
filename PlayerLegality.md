[toc]

# Player 合法性检测

## 接口

```python
Parser(game_map) 	#合法性检测器的构造函数，传入游戏状态系统对象
Parser.parse(operation)	#控制器传入符合Json格式的字符串或者字典，由合法性检测section进行处理
Parser.set_round(round) #修改合法性检测的round参数（在检测例如是否在本回合召唤时有用）

# example
parser = Parser(game_map)
parser.set_round(1)
parser.parse(operation)
```

## Operation Json格式

> 接收json->解析json->合法性判断->调用游戏状态接口

### 总体

```json
{
  "player": 1,				//玩家id，0为先手玩家，1为后手玩家
  "operation_type": "move",	//操作方法
  "round": 1,				//该操作对应的逻辑回合
  "operation_parameters": {}//具体参数
}
```

### operation type

#### 游戏开始

- forbid
- select

#### 游戏中

- startround
- endround
- summon
- move
- attack
- use

### operation parameters

#### 游戏开始

---

##### 神器禁用

```json
//operation_type: "forbid"
{
    "type": "Artifact",
    "target": "A/abstain or (1/-1)"	//禁用神器的种类（字符串还是id）		 
}
```

- 不在范围内的都属于弃权

##### 神器选择

```json
//operation_type: "select"
{
    "type": "Artifact",
    "target": 2		//选择神器的种类
}
```

###### 合法性

- 不在范围内？

##### 生物选择

```json
//operation_type: "select"
{
	"type": "Bio",
    "target": 3		//选择生物种类
}
```

###### 合法性

- 5种
- 不同

##### 陷阱选取

```json
//operation_type: "select"
{
    "type": "Trap",
    "target": 1		//选择陷阱种类
}
```

###### 合法性

- 3张



#### 游戏中

---

##### 开始回合

```json
//operation_type: "startround"
null（不需要额外参数）
```

##### 结束回合

```json
//operation_type: "endround"
null（不需要额外参数）
```

##### 移动

```json
//operation_type: "move"
{
    "mover": 1,				//移动的生物的编号
    "position": [x, y, z]	//移动到的位置
}
```

###### 合法性

- 深渊
  - 空中单位可以经过和停留
- 单位重叠
- 最大行动力 > 0
- 非本回合 召唤 (除非有特殊词条)
- 本回合未 移动 或 攻击 (除非有特殊词条)
- 不处于一些导致无法移动的状态中

##### 召唤（出兵）

```json
//operation_type: "summon"
{
  "postion": [x, y, z], 	//召唤位置
  "type": "Elf",	 		//召唤种类
  "star": 5					//召唤星级
}
```

###### 合法性

- 是否在出兵点
- 生物重叠
- 生物槽消耗
- 法力值消耗

##### 攻击

```json
//operation_type: "attack"
{
  "attacker": 8,		//攻击方生物的编号
  "target": 2,			//攻击目标（生物/神迹)的编号
}
```

###### 合法性

- 攻击者合法：
  - 攻击者攻击力 $ > 0 $
  - 不处于死亡状态
  - 攻击者 非本回合 召唤 (除非有特殊词条)
  - 攻击者 本回合未 移动 或 攻击 (除非有特殊词条)
  - 攻击者 不处于一些导致无法攻击的状态中
- 被攻击者 为 合法攻击目标 当且仅当:
  - 被攻击者 与 攻击者 的距离(无视地形)在 攻击者 的 攻击范围 内
  - 被攻击者 生命值 > 0
  - 被攻击者 为 空中生物 时 攻击者 有 飞行 或 对空 词条
  - 被攻击者 不处于一些导致无法被攻击的状态中

##### 使用神器

```json
//operation_type: "use"
{
    "type": "Artifact",
    "card": 1,	//使用的神器的编号
    "target":	2	//有些神器有使用对象(optional)
}
```

###### 合法性

- 法力消耗
- 再装填时间

##### 设置陷阱

to be continue ...
