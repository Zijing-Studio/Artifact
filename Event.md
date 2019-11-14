# Usage

```python
emit(Event(<name>,[parameter_dict = {}],[priority = 0]))
```



# Event protocol

[toc]

## Damage

```json
{
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

发动攻击触发器

```json
{
    "source": Unit,
    "target": Unit
}
```

## Attacked

被指定为攻击目标

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

