'''
AI相关的SDK
'''

import sys
import json
import random


def convert_byte(data_str):
    '''加数据长度作为数据头,并转化为bytes,用于发送操作

    参数:

    data_str: str
    '''
    message_len = len(data_str)
    message = message_len.to_bytes(4, byteorder='big', signed=True)
    message += bytes(data_str, encoding="utf8")
    return message


def send_opt(data_str):
    '''发送操作

    参数:

    data_str: str

    '''
    sys.stdout.buffer.write(convert_byte(data_str))
    sys.stdout.flush()


def read_opt():
    '''读取发过来的操作

    (一般来说,AI收到的信息前四位表示json长度,后面是一个json串)
    '''
    read_buffer = sys.stdin.buffer
    data_length = read_buffer.read(4)
    data = read_buffer.read(int(data_length.decode()))
    return json.loads(data)


class LogicAPI:
    '''SDK提供的接口
    '''

    def get_game_info(self):
        '''获取游戏信息（地图、角色、回合）

        每个小回合开始的时候都会发游戏信息的，一般来说没必要用这个接口
        '''
        message = {"operation_type": "gameinfo"}
        send_opt(json.dumps(message))
        game_info = read_opt()
        return game_info

    def summon(self, _round, _type, star, position):
        '''在地图position处召唤一个本方类型为_type，星级为star的单位

        参数:

        _round: 当前回合(若游戏实际回合不等于_round，则指令无效)

        _type: 描述单位类型的字符串

        star: 单位星级

        position: 单位在地图上的[x,y,z]位置

        '''
        message = {
            "round": _round,
            "operation_type": "summon",
            "operation_parameters":
            {
                "position": position,
                "type": _type,
                "star": star,
            }
        }
        send_opt(json.dumps(message))

    def move(self, _round, mover, position):
        '''将地图上id为mover的单位移动到地图position处

        参数:

        _round: 当前回合(若游戏实际回合不等于_round，则指令无效)

        mover: 需要移动的单位的id

        position: 目标在地图上的[x,y,z]位置
        '''
        message = {
            "round": _round,
            "operation_type": "move",
            "operation_parameters":
            {
                "mover": mover,
                "position": position
            }
        }
        send_opt(json.dumps(message))

    def attack(self, _round, attacker, target):
        '''令地图上id为attacker的单位攻击地图上id为target的单位

        参数:

        _round: 当前回合(若游戏实际回合不等于_round，则指令无效)

        attacker: 攻击单位的id

        target: 被攻击单位的id
        '''
        message = {
            "round": _round,
            "operation_type": "attack",
            "operation_parameters":
            {
                "attacker": attacker,
                "target": target,
            }
        }
        send_opt(json.dumps(message))

    def end(self, _round):
        '''结束当前回合

        参数:

        _round: 当前回合(若游戏实际回合不等于_round，则指令无效)
        '''
        message = {
            "round": _round,
            "operation_type": "end"
        }
        send_opt(json.dumps(message))


class PlayerAI:
    '''玩家编写的ai

    属性:

    logic_api: 玩家调用的api

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

    def __init__(self, logic_api, game_info):
        self.logic_api = logic_api
        self.round = game_info['round']         # 当前回合
        self.my_camp = game_info['camp']        # 己方阵营
        self.map = game_info['map']             # 地图信息
        self.players = game_info['players']     # 两名玩家的信息

    def play(self):
        '''用户需要编写的ai操作函数
        '''
        if self.round < 20:
            self.logic_api.end(self.round)
        else:
            exit(0)
        '''
        i = random.randint(0, 10)
        if i == 1:
            self.logic_api.summon(self.round, 'Archer', 1,
                                  [random.randint(1, 10), random.randint(1, 10),
                                   random.randint(1, 10)])
        elif i == 2:
            self.logic_api.move(self.round, random.randint(0, 10),
                                [random.randint(1, 10), random.randint(1, 10),
                                 random.randint(1, 10)])
        elif i == 3:
            self.logic_api.attack(self.round, random.randint(0, 10),
                                  random.randint(0, 10))
        elif i == 4:
            self.logic_api.end(self.round)
        '''


def start():
    '''
    循环入口
    '''
    logic_api = LogicAPI()
    while True:
        game_info = read_opt()
        player_ai = PlayerAI(logic_api, game_info)
        player_ai.play()


if __name__ == '__main__':
    start()
