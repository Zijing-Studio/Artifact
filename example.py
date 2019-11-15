#!/usr/bin/python
# -*- coding:utf-8 -*-

from StateSystem import StateSystem
from PlayerLegality.player_legality import Parser

game_map = StateSystem()
parser = Parser(game_map)

operations = [
    {
        "player": 0,
        "operation_type": "summon",
        "operation_parameters": {
            "position": [0, 0, 0],
            "type": "Archer",
            "star": 1
            }
    },
    {
        "player": 1,
        "operation_type": "summon",
        "operation_parameters": {
            "position": [0, 1, -1],
            "type": "Archer",
            "star": 1
            }
    },
    # move conflict
    {
        "player": 0,
        "operation_type": "move",
        "operation_parameters": {
            "mover": 0,
            "position": [0, 1, -1]
            }
    },
    # move successfully
    {
        "player": 0,
        "operation_type": "move",
        "operation_parameters": {
            "mover": 0,
            "position": [0, 3, -3]
            }
    },
    {
        "player": 0,
        "operation_type": "attack",
        "operation_parameters": {
            "attacker": 0,
            "target": 1
            }
    },
    ]

for op in operations:
    parser.parse(op)
