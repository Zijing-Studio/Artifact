'''
logic_SDK
'''

import json
import sys

# pylint: disable = R0801


def logic_convert_byte(data_str):
    '''
    传输数据的时候加数据长度作为数据头
    '''
    message_len = len(data_str)
    message = message_len.to_bytes(4, byteorder='big', signed=True)
    message += bytes(data_str, encoding="utf8")
    return message


def read_player_state():
    '''
    获取player启动状态
    '''
    read_buffer = sys.stdin.buffer
    data_len = int.from_bytes(read_buffer.read(4), byteorder='big', signed=True)
    data = read_buffer.read(data_len)
    return json.loads(data)['player_list']


def read_opt():
    '''
    读取发过来的操作
    '''
    read_buffer = sys.stdin.buffer
    data_len = int.from_bytes(read_buffer.read(4), byteorder='big', signed=True)
    data = read_buffer.read(data_len)
    return json.loads(data)


def send_end_info(end_info):
    '''
    发送终局信息
    '''
    end_dict = {}
    end_dict['state'] = -1
    end_dict['end_info'] = end_info
    sys.stdout.buffer.write(logic_convert_byte(json.dumps(end_dict)))
    sys.stdout.flush()
    sys.exit()


def send_init(time, length):
    '''
    发送初始化信息
    '''
    init_dict = {"time": time, "length": length}
    sys.stdout.buffer.write(logic_convert_byte(json.dumps({"state": 0, "content": init_dict})))
    sys.stdout.flush()


def send_state(state_dict):
    '''
    发送回合信息
    '''
    sys.stdout.buffer.write(logic_convert_byte(json.dumps(state_dict)))
    sys.stdout.flush()
