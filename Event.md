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

Priority = -4
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