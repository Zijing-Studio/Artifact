'''
裁判程序
'''

import sys
import threading
import shlex
import subprocess
import json
import time
import rserver


#pylint: disable = W0702


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
        self.type_tag = type_tag
        # 尝试启动AI进程并检测异常
        try:
            self.subpro = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE,
                                           stdin=subprocess.PIPE, universal_newlines=True)
        except:
            self.end_tag = True
            self.type_tag = 0

    def set_judger(self, judge_thread):
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
        while not self.end_tag:
            return_code = self.subpro.poll()
            if return_code is not None:
                self.judge_thread.send_run_error(self.player_id)
                break
            try:
                read_buffer = self.subpro.stdout.buffer
                data_len = int.from_bytes(read_buffer.read(
                    4), byteorder='big', signed=True)
                if data_len > self.length_limit:
                    data_len = 0
                else:
                    data = read_buffer.read(data_len)
            except:
                self.judge_thread.send_run_error(self.player_id)
                break
            else:
                if data_len != 0:
                    self.judge_thread.receive_message(
                        data.decode(), self.player_id)


class Judger(threading.Thread):
    '''
    和逻辑及控制器通信的线程
    '''

    def __init__(self, command, debug_logic=False, debug_ai=False):
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
        self.listen_list = []  # 监听列表
        self.active_list = []  # 存活AI列表
        self.player_list = []  # 玩家列表
        self.player_num = 0
        self.end_tag = False
        self.std_buffer = None
        self.config = None
        self.replay = None
        self.debug_logic = debug_logic
        self.debug_ai = debug_ai
        self.time_thread = Time_thread(self, self.time_limit)
        self.time_thread.start()
        # 尝试启动逻辑进程并检测异常
        try:
            self.subpro = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE,
                                           stdin=subprocess.PIPE, universal_newlines=True)
        except:
            pass
            # logic_start_error(command)

    def set_std(self, std_buffer):
        self.std_buffer = std_buffer

    def set_config(self, config_str):
        self.config = config_str

    def set_replay(self, replay_path):
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
            player_thread.destory()
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
        '''
        接收选手消息后的处理(看效率可能会修改成队列实现)
        '''
        player_message_dict = {'player': player_id, 'content': data}
        if self.debug_ai:
            self.std_buffer.write(
                bytes(json.dumps(player_message_dict), encoding='utf-8'))
        send_flag = False
        self.mutex_listen.acquire()
        for listen_id in self.listen_list:
            if listen_id == player_id:
                send_flag = True
                break
        self.mutex_listen.release()
        if send_flag:
            self.write(convert_byte(json.dumps(player_message_dict)))

    def send_message(self, send_goal, logic_data):
        '''
        解析json并发送消息
        '''
        if self.debug_logic:
            self.std_buffer.write(logic_data)
        if send_goal != -1:
            try:
                assert(send_goal >= 0)
                assert(send_goal < self.player_num)
            except:
                self.clear_all()
                logic_goal_error(send_goal)
                return True
            else:
                self.player_list[send_goal].write(logic_data)
                return False
        try:
            data = json.loads(logic_data)
            game_state = data['state']
        except:
            self.clear_all()
            logic_decode_error(logic_data.decode())
            return True
        if not isinstance(game_state, int):
            self.clear_all()
            logic_decode_error(logic_data.decode())
            return True
        if game_state > 0:
            self.mutex_listen.acquire()
            try:
                self.listen_list = data['listen']
                send_list = data['player']
                data_list = data['content']
            except:
                self.clear_all()
                logic_decode_error(logic_data.decode())
                return True
            self.mutex_listen.release()
            for player_index, content in enumerate(data_list):
                try:
                    self.player_list[send_list[player_index]].write(
                        bytes(content, encoding="utf-8"))
                except:
                    self.clear_all()
                    logic_send_error(logic_data.decode())
                    return True
            self.time_thread.awake(game_state)
        elif game_state < 0:
            self.clear_all()
            try:
                end_str = data['end_info']
            except:
                pass
                logic_decode_error(logic_data.decode())
            else:
                self.std_buffer.write(convert_byte(end_str))
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
        error_data = {'player_list': active_list, 'player_num': len(active_list),
                      'replay': self.replay}
        if self.config is not None:
            error_data['config'] = self.config
        self.write(convert_byte(json.dumps(error_data)))

    def send_run_error(self, player_id):
        '''
        向逻辑发送运行异常信息
        '''
        error_content = {'player': player_id,
                         'error': 0, 'error_log': "RUN ERROR"}
        error_data = {'player': -1, 'content': json.dumps(error_content)}
        self.write(convert_byte(json.dumps(error_data)))

    def send_timeout_error(self, state):
        '''
        向逻辑发送超时信息
        '''
        error_content = {'player': state,
                         'error': 1, 'error_log': "TIMEOUT ERROR"}
        error_data = {'player': -1, 'content': json.dumps(error_content)}
        self.write(convert_byte(json.dumps(error_data)))

    def run(self):
        '''
        监听逻辑发送的消息
        '''
        while True:
            return_code = self.subpro.poll()
            try:
                read_buffer = self.subpro.stdout.buffer
                data_len = int.from_bytes(read_buffer.read(
                    4), byteorder='big', signed=True)
                send_goal = int.from_bytes(
                    read_buffer.read(4), byteorder='big', signed=True)
                data = read_buffer.read(data_len)
            except:
                # 逻辑进程崩溃
                self.clear_all()
                logic_run_error()
                break
            else:
                if data_len != 0:
                    end_tag = self.send_message(send_goal, data)
                    if end_tag:
                        break
            if return_code is not None:
                self.clear_all()
                logic_run_error()
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

    def set_end_tag(self):
        self.end_tag = True

    def success(self, type):
        success_dict = {"type": type, "success": 1}
        self.write(convert_byte(json.dumps(success_dict)))

    def fail(self, type):
        fail_dict = {"type": type, "success": 0}
        self.write(convert_byte(json.dumps(fail_dict)))

    def write(self, msg):
        self.mutex_out.acquire()
        sys.stdout.buffer.write(msg)
        sys.stdout.flush()
        self.mutex_out.release()

    def create_ai(self, index, command):
        while(len(self.player_thread_list) <= index):
            self.player_thread_list.append(None)
        self.player_thread_list[index] = Player(None, command, index, 1)

    def del_ai(self, index):
        self.player_thread_list[index].destory()
        self.player_thread_list[index] = None

    def create_human(self, index, ip, port, room_id):
        while len(self.player_thread_list) <= index:
            self.player_thread_list.append(None)
        self.player_thread_list[index] = rserver.RServer(
            ip, port, room_id, index)
        self.player_thread_list[index].build_server()
        self.player_thread_list[index].set_std(self)

    def start_game(self, command, config, replay, has_config=True):
        self.judge_thread = Judger(command, self.debug_logic, self.debug_ai)
        for player_thread in self.player_thread_list:
            player_thread.set_judger(self.judge_thread)
            player_thread.start()
        self.judge_thread.set_std(self)
        if has_config:
            self.judge_thread.set_config(config)
        self.judge_thread.set_replay(replay)
        self.judge_thread.init(self.player_thread_list)
        self.judge_thread.start()

    def run_game(self, logic_command, command_list, replay_path):
        for index, command in enumerate(command_list):
            self.create_ai(index, command)
        self.start_game(logic_command, "", replay_path, has_config=False)

    def opt_test(self, opt_str):
        if opt_str == 'help':
            print(
                "For the following <index>, it's an integer belonging to [0, 100)")
            print("For the following <command>, if there is ' ' with '+' instead")
            print('    example:python3+logic.py')
            print('INSTRUCTION SET:')
            print('  state:get the AI information that has been started')
            print('    example:state')
            print(
                "  debug_logic:negate the debug_logic state, you can input 'state' to check debug_logic state")
            print(
                '    if your debug_logic state is True, the message from logic will be output in std_out')
            print('    example:debug_logic')
            print(
                "  debug_ai:negate the debug_ai state, you can input 'state' to check debug_ai state")
            print(
                '    if your debug_ai state is True, the message from ai will be output in std_out')
            print('    example:debug_ai')
            #print('  load <path>:load instrutions from <path>, One instruction per line')
            #print('    example:load instruction.txt')
            print('  0 <index> <command>:start an AI numbered <index> with <command>')
            print('    example:0 0 python3+ai.py')
            print('  1 <index> <ip> <port> <room_id>:start a human player numbered <index> connected with <ip>:<port>')
            print('    judger can only check index, then it will start a server using <ip>:<port>, you need to make sure <ip>:<port> is right')
            print('    example:1 0 0.0.0.0 14285 1')
            print('  2 <index>: delete an AI numbered <index>')
            print('    example:2 0')
            print('  3 <index>: delete a huamn player numbered <index>')
            print('    example:3 0')
            print('  4 <command> <config> <replay>:start your game with <command>, the meaning of\
                <config> and <replay> can be found in Game Development Manual when the game is initialized')
            print('  	when you use this command(4), you need to make sure all AIs are started and the index is sorted from 0')
            print('     after using this command(4) successfully, you cannot use the instrution set until your game is over')
            print('     example:4 logic.py my_config replay.json')
            print('  5:quit all of the processes and threads')
            print("    if you don't use command(4) to start a game, we recommend that you exit with command(5) rather than violently withdraw")
            print('    example:5')
        elif opt_str == 'state':
            print('debug_logic = %s' %
                  ('True' if(self.debug_logic) else 'False'))
            print('debug_ai = %s' % ('True' if(self.debug_ai) else 'False'))
            while len(self.player_thread_list) > 0 and\
                    self.player_thread_list[len(self.player_thread_list)-1] is None:
                self.player_thread_list.pop()
            print('index    AI_state')
            for index, player_thread in enumerate(self.player_thread_list):
                if player_thread is not None:
                    print('%5d    True' % (index))
        elif opt_str == 'debug_logic':
            self.debug_logic = (~self.debug_logic)
        elif opt_str == 'debug_ai':
            self.debug_ai = (~self.debug_ai)
        else:
            opt_list = opt_str.split(' ')
            try:
                opt_list[0] = int(opt_list[0])
                assert(opt_list[0] >= 0)
                assert(opt_list[0] <= 5)
            except:
                print('Your instrution is wrong, please check your input')
            else:
                if opt_list[0] == 0:
                    try:
                        index = int(opt_list[1])
                        command = opt_list[2].replace("+", " ")
                        assert(len(opt_list) == 3)
                        assert(index >= 0)
                        assert(index < 100)
                    except:
                        print('Your instrution is wrong, please check your input')
                    else:
                        if len(self.player_thread_list) > index and self.player_thread_list[index] is not None:
                            print('You have started a process numbered %d' %
                                  (index))
                        else:
                            self.create_ai(index, command)
                            if self.player_thread_list[index].end_tag:
                                self.player_thread_list[index] = None
                                print('start error! <index>: %d, <command>: %s' % (
                                    index, command))
                            else:
                                print('start successfully! <index>: %d, <command>: %s' % (
                                    index, command))
                elif opt_list[0] == 1:
                    try:
                        index = int(opt_list[1])
                        ip = opt_list[2]
                        port = opt_list[3]
                        room_id = opt_list[4]
                        assert(len(opt_list) == 5)
                        assert(index >= 0)
                        assert(index < 100)
                    except:
                        print('Your instrution is wrong, please check your input')
                    else:
                        if len(self.player_thread_list) > index and self.player_thread_list[index] is not None:
                            print('You have started a process numbered %d' %
                                  (index))
                        else:
                            self.create_human(index, ip, port, room_id)
                elif opt_list[0] == 2:
                    try:
                        index = int(opt_list[1])
                        assert(len(opt_list) == 2)
                        assert(index >= 0)
                        assert(index < 100)
                    except:
                        print('Your instrution is wrong, please check your input')
                    else:
                        if len(self.player_thread_list) <= index:
                            print('cannot find an process numbered %d' %
                                  (index))
                        elif self.player_thread_list[index] == None:
                            print('cannot find an process numbered %d' %
                                  (index))
                        else:
                            self.del_ai(index)
                            print('process numberd %d has been deleted!' %
                                  (index))
                elif opt_list[0] == 3:
                    try:
                        index = int(opt_list[1])
                        assert(len(opt_list) == 2)
                        assert(index >= 0)
                        assert(index < 100)
                    except:
                        print('Your instrution is wrong, please check your input')
                    else:
                        if len(self.player_thread_list) <= index:
                            print('cannot find an process numbered %d' %
                                  (index))
                        elif self.player_thread_list[index] == None:
                            print('cannot find an process numbered %d' %
                                  (index))
                        else:
                            self.del_ai(index)
                            print('process numberd %d has been deleted!' %
                                  (index))
                elif opt_list[0] == 4:
                    try:
                        command = opt_list[1].replace("+", " ")
                        config = opt_list[2]
                        replay = opt_list[3]
                        assert(len(opt_list) == 4)
                    except:
                        print('Your instrution is wrong, please check your input')
                    else:
                        while len(self.player_thread_list) > 0 and\
                                self.player_thread_list[len(self.player_thread_list)-1] is None:
                            self.player_thread_list.pop()
                        can_flag = True
                        for player_thread in self.player_thread_list:
                            if player_thread is None:
                                can_flag = False
                                break
                        if can_flag:
                            print('start game! <command>: %s, <config>: %s, <replay>: %s' % (
                                command, config, replay))
                            self.start_game(command, config, replay)
                            return True
                        else:
                            print(
                                'when you use this command(4), you need to make sure all AIs are started and the index is sorted from 0')
                elif opt_list[0] == 5:
                    for index, player_thread in enumerate(self.player_thread_list):
                        if player_thread is not None:
                            player_thread.destory()
                            self.player_thread_list[index] = None
                    return True
        return False

    def run_test(self):
        print('You can input help to know the instrution set')
        print('> ', end="", flush=True)
        while True:
            opt_str = input()
            can_break = self.opt_test(opt_str)
            if can_break:
                break
            print('> ', end="", flush=True)

    def run_buffer(self):
        while True:
            data_len_bytes = self.read_buffer.read(4)
            if data_len_bytes is not None:
                data_len = int.from_bytes(
                    data_len_bytes, byteorder='big', signed=True)
                if data_len == 0:
                    continue
                data = self.read_buffer.read(data_len)
                data_dict = json.loads(data)
                if data_dict['type'] == 0:
                    index = data_dict['index']
                    command = data_dict['command']
                    self.create_ai(index, command)
                    if self.player_thread_list[index].end_tag:
                        self.fail(0)
                    else:
                        self.success(0)
                elif data_dict['type'] == 1:
                    index = data_dict['index']
                    ip = data_dict['ip']
                    port = data_dict['port']
                    room_id = data_dict['room_id']
                    self.create_human(index, ip, port, room_id)
                elif data_dict['type'] == 2:
                    index = data_dict['index']
                    self.del_ai(index)
                    self.success(2)
                elif data_dict['type'] == 3:
                    index = data_dict['index']
                    self.player_thread_list[index].destory()
                    self.player_thread_list[index] = None
                    self.success(3)
                elif data_dict['type'] == 4:
                    command = data_dict['command']
                    config = data_dict['config']
                    replay = data_dict['replay']
                    while len(self.player_thread_list) > 0 and\
                            self.player_thread_list[len(self.player_thread_list)-1] is None:
                        self.player_thread_list.pop()
                    self.start_game(command, config, replay)
                    self.success(4)
                elif data_dict['type'] == 5:
                    if self.judge_thread is not None:
                        self.judge_thread.destroy()
                        self.judge_thread.join()
                        for player_thread in self.player_thread_list:
                            player_thread.join()
                    else:
                        for index, player_thread in enumerate(self.player_thread_list):
                            if player_thread is not None:
                                player_thread.destory()
                                self.player_thread_list[index] = None
                    break
            else:
                if self.end_tag:
                    self.judge_thread.join()
                    for player_thread in self.player_thread_list:
                        player_thread.join()
                    break


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

    def run(self):
        while True:
            self.event.wait()
            self.mutex.acquire()
            self.now_state = self.state
            if self.state == -1:
                self.mutex.release()
                break
            self.mutex.release()
            # 开始计时
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
    path_list = [command_str.replace("+", " ")
                 for command_str in sys.argv[2:argv_len-1]]
    replay_path = sys.argv[argv_len-1]
    return logic_command, path_list, replay_path


def convert_byte(data_str):
    '''
    judger 传输数据的时候加数据长度作为数据头
    '''
    message_len = len(data_str)
    message = message_len.to_bytes(4, byteorder='big', signed=True)
    message += bytes(data_str, encoding="utf8")
    return message


def logic_run_error():
    pass
    # sys.stdout.buffer.write(convert_byte(""))
    # sys.stdout.flush()


def logic_decode_error(error_str):
    pass
    #sys.stdout.buffer.write(convert_byte(error_str+"DECODE ERROR"))
    # sys.stdout.flush()


def logic_goal_error(error_goal):
    pass


def logic_send_error(error_str):
    pass


def main():
    '''
    主函数
    '''
    std_buffer = std_thread()
    if len(sys.argv) == 1:
        std_buffer.run_buffer()
    elif sys.argv[1] == 'test_mode':
        std_buffer.run_test()
    else:
        logic, path_list, replay_path = system_convert()
        std_buffer.run_game(logic, path_list, replay_path)


if __name__ == "__main__":
    main()
