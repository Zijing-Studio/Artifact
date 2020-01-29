'''
AI相关的SDK
'''

import sys
import json


def convert_byte(data_str):
    '''加数据长度作为数据头,并转化为bytes,用于发送操作

    Args:

    data_str: str
    '''
    message_len = len(data_str)
    message = message_len.to_bytes(4, byteorder='big', signed=True)
    message += bytes(data_str, encoding="utf8")
    return message


def send_opt(data_str):
    '''发送操作

    Args:

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


def init(artifacts, creatures):
    '''选择初始神器和生物

    Args:

    artifacts: 神器名字的字符串数组(长度为1)

    creatures: 生物名字的字符串数组(长度为3)
    '''
    message = {
        "round": 0,
        "operation_type": "init",
        "operation_parameters":
        {
            "artifacts": artifacts,
            "creatures": creatures
        }
    }
    send_opt(json.dumps(message))

def summon(_round, _type, star, position):
    '''在地图position处召唤一个本方类型为_type，星级为star的单位

    Args:

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

def move(_round, mover, position):
    '''将地图上id为mover的单位移动到地图position处

    Args:

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


def attack(_round, attacker, target):
    '''令地图上id为attacker的单位攻击地图上id为target的单位

    Args:

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


def end_round(_round):
    '''结束当前回合

    Args:

    _round: 当前回合(若游戏实际回合不等于_round，则指令无效)
    '''
    message = {
        "round": _round,
        "operation_type": "endround"
    }
    send_opt(json.dumps(message))
