# State System Parse

### Usage

```python
sys.parse()
```

### Return

A dictionary of all information.  

#### Ex:

```python
{
    'map': {
        'units': [
            {
                'id': 4, 
                'camp': 0, 
                'name': 'BlackBat (Level 1)', 
                'cost': 2, 
                'atk': 1, 
                'max_hp': 1,
                'hp': 1, 
                'atk_range': (0, 1), 
                'max_move': 5, 
                'cool_down': 2, 
                'pos': (0, 1, -1), 
                'level': 1, 
                'flying': True,
                'atk_flying': True, 
                'agility': False, 
                'holy_shield': False
            }, {
                'id': 5, 
                'camp': 0, 
                'name': 'Inferno (Level 1)',
                'cost': 8, 
                'atk': 8, 
                'max_hp': 8, 
                'hp': 8, 
                'atk_range': (1, 1), 
                'max_move': 3, 
                'cool_down': 999, 
                'pos': (0, 1, 0), 
                'level': 1, 
                'flying': False, 
                'atk_flying': False,
                'agility': False, 
                'holy_shield': False
            }
        ],
        'barracks': [
            {
                'pos': (-6, -6, 12),
                'camp': None, 
                'summon_pos_list': [(-7, -5, 12), (-5, -7, 12), (-5, -6, 11)]
            }, {
                'pos': (6, 6, -12), 
                'camp': None,
                'summon_pos_list': [(7, 5, -12), (5, 7, -12), (5, 6, -11)]
            }, {
                'pos': (0, -5, 5),
                'camp': None, 
                'summon_pos_list': [(0, -4, 4), (-1, -4, 5), (-1, -5, 6)]
            }, {'pos': (0, 5, -5),
                'camp': None,
                'summon_pos_list': [(0, 4, -4), (1, 4, -5), (1, 5, -6)]
            }
        ], 
        'relics': [
            {'camp': 0, 'max_hp': 30, 'hp': 30, 'pos': (-7, 7, 0), 'name': 'Relic (belongs to Player 0)', 'id': 0},
            {'camp': 1, 'max_hp': 30, 'hp': 30, 'pos': (7, -7, 0), 'name': 'Relic (belongs to Player 1)', 'id': 1}
        ], 
        'obstacles': [
            {'type': 'Abyss', 'pos': (0, 0, 0), 'allow_flying': True, 'allow_ground': False}, 
            {'type': 'Abyss', 'pos': (-1, 0, 1), 'allow_flying': True, 'allow_ground': False},
            {'type': 'Abyss', 'pos': (0, -1, 1), 'allow_flying': True, 'allow_ground': False}, 
            {'type': 'Abyss', 'pos': (1, -1, 0), 'allow_flying': True, 'allow_ground': False},
            {'type': 'Abyss', 'pos': (1, 0, -1), 'allow_flying': True, 'allow_ground': False},
            {'type': 'Abyss', 'pos': (0, 1, -1), 'allow_flying': True, 'allow_ground': False}, 
            {'type': 'Abyss', 'pos': (-1, 1, 0), 'allow_flying': True, 'allow_ground': False}, 
            {'type': 'Abyss', 'pos': (-2, -1, 3), 'allow_flying': True, 'allow_ground': False},
            {'type': 'Abyss', 'pos': (-1, -2, 3), 'allow_flying': True, 'allow_ground': False}, 
            {'type': 'Abyss', 'pos': (-2, -2, 4), 'allow_flying': True, 'allow_ground': False},
            {'type': 'Abyss', 'pos': (-3, -2, 5), 'allow_flying': True, 'allow_ground': False}, 
            {'type': 'Abyss', 'pos': (-4, -4, 8), 'allow_flying': True, 'allow_ground': False}, 
            {'type': 'Abyss', 'pos': (-5, -4, 9), 'allow_flying': True, 'allow_ground': False},
            {'type': 'Abyss', 'pos': (-4, -5, 9), 'allow_flying': True, 'allow_ground': False},
            {'type': 'Abyss', 'pos': (-5, -5, 10), 'allow_flying': True, 'allow_ground': False}, 
            {'type': 'Abyss', 'pos': (-6, -5, 11), 'allow_flying': True, 'allow_ground': False}, 
            {'type': 'Abyss', 'pos': (1, 2, -3), 'allow_flying': True, 'allow_ground': False}, 
            {'type': 'Abyss', 'pos': (2, 1, -3), 'allow_flying': True, 'allow_ground': False}, 
            {'type': 'Abyss', 'pos': (2, 2, -4), 'allow_flying': True, 'allow_ground': False},
            {'type': 'Abyss', 'pos': (3, 2, -5), 'allow_flying': True, 'allow_ground': False}, 
            {'type': 'Abyss', 'pos': (4, 4, -8), 'allow_flying': True, 'allow_ground': False},
            {'type': 'Abyss', 'pos': (5, 4, -9), 'allow_flying': True, 'allow_ground': False},
            {'type': 'Abyss', 'pos': (4, 5, -9), 'allow_flying': True, 'allow_ground': False}, 
            {'type': 'Abyss', 'pos': (5, 5, -10), 'allow_flying': True, 'allow_ground': False}, 
            {'type': 'Abyss', 'pos': (6, 5, -11), 'allow_flying': True, 'allow_ground': False}
        ],
        'ground_obstacles': [
            {'type': 'Abyss', 'pos': (0, 0, 0), 'allow_flying': True, 'allow_ground': False}, 
            {'type': 'Abyss', 'pos': (-1, 0, 1), 'allow_flying': True, 'allow_ground': False}, 
            {'type': 'Abyss', 'pos': (0, -1, 1), 'allow_flying': True, 'allow_ground': False},
            {'type': 'Abyss', 'pos': (1, -1, 0), 'allow_flying': True, 'allow_ground': False}, 
            {'type': 'Abyss', 'pos': (1, 0, -1), 'allow_flying': True, 'allow_ground': False},
            {'type': 'Abyss', 'pos': (0, 1, -1), 'allow_flying': True, 'allow_ground': False},
            {'type': 'Abyss', 'pos': (-1, 1, 0), 'allow_flying': True, 'allow_ground': False}, 
            {'type': 'Abyss', 'pos': (-2, -1, 3), 'allow_flying': True, 'allow_ground': False},
            {'type': 'Abyss', 'pos': (-1, -2, 3), 'allow_flying': True, 'allow_ground': False}, 
            {'type': 'Abyss', 'pos': (-2, -2, 4), 'allow_flying': True, 'allow_ground': False},
            {'type': 'Abyss', 'pos': (-3, -2, 5), 'allow_flying': True, 'allow_ground': False},
            {'type': 'Abyss', 'pos': (-4, -4, 8), 'allow_flying': True, 'allow_ground': False}, 
            {'type': 'Abyss', 'pos': (-5, -4, 9), 'allow_flying': True, 'allow_ground': False}, 
            {'type': 'Abyss', 'pos': (-4, -5, 9), 'allow_flying': True, 'allow_ground': False},
            {'type': 'Abyss', 'pos': (-5, -5, 10), 'allow_flying': True, 'allow_ground': False},
            {'type': 'Abyss', 'pos': (-6, -5, 11), 'allow_flying': True, 'allow_ground': False},
            {'type': 'Abyss', 'pos': (1, 2, -3), 'allow_flying': True, 'allow_ground': False}, 
            {'type': 'Abyss', 'pos': (2, 1, -3), 'allow_flying': True, 'allow_ground': False}, 
            {'type': 'Abyss', 'pos': (2, 2, -4), 'allow_flying': True, 'allow_ground': False}, 
            {'type': 'Abyss', 'pos': (3, 2, -5), 'allow_flying': True, 'allow_ground': False}, 
            {'type': 'Abyss', 'pos': (4, 4, -8), 'allow_flying': True, 'allow_ground': False}, 
            {'type': 'Abyss', 'pos': (5, 4, -9), 'allow_flying': True, 'allow_ground': False}, 
            {'type': 'Abyss', 'pos': (4, 5, -9), 'allow_flying': True, 'allow_ground': False},
            {'type': 'Abyss', 'pos': (5, 5, -10), 'allow_flying': True, 'allow_ground': False},
            {'type': 'Abyss', 'pos': (6, 5, -11), 'allow_flying': True, 'allow_ground': False}
        ],
        'flying_obstacles': []
    }, 
    'players': [
        {
            'camp': 0,
         	'artifact': [
                {
                    'id': 0,
                    'name': 'SalamanderShield',
                    'camp': 0, 
                    'cost': 6, 
                    'max_cool_down': 6, 
                 	'cool_down_time': 0, 
                 	'state': 'Ready', 
                 	'target_type': 'Unit'
             	}, {
                    'id': 1,
                    'name': 'InfernoFlame',
                    'camp': 0, 
                    'cost': 6, 
                    'max_cool_down': 6, 
                    'cool_down_time': 0, 
                    'state': 'In Use',
                    'target_type': 'Pos'
             	}
         	], 
         	'mana': -15, 
         	'max_mana': 1,
         	'creature_capacity': [
             	{
                 	'type': 'BlackBat', 
                 	'available_count': 3,
                 	'cool_down_list': []
             	}, {
                 	'type': 'Priest', 
                 	'available_count': 4,
                 	'cool_down_list': []
             	}, {
                 	'type': 'Archer',
                 	'available_count': 3,
                    'cool_down_list': []
             	}
         	], 
        	'newly_summoned_id_list': [4, 5]
        }, {
            'camp': 1, 
            'artifact': [
                {
                    'id': 2,
                    'name': 'SalamanderShield', 
                    'camp': 1,
                    'cost': 6, 
                    'max_cool_down': 6, 
                    'cool_down_time': 0, 
                    'state': 'Ready', 
                    'target_type': 'Unit'
                }, {
                    'id': 3,
                    'name': 'HolyLight',
                    'camp': 1, 
                    'cost': 6, 
                    'max_cool_down': 6,
                    'cool_down_time': 0, 
                    'state': 'Ready', 
                    'target_type': 'Pos'
                }
            ],
            'mana': 0,
            'max_mana': 2, 
            'creature_capacity': [
                {
                    'type': 'BlackBat',
                    'available_count': 3,
                    'cool_down_list': [2]
                }, {
                    'type': 'Priest',
                    'available_count': 4,
                    'cool_down_list': []
                }, {
                    'type': 'Archer', 
                    'available_count': 3,
                    'cool_down_list': []
                }
            ],
            'newly_summoned_id_list': [3]
        }
    ]
}                                                                                                                                                                                              
```

