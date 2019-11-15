#!/usr/bin/python
# -*- coding:utf-8 -*-

from StateSystem import StateSystem
from PlayerLegality.player_legality import Parser

game_map = StateSystem()
parser = Parser(game_map)

operations = [
    # round 1
    [{
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
    }],
    # round 2
    [
    # move conflict
    {
        "player": 0,
        "operation_type": "move",
        "operation_parameters": {
            "mover": 0,
            "position": [0, 1, -1]
            }
    }],
    # round 3
    [
    # move out of range
    {
        "player": 0,
        "operation_type": "move",
        "operation_parameters": {
            "mover": 0,
            "position": [0, 3, -3]
            }
    }
    ],
    # round 4
    [
    # attack out of range
    {
        "player": 0,
        "operation_type": "attack",
        "operation_parameters": {
            "attacker": 0,
            "target": 1
            }
    }
    ],
    # round 5
    [
    # move successfully
    {
        "player": 0,
        "operation_type": "move",
        "operation_parameters": {
            "mover": 0,
            "position": [0, -1, 1]
            }
    }
    ],
    # round 6
    [
    # attack successfully
    {
        "player": 0,
        "operation_type": "attack",
        "operation_parameters": {
            "attacker": 0,
            "target": 1
            }
    }
    ]
    ]

i = 0
for round_operations in operations:
    i += 1
    print("\n===========round {}==========\n".format(i))
    parser.set_round(i)
    for op in round_operations:
        parser.parse(op)
