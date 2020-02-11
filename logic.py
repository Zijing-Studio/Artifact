'''游戏主体逻辑
'''

import sys
import json
import random
import logic_sdk
from PlayerLegality.player_legality import Parser
from StateSystem.StateSystem import StateSystem


class Game:
    '''游戏 Artifact
    '''
    # pylint: disable=too-many-instance-attributes

    def __init__(self):
        '''初始化变量
        '''
        self.player0 = -1       # player0对应的编号
        self.player1 = -1       # player1对应的编号
        self.media_player = []  # 播放器
        self.audience = []      # 观众
        self.replay = ""        # 录像文件存储处
        self.state = 0          # 当前消息回合
        self.listen = 0         # 当前监听的玩家(当前回合玩家)
        self._round = -1        # 当前游戏回合
        self.is_end = False     # 是否结束
        self.statesystem = StateSystem()
        self.parser = Parser(self.statesystem)

    def check_game_end(self):
        '''判断游戏是否结束，若结束则结束对局
        '''
        # 最大回合数
        if self._round == 10000:
            self.end(-1)

        hp0 = self.statesystem.get_relic_by_id(0).hp
        hp1 = self.statesystem.get_relic_by_id(1).hp
        if hp0 <= 0 and hp1 <= 0:   # 平局
            self.is_end = True
            self.end(-1)
        elif hp1 <= 0:              # 0号玩家胜利
            self.is_end = True
            self.end(0)
        elif hp0 <= 0:              # 1号玩家胜利
            self.is_end = True
            self.end(1)

    def change_round(self):
        '''回合转换,切换到下一个玩家
        '''
        self._round += 1
        self.parser.set_round(self._round)
        self.listen = self.player1 if self.listen == self.player0 else self.player0

    def get_round_ope(self):
        '''一个游戏回合(主要阶段)内的操作
        '''
        # pylint: disable=too-many-branches
        while not self.is_end:
            self.state += 1
            self.send_game_info()
            opt_dict = logic_sdk.read_opt()
            if opt_dict["player"] == self.listen:
                parser_respond = self.parser.parse(opt_dict["content"])
                if not parser_respond:
                    continue
                self.send_media_info()
                self.check_game_end()
                # 结束回合
                if json.loads(opt_dict["content"])["operation_type"] == "endround":
                    break
            # AI异常
            elif opt_dict['player'] == -1:
                opt = json.loads(opt_dict['content'])
                # AI异常退出
                if opt['error'] == 0:
                    if opt['player'] == self.player0:
                        self.end(self.player1)
                    else:
                        self.end(self.player0)
                # 超时
                elif opt['error'] == 1:
                    self.parser.parse(json.dumps(
                        {"player": 0 if self.listen == self.player0 else 1,
                         "round": self._round,
                         "operation_type": "endround",
                         "operation_parameters": {}}))
                    break

    def get_media_info(self, events):
        '''把事件转为给播放器的二进制序列

        Args:
            events: 事件数组
        '''
        # pylint: disable=too-many-branches
        # pylint: disable=too-many-statements
        creature_names = ["", "Swordman", "Archer",
                          "BlackBat", "Priest", "VolcanoDargon"]
        artifact_names = ["", "HolyLight", "SalamanderShield", "InfernoFlame"]

        media_info = bytes()
        for event in events:
            if event.name == "TurnStart":
                # round
                media_info += self._round.to_bytes(4, 'big', signed=True)
                # event
                media_info += int(1).to_bytes(4, 'big', signed=True)
                # camp
                media_info += int(self._round %
                                  2).to_bytes(4, 'big', signed=True)
                # 0
                media_info += int(0).to_bytes(4, 'big', signed=True)
                media_info += int(0).to_bytes(4, 'big', signed=True)
                media_info += int(0).to_bytes(4, 'big', signed=True)
                media_info += int(0).to_bytes(4, 'big', signed=True)
            elif event.name == "TurnEnd":
                # round
                media_info += self._round.to_bytes(4, 'big', signed=True)
                # event
                media_info += int(2).to_bytes(4, 'big', signed=True)
                # camp
                media_info += int(self._round %
                                  2).to_bytes(4, 'big', signed=True)
                # 0
                media_info += int(0).to_bytes(4, 'big', signed=True)
                media_info += int(0).to_bytes(4, 'big', signed=True)
                media_info += int(0).to_bytes(4, 'big', signed=True)
                media_info += int(0).to_bytes(4, 'big', signed=True)
            elif event.name == "Spawn":
                # round
                media_info += self._round.to_bytes(4, 'big', signed=True)
                # event
                media_info += int(3).to_bytes(4, 'big', signed=True)
                # type
                media_info += int(creature_names.index(event.parameter_dict['source'].type)
                                  + 10 * event.parameter_dict['source'].camp).to_bytes(
                                      4, 'big', signed=True)
                # level
                media_info += int(event.parameter_dict['source'].level).to_bytes(
                    4, 'big', signed=True)
                # posX
                media_info += event.parameter_dict['pos'][0].to_bytes(
                    4, 'big', signed=True)
                # posY
                media_info += event.parameter_dict['pos'][1].to_bytes(
                    4, 'big', signed=True)
                # id
                media_info += event.parameter_dict['source'].id.to_bytes(
                    4, 'big', signed=True)
            elif event.name == "Move":
                # round
                media_info += self._round.to_bytes(4, 'big', signed=True)
                # event
                media_info += int(4).to_bytes(4, 'big', signed=True)
                # id
                media_info += event.parameter_dict['source'].id.to_bytes(
                    4, 'big', signed=True)
                # desX
                media_info += event.parameter_dict['dest'][0].to_bytes(
                    4, 'big', signed=True)
                # desY
                media_info += event.parameter_dict['dest'][1].to_bytes(
                    4, 'big', signed=True)
                # 0
                media_info += int(0).to_bytes(4, 'big', signed=True)
                media_info += int(0).to_bytes(4, 'big', signed=True)
            elif event.name == "Attack":
                # round
                media_info += self._round.to_bytes(4, 'big', signed=True)
                # event
                media_info += int(5).to_bytes(4, 'big', signed=True)
                # id1
                media_info += event.parameter_dict['source'].id.to_bytes(
                    4, 'big', signed=True)
                # id2
                media_info += event.parameter_dict['target'].id.to_bytes(
                    4, 'big', signed=True)
                # 0
                media_info += int(0).to_bytes(4, 'big', signed=True)
                media_info += int(0).to_bytes(4, 'big', signed=True)
                media_info += int(0).to_bytes(4, 'big', signed=True)
            elif event.name == "Damage":
                # round
                media_info += self._round.to_bytes(4, 'big', signed=True)
                # event
                media_info += int(6).to_bytes(4, 'big', signed=True)
                # id2
                media_info += event.parameter_dict['target'].id.to_bytes(
                    4, 'big', signed=True)
                # id1
                media_info += event.parameter_dict['source'].id.to_bytes(
                    4, 'big', signed=True)
                # damage
                media_info += event.parameter_dict['damage'].to_bytes(
                    4, 'big', signed=True)
                # 0
                media_info += int(0).to_bytes(4, 'big', signed=True)
                media_info += int(0).to_bytes(4, 'big', signed=True)
            elif event.name == "Death":
                # round
                media_info += self._round.to_bytes(4, 'big', signed=True)
                # event
                media_info += int(7).to_bytes(4, 'big', signed=True)
                # id
                media_info += event.parameter_dict['source'].id.to_bytes(
                    4, 'big', signed=True)
                # 0
                media_info += int(0).to_bytes(4, 'big', signed=True)
                media_info += int(0).to_bytes(4, 'big', signed=True)
                media_info += int(0).to_bytes(4, 'big', signed=True)
                media_info += int(0).to_bytes(4, 'big', signed=True)
            elif event.name == "Heal":
                # round
                media_info += self._round.to_bytes(4, 'big', signed=True)
                # event
                media_info += int(8).to_bytes(4, 'big', signed=True)
                # id2
                media_info += event.parameter_dict['target'].id.to_bytes(
                    4, 'big', signed=True)
                # id1
                media_info += event.parameter_dict['source'].id.to_bytes(
                    4, 'big', signed=True)
                # h
                media_info += event.parameter_dict['heal'].to_bytes(
                    4, 'big', signed=True)
                # 0
                media_info += int(0).to_bytes(4, 'big', signed=True)
                media_info += int(0).to_bytes(4, 'big', signed=True)
            elif event.name == "ActivateArtifact":
                # round
                media_info += self._round.to_bytes(4, 'big', signed=True)
                # event
                media_info += int(9).to_bytes(4, 'big', signed=True)
                # camp
                media_info += event.parameter_dict['camp'].to_bytes(
                    4, 'big', signed=True)
                media_info += int(artifact_names.index(
                    event.parameter_dict['name']) + 10 * event.parameter_dict['camp']
                                 ).to_bytes(4, 'big', signed=True)
                if (event.parameter_dict['name'] == "HolyLight" or
                        event.parameter_dict['name'] == "InfernoFlame"):
                    media_info += event.parameter_dict['target'][0].to_bytes(
                        4, 'big', signed=True)
                    media_info += event.parameter_dict['target'][1].to_bytes(
                        4, 'big', signed=True)
                    media_info += int(0).to_bytes(4, 'big', signed=True)
                elif event.parameter_dict['name'] == "SalamanderShield":
                    media_info += int(0).to_bytes(4, 'big', signed=True)
                    media_info += int(0).to_bytes(4, 'big', signed=True)
                    media_info += event.parameter_dict['target'].id.to_bytes(
                        4, 'big', signed=True)
            elif event.name == "GameStart":
                # round
                media_info += self._round.to_bytes(4, 'big', signed=True)
                # event
                media_info += int(11).to_bytes(4, 'big', signed=True)
                # camp
                media_info += event.parameter_dict['camp'].to_bytes(
                    4, 'big', signed=True)
                # a0
                media_info += int(artifact_names.index(
                    event.parameter_dict['cards']["artifacts"][0] +
                    10 * event.parameter_dict['camp'])
                                 ).to_bytes(4, 'big', signed=True)
                # c1 c2 c3
                for creature_name in event.parameter_dict['cards']["creatures"]:
                    media_info += int(creature_names.index(creature_name) +
                                      10 * event.parameter_dict['camp']
                                      ).to_bytes(4, 'big', signed=True)
            elif event.name == "HolyShieldAdd":
                # round
                media_info += self._round.to_bytes(4, 'big', signed=True)
                # event
                media_info += int(12).to_bytes(4, 'big', signed=True)
                # id0
                media_info += event.parameter_dict['source'].id.to_bytes(
                    4, 'big', signed=True)
                # 0
                media_info += int(0).to_bytes(4, 'big', signed=True)
                media_info += int(0).to_bytes(4, 'big', signed=True)
                media_info += int(0).to_bytes(4, 'big', signed=True)
                media_info += int(0).to_bytes(4, 'big', signed=True)
            elif event.name == "HolyShieldBreak":
                # round
                media_info += self._round.to_bytes(4, 'big', signed=True)
                # event
                media_info += int(13).to_bytes(4, 'big', signed=True)
                # id0
                media_info += event.parameter_dict['source'].id.to_bytes(
                    4, 'big', signed=True)
                # 0
                media_info += int(0).to_bytes(4, 'big', signed=True)
                media_info += int(0).to_bytes(4, 'big', signed=True)
                media_info += int(0).to_bytes(4, 'big', signed=True)
                media_info += int(0).to_bytes(4, 'big', signed=True)
            elif event.name == "Attacking":
                # round
                media_info += self._round.to_bytes(4, 'big', signed=True)
                # event
                media_info += int(14).to_bytes(4, 'big', signed=True)
                # id1
                media_info += event.parameter_dict['source'].id.to_bytes(
                    4, 'big', signed=True)
                # id2
                media_info += event.parameter_dict['target'].id.to_bytes(
                    4, 'big', signed=True)
                # 0
                media_info += int(0).to_bytes(4, 'big', signed=True)
                media_info += int(0).to_bytes(4, 'big', signed=True)
                media_info += int(0).to_bytes(4, 'big', signed=True)
            elif event.name == "Attacked":
                # round
                media_info += self._round.to_bytes(4, 'big', signed=True)
                # event
                media_info += int(15).to_bytes(4, 'big', signed=True)
                # id1
                media_info += event.parameter_dict['source'].id.to_bytes(
                    4, 'big', signed=True)
                # id2
                media_info += event.parameter_dict['target'].id.to_bytes(
                    4, 'big', signed=True)
                # 0
                media_info += int(0).to_bytes(4, 'big', signed=True)
                media_info += int(0).to_bytes(4, 'big', signed=True)
                media_info += int(0).to_bytes(4, 'big', signed=True)
            elif event.name == "Leave":
                # round
                media_info += self._round.to_bytes(4, 'big', signed=True)
                # event
                media_info += int(16).to_bytes(4, 'big', signed=True)
                # id0
                media_info += event.parameter_dict['source'].id.to_bytes(
                    4, 'big', signed=True)
                # posX
                media_info += event.parameter_dict['pos'][0].to_bytes(
                    4, 'big', signed=True)
                # posY
                media_info += event.parameter_dict['pos'][1].to_bytes(
                    4, 'big', signed=True)
                # 0
                media_info += int(0).to_bytes(4, 'big', signed=True)
                media_info += int(0).to_bytes(4, 'big', signed=True)
            elif event.name == "Arrive":
                # round
                media_info += self._round.to_bytes(4, 'big', signed=True)
                # event
                media_info += int(17).to_bytes(4, 'big', signed=True)
                # id0
                media_info += event.parameter_dict['source'].id.to_bytes(
                    4, 'big', signed=True)
                # posX
                media_info += event.parameter_dict['pos'][0].to_bytes(
                    4, 'big', signed=True)
                # posY
                media_info += event.parameter_dict['pos'][1].to_bytes(
                    4, 'big', signed=True)
                # 0
                media_info += int(0).to_bytes(4, 'big', signed=True)
                media_info += int(0).to_bytes(4, 'big', signed=True)
            elif event.name == "Summon":
                # round
                media_info += self._round.to_bytes(4, 'big', signed=True)
                # event
                media_info += int(18).to_bytes(4, 'big', signed=True)
                # type
                if event.parameter_dict['source'].type == 'Swordman':
                    media_info += int(1 + 10 * event.parameter_dict['source'].camp).to_bytes(
                        4, 'big', signed=True)
                elif event.parameter_dict['source'].type == 'Archer':
                    media_info += int(2 + 10 * event.parameter_dict['source'].camp).to_bytes(
                        4, 'big', signed=True)
                elif event.parameter_dict['source'].type == 'BlackBat':
                    media_info += int(3 + 10 * event.parameter_dict['source'].camp).to_bytes(
                        4, 'big', signed=True)
                elif event.parameter_dict['source'].type == 'Priest':
                    media_info += int(4 + 10 * event.parameter_dict['source'].camp).to_bytes(
                        4, 'big', signed=True)
                elif event.parameter_dict['source'].type == 'VolcanoDragon':
                    media_info += int(5 + 10 * event.parameter_dict['source'].camp).to_bytes(
                        4, 'big', signed=True)
                else:
                    pass
                # level
                media_info += int(event.parameter_dict['source'].level).to_bytes(
                    4, 'big', signed=True)
                # posX
                media_info += event.parameter_dict['pos'][0].to_bytes(
                    4, 'big', signed=True)
                # posY
                media_info += event.parameter_dict['pos'][1].to_bytes(
                    4, 'big', signed=True)
                # 0
                media_info += int(0).to_bytes(4, 'big', signed=True)
        return media_info

    def send_media_info(self, media_info=b''):
        '''把信息发给播放器及记录于录像文件

        Args:
            media_info: 给播放器的信息字符串 为空时会直接从事件堆中取
        '''
        if media_info == b'':
            media_info = self.get_media_info(self.statesystem.event_heap.record)
            self.statesystem.event_heap.record.clear()
            if media_info != b'':
                self.send_media_info(media_info)
        with open(self.replay, 'ab') as replay_file:
            replay_file.write(media_info)
        for media in self.media_player:
            logic_sdk.send_message_goal(media_info, media)

    def send_game_info(self):
        '''向当前回合的玩家发送游戏当前局面信息
        '''
        state_dict = {'state': self.state, 'listen': [self.listen],
                      'player': [self.listen], 'content': []}
        message = dict()
        if self._round == -1:
            message = {'camp': 0 if self.listen == self.player0 else 1}
        else:
            message = self.statesystem.parse()
            message['round'] = self._round
            message['camp'] = 0 if self.listen == self.player0 else 1
        # 前四位表示长度 后面是表示信息的json格式字符串
        json_length = str(len(json.dumps(message)))
        state_dict['content'] = [
            "0" * (4 - len(json_length)) + json_length + json.dumps(message)]
        logic_sdk.send_state(state_dict)

    def init_player(self, player_list):
        '''根据玩家列表进行初始化处理

        Args:
            player_list:
            [1, 0, 2]表示0号玩家为本地AI或者远程算力连接，1号玩家未正常启动进程，2号玩家是远程连接播放器
            0: 该玩家进入游戏失败
            1: 该玩家正常进入游戏，且为评测机本地AI或者远程算力
            2: 该玩家正常进入游戏，且为远程连接播放器
        '''
        for player, status in enumerate(player_list):
            if status == 1:
                if self.player0 == -1:
                    self.player0 = player
                elif self.player1 == -1:
                    self.player1 = player
            elif status == 2:
                self.media_player.append(player)

        if self.player0 == -1:
            # 没有玩家连入
            self.end(-1)
        elif self.player1 == -1:
            # 只有一位玩家连入
            self.end(self.player0)
        elif random.randint(0, 1):
            # 随机分配先后手
            self.player0, self.player1 = self.player1, self.player0

    def select_cards(self):
        '''玩家选择初始卡组
        '''
        is_player0_ready = is_player1_ready = False
        # 0号玩家
        self.state += 1
        self.listen = self.player0
        self.send_game_info()
        opt_dict0 = logic_sdk.read_opt()
        if opt_dict0["player"] == self.player0:
            is_player0_ready = self.parser.parse(opt_dict0["content"])
        # 1号玩家
        self.state += 1
        self.listen = self.player1
        self.send_game_info()
        opt_dict1 = logic_sdk.read_opt()
        if opt_dict1["player"] == self.player1:
            is_player1_ready = self.parser.parse(opt_dict0["content"])
        # 双方玩家是否均准备好卡组
        if not is_player0_ready and not is_player1_ready:
            self.is_end = True
            self.end(-1)
        elif not is_player0_ready:
            self.is_end = True
            self.end(1)
        elif not is_player0_ready:
            self.is_end = True
            self.end(0)

    def start(self):
        '''开始游戏
        '''
        # 设置玩家、播放器
        opt_dict = logic_sdk.read_opt()
        self.init_player(opt_dict['player_list'])
        self.replay = opt_dict['replay']
        # 每个回合的时间限制和单条消息的最大长度
        logic_sdk.send_init(3, 2048)
        # 处理初始卡组
        self.select_cards()
        # 播放器协议初始（播放器版本号）& 选卡情况
        self.send_media_info(int(0).to_bytes(4, 'big', signed=True))
        self.send_media_info()
        # 游戏回合
        self._round = 0
        self.parser.set_round(0)
        self.listen = self.player0
        while not self.is_end:
            # 回合开始
            self.parser.parse(json.dumps(
                {"player": 0 if self.listen == self.player0 else 1,
                 "round": self._round,
                 "operation_type": "startround", "operation_parameters": {}}))
            self.send_media_info()
            self.check_game_end()
            self.get_round_ope()
            self.send_media_info()
            self.check_game_end()
            self.change_round()

    def end(self, winner):
        '''游戏终局处理

        Args:
            winner: 胜者。-1表示平局，0/1表示0/1号玩家获胜。
        '''
        media_info = bytes()
        media_info += self._round.to_bytes(4, 'big', signed=True)
        media_info += int(10).to_bytes(4, 'big', signed=True)
        end_info = {str(self.player0): 0, str(self.player1): 0}
        if winner == -1:
            media_info += int(2).to_bytes(4, 'big', signed=True)
            # 计算得分

        elif winner == 0:
            media_info += int(0).to_bytes(4, 'big', signed=True)
            # 计算得分
            end_info[str(self.player0)] = 2
            end_info[str(self.player1)] = 1
        else:  # winner == 1
            media_info += int(1).to_bytes(4, 'big', signed=True)
            # 计算得分
            end_info[str(self.player0)] = 1
            end_info[str(self.player1)] = 2
        media_info += int(0).to_bytes(4, 'big', signed=True)
        media_info += int(0).to_bytes(4, 'big', signed=True)
        media_info += int(0).to_bytes(4, 'big', signed=True)
        media_info += int(0).to_bytes(4, 'big', signed=True)
        media_info += int(-1).to_bytes(4, 'big', signed=True)
        self.send_media_info(media_info)
        logic_sdk.send_end_info(end_info)
        sys.exit()


if __name__ == '__main__':
    game = Game()
    game.start()
