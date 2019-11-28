'''
ai_SDK
'''

import sys
import json
import random

# pylint: disable = R0201
# pylint: disable = R0801


class LogicAPI:
    '''
    SDK提供的接口
    '''

    def get_game_info(self):
        '''
        获取游戏信息（地图、角色、回合）
        '''
        message = {"operation_type": "gameinfo"}
        sys.stdout.buffer.write(ai_convert_byte(json.dumps(message)))
        sys.stdout.flush()
        game_info = read_opt()
        return game_info

    def summon(self, _round, _type, star, position):
        '''
        在地图position处召唤一个本方类型为type，星级为star的单位

        参数:

        _round: 当前回合(若游戏实际回合不等于round，则指令无效)

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
        sys.stdout.buffer.write(ai_convert_byte(json.dumps(message)))
        sys.stdout.flush()

    def move(self, _round, mover, position):
        '''
        将地图上id为mover的单位移动到地图position处

        参数:

        _round: 当前回合(若游戏实际回合不等于round，则指令无效)

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
        sys.stdout.buffer.write(ai_convert_byte(json.dumps(message)))
        sys.stdout.flush()

    def attack(self, _round, attacker, target):
        '''
        令地图上id为attacker的单位攻击地图上id为target的单位

        参数:

        round: 当前回合(若游戏实际回合不等于round，则指令无效)

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
        sys.stdout.buffer.write(ai_convert_byte(json.dumps(message)))
        sys.stdout.flush()

    def end(self, _round):
        '''
        结束当前回合

        参数:

        round: 当前回合(若游戏实际回合不等于round，则指令无效)
        '''
        message = {
            "round": 1,
            "operation_type": "end"
        }
        sys.stdout.buffer.write(ai_convert_byte(json.dumps(message)))
        sys.stdout.flush()


def ai_convert_byte(data_str):
    '''
    传输数据的时候加数据长度作为数据头
    '''
    message_len = len(data_str)
    message = message_len.to_bytes(4, byteorder='big', signed=True)
    message += bytes(data_str, encoding="utf8")
    return message


def send_opt(data_str):
    '''
    发送自己的操作
    '''
    sys.stdout.buffer.write(ai_convert_byte(data_str))
    sys.stdout.flush()


def read_opt():
    '''
    读取发过来的操作
    '''
    read_buffer = sys.stdin.buffer
    data_len = int.from_bytes(read_buffer.read(
        4), byteorder='big', signed=True)
    data = read_buffer.read(data_len)
    return json.loads(data)


def player_ai(logic):
    '''
    用户需要编写的AI函数
    '''
    i = random.randint(1, 4)
    if i == 0:
        # 这里需要输入数据头以及json 暂时不测
        game_info = logic.get_game_info()
        print("gameinfo:", game_info)
    elif i == 1:
        logic.summon(random.randint(0, 100), '', random.randint(1, 5),
                     [random.randint(1, 10), random.randint(1, 10),
                      random.randint(1, 10)])
    elif i == 2:
        logic.move(random.randint(0, 100), random.randint(0, 10),
                   [random.randint(1, 10), random.randint(1, 10),
                    random.randint(1, 10)])
    elif i == 3:
        logic.attack(random.randint(0, 100), random.randint(0, 10),
                     random.randint(0, 10))
    elif i == 4:
        logic.end(random.randint(0, 100))


def start():
    '''
    循环入口
    '''
    logic_message = LogicAPI()
    read_buffer = sys.stdin.buffer
    for i in range(10):
        read_buffer.flush()
        read_buffer.read(1)
        print("")
        player_ai(logic_message)


if __name__ == '__main__':
    start()
