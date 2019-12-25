'''
AI
'''

import api
import random


class PlayerAI:
    '''玩家编写的ai

    属性:

    api: 玩家调用的api

    game_info: 游戏目前局面信息
    举例:

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
        ],
        'round': round,
        'camp': camp
    }
    '''

    def __init__(self, game_info):
        self.round = game_info['round']         # 当前回合
        self.my_camp = game_info['camp']        # 己方阵营
        self.map = game_info['map']             # 地图信息
        self.players = game_info['players']     # 两名玩家的信息

    def play(self):
        '''用户需要编写的ai操作函数
        '''
        if self.round < 20:
            api.end(self.round)
        else:
            exit(0)
        '''
        i = random.randint(0, 10)
        if i == 1:
            api.summon(self.round, 'Archer', 1,
                                  [random.randint(1, 10), random.randint(1, 10),
                                   random.randint(1, 10)])
        elif i == 2:
            api.move(self.round, random.randint(0, 10),
                                [random.randint(1, 10), random.randint(1, 10),
                                 random.randint(1, 10)])
        elif i == 3:
            api.attack(self.round, random.randint(0, 10),
                                  random.randint(0, 10))
        elif i == 4:
            api.end(self.round)
        '''


def start():
    '''
    循环入口
    '''
    while True:
        game_info = api.read_opt()
        player_ai = PlayerAI(game_info)
        player_ai.play()


if __name__ == '__main__':
    start()
