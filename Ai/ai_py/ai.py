'''
AI
'''

import ai_sdk


class AI:
    '''玩家编写的ai
    '''

    def __init__(self):
        self.map = dict()                       # 地图信息
        self.players = list()                   # 两名玩家的信息
        self.round = 0                          # 当前回合
        self.my_camp = -1                       # 己方阵营

    def choose_cards(self):
        '''选择初始卡组

        Args:
            artifacts: 神器名字数组(长度为1)
            creatures: 生物名字数组(长度为3)
        '''
        # 先获取阵营后选卡组
        self.my_camp = ai_sdk.read_opt()['camp']
        # artifacts和creatures可以修改
        artifacts = ["HolyLight"]
        creatures = ["Archer", "Swordman", "Priest"]
        ai_sdk.init(self.my_camp, artifacts, creatures)

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
            ai_sdk.end_round(self.my_camp, self.round)
        else:
            exit(0)


def main():
    '''启动AI
    '''
    player_ai = AI()
    player_ai.choose_cards()
    while True:
        player_ai.update_game_info()
        player_ai.play()


if __name__ == '__main__':
    main()
