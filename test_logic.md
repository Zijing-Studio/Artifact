## 测试用输入指令

初始化

{"player_list": [1, 1], "replay": "replay.map"}

gameinfo:

{"player": 0, "content": {"operation_type": "gameinfo"}}

summon:

{"player": 0, "content": {"round": 0, "operation_type": "summon", "operation_parameters": {"position": [-5, -11, 16], "type": "Archer", "star": 1}}}

move:

{"player": 0, "content": {"round": 0, "operation_type": "move", "operation_parameters": {"mover": 1, "position": [0, 0, 0]}}}

attack:

{"player": 0, "content": {"round": 3, "operation_type": "attack", "operation_parameters": {"attacker": 1, "target": 5}}}

end:
{"player": 0, "content": {"round": 0, "operation_type": "end"}}

AI异常退出

{"player": -1, "content": {"error": 0, "player": 1, "error_log": ""}}

AI本回合超时

{"player": -1, "content": {"error": 1, "player": 1, "state": 4, "error_log": ""}}


## logic的输出

{"state": 233, "listen": [0], "player": [0, 1], "content": ["0", "1"]}

## 一个例子

(这个例子后面有点问题用前两个回合的就好)

{"player_list": [1, 1], "replay": "replay.map"}

ROUND 0

{"player": 0, "content": {"round": 0, "operation_type": "summon", "operation_parameters": {"position": [-7, -12, 19], "type": "Archer", "star": 1}}}

{"player": 0, "content": {"round": 0, "operation_type": "end"}}

ROUND 1

{"player": 1, "content": {"round": 1, "operation_type": "summon", "operation_parameters": {"position": [9, -24, 15], "type": "Archer", "star": 1}}}

{"player": 1, "content": {"round": 1, "operation_type": "end"}}

ROUND 2

{"player": 0, "content": {"round": 2, "operation_type": "move", "operation_parameters": {"mover": 3, "position": [-2, -14, 16]}}}

{"player": 0, "content": {"round": 2, "operation_type": "end"}}

ROUND 3

{"player": 1, "content": {"round": 3, "operation_type": "move", "operation_parameters": {"mover": 4, "position": [6, -21, 15]}}}

{"player": 1, "content": {"round": 3, "operation_type": "end"}}

ROUND 4

{"player": 0, "content": {"round": 4, "operation_type": "move", "operation_parameters": {"mover": 3, "position": [1, -16, 15]}}}

{"player": 0, "content": {"round": 4, "operation_type": "end"}}

ROUND 5

{"player": 1, "content": {"round": 5, "operation_type": "move", "operation_parameters": {"mover": 4, "position": [3, -18, 15]}}}

{"player": 1, "content": {"round": 5, "operation_type": "end"}}

ROUND 6

{"player": 0, "content": {"round": 6, "operation_type": "end"}}

ROUND 7

{"player": 1, "content": {"round": 7, "operation_type": "attack", "operation_parameters": {"attacker": 4, "target": 3}}}

{"player": 1, "content": {"round": 7, "operation_type": "end"}}

ROUND 8

{"player": 0, "content": {"round": 8, "operation_type": "move", "operation_parameters": {"mover": 3, "position": [2, -17, 15]}}}

{"player": 0, "content": {"round": 8, "operation_type": "end"}}

ROUND 9

{"player": 1, "content": {"round": 9, "operation_type": "end"}}

ROUND 10

{"player": 0, "content": {"round": 10, "operation_type": "attack", "operation_parameters": {"attacker": 3, "target": 4}}}

{"player": 0, "content": {"round": 10, "operation_type": "end"}}

ROUND 11

{"player": 1, "content": {"round": 11, "operation_type": "end"}}

ROUND 12

{"player": 0, "content": {"round": 12, "operation_type": "move", "operation_parameters": {"mover": 3, "position": [5, -20, 15]}}}

{"player": 0, "content": {"round": 12, "operation_type": "end"}}

ROUND 13

{"player": 1, "content": {"round": 13, "operation_type": "end"}}

ROUND 14

{"player": 0, "content": {"round": 14, "operation_type": "move", "operation_parameters": {"mover": 3, "position": [8, -23, 15]}}}

{"player": 0, "content": {"round": 14, "operation_type": "end"}}

ROUND 15

{"player": 1, "content": {"round": 15, "operation_type": "end"}}

ROUND 16

{"player": 0, "content": {"round": 16, "operation_type": "move", "operation_parameters": {"mover": 3, "position": [8, -24, 16]}}}

{"player": 0, "content": {"round": 16, "operation_type": "end"}}

ROUND 17

{"player": 1, "content": {"round": 17, "operation_type": "end"}}

ROUND 18

{"player": 0, "content": {"round": 18, "operation_type": "attack", "operation_parameters": {"attacker": 3, "target": 1}}}

{"player": 0, "content": {"round": 18, "operation_type": "end"}}

ROUND 19

{"player": 1, "content": {"round": 19, "operation_type": "end"}}

ROUND 20

{"player": 0, "content": {"round": 20, "operation_type": "attack", "operation_parameters": {"attacker": 3, "target": 1}}}

{"player": 0, "content": {"round": 20, "operation_type": "end"}}

ROUND 21

{"player": 1, "content": {"round": 21, "operation_type": "end"}}

...

ROUND 46

{"player": 0, "content": {"round": 46, "operation_type": "attack", "operation_parameters": {"attacker": 3, "target": 1}}}

{"player": 0, "content": {"round": 46, "operation_type": "end"}}