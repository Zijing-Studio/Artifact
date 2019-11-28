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
        'units': [], 
        'barracks': [], 
        'relics': [
            {'camp': 0, 'max_hp': 30, 'hp': 30, 'pos': (0, 0, 0)}, 
            {'camp': 1, 'max_hp': 30, 'hp': 30, 'pos': (1, 1, -2)}
        ], 
        'obstacles': []
    },
    'players': [
        {
            'camp': 0,
            'artifact': [],
            'mana': 2,
            'max_mana': 2,
            'creature_capacity': [
                {'type': 'Archer', 'available_count': 2, 'cool_down_list': [4]}
            ],
            'newly_summoned_id_list': [0]
        }, 
        {
            'camp': 1, 
            'artifact': [], 
            'mana': 2, 
            'max_mana': 2,
            'creature_capacity': [
                {'type': 'Archer', 'available_count': 2, 'cool_down_list': [4]}
            ],
            'newly_summoned_id_list': [1]
        }
    ]
}
```

