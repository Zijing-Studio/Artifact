'''
AI
'''
import functools
import random
import calculator
from card import CARD_DICT
from ai_client import AiClient


class AI(AiClient):
    '''玩家编写的ai
    '''

    def __init__(self):
        super().__init__()
        # 以下是玩家自己的初始构造
        self.relic_pos = list()
        self.enemy_pos = list()
        self.target_barrack = list()

    def choose_cards(self):
        '''(根据初始阵营)选择初始卡组
        '''
        # artifacts和creatures可以修改
        self.artifacts = ["HolyLight"]
        self.creatures = ["Archer", "Swordman", "VolcanoDragon"]
        self.init()

    def early_stage(self):
        """
        在费用较低时尽可能爆等星级为1的兵，优先度剑士>弓箭手>火山龙
        """
        if self.round == 0 or self.round == 1:
            # 先确定自己的基地、对方的基地
            self.relic_pos = self.map.relics[self.my_camp].pos
            self.enemy_pos = self.map.relics[self.my_camp ^ 1].pos
            self.target_barrack = self.map.barracks[0]

            # 确定离自己基地最近的驻扎点的位置
            for barrack in self.map.barracks:
                if calculator.cube_distance(self.relic_pos, barrack.pos) < \
                        calculator.cube_distance(self.relic_pos, self.target_barrack.pos):
                    self.target_barrack = barrack

            # 在正中心偏右召唤一个弓箭手，用来抢占驻扎点
            self.summon('Archer', 1, self.pos_shift(self.relic_pos, 'SF'))
        else:
            # 神器能用就用，选择覆盖单位数最多的地点
            # TODO
            if self.players[self.my_camp].mana >= 6 and self.can_use_artifact():
                pos_list = calculator.all_pos_in_map()
                best_pos = pos_list[0]
                max_benefit = 0
                for pos in pos_list:
                    unit_list = calculator.units_in_range(
                        pos, 2, self.map, self.my_camp)
                    if len(unit_list) > max_benefit:
                        best_pos = pos, max_benefit = len(unit_list)
                self.use(self.players[self.my_camp]['Artifact'][0]['id'], best_pos)
                self.update_game_info()
            
            # 之后先战斗，再移动
            self.battle()
            self.update_game_info()
            self.march()
            self.update_game_info()

            # 最后进行召唤
            # 将所有本方出兵点按照到对方基地的距离排序，从近到远出兵
            summon_pos_list = self.get_summon_pos_by_camp(self.my_camp)
            summon_pos_list.sort(key=lambda _pos: calculator.cube_distance(_pos, self.enemy_pos))
            available_summon_pos_list = []
            for pos in summon_pos_list:
                unit_on_pos_ground = self.get_unit_by_pos(pos, 0)
                if unit_on_pos_ground is None:
                    available_summon_pos_list.append(pos)
            del summon_pos_list

            # 统计各个生物的可用数量，在假设出兵点无限的情况下，按照1个剑士、1个弓箭手、1个火山龙的顺序召唤
            mana = self.players[self.my_camp].mana
            deck = self.players[self.my_camp].creature_capacity
            available_count = {}
            for card_unit in deck:
                available_count[card_unit.type] = card_unit.available_count
            summon_list = []

            # 剑士和弓箭手数量不足或者格子不足则召唤火山龙
            if (len(available_summon_pos_list) == 1 or available_count['Swordman'] + available_count['Archer'] < 2) \
                    and mana >= 5:
                summon_list = ['VolcanoDragon']
                mana -= 5
            while mana >= 2:
                if available_count['Swordman'] > 0 and mana >= CARD_DICT['Swordman'][1].cost:
                    summon_list.append('Swordman')
                    mana -= CARD_DICT['Swordman'][1].cost
                    available_count['Swordman'] -= 1
                if available_count['Archer'] > 0 and mana >= CARD_DICT['Archer'][1].cost:
                    summon_list.append('Archer')
                    mana -= CARD_DICT['Archer'][1].cost
                    available_count['Archer'] -= 1
                if available_count['VolcanoDragon'] > 0 and mana >= CARD_DICT['VolcanoDragon'][1].cost:
                    summon_list.append('VolcanoDragon')
                    mana -= CARD_DICT['VolcanoDragon'][1].cost
                    available_count['VolcanoDragon'] -= 1

            for pos in available_summon_pos_list:
                self.summon(summon_list[0], 1, pos)
                summon_list.pop(0)

    def battle(self):
        """
        基本思路，行动顺序:
        火山龙：攻击高>低 （大AOE输出），随机攻击
        剑士：攻击低>高 打消耗，优先打攻击力低的
        弓箭手：攻击高>低 优先打不能反击的攻击力最高的，其次打能反击的攻击力最低的
        对单位的战斗完成后，对神迹进行输出
        """
        ally_list = self.get_units_by_camp(self.my_camp)

        # 自定义排列顺序
        def cmp(unit1, unit2):
            if unit1.can_atk != unit2.can_atk:  # 首先要能动
                return unit1.can_atk > unit2.can_atk
            elif unit1.type != unit2.type:  # 火山龙>剑士>弓箭手
                def type_id_gen(
                    typename): return 0 if typename == 'VolcanoDragon' else 1 if typename == 'Swordman' else 2
                return type_id_gen(unit1.type) < type_id_gen(unit2.type)
            elif unit1.type == 'VolcanoDragon' or unit1.type == 'Archer':
                return unit1.atk > unit2.atk
            else:
                return unit1.atk < unit2.atk

        # 按顺序排列好单位，依次攻击
        ally_list.sort(key=functools.cmp_to_key(cmp))
        for ally in ally_list:
            if not ally.can_atk:
                break
            enemy_list = self.get_units_by_camp(self.my_camp ^ 1)
            target_list = []
            for enemy in enemy_list:
                if self.can_attack(ally.id, enemy.id):
                    target_list.append(enemy)
            if len(target_list) == 0:
                continue

            if ally.type == 'VolcanoDragon':
                tar = random.randint(0, len(target_list) - 1)
                self.attack(ally.id, target_list[tar].id)
                self.update_game_info()

            elif ally.type == 'Swordman':
                enemy_list.sort(key=lambda _enemy: _enemy.atk)
                self.attack(ally.id, target_list[0].id)
                self.update_game_info()

            elif ally.type == 'Archer':
                enemy_list.sort(key=lambda _enemy: _enemy.atk, reverse=True)
                suc = False
                for enemy in target_list:
                    if not self.can_attack(enemy.id, ally.id):
                        self.attack(ally.id, enemy.id)
                        suc = True
                        self.update_game_info()
                        break
                if suc:
                    continue
                enemy_list.sort(key=lambda _enemy: _enemy.atk)
                self.attack(ally.id, target_list[0].id)
                self.update_game_info()

        # 最后攻击神迹
        ally_list = self.get_units_by_camp(self.my_camp)
        ally_list.sort(key=functools.cmp_to_key(cmp))
        for ally in ally_list:
            if ally.can_atk == 0:
                break
            dis = calculator.cube_distance(ally.pos, self.enemy_pos)
            if CARD_DICT[ally.type][ally.level].min_atk_range <= dis \
                    <= CARD_DICT[ally.type][ally.level].max_atk_range:
                self.attack(ally.id, self.my_camp ^ 1)

    def march(self):
        """
        先动所有剑士，冲家，若驻扎点上没有地面单位，则让弓箭手能走上去就走上去，然后火龙能走上去就走上去，其他情况下尽可能冲家
        """
        ally_list = self.get_units_by_camp(self.my_camp)
        ally_list.sort(key=lambda typename: 0 if typename ==
                       'Swordman' else 1 if typename == 'Archer' else 2)
        for ally in ally_list:
            if ally.type == 'Swordman':
                reach_list = calculator.reachable(ally, self.map)
                if len(reach_list) == 0:
                    continue
                reach_list.sort(
                    key=lambda _pos: calculator.cube_distance(_pos, self.enemy_pos))
                self.move(ally.id, reach_list[0])

            else:
                # TODO
                # reach_list = calculator.reachable(ally, self.map)
                if len(reach_list) == 0:
                    continue
                if self.get_unit_by_pos(self.target_barrack, False) is None \
                        and self.target_barrack in reach_list:
                    self.move(ally.id, self.target_barrack)
                    self.update_game_info()
                reach_list.sort(
                    key=lambda _pos: calculator.cube_distance(_pos, self.enemy_pos))
                self.move(ally.id, reach_list[0])

    def pos_shift(self, pos, direct: str):
        """
        对于给定位置，给出按照自己的视角（基地在最下方）的某个方向移动一步后的位置
        :param pos:  [x, y, z]
        :param direct: 一个str，含2个字符，意义见注释
        :return: 移动后的位置 [x', y' ,z']
        """
        if self.my_camp == 0:
            if direct.upper() == "FF":  # Straight-forward
                return [pos[0] + 1, pos[1] - 1, pos[2]]
            elif direct.upper() == "SF":  # Superior-forward (the direction which goes nearer to the barrack)
                return [pos[0] + 1, pos[1], pos[2] - 1]
            elif direct.upper() == "IF":  # Inferior-forward
                return [pos[0], pos[1] + 1, pos[2] - 1]
            elif direct.upper() == "BB":  # Straight-backward
                return [pos[0] - 1, pos[1] + 1, pos[2]]
            elif direct.upper() == "SB":  # Superior-backward
                return [pos[0], pos[1] - 1, pos[2] + 1]
            elif direct.upper() == "IB":  # Inferior-backward
                return [pos[0] - 1, pos[1], pos[2] + 1]

        else:
            if direct.upper() == "FF":  # Straight-forward
                return [pos[0] - 1, pos[1] + 1, pos[2]]
            elif direct.upper() == "SF":  # Superior-forward (the direction which goes nearer to the barrack)
                return [pos[0] - 1, pos[1], pos[2] + 1]
            elif direct.upper() == "IF":  # Inferior-forward
                return [pos[0], pos[1] - 1, pos[2] + 1]
            elif direct.upper() == "BB":  # Straight-backward
                return [pos[0] + 1, pos[1] - 1, pos[2]]
            elif direct.upper() == "SB":  # Superior-backward
                return [pos[0], pos[1] + 1, pos[2] - 1]
            elif direct.upper() == "IB":  # Inferior-backward
                return [pos[0] + 1, pos[1], pos[2] - 1]

    def play(self):
        '''玩家需要编写的ai操作函数
        '''
        self.early_stage()
        self.end_round()


def main():
    '''启动AI
    '''
    player_ai = AI()
    player_ai.choose_cards()
    while True:
        player_ai.update_game_info()
        player_ai.play()


if __name__ == '__main__':
    main()
