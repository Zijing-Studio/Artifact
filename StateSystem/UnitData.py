UNIT_DATA = {
    "Archer": {
        "cost": [2,4,6],
        "atk": [1,2,3],
        "hp": [1,2,3],
        "atk_range": [(3,4),(3,4),(3,4)],
        "max_move": [3,3,3],
        "cool_down": [4,4,4],
        "duplicate": 3,
        "flying": False,            # 飞行
        "atk_flying": True,         # 对空
        "agility": False,           # 迅捷
        "holy_shield": False        # 圣盾
    },
    "Swordsman": {
        "cost": [2,4,6],
        "atk": [2,4,6],
        "hp": [2,4,6],
        "atk_range": [(1,1),(1,1),(1,1)],
        "max_move": [3,3,3],
        "cool_down": [3,3,3],
        "duplicate": 4,
        "flying": False,
        "atk_flying": False,
        "agility": False,
        "holy_shield": False
    },
    "BlackBat": {
        "cost": [2,3,5],
        "atk": [1,3,5],
        "hp": [1,1,2],
        "atk_range": [(0,1),(0,1),(0,1)],
        "max_move": [5,5,5],
        "cool_down": [2,2,2],
        "duplicate": 3,
        "flying": True,
        "atk_flying": True,
        "agility": False,
        "holy_shield": False
    },
    "Priest": {
        "cost": [2,3,5],
        "atk": [0,0,0],
        "hp": [2,2,3],
        "atk_range": [(0,0),(0,0),(0,0)],
        "max_move": [3,3,3],
        "cool_down": [4,4,5],
        "duplicate": 3,
        "flying": False,
        "atk_flying": False,
        "agility": False,
        "holy_shield": False
    },
    "VolcanoDragon": {
        "cost": [5,7,9],
        "atk": [3,4,5],
        "hp": [5,7,9],
        "atk_range": [(1,2),(1,2),(1,2)],
        "max_move": [2,2,2],
        "cool_down": [5,5,5],
        "duplicate": 3,
        "flying": False,
        "atk_flying": False,
        "agility": False,
        "holy_shield": False
    },
    "Inferno": {
        "cost": [8],
        "atk": [8],
        "hp": [12],
        "atk_range": [(1,1)],
        "max_move": [3],
        "cool_down": [999],
        "duplicate": 1,
        "flying": False,
        "atk_flying": False,
        "agility": False,
        "holy_shield": False
    }
}

ARTIFACTS = [
    {
        "name": "HolyLight",
        "target_type": "Pos",
        "cost": 6,
        "cool_down": 4
    },
    {
        "name": "SalamanderShield",
        "target_type": "Unit",
        "cost": 6,
        "cool_down": 4
    },
    {
        "name": "InfernoFlame",
        "target_type": "Pos",
        "cost": 8,
        "cool_down": 6
    }
]

UNIT_NAME_PARSED = {
    "Archer": 0,
    "Swordsman": 1,
    "BlackBat": 2,
    "Priest": 3,
    "VolcanoDragon": 4,
    "Inferno": 5
}

ARTIFACT_NAME_PARSED = {
    "HolyLight": 0,
    "SalamanderShield": 1,
    "InfernoFlame": 2
}

ARTIFACT_STATE_PARSED = {
    "Ready": 0,
    "In Use": 1,
    "Cooling Down":2
}

ARTIFACT_TARGET_PARSED = {
    "Pos": 0,
    "Unit": 1
}