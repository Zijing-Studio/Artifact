# Usage

```python
emit(Event(<name>,[parameter_dict = {}],[priority = 0]))
```



# Event protocol

[toc]

## Damage

```json
{
    "source": Unit,
    "target": Unit,
    "damage": int
}
```

## Attack

```json
{
    "source": Unit,
    "target": Unit
}
```

## Attacking

发动攻击前触发器

```json
{
    "source": Unit,
    "target": Unit
}
```

## Attacked

发动攻击后触发器

```json
{
    "source": Unit,
    "target": Unit
}
```

## Move

```json
{
    "source": Unit,
    "dest": Pos
}
```

## UpdateRingBuff

```json
{}

Priority = 3 (when in move)
```

## Leave

```json
{
    "source": Unit,
    "pos": Pos
}
```

## Arrive

```
{
	"source": Unit,
    "pos": Pos
}
```

## Summon

```json
{
    "type": String,
    "level": int,
    "pos": Pos,
    "camp": Camp(int)
}
```

## Spawn

召唤完成的事件

```json
{
    "source": unit,
    "pos": Pos
}
```

## CheckDeath

判断死亡的事件，交由**State System**处理

```
{}
```

## Death

一个生物死亡的事件

```
{
	"source": unit
}
```

## TurnStart

依次触发如下事件，没有参数

### Refresh

玩家回合开始刷新事件，会刷新法力水晶和生物冷却

```
{
	"camp": camp
}
```

### CheckBarrack

回合开始刷新驻扎点占领情况，没有参数，交由**State System**处理

### NewTurn

供生物接受，触发回合开始的触发器

## TurnEnd

回合结束事件，会触发所有回合结束事件

## Heal

治疗事件

```
{
    "source": Unit,
    "target": Unit,
    "heal": int
}
```

## ActivateArtifact

使用神器

```
{
	"camp": camp,
	"name": String,
	"target": pos/unit
}
```

