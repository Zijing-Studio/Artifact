'''
logic_sdk
'''

import json
import sys


DEBUG = True  # DEBUG时会生成一个log.txt记录logic收发的信息


def logic_convert_byte(data_str, send_goal):
    '''
    传输数据的时候加数据长度作为数据头
    '''
    message_len = len(data_str)
    message = message_len.to_bytes(4, byteorder='big', signed=True)
    message += send_goal.to_bytes(4, byteorder='big', signed=True)
    if isinstance(data_str, str):
        message += bytes(data_str, encoding="utf8")
    elif isinstance(data_str, bytes):
        message += data_str
    return message


def read_opt():
    '''
    读取发过来的操作
    '''
    read_buffer = sys.stdin.buffer
    data_len = int.from_bytes(read_buffer.read(4), byteorder='big', signed=True)
    data = read_buffer.read(data_len)
    if DEBUG:
        with open('log.txt', 'a') as logfile:
            logfile.write('judger->logic:\n'+str(json.loads(data))+'\n')
    try:
        opt = json.loads(data)
    except json.decoder.JSONDecodeError:
        return False
    else:
        return opt


def send_end_info(end_info):
    '''
    发送终局信息
    '''
    end_dict = {}
    end_dict['state'] = -1
    end_dict['end_info'] = json.dumps(end_info)
    if DEBUG:
        with open('log.txt', 'a') as logfile:
            logfile.write('end:\n'+end_dict['end_info']+'\n')
    sys.stdout.buffer.write(logic_convert_byte(json.dumps(end_dict), -1))
    sys.stdout.flush()


def send_init(time, length):
    '''
    发送初始化信息
    '''
    init_dict = {"time": time, "length": length}
    sys.stdout.buffer.write(logic_convert_byte(json.dumps({"state": 0, "content": init_dict}), -1))
    sys.stdout.flush()


def send_state(state_dict):
    '''
    发送回合信息
    '''
    if DEBUG:
        with open('log.txt', 'a') as logfile:
            logfile.write('logic->judger:\n'+json.dumps(state_dict)+'\n')
    sys.stdout.buffer.write(logic_convert_byte(json.dumps(state_dict), -1))
    sys.stdout.flush()


def send_message_goal(message_str, send_goal):
    '''
    发送二进制流
    '''
    if DEBUG:
        with open('log.txt', 'a') as logfile:
            logfile.write('logic->'+str(send_goal)+':\n'+message_str+'\n')
    sys.stdout.buffer.write(logic_convert_byte(message_str, send_goal))
    sys.stdout.flush()
