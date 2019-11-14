command统一格式：

| 回合数      | 命令类型  | 参数 |       |      |      |
| ----------- | --------- | ---- | ----- | ---- | ---- |
| currentTurn | 0(Summon) | Type | posX  | posZ | 0    |
| currentTurn | 1(Move)   | id   | desX  | desY | 0    |
| currentTurn | 2(Attack) | id   | tarId | 0    | 0    |



一个例子：
0(版本号)
0 0 1 -2 17 0
0 0 5 -1 15 0
0 0 6 0 14 0
0 0 8 1 15 0
1 1 2 5 14 0
1 1 0 -4 17 0
2 2 1 0 0 0
2 2 2 1 0 0