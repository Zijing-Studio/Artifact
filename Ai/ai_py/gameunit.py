'''游戏单位
'''


class Unit:
    '''生物
    '''

    def __init__(self, unit_dict=None):
        if unit_dict is None:
            unit_dict = dict()
        self.id = unit_dict.get('id', -1)  # id
        self.camp = unit_dict.get('camp', -1)  # 阵营
        self.type = unit_dict.get('type', '')  # 种类
        self.name = unit_dict.get('name', '')  # 名字
        self.cost = unit_dict.get('cost', 0)  # 法力消耗
        self.atk = unit_dict.get('atk', 0)  # 攻击
        self.max_hp = unit_dict.get('max_hp', 0)  # 生命上限
        self.hp = unit_dict.get('hp', 0)  # 当前生命
        self.atk_range = unit_dict.get('atk_range', [0, 0])  # 最小攻击范围 最大攻击范围
        self.max_move = unit_dict.get('max_move', 0)  # 行动力
        self.cool_down = unit_dict.get('cool_down', 0)  # 冷却时间
        self.pos = unit_dict.get('pos', [0, 0, 0])  # 位置
        self.level = unit_dict.get('level', 0)  # 等级
        self.flying = unit_dict.get('flying', False)  # 是否飞行
        self.atk_flying = unit_dict.get('atk_flying', False)  # 是否对空
        self.agility = unit_dict.get('agility', False)  # 是否迅捷
        self.holy_shield = unit_dict.get('holy_shield', False)  # 有无圣盾
        self.can_atk = unit_dict.get('can_atk', False)  # 能否攻击
        self.can_move = unit_dict.get('can_move', False)  # 能否移动

class Barrack:
    '''驻扎点
    '''

    def __init__(self, barrack_dict=None):
        if barrack_dict is None:
            barrack_dict = dict()
        self.pos = barrack_dict.get('pos', [0, 0, 0])  # 位置
        self.camp = barrack_dict.get('camp', -1)  # 阵营
        if self.camp == None:
            self.camp = -1
        self.summon_pos_list = barrack_dict.get(
            'summon_pos_list', [[0, 0, 0]])  # 出兵点位置

class Miracle:
    '''神迹
    '''

    def __init__(self, miracle_dict=None):
        if miracle_dict is None:
            miracle_dict = dict()
        self.camp = miracle_dict.get('camp', -1)  # 阵营
        self.max_hp = miracle_dict.get('max_hp', -1)  # 最大生命值
        self.hp = miracle_dict.get('hp', -1)  # 当前生命值
        self.pos = miracle_dict.get('pos', [0, 0, 0])  # 位置
        self.summon_pos_list = miracle_dict.get(
            'summon_pos_list', [[0, 0, 0]])  # 初始出兵点位置
        self.name = miracle_dict.get('name', '')  # 名字
        self.id = miracle_dict.get('id', -1)  # id

class Obstacle:
    def __init__(self, obstacle_dict=None):
        if obstacle_dict is None:
            obstacle_dict = dict()
        self.type = obstacle_dict.get('type', '')  # 种类
        self.pos = obstacle_dict.get('pos', [0, 0, 0])  # 位置
        self.allow_flying = obstacle_dict.get(
            'allow_flying', False)  # 是否允许飞行生物通过
        self.allow_ground = obstacle_dict.get(
            'allow_ground', False)  # 是否允许地面生物通过

class Artifact:
    '''神器
    '''
    def __init__(self, artifact_dict=None):
        if artifact_dict is None:
            artifact_dict = dict()
        self.id = artifact_dict.get('id', -1)  # id
        self.name = artifact_dict.get('name', '')  # 名字
        self.camp = artifact_dict.get('camp', -1)  # 阵营
        self.cost = artifact_dict.get('cost', 0)  # 法力消耗
        self.max_cool_down = artifact_dict.get('max_cool_down', 0)  # 最大冷却时间
        self.cool_down_time = artifact_dict.get('cool_down_time', 0)  # 当前冷却时间
        self.state = artifact_dict.get('state', '')  # 使用状态
        self.target_type = artifact_dict.get('target_type', '')  # 目标种类

class CreatureCapacity:
    def __init__(self, creature_capacity_dict=None):
        if creature_capacity_dict is None:
            creature_capacity_dict = dict()
        self.type = creature_capacity_dict.get('type', '')            # 种类
        self.available_count = creature_capacity_dict.get(
            'available_count', 1)  # 生物槽容量
        self.cool_down_list = creature_capacity_dict.get(
            'cool_down_list', [0])  # 冷却时间

class Map:
    '''地图
    '''
    def __init__(self, map_dict=None):
        self.units = [Unit()]
        self.barracks = [Barrack()]
        self.miracles = [Miracle()]
        self.obstacles = [Obstacle()]
        self.flying_obstacles = [Obstacle()]
        self.ground_obstacles = [Obstacle()]
        if map_dict is None:
            return
        units_dict_list = map_dict.get('units', [])
        self.units = [Unit(x) for x in units_dict_list]
        barracks_dict_list = map_dict.get('barracks', [])
        self.barracks = [Barrack(x) for x in barracks_dict_list]
        miracles_dict_list = map_dict.get('miracles', [])
        self.miracles = [Miracle(x) for x in miracles_dict_list]
        obstacles_dict_list = map_dict.get('obstacles', [])
        self.obstacles = [Obstacle(x) for x in obstacles_dict_list]
        flying_obstacles_dict_list = map_dict.get('flying_obstacles', [])
        self.flying_obstacles = [Obstacle(x) for x in flying_obstacles_dict_list]
        ground_obstacles_dict_list = map_dict.get('ground_obstacles', [])
        self.ground_obstacles = [Obstacle(x) for x in ground_obstacles_dict_list]

class Player:
    '''玩家
    '''

    def __init__(self, player_dict=None):
        if player_dict is None:
            player_dict = dict()
        self.camp = player_dict.get('camp', -1)  # 阵营
        self.artifact = [Artifact()]
        artifact_dict_list = player_dict.get('artifact', [])  # 神器
        self.artifact = [Artifact(x) for x in artifact_dict_list]
        self.mana = player_dict.get('mana', 0)  # 当前法力值
        self.max_mana = player_dict.get('max_mana', 0)  # 最大法力值
        self.creature_capacity = [CreatureCapacity()]
        creature_capacity_dict_list = player_dict.get('creature_capacity', [])
        self.creature_capacity = [CreatureCapacity(x) for x in creature_capacity_dict_list]
        self.new_summoned_id_list = player_dict.get(
            'new_summoned_id_list', [])  # 最新召唤的生物id
