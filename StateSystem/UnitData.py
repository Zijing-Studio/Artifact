UNIT_DATA = {
    "Archer": {
        "cost": [2,4,6],
        "atk": [1,2,3],
        "hp": [1,3,5],
        "atk_range": [(2,4),(2,4),(2,4)],
        "max_move": [3,3,3],
        "cool_down": [4,4,4],
        "duplicate": 3,
        "flying": False,            # 飞行
        "atk_flying": True,         # 对空
        "agility": False,           # 迅捷
        "holy_shield": False        # 圣盾
    },
    "Swordman": {
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
        "atk": [1,2,3],
        "hp": [1,1,2],
        "atk_range": [(0,1),(0,1),(0,1)],
        "max_move": [5,5,5],
        "cool_down": [2,2,2],
        "duplicate": 4,
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
        "duplicate": 4,
        "flying": False,
        "atk_flying": False,
        "agility": False,
        "holy_shield": True
    },
    "VolcanoDragon": {
        "cost": [5,7,9],
        "atk": [3,4,5],
        "hp": [5,7,9],
        "atk_range": [(1,2),(1,2),(1,2)],
        "max_move": [3,3,3],
        "cool_down": [5,5,5],
        "duplicate": 3,
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
        "cool_down": 6
    }
]