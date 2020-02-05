'''
AI
'''

import ai_sdk
import calculator


class AI:
    '''玩家编写的ai
    '''

    def __init__(self, artifacts, creatures):
        self.round = 0                          # 当前回合
        self.my_camp = -1                       # 己方阵营
        self.map = dict()                       # 地图信息
        self.players = list()                   # 两名玩家的信息
        ai_sdk.init(artifacts, creatures)       # 选择初始卡组

    def update_game_info(self):
        '''更新游戏信息
        '''
        game_info = ai_sdk.read_opt()
        self.round = game_info['round']         # 当前回合
        self.my_camp = game_info['camp']        # 己方阵营
        self.map = game_info['map']             # 地图信息
        self.players = game_info['players']     # 两名玩家的信息

    def get_distance_on_ground(self, pos_a, pos_b):
        '''获取己方单位从位置pos_a到位置pos_b的地面距离
        '''
        # 地图边界
        obstacles_pos = calculator.MAPBORDER[:]
        # 地面障碍
        obstacles_pos += self.map["ground_obstacles"][:]
        # 敌方地面生物
        for unit in self.map["units"]:
            if unit["camp"] != self.my_camp and (not unit["flying"]):
                obstacles_pos.append(unit["pos"])
        return len(calculator.search_path(pos_a, pos_b, obstacles_pos, []))

    def get_distance_in_sky(self, pos_a, pos_b):
        '''获取己方单位从位置pos_a到位置pos_b的飞行距离
        '''
        # 地图边界
        obstacles_pos = calculator.MAPBORDER[:]
        # 地面障碍
        obstacles_pos += self.map["flying_obstacles"][:]
        # 敌方地面生物
        for unit in self.map["units"]:
            if unit["camp"] != self.my_camp and unit["flying"]:
                obstacles_pos.append(unit["pos"])
        return len(calculator.search_path(pos_a, pos_b, obstacles_pos, []))

    def get_units(self, pos):
        '''对于指定位置pos,获取其上所有生物
        '''
        return [unit for unit in self.map["units"] if unit["pos"] == pos]

    def check_barrack(self, pos):
        '''对于指定位置pos,判断其驻扎情况

        不是驻扎点返回-2,中立返回-1,否则返回占领该驻扎点的阵营(0/1)
        '''
        for barrack in self.map["barracks"]:
            if barrack["pos"] == pos:
                return barrack["camp"]
        return -2

    def can_attack(self, attacker, target):
        '''判断生物attacker能否攻击到生物target(只考虑攻击力、攻击范围)
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

    def can_use_artifact(self, artifact, target):
        '''判断能否对目标target使用神器artifact(不考虑消耗、冷却)
        '''
        if artifact["name"] == "HolyLight":
            return calculator.in_map(target)
        if artifact["name"] == "InfernoFlame":
            # 无地面生物
            for unit in self.map["units"]:
                if (unit["pos"] == target) and (not unit["flying"]):
                    return False
            # 神迹范围<=5
            if calculator.cube_distance(target, self.map.relics[self.my_camp]["pos"]) <= 5:
                return True
            # 占领驻扎点范围<=3
            for barrack in self.map["barracks"]:
                if (barrack["camp"] == self.my_camp and
                        calculator.cube_distance(target, barrack["pos"]) <= 3):
                    return True
        elif artifact["name"] == "SalamanderShield":
            return artifact["camp"] == unit["camp"]
        return False

    def play(self):
        '''玩家需要编写的ai操作函数
        '''
        if self.round < 20:
            ai_sdk.end_round(self.round)
        else:
            exit(0)


def main():
    '''启动AI
    '''
    player_ai = AI(["artifact"], ["creature0", "creature1", "creature2"])
    while True:
        player_ai.update_game_info()
        player_ai.play()


if __name__ == '__main__':
    main()
