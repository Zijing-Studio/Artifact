'''
游戏逻辑
'''

import sys
import json
import logic_python_SDK
from PlayerLegality.player_legality import Parser
from StateSystem.StateSystem import StateSystem

# pylint: disable = R1702
# pylint: disable = R0801


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
        self.state = 0          # 当前消息回合
        self.listen = 0         # 当前监听的玩家
        self._round = 0         # 当前游戏回合
        self.is_end = False     # 是否结束
        self.statesystem = StateSystem()
        self.parser = Parser(self.statesystem)

    def get_game_end(self):
        '''
        判断游戏是否结束，若结束则结束对局
        '''
        hp0 = self.statesystem.get_relic_by_id(0).hp
        hp1 = self.statesystem.get_relic_by_id(1).hp
        if hp0 == hp1 == 0:
            self.is_end = True
            self.game_end(-1)
        elif hp0 == 0:  # 0号玩家胜利条件
            self.is_end = True
            self.game_end(self.player0)
        elif hp1 == 1:  # 1号玩家胜利条件
            self.is_end = True
            self.game_end(self.player1)

    def get_next_player(self):
        '''
        回合转换，切换到下一个玩家
        '''
        self._round += 1
        self.parser.set_round(self._round)
        if self.listen == self.player0:
            self.listen = self.player1
        elif self.listen == self.player1:
            self.listen = self.player0

    def get_state_opt(self):
        '''
        在一个游戏回合内的监听循环
        '''
        while True:
            self.state += 1
            self.send_state_dict()
            opt_dict = logic_python_SDK.read_opt()
            if opt_dict['player'] == self.listen:
                opt = opt_dict['content']
                # 查询当前游戏信息
                if opt["operation_type"] == "gameinfo":
                    # logic_python_SDK.send_state(self.get_state_dict(self.game_message()))
                    continue
                elif opt["round"] != self._round:
                    continue
                # 结束回合
                if opt["operation_type"] == "end":
                    break
                # 输入操作指令
                if self.player0 == self.listen:
                    opt['player'] = 0
                else:
                    opt['player'] = 1
                parser_respond = self.parser.parse(opt)
                if isinstance(parser_respond, BaseException):
                    pass
                elif not parser_respond:
                    pass
                else:
                    media_info = self.get_media_info(self.statesystem.event_heap.record)
                    self.statesystem.event_heap.record.clear()
                    self.send_media_dict(media_info)

            elif opt_dict['player'] == -1:
                opt = opt_dict['content']
                # AI异常退出
                if opt['error'] == 0:
                    if opt['player'] == self.player0:
                        self.game_end(self.player1)
                    else:
                        self.game_end(self.player0)
                # 超时
                elif opt['error'] == 1:
                    break

    def get_media_info(self, events):
        '''
        把事件转为给播放器的二进制序列
        '''
        media_info = bytes()
        for event in events:
            if event.name == "Spawn":
                # currentRound
                media_info += self._round.to_bytes(4, 'big', signed=True)
                # event
                media_info += int(0).to_bytes(4, 'big', signed=True)
                # type
                if event.parameter_dict['source'].type == 'Swordman':
                    if event.parameter_dict['source'].camp == 0:
                        media_info += int(1).to_bytes(4, 'big', signed=True)
                    elif event.parameter_dict['source'].camp == 1:
                        media_info += int(14).to_bytes(4, 'big', signed=True)
                elif event.parameter_dict['source'].type == 'Archer':
                    if event.parameter_dict['source'].camp == 0:
                        media_info += int(2).to_bytes(4, 'big', signed=True)
                    elif event.parameter_dict['source'].camp == 1:
                        media_info += int(15).to_bytes(4, 'big', signed=True)
                elif event.parameter_dict['source'].type == 'BlackBat':
                    if event.parameter_dict['source'].camp == 0:
                        media_info += int(5).to_bytes(4, 'big', signed=True)
                    elif event.parameter_dict['source'].camp == 1:
                        media_info += int(18).to_bytes(4, 'big', signed=True)
                else:
                    pass
                # level
                media_info += int(event.parameter_dict['source'].level).to_bytes(4, 'big', signed=True)
                # posX
                media_info += event.parameter_dict['pos'][0].to_bytes(4, 'big', signed=True)
                # posY
                media_info += event.parameter_dict['pos'][1].to_bytes(4, 'big', signed=True)
                # id
                media_info += event.parameter_dict['source'].id.to_bytes(4, 'big', signed=True)
            elif event.name == "Move":
                # currentRound
                media_info += self._round.to_bytes(4, 'big', signed=True)
                # event
                media_info += int(1).to_bytes(4, 'big', signed=True)
                # id
                media_info += event.parameter_dict['source'].id.to_bytes(4, 'big', signed=True)
                # desX
                media_info += event.parameter_dict['dest'][0].to_bytes(4, 'big', signed=True)
                # desY
                media_info += event.parameter_dict['dest'][1].to_bytes(4, 'big', signed=True)
                # 0
                media_info += int(0).to_bytes(4, 'big', signed=True)
                media_info += int(0).to_bytes(4, 'big', signed=True)
            elif event.name == "Attack":
                # currentRound
                media_info += self._round.to_bytes(4, 'big', signed=True)
                # event
                media_info += int(2).to_bytes(4, 'big', signed=True)
                # id
                media_info += event.parameter_dict['source'].id.to_bytes(4, 'big', signed=True)
                # tarId
                media_info += event.parameter_dict['target'].id.to_bytes(4, 'big', signed=True)
                # 0
                media_info += int(0).to_bytes(4, 'big', signed=True)
                media_info += int(0).to_bytes(4, 'big', signed=True)
                media_info += int(0).to_bytes(4, 'big', signed=True)
            elif event.name == "Damage":
                # currentRound
                media_info += self._round.to_bytes(4, 'big', signed=True)
                # event
                media_info += int(3).to_bytes(4, 'big', signed=True)
                # id2
                media_info += event.parameter_dict['target'].id.to_bytes(4, 'big', signed=True)
                # id1
                media_info += event.parameter_dict['source'].id.to_bytes(4, 'big', signed=True)
                # damage
                media_info += event.parameter_dict['damage'].to_bytes(4, 'big', signed=True)
                # 0
                media_info += int(0).to_bytes(4, 'big', signed=True)
                media_info += int(0).to_bytes(4, 'big', signed=True)
            elif event.name == "Death":
                # currentRound
                media_info += self._round.to_bytes(4, 'big', signed=True)
                # event
                media_info += int(4).to_bytes(4, 'big', signed=True)
                # id
                media_info += event.parameter_dict['source'].id.to_bytes(4, 'big', signed=True)
                # 0
                media_info += int(0).to_bytes(4, 'big', signed=True)
                media_info += int(0).to_bytes(4, 'big', signed=True)
                media_info += int(0).to_bytes(4, 'big', signed=True)
                media_info += int(0).to_bytes(4, 'big', signed=True)
            else:
                pass
        return media_info

    def send_media_dict(self, media_info, file="old"):
        '''
        把信息发给播放器及记录
        '''
        if media_info == b'':
            return
        if self.replay != "":
            if file == "old":
                with open(self.replay, 'ab') as replay_file:
                    replay_file.write(media_info)
            elif file == "new":
                with open(self.replay, 'wb') as replay_file:
                    replay_file.write(media_info)
        media_dict = {}
        media_dict['state'] = self.state
        media_dict['listen'] = [self.listen]
        media_dict['player'] = self.media_player[:]
        media_dict['content'] = [media_info] * len(self.media_player)
        logic_python_SDK.send_state(media_dict)

    def send_state_dict(self):
        '''
        发送游戏当前局面信息
        '''
        state_dict = {}
        state_dict['state'] = self.state
        state_dict['listen'] = [self.listen]
        state_dict['player'] = [self.listen]
        message = self.statesystem.parse()
        message['round'] = self._round
        if self.listen == self.player0:
            message['player'] = 0
        else:
            message['player'] = 1
        state_dict['content'] = [message]
        logic_python_SDK.send_state(state_dict)

    def game_init(self, player_list):
        '''
        根据玩家列表进行初始化处理
        '''
        for player, status in enumerate(player_list):
            if status in (1, 2):
                if self.player0 == -1:
                    self.player0 = player
                elif self.player1 == -1:
                    self.player1 = player
            elif status == 3:
                self.media_player.append(player)
            elif status == 4:
                self.audience.append(player)

        if self.player0 == -1:
            # 没有玩家连入
            self.game_end(-1)
        elif self.player1 == -1:
            # 只有一位玩家连入
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

        # 播放器版本号
        self.send_media_dict(int(0).to_bytes(4, 'big', signed=True), file="new")

        while not self.is_end:
            # 每个游戏回合
            print("ROUND ", self._round)
            self.get_state_opt()
            self.get_next_player()
            self.get_game_end()

    def game_end(self, winner):
        '''
        游戏终局处理
        '''
        media_info = bytes()
        media_info += self._round.to_bytes(4, 'big', signed=True)
        media_info += int(5).to_bytes(4, 'big', signed=True)
        if winner == -1:
            media_info += int(2).to_bytes(4, 'big', signed=True)
            logic_python_SDK.send_end_info("draw!")
        else:
            if winner == self.player0:
                media_info += int(0).to_bytes(4, 'big', signed=True)
            else:
                media_info += int(1).to_bytes(4, 'big', signed=True)
            logic_python_SDK.send_end_info("player " + str(winner) + " win!")
        media_info += int(0).to_bytes(4, 'big', signed=True)
        media_info += int(0).to_bytes(4, 'big', signed=True)
        media_info += int(0).to_bytes(4, 'big', signed=True)
        media_info += int(0).to_bytes(4, 'big', signed=True)
        media_info += int(-1).to_bytes(4, 'big', signed=True)
        self.send_media_dict(media_info)
        sys.exit()


def main():
    '''
    主函数
    '''
    game = Game()
    game.start()


if __name__ == '__main__':
    main()
