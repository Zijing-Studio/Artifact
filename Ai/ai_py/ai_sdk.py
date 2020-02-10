'''AI相关的SDK
'''

import sys
import json
import calculator


def convert_byte(data_str):
    '''加数据长度作为数据头,并转化为bytes

    Args:
        data_str: str

    Returns:
        头部加上了长度的bytes串
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
    '''读取信息

    Return:
        dict
    '''
    read_buffer = sys.stdin.buffer
    data_length = read_buffer.read(4)
    data = read_buffer.read(int(data_length.decode()))
    return json.loads(data)

def init(player, artifacts, creatures):
    '''玩家player选择初始神器artifacts和生物creatures

    Args:
        player: 玩家阵营
        artifacts: 神器名字的字符串数组
        creatures: 生物名字的字符串数组
    '''
    message = {
        "player": player,
        "round": 0,
        "operation_type": "init",
        "operation_parameters":
        {
            "artifacts": artifacts,
            "creatures": creatures
        }
    }
    send_opt(json.dumps(message))

def summon(player, _round, _type, star, position):
    '''玩家player在地图position处召唤一个本方类型为_type,星级为star的单位

    Args:
        player: 玩家阵营
        _round: 当前回合(若游戏实际回合不等于_round，则指令无效)
        _type: 描述单位类型的字符串
        star: 单位星级
        position: 单位在地图上的[x,y,z]位置
    '''
    message = {
        "player": player,
        "round": _round,
        "operation_type": "summon",
        "operation_parameters":
        {
            "position": position,
            "type": _type,
            "star": star
        }
    }
    send_opt(json.dumps(message))

def move(player, _round, mover, position):
    '''玩家player将id为mover的单位移动到地图position处

    Args:
        player: 玩家阵营
        _round: 当前回合(若游戏实际回合不等于_round，则指令无效)
        mover: 需要移动的单位的id
        position: 目标在地图上的[x,y,z]位置
    '''
    message = {
        "player": player,
        "round": _round,
        "operation_type": "move",
        "operation_parameters":
        {
            "mover": mover,
            "position": position
        }
    }
    send_opt(json.dumps(message))

def attack(player, _round, attacker, target):
    '''玩家player令id为attacker的单位攻击id为target的单位

    Args:
        player: 玩家阵营
        _round: 当前回合(若游戏实际回合不等于_round，则指令无效)
        attacker: 发起攻击单位的id
        target: 被攻击单位的id
    '''
    message = {
        "player": player,
        "round": _round,
        "operation_type": "attack",
        "operation_parameters":
        {
            "attacker": attacker,
            "target": target
        }
    }
    send_opt(json.dumps(message))

def use(player, _round, artifact, target):
    '''玩家player对target目标使用artifact神器

    Args:
        player: 玩家阵营
        _round: 当前回合(若游戏实际回合不等于_round，则指令无效)
        artifact: 使用的神器的id
        target: 目标单位的id / 地图的[x,y,z]位置
    '''
    message = {
        "player": player,
        "round": _round,
        "operation_type": "use",
        "operation_parameters":
        {
            "card": artifact,
            "target": target
        }
    }
    send_opt(json.dumps(message))

def end_round(player, _round):
    '''玩家player结束当前回合

    Args:
        player: 玩家阵营
        _round: 当前回合(若游戏实际回合不等于_round，则指令无效)
    '''
    message = {
        "player": player,
        "round": _round,
        "operation_type": "endround",
        "operation_parameters": {}
    }
    send_opt(json.dumps(message))

def get_distance_on_ground(_map, pos_a, pos_b, camp):
    '''获取地图_map上camp阵营单位从位置pos_a到位置pos_b的地面距离(不经过地面障碍或敌方地面单位)

    Args:
        _map: 地图
        pos_a: 起点坐标
        pos_b: 终点坐标
        camp: 单位阵营

    Returns:
        int 距离
    '''
    # 地图边界
    obstacles_pos = calculator.MAPBORDER[:]
    # 地面障碍
    obstacles_pos += _map["ground_obstacles"][:]
    # 敌方地面生物
    for unit in _map["units"]:
        if unit["camp"] != camp and (not unit["flying"]):
            obstacles_pos.append(unit["pos"])
    return len(calculator.search_path(pos_a, pos_b, obstacles_pos, []))

def get_distance_in_sky(_map, pos_a, pos_b, camp):
    '''获取地图_map上camp阵营单位从位置pos_a到位置pos_b的飞行距离(不经过飞行障碍或敌方飞行单位)

    Args:
        _map: 地图
        pos_a: 起点坐标
        pos_b: 终点坐标
        camp: 单位阵营

    Returns:
        int,距离
    '''
    # 地图边界
    obstacles_pos = calculator.MAPBORDER[:]
    # 地面障碍
    obstacles_pos += _map["flying_obstacles"][:]
    # 敌方地面生物
    for unit in _map["units"]:
        if unit["camp"] != camp and unit["flying"]:
            obstacles_pos.append(unit["pos"])
    return len(calculator.search_path(pos_a, pos_b, obstacles_pos, []))

def get_units(_map, pos):
    '''获取地图_map上位置pos上所有生物

    Args:
        _map: 地图
        pos: 坐标

    Returns:
        list 包含Unit
    '''
    return [unit for unit in _map["units"] if unit["pos"] == pos]

def check_barrack(_map, pos):
    '''对于指定位置pos,判断其驻扎情况

    Args:
        _map: 地图
        pos: 坐标

    Returns:
        int 不是驻扎点返回-2,中立返回-1,否则返回占领该驻扎点的阵营(0/1)
    '''
    for barrack in _map["barracks"]:
        if barrack["pos"] == pos:
            return barrack["camp"]
    return -2

def can_attack(attacker, target):
    '''判断生物attacker能否攻击到生物target(只考虑攻击力、攻击范围)

    Args:
        attacker: 发起攻击的单位的id
        target: 受攻击的单位的id

    Returns:
        bool 能攻击到返回True,不能攻击到返回False
    '''
    # 攻击力小于等于0的单位无法攻击
    if attacker["atk"] <= 0:
        return False
    # 攻击范围
    dist = calculator.cube_distance(attacker["pos"], target["pos"])
    if dist < attacker["atk_range"][0] or dist > attacker["atk_range"][1]:
        return False
    # 对空攻击
    if target["flying"] and (not attacker["atk_flying"]):
        return False
    return True

def can_use_artifact(_map, artifact, target, camp):
    '''判断阵营camp能否对目标target使用神器artifact(不考虑消耗、冷却)

    Args:
        _map: 地图
        artifact: 神器
        target: 目标(id或者位置)
        camp: 使用神器的阵营

    Returns:
        bool 能攻击到返回True,不能攻击到返回False
    '''
    if artifact["name"] == "HolyLight":
        return calculator.in_map(target)
    if artifact["name"] == "InfernoFlame":
        # 无地面生物
        for unit in _map["units"]:
            if (unit["pos"] == target) and (not unit["flying"]):
                return False
        # 神迹范围<=5
        if calculator.cube_distance(target, _map["relics"][camp]["pos"]) <= 5:
            return True
        # 占领驻扎点范围<=3
        for barrack in _map["barracks"]:
            if (barrack["camp"] == camp and
                    calculator.cube_distance(target, barrack["pos"]) <= 3):
                return True
    elif artifact["name"] == "SalamanderShield":
        return artifact["camp"] == target["camp"]
    return False
