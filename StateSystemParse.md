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
                'id': 3, 
                'camp': 1, 
                'name': 'BlackBat (Level 1)', 
                'cost': 2, 
                'atk': 1, 
                'max_hp': 1, 
                'hp': 1, 
                'atk_range': (0, 1), 
                'max_move': 5, 
                'cool_down': 2, 
                'pos': (0, 0, 0), 
                'level': 1, 
                'flying': True, 
                'atk_flying': True
            }, {
                'id': 4, 
                'camp': 0, 
                'name': 'Priest (Level 1)', 
                'cost': 2, 
                'atk': 0, 
                'max_hp': 2, 
                'hp': 2, 
                'atk_range': (0, 0), 
                'max_move': 3, 
                'cool_down': 4, 
                'pos': (0, 1, -1), 
                'level': 1, 
                'flying': False, 
                'atk_flying': False
            }, {
                'id': 5, 
                'camp': 0, 
                'name': 'Priest (Level 1)', 
                'cost': 2, 
                'atk': 0, 
                'max_hp': 2, 
                'hp': 2, 
                'atk_range': (0, 0), 
                'max_move': 3, 
                'cool_down': 4, 
                'pos': (0, -2, 2), 
                'level': 1, 
                'flying': False, 
                'atk_flying': False
            }, {
                'id': 6, 
                'camp': 0, 
                'name': 'Priest (Level 1)',
                'cost': 2, 
                'atk': 0, 
                'max_hp': 2, 
                'hp': 2,
                'atk_range': (0, 0), 
                'max_move': 3, 
                'cool_down': 4, 
                'pos': (0, 0, 0), 
                'level': 1, 
                'flying': False, 
                'atk_flying': False
            }
        ], 
        'barracks': [
            {
                'pos': (0, 0, 0), 
                'camp': None,
                'summon_pos_list': []
            }
        ], 
        'relics': [
            {'camp': 0, 'max_hp': 30, 'hp': 30, 'pos': (0, 0, 0), 'name': 'Relic (belongs to Player 0)', 'id': 0}, 
            {'camp': 1, 'max_hp': 30, 'hp': 30, 'pos': (1, 1, -2), 'name': 'Relic (belongs to Player 1)', 'id': 1}
        ],
        'obstacles': []
    },
    'players': [
        {
            'camp': 0, 
            'artifact': [
                {
                    'id': 0, 
                    'name': 'HolyLight', 
                    'camp': 0, 
                    'cost': 6, 
                    'max_cool_down': 6, 
                    'cool_down_time': 0, 
                    'state': 'Ready', 
                    'target_type': 'Pos'
                }
            ], 
            'mana': 9, 
            'max_mana': 9,
            'creature_capacity': [
                {'type': 'Archer', 'available_count': 3, 'cool_down_list': []}
            ], 
            'newly_summoned_id_list': []
        }, {
            'camp': 1, 
            'artifact': [
                {
                    'id': 1,
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
                {'type': 'Archer', 'available_count': 3, 'cool_down_list': []}
            ],
            'newly_summoned_id_list': [3]
        }
    ]
}
```

