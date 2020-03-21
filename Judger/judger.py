'''
裁判程序
'''

#pylint: disable = W0702
#pylint: disable = C0412
#pylint: disable = R1702
#pylint: disable = R0914

import os
import sys
import threading
import shlex
import subprocess
import json
import time

class Player(threading.Thread):
    '''
    监听ai发送的消息的线程
    '''
    def __init__(self, judge_thread, command, player_id, type_tag):
        '''
        初始化,启动ai进程
        '''
        threading.Thread.__init__(self)
        self.judge_thread = judge_thread
        self.end_tag = False
        self.player_id = player_id
        self.length_limit = 2048
        self.length_sum = 8*1024*1024
        self.type_tag = type_tag
        #尝试启动AI进程并检测异常
        try:
            self.subpro = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE,\
                stdin=subprocess.PIPE, universal_newlines=True)
        except:
            self.end_tag = True
            self.type_tag = 0

    def set_judger(self, judge_thread):
        '''
        设置judger
        '''
        self.judge_thread = judge_thread

    def change_length(self, length):
        '''
        变更长度
        '''
        self.length_limit = length

    def destory(self):
        '''
        退出run函数循环
        '''
        self.end_tag = True
        try:
            self.subpro.terminate()
        except:
            pass
        if self.judge_thread is not None:
            self.judge_thread.awake()

    def write(self, msg):
        '''
        向ai发送消息
        '''
        try:
            self.subpro.stdin.buffer.write(msg)
            self.subpro.stdin.flush()
        except:
            pass

    def run(self):
        '''
        监听ai发送的消息
        '''
        sum = 0
        while not self.end_tag:
            # print(sum)
            return_code = self.subpro.poll()
            if return_code is not None:
                self.judge_thread.send_run_error(self.player_id)
                break
            try:
                read_buffer = self.subpro.stdout.buffer
                data_len = int.from_bytes(read_buffer.read(4), byteorder='big', signed=True)
                if data_len > self.length_limit or sum+data_len > self.length_sum:
                    data_len = 0
                    self.judge_thread.send_ole_error(self.player_id)
                    break
                else:
                    sum += data_len
                    data = read_buffer.read(data_len)
            except:
                self.judge_thread.send_run_error(self.player_id)
                break
            else:
                if data_len != 0:
                    self.judge_thread.receive_message(data.decode(), self.player_id)

class Judger(threading.Thread):
    '''
    和逻辑及控制器通信的线程
    '''
    def __init__(self, command, std_buffer, debug_logic=False, debug_ai=False):
        '''
        线程初始化
        '''
        threading.Thread.__init__(self)
        self.mutex_num = threading.Lock()
        self.mutex_buffer = threading.Lock()
        self.mutex_listen = threading.Lock()
        self.event = threading.Event()
        self.time_limit = 20
        self.length_limit = 2048
        self.listen_list = [] #监听列表
        self.active_list = [] #存活AI列表
        self.player_list = [] #玩家列表
        self.player_num = 0
        self.end_tag = False
        self.std_buffer = std_buffer
        self.config = None
        self.replay = None
        self.debug_logic = debug_logic
        self.debug_ai = debug_ai
        self.record = []
        self.start_flag = False
        self.state = 0
        #尝试启动逻辑进程并检测异常
        try:
            self.subpro = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE,\
                stdin=subprocess.PIPE, universal_newlines=True)
        except:
            self.end_tag = True
            self.std_buffer.logic_start_error(command)
        else:
            self.time_thread = Time_thread(self, self.time_limit)
            self.time_thread.start()
            # self.std_buffer.logic_start_normal()

    def set_config(self, config_str):
        '''
        设置游戏初始信息
        '''
        self.config = config_str

    def set_replay(self, replay_path):
        '''
        设置游戏replay路径
        '''
        self.replay = replay_path

    def awake(self):
        '''
        确保所有ai进程退出后唤醒线程发送消息
        '''
        self.mutex_num.acquire()
        self.player_num = self.player_num-1
        if self.player_num == 0:
            self.event.set()
        self.mutex_num.release()

    def init(self, player_list):
        '''
        初始化
        '''
        self.player_list = player_list
        self.player_num = len(player_list)
        self.last_message = [-1 for i in range(self.player_num)]
        self.re_flag = [False for i in range(self.player_num)]
        self.ole_flag = [False for i in range(self.player_num)]
        self.tle_flag = False
        for player_thread in self.player_list:
            if player_thread.end_tag:
                self.active_list.append(0)
            else:
                self.active_list.append(player_thread.type_tag)
        for player_thread in self.player_list:
            player_thread.change_length(self.length_limit)
        self.send_start_error(self.active_list)

    def destroy(self):
        '''
        清理自己
        '''
        try:
            self.subpro.terminate()
        except:
            pass

    def clear_all(self):
        '''
        清理线程
        '''
        self.event.clear()
        for player_thread in self.player_list:
            try:
                player_thread.destory()
            except:#pragma no cover
                pass
        try:
            self.subpro.terminate()
        except:
            pass
        self.time_thread.awake(-1)
        self.time_thread.join()
        self.event.wait(3)

    def write(self, msg):
        '''
        向逻辑发送消息
        '''
        self.mutex_buffer.acquire()
        try:
            self.subpro.stdin.buffer.write(msg)
            self.subpro.stdin.flush()
        except:
            pass
        self.mutex_buffer.release()

    def receive_message(self, data, player_id):
        player_message_dict = {'player': player_id, 'content': data}
        if self.debug_ai:#pragma no cover
            self.std_buffer.write(bytes(json.dumps(player_message_dict), encoding='utf-8'))
        send_flag = False
        self.mutex_listen.acquire()
        for listen_id in self.listen_list:
            if listen_id == player_id:
                send_flag = True
                break
        if send_flag:
            self.last_message[player_id] = self.time_thread.get_time()*1000.0
        self.mutex_listen.release()
        if send_flag:
            self.write(convert_byte(json.dumps(player_message_dict)))

    def send_message(self, send_goal, logic_data):
        '''
        解析json并发送消息
        '''
        if self.debug_logic:#pragma no cover
            self.std_buffer.write(logic_data)
        if send_goal != -1:
            try:
                assert send_goal >= 0
                assert send_goal < self.player_num
            except:
                self.clear_all()
                self.std_buffer.logic_goal_error(send_goal)
                return True
            else:
                self.player_list[send_goal].write(logic_data)
                return False
        try:
            data = json.loads(logic_data)
            game_state = data['state']
            self.state = game_state
        except:
            self.clear_all()
            print(logic_data)
            print(send_goal)
            self.std_buffer.logic_decode_error(logic_data.decode())
            return True
        if not isinstance(game_state, int):
            self.clear_all()
            self.std_buffer.logic_decode_error(logic_data.decode())
            return True
        if game_state > 0:
            self.mutex_listen.acquire()
            if self.start_flag:
                tmp_list = []
                for i in self.listen_list:
                    tmp_dict = {"position": i, 'time': self.last_message[i]}
                    tmp_dict['memory'] = 0
                    if self.re_flag[i]:
                        tmp_dict['status'] = 'RE'
                    elif self.ole_flag[i]:
                        tmp_dict['status'] = 'OLE'
                    elif self.tle_flag:
                        tmp_dict['status'] = 'TLE'
                    else:
                        tmp_dict['status'] = 'OK'
                    tmp_list.append(tmp_dict)
                self.record.append(tmp_list)
            else:
                self.start_flag = True
            self.time_thread.awake(game_state)
            self.tle_flag = False
            try:
                self.listen_list = data['listen']
                send_list = data['player']
                data_list = data['content']
            except:
                self.clear_all()
                self.std_buffer.logic_decode_error(logic_data.decode())
                return True
            self.last_message = [-1 for i in range(self.player_num)]
            self.mutex_listen.release()

            for player_index, content in enumerate(data_list):
                try:
                    self.player_list[send_list[player_index]].write(\
                        bytes(content, encoding="utf-8"))
                except:
                    self.clear_all()
                    self.std_buffer.logic_send_error(logic_data.decode())
                    return True
        elif game_state < 0:
            self.clear_all()
            try:
                end_str = data['end_info']
            except:
                self.std_buffer.logic_decode_error(logic_data.decode())
            else:
                data['record'] = self.record
                del data['state']
                print(json.dumps(data))
                self.std_buffer.set_end_tag()
        else:
            if data.__contains__('time'):
                self.time_limit = data['time']
                self.time_thread.change(self.time_limit)
            if data.__contains__('length'):
                self.length_limit = data['length']
                for player_thread in self.player_list:
                    player_thread.change_length(self.length_limit)
        return game_state < 0

    def send_start_error(self, active_list):
        '''
        向逻辑发送启动异常信息
        '''
        error_data = {'player_list': active_list, 'player_num': len(active_list),\
                        'replay': self.replay}
        if self.config is not None:
            error_data['config'] = self.config
        self.write(convert_byte(json.dumps(error_data)))

    def send_run_error(self, player_id):
        '''
        向逻辑发送运行异常信息
        '''
        self.re_flag[player_id] = True
        error_content = {'player': player_id, 'state': self.state, 'error': 0, 'error_log': "RUN ERROR"}
        error_data = {'player': -1, 'content': json.dumps(error_content)}
        self.write(convert_byte(json.dumps(error_data)))

    def send_ole_error(self, player_id):
        '''
        向逻辑发送运行异常信息
        '''
        self.ole_flag[player_id] = True
        error_content = {'player': player_id, 'state': self.state, 'error': 2, 'error_log': "OLE ERROR"}
        error_data = {'player': -1, 'content': json.dumps(error_content)}
        self.write(convert_byte(json.dumps(error_data)))

    def send_timeout_error(self, state):
        '''
        向逻辑发送超时信息
        '''
        self.mutex_listen.acquire()
        self.tle_flag = True
        self.mutex_listen.release()
        for player_id in self.listen_list:
            error_content = {'player': player_id, 'state' : state,'error': 1, 'error_log': "TIMEOUT ERROR"}
            error_data = {'player': -1, 'content': json.dumps(error_content)}
            self.write(convert_byte(json.dumps(error_data)))

    def run(self):
        '''
        监听逻辑发送的消息
        '''
        while True:
            try:
                read_buffer = self.subpro.stdout.buffer
                data_len = int.from_bytes(read_buffer.read(4), byteorder='big', signed=True)
                send_goal = int.from_bytes(read_buffer.read(4), byteorder='big', signed=True)
                data = read_buffer.read(data_len)
            except:
                #逻辑进程崩溃
                self.clear_all()
                self.std_buffer.logic_run_error()
                break
            else:
                if data_len != 0:
                    end_tag = self.send_message(send_goal, data)
                    if end_tag:
                        break
                else:
                    return_code = self.subpro.poll()
                    if return_code is not None:
                        self.clear_all()
                        self.std_buffer.logic_run_error()
                        break

class std_thread(threading.Thread):
    '''
    用来管理标准输入输出的线程
    '''
    def __init__(self):
        '''
        初始化
        '''
        threading.Thread.__init__(self)
        self.judge_thread = None
        self.mutex_out = threading.Lock()
        self.read_buffer = sys.stdin.buffer
        self.end_tag = False
        self.player_thread_list = []
        self.debug_logic = False
        self.debug_ai = False
        self.logic_start_flag = False

    def logic_run_error(self):
        '''
        逻辑崩溃
        '''
        print("logic_run_error")

    def logic_decode_error(self, error_str):
        '''
        逻辑解析失败
        '''
        print("logic_decode_error")

    def logic_goal_error(self, error_goal):
        '''
        逻辑发送目标错误
        '''
        print("logic_goal_error")

    def logic_send_error(self, error_str):
        '''
        逻辑信息发送失败
        '''
        print("logic_send_error")

    def logic_start_error(self, error_command):
        '''
        逻辑启动失败
        '''
        print("logic_start_error")

    def set_end_tag(self):
        '''
        标志线程结束
        '''
        self.end_tag = True

    def create_ai(self, index, command):
        '''
        新建一个AI
        '''
        while len(self.player_thread_list) <= index:
            self.player_thread_list.append(None)
        self.player_thread_list[index] = Player(None, command, index, 1)

    def start_game(self, command, config, replay, has_config=True):
        '''
        开始游戏
        '''
        self.debug_logic = False
        self.debug_ai = False
        self.judge_thread = Judger(command, self, self.debug_logic, self.debug_ai)
        if self.judge_thread.end_tag:
            for player_thread in self.player_thread_list:
                player_thread.destory()
            self.judge_thread.destroy()
            return False
        if has_config:
            self.judge_thread.set_config(config)
        self.judge_thread.set_replay(replay)
        for player_thread in self.player_thread_list:
            player_thread.set_judger(self.judge_thread)
            player_thread.start()
        self.judge_thread.init(self.player_thread_list)
        self.judge_thread.start()
        return True

    def run_game(self, logic_command, command_list, replay_path):
        '''
        命令行启动游戏
        '''
        for index, command in enumerate(command_list):
            self.create_ai(index, command)
        self.start_game(logic_command, "", replay_path, has_config=False)

class Time_thread(threading.Thread):
    '''
    用来计时的线程
    '''
    def __init__(self, judger, time_limit):
        '''
        初始化
        '''
        threading.Thread.__init__(self)
        self.time_limit = time_limit
        self.start_time = time.time()
        self.judger = judger
        self.state = 0
        self.now_state = 0
        self.event = threading.Event()
        self.mutex = threading.Lock()
        self.event.clear()

    def change(self, time_limit):
        '''
        修改时间限制
        '''
        self.mutex.acquire()
        self.time_limit = time_limit
        self.mutex.release()

    def awake(self, state):
        '''
        唤醒线程
        '''
        self.mutex.acquire()
        self.state = state
        self.event.set()
        self.mutex.release()

    def get_time(self):
        self.mutex.acquire()
        ans = time.time()-self.start_time
        self.mutex.release()
        return ans

    def run(self):
        while True:
            self.event.wait()
            self.mutex.acquire()
            self.now_state = self.state
            if self.state == -1:
                self.mutex.release()
                break
            self.mutex.release()
            #开始计时
            self.start_time = time.time()
            while True:
                self.mutex.acquire()
                if self.now_state == self.state:
                    end_time = time.time()
                    if end_time-self.start_time >= self.time_limit:
                        self.judger.send_timeout_error(self.now_state)
                        self.mutex.release()
                        break
                else:
                    self.mutex.release()
                    break
                self.mutex.release()
            self.mutex.acquire()
            if self.now_state == self.state:
                self.event.clear()
            self.mutex.release()


def system_convert():
    '''
    获取命令行参数
    '''
    argv_len = len(sys.argv)
    logic_command = sys.argv[1].replace("+", " ")
    path_list = [command_str.replace("+", " ") for command_str in sys.argv[2:argv_len-1]]
    replay_path = sys.argv[argv_len-1]
    return logic_command, path_list, replay_path

def convert_byte(data_str):
    '''
    传输数据的时候加数据长度作为数据头
    '''
    msg_len = len(data_str)
    msg = msg_len.to_bytes(4, byteorder='big', signed=True)
    msg += bytes(data_str, encoding="utf8")
    return msg

def main():
    '''
    主函数
    '''
    std_buffer = std_thread()
    logic, path_list, replay_path = system_convert()
    std_buffer.run_game(logic, path_list, replay_path)

if __name__ == "__main__":#pragma: no cover
    main()
