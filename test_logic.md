## 测试用输入指令

初始化

{"player_list": [1, 1], "replay": "replay.txt"}

gameinfo:

{"player": 0, "content": {"operation_type": "gameinfo"}}

summon:

{"player": 0, "content": {"round": 0, "operation_type": "summon", "operation_parameters": {"position": [-5, -11, 16], "type": "Archer", "star": 1}}}

move:

{"player": 0, "content": {"round": 0, "operation_type": "move", "operation_parameters": {"mover": 1, "position": [0, 0, 0]}}}

attack:

{"player": 0, "content": {"round": 3, "operation_type": "attack", "operation_parameters": {"attacker": 1, "target": 5}}}

end:
{"player": 0, "content": {"player": 0, "content": {"round": 0, "operation_type": "end"}}}

AI异常退出

{"player": -1, "content": {"error": 0, "player": 1, "error_log": ""}}

AI本回合超时

{"player": -1, "content": {"error": 1, "player": 1, "state": 4, "error_log": ""}}


## logic的输出

{"state": 233, "listen": [0], "player": [0, 1], "content": ["0", "1"]}