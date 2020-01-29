'''
AI
'''

import ai_sdk
import random


class AI:
    '''玩家编写的ai
    '''

    def __init__(self, artifacts, creatures):
        self.round = 0                          # 当前回合
        self.my_camp = -1                       # 己方阵营
        self.map = dict()                       # 地图信息
        self.players = list()                   # 两名玩家的信息
        ai_sdk.init(artifacts, creatures)       # 选择初始卡组

    def update_game_info(self):
        '''更新游戏信息
        '''
        game_info = ai_sdk.read_opt()
        self.round = game_info['round']         # 当前回合
        self.my_camp = game_info['camp']        # 己方阵营
        self.map = game_info['map']             # 地图信息
        self.players = game_info['players']     # 两名玩家的信息


    def play(self):
        '''玩家需要编写的ai操作函数
        '''
        if self.round < 20:
            ai_sdk.end_round(self.round)
        else:
            exit(0)
        '''
        i = random.randint(0, 10)
        if i == 1:
            ai_sdk.summon(self.round, 'Archer', 1,
                                  [random.randint(1, 10), random.randint(1, 10),
                                   random.randint(1, 10)])
        elif i == 2:
            ai_sdk.move(self.round, random.randint(0, 10),
                                [random.randint(1, 10), random.randint(1, 10),
                                 random.randint(1, 10)])
        elif i == 3:
            ai_sdk.attack(self.round, random.randint(0, 10),
                                  random.randint(0, 10))
        elif i == 4:
            ai_sdk.end(self.round)
        '''


def main():
    '''启动AI
    '''
    player_ai = AI(["artifact"], ["creature0", "creature1", "creature2"])
    while True:
        player_ai.update_game_info()
        player_ai.play()


if __name__ == '__main__':
    main()
