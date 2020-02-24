'''
AI
'''

from ai_client import AiClient


class AI(AiClient):
    '''玩家编写的ai
    '''

    def __init__(self):
        super().__init__()
        # 以下是玩家自己的初始构造

    def choose_cards(self):
        '''(根据初始阵营)选择初始卡组
        '''
        # artifacts和creatures可以修改
        self.artifacts = ["HolyLight"]
        self.creatures = ["Archer", "Swordsman", "VolcanoDragon"]
        self.init()

    def play(self):
        '''玩家需要编写的ai操作函数
        '''
        if self.round < 20:
            self.end_round()
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
