import sys
import json
import queue
import asyncio
import logging
import threading
import websockets

DEBUG_MODE = True

IP = '0.0.0.0'
PORT = 14285
ROOM_ID = '1'
SEAT = '0'

#pylint: disable = R0201
#pylint: disable = R0801

# logging.basicConfig(filename='remote_server.txt', level=logging.INFO)
logger = logging.getLogger('  rserver')

def convert_byte(data_str):
    '''
    传输数据的时候加数据长度作为数据头
    '''
    message_len = len(data_str)
    message = message_len.to_bytes(4, byteorder='big', signed=True)
    message += bytes(data_str, encoding="utf8")
    return message


class RServer():
    USERS = set()
    player = None

    recv_msg_queue = queue.Queue()
    send_msg_queue = queue.Queue()

    server_thread = threading.Thread

    def __init__(self, ip=IP, port=PORT, room_id=ROOM_ID, seat=SEAT, loop=None):
        logger.info('%s %s %s %s' % (ip, port, room_id, seat))
        self.seat = 0
        self.judger = None
        self.std_thread = None
        self.ip = ip
        self.port = port
        self.room_id = room_id
        self.seat = seat
        self.loop = loop
        self.end_tag = False
        self.type_tag = 2
        self.length_limit = 2 ** 16

    def build_server(self):
        self.server_thread = threading.Thread(target=self.run)
        self.server_thread.start()

    
    def destory(self):
        #coro = self.player.close()
        #future = asyncio.ensure_future(coro, self.loop)
        if self.judger is not None:
            self.judger.awake()

    async def register(self, websocket):
        self.USERS.add(websocket)
        logger.info('%s connected' % websocket)

    async def unregister(self, websocket):
        self.USERS.remove(websocket)
        logger.info('%s disconnected' % websocket)

    def player_connect(self, ws, token: str):
        judge_ip, lst = token.split(':')
        port, room, username, seat = token.split('/')
        if '' in [judge_ip, port, room, username, seat]:
            logger.info('token %s invalid' % token)
            return False
        if self.player is not None:
            return False

        self.player = ws
        self.std_thread.write(convert_byte(json.dumps({'type': 1, 'index': int(self.seat), 'success': 1})))

        return True

    async def handler(self, websocket, path):
        logger.info('%s' % websocket)
        try:
            await self.register(websocket)
            async for message in websocket:
                logger.info('from %s received:\n%s' % (websocket, message))
                try:
                    data = json.loads(message)
                    token = data["token"]
                    if data["request"] == "connect":
                        flag = self.player_connect(websocket, token)
                        if not flag:
                            logger.info('invalid connection info, quit')
                            break
                    elif data["request"] == "action":
                        self.recv_msg(data["content"])
                except:
                    logger.exception('error occured when reading message from %s' % websocket)
        except:
            logger.exception('in rserver handler')
        finally:
            await self.unregister(websocket)

    def run(self):
        try:
            logging.info('running!')
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            start_server = websockets.serve(self.handler, self.ip, self.port)
            self.loop.run_until_complete(start_server)
            logging.info('built server!')
            self.loop.run_forever()
        except:
            logging.exception('invalid at run')

    def join(self):
        # self.server_thread.join()
        pass

    def recv_msg(self, msg):
        try:
            self.judger.receive_message(msg, int(self.seat))
        except:
            logger.exception('in receiving message')

    def get_msg(self):
        while self.recv_msg_queue.empty():
            continue
        return self.recv_msg_queue.get()

    def send_msg(self, msg):
        coro = self.player.send(msg)
        future = asyncio.run_coroutine_threadsafe(coro, self.loop)

    def send2player(self, msg, request='action'):
        self.send_msg(json.dumps({'request': request, 'content': msg}))

    def set_judger(self, judger):
        self.judger = judger

    def set_std(self, std_thread):
        self.std_thread = std_thread

    def write(self, msg):
        self.send2player(msg.decode())

    def change_length(self, length):
        del length

    def start(self):
        return None





'''
def start(ip=IP, port=PORT, room_id=ROOM_ID, seat=SEAT):
    global IP, PORT, ROOM_ID, SEAT
    IP, PORT, ROOM_ID, SEAT = ip, port, room_id, seat
    server.build_server(ip, port)
'''

'''
if __name__ == '__main__':
    try:
        IP = sys.argv[1]
        PORT = int(sys.argv[2])
        ROOM_ID = sys.argv[3]
        SEAT = sys.argv[4]
    except:
        logger.info('Using default arguments, no room id and seat')
    start(IP, PORT, ROOM_ID, SEAT)
    import time
    cnt = 0
    while server.player is None:
        cnt += 1
        if cnt % 10000000 == 0:
            logger.info('player not connected yet %s' % cnt)
    logger.info('connected')
    send2player(msg='', request='connected')
    send2player(r"{'player': ['player1', 'player2', 'player3'],'position': 0}".replace('\'', '"'))
    time.sleep(1)
    send2player(r"{'current player': 0,'top card': 'red_0','color': 'red','direction': 0,"
                r"'player1': ['red_1', 'red_+2'],'player2': 3,'player3': 3}".replace('\'', '"'))
    msg = get_player_opt()
    logger.info('get opt from player: %s' % msg)
    send2player(r"{'current player': 1,'top card': 'red_1','color': 'red','direction': 0,"
                r"'player1': ['red_+2'],'player2': 3,'player3': 3}".replace('\'', '"'))
    time.sleep(5)
    send2player({'end_info': 'game over you *** !'})
    # send2player(r"")
'''
