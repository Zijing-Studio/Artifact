'''
游戏逻辑
'''

import sys
import json
import logic_python_SDK

# pylint: disable = R1702
# pylint: disable = R0801

DEBUG = True


class Game:
    '''
    游戏类
    '''
    def __init__(self):
        '''
        初始化
        '''
        self.state = 1  # 当前回合数
        self.listen = 0  # 当前监听的玩家

    def get_game_end(self):
        '''
        获取游戏终局信息并结束对局
        '''
        if 1 == 1:  # 1号玩家胜利条件
            game_end(1, 0)
        elif 2 == 2:  # 2号玩家胜利条件
            game_end(0, 1)
        else:
            game_end(0, 0)

    def get_next_player(self):
        '''
        切换到下一个玩家
        '''
        self.listen = 1-self.listen
        # 判断胜利情况，若游戏结束，则game_end

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
                    ans_list = []
                    # ans_list.append(表示地图状态的字符串)
                    logic_python_SDK.send_state(self.get_state_dict("".join(ans_list)))

                # 输入操作指令
                else:
                    # 处理ai传过来的信息，转交给合法性检测方 parse(opt_dict)?
                    # （等待合法性检测、状态系统、事件堆）
                    # 处理事件堆传过来的信息，转交给播放器方

                    # 回合结束，切换玩家回合
                    self.get_next_player()
                    self.state += 1

                    break

            elif opt_dict['player'] == -1:
                opt = json.loads(opt_dict['content'])
                if opt['error'] == 0:
                    if opt['player'] == 0:
                        game_end(0, 1)
                    else:
                        game_end(1, 0)
                else:
                    if self.listen == 0:
                        game_end(0, 1)
                    else:
                        game_end(1, 0)

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

    def start(self):
        '''
        开始游戏
        '''
        game_init(logic_python_SDK.read_player_state())
        logic_python_SDK.send_init(3, 1024)
        # 处理初始卡组

        while True:
            logic_python_SDK.send_state(self.get_state_dict(self.board_message()))
            self.get_state_opt()


def game_init(player_list):
    '''
    游戏初始化处理
    '''
    first_state = player_list[0]
    second_state = player_list[1]
    if first_state == 0 or second_state == 0:
        game_end(first_state, second_state)


def game_end(first_state, second_state):
    '''
    游戏终局处理
    '''
    if first_state == second_state:
        logic_python_SDK.send_end_info("draw!")
    elif first_state == 0:
        logic_python_SDK.send_end_info("player1 win!")
    else:
        logic_python_SDK.send_end_info("player0 win!")
    sys.exit()


def main():
    '''
    主函数
    '''
    game = Game()
    game.start()


if __name__ == '__main__':
    main()
