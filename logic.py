'''
游戏逻辑
'''

import sys
import json
import logic_python_SDK
from PlayerLegality.player_legality import Parser
from StateSystem import StateSystem

# pylint: disable = R1702
# pylint: disable = R0801

DEBUG = True


class Game:
    '''
    游戏类
    '''
    # pylint: disable=too-many-instance-attributes

    def __init__(self):
        '''
        初始化
        '''
        self.player0 = -1       # player0对应的编号
        self.player1 = -1       # player1对应的编号
        self.media_player = []  # 播放器
        self.audience = []      # 观众
        self.replay = ""        # 录像文件存储处
        self.state = 0          # 当前回合数
        self.listen = 0         # 当前监听的玩家
        self.is_end = False     # 是否结束
        self.statesystem = StateSystem()
        self.parser = Parser()

    def get_game_end(self):
        '''
        获取游戏终局信息并结束对局
        '''
        if 0 == 0:  # 0号玩家胜利条件
            self.is_end = True
            self.game_end(self.player0)
        elif 1 == 1:  # 1号玩家胜利条件
            self.is_end = True
            self.game_end(self.player1)
        else:
            self.is_end = True
            self.game_end(-1)

    def get_next_player(self):
        '''
        切换到下一个玩家
        '''
        if self.listen == self.player0:
            self.listen = self.player1
        elif self.listen == self.player1:
            self.listen = self.player0
        # 判断胜利情况，若游戏结束，则self.get_game_end()

    def get_state_opt(self):
        '''
        监听循环
        '''
        while True:
            opt_dict = logic_python_SDK.read_opt()
            if opt_dict['player'] == self.listen:
                opt = opt_dict['content']
                # 查询当前地图状态
                if opt[0] == '#':
                    logic_python_SDK.send_state(self.get_state_dict(
                        self.board_message()))

                # 输入操作指令
                else:
                    opt['player'] = self.listen
                    parser_respond = self.parser.parse(opt)
                    if isinstance(parser_respond, BaseException):
                        pass
                    elif not parser_respond:
                        pass
                    else:
                        media_events = ""
                        for event in self.statesystem.event_heap.record:
                            # 处理event
                            pass
                        self.statesystem.event_heap.record.clear()
                        state_dict = {}
                        state_dict['state'] = self.state
                        state_dict['listen'] = [self.listen]
                        state_dict['player'] = self.media_player[:]
                        state_dict['content'] = [media_events] * len(self.media_player)
                        logic_python_SDK.send_state(state_dict)

            elif opt_dict['player'] == -1:
                opt = json.loads(opt_dict['content'])
                # AI异常退出
                if opt['error'] == 0:
                    if opt['player'] == self.player0:
                        self.game_end(self.player1)
                    else:
                        self.game_end(self.player0)
                # 超时
                elif opt['error'] == 1:
                    # 回合结束，切换玩家回合
                    self.get_next_player()
                    self.state += 1

    def get_state_dict(self, content_str):
        '''
        获取局面描述的字典
        '''
        state_dict = {}
        state_dict['state'] = self.state
        state_dict['listen'] = [self.listen]
        state_dict['player'] = [self.listen]
        state_dict['content'] = [content_str]
        return state_dict

    def board_message(self):
        '''
        返回局面描述的字符串
        '''
        board_str = [str(self.listen)]
        # board_str.append(局面描述)
        return "#"+"".join(board_str)+"#"

    def game_init(self, player_list):
        '''
        游戏初始化处理
        '''
        for player, status in enumerate(player_list):
            if status in (1, 2):
                if self.player0 != -1:
                    self.player0 = player
                elif self.player1 != -1:
                    self.player1 = player
            elif status == 3:
                self.media_player.append(player)
            elif status == 4:
                self.audience.append(player)

        if self.player1 == -1:
            # 没有玩家连入
            self.game_end(-1)
        if self.player0 != -1 and self.player1 == -1:
            self.game_end(self.player0)

    def start(self):
        '''
        开始游戏
        '''
        opt_dict = logic_python_SDK.read_opt()
        self.replay = opt_dict['replay']
        self.game_init(opt_dict['player_list'])
        logic_python_SDK.send_init(3, 1024)
        # 处理初始卡组

        while not self.is_end:
            logic_python_SDK.send_state(self.get_state_dict(
                self.board_message()))
            self.get_state_opt()

    def game_end(self, winner):
        '''
        游戏终局处理
        '''
        if winner == -1:
            logic_python_SDK.send_end_info("draw!")
        else:
            logic_python_SDK.send_end_info("player " + str(winner) + " win!")
        sys.exit()


def main():
    '''
    主函数
    '''
    game = Game()
    game.start()


if __name__ == '__main__':
    main()
