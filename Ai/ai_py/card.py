'''标准卡牌
'''


class Creature:
    '''生物
    '''
    
    def __init__(self, _type, _count, _cost, _atk, _maxhp, _minatk, _maxatk,
                 _maxmove, _cool, _fly, _atkfly, _agility, _holyshield):
        self.type = _type  # 种类
        self.available_count = _count  # 生物槽容量
        self.cost = _cost  # 法力消耗
        self.atk = _atk  # 攻击
        self.max_hp = _maxhp  # 最大生命值
        self.min_atk_range = _minatk  # 最小攻击范围
        self.max_atk_range = _maxatk  # 最大攻击范围
        self.max_move = _maxmove  # 行动力
        self.cool_down = _cool  # 冷却时间
        self.flying = _fly  # 是否飞行
        self.atk_flying = _atkfly  # 能否对空
        self.agility = _agility  # 是否迅捷
        self.holy_shield = _holyshield  # 有无圣盾


class Artifact:
    '''神器
    '''
    
    def __init__(self, _name, _cost, _cool, _targettype):
        self.name = _name  # 名字
        self.cost = _cost  # 法力消耗
        self.cool_down = _cool  # 冷却时间
        self.target_type = _targettype  # 目标类型


SWORDSMAN = [Creature("Swordsman", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            Creature("Swordsman", 4, 2, 2, 2, 1, 1, 3, 3, 0, 0, 0, 0),
            Creature("Swordsman", 4, 4, 4, 4, 1, 1, 3, 3, 0, 0, 0, 0),
            Creature("Swordsman", 4, 6, 6, 6, 1, 1, 3, 3, 0, 0, 0, 0)]

ARCHER = [Creature("Archer", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
          Creature("Archer", 3, 2, 1, 1, 2, 4, 3, 4, 0, 1, 0, 0),
          Creature("Archer", 3, 2, 1, 1, 2, 4, 3, 4, 0, 1, 0, 0),
          Creature("Archer", 3, 2, 1, 1, 2, 4, 3, 4, 0, 1, 0, 0)]

BLACKBAT = [Creature("BlackBat", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            Creature("BlackBat", 4, 2, 1, 1, 0, 1, 5, 2, 1, 1, 0, 0),
            Creature("BlackBat", 4, 3, 2, 1, 0, 1, 5, 2, 1, 1, 0, 0),
            Creature("BlackBat", 4, 5, 3, 2, 0, 1, 5, 2, 1, 1, 0, 0)]

PRIEST = [Creature("Priest", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
          Creature("Priest", 4, 2, 0, 2, 0, 0, 3, 4, 0, 0, 0, 0),
          Creature("Priest", 4, 3, 0, 2, 0, 0, 3, 4, 0, 0, 0, 0),
          Creature("Priest", 4, 5, 0, 3, 0, 0, 3, 5, 0, 0, 0, 0)]

VOLCANOGRAGON = [Creature("VolcanoDragon", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                 Creature("VolcanoDragon", 3, 5, 3, 5, 1, 2, 3, 5, 0, 0, 0, 0),
                 Creature("VolcanoDragon", 3, 7, 4, 7, 1, 2, 3, 5, 0, 0, 0, 0),
                 Creature("VolcanoDragon", 3, 9, 5, 9, 1, 2, 3, 5, 0, 0, 0, 0)]

HOLYLIGHT = Artifact("HolyLight", 8, 6, "Pos")

SALAMANDERSHIELD = Artifact("SalamanderShield", 6, 6, "Unit")

INFERNOFLAME = Artifact("InfernoFlame", 6, 6, "Pos")

INFERNO = Creature("Inferno", 0, 0, 8, 8, 1, 1, 3, 0, 0, 0, 0, 0)

CARD_DICT = {
    'Swordsman': SWORDSMAN,
    'Archer': ARCHER,
    'BlackBat': BLACKBAT,
    'Priest': PRIEST,
    'VolcanoDragon': VOLCANOGRAGON
}

if __name__ == "__main__":
    print("3星弓箭手的攻击力:", ARCHER[3].atk)
    print("圣光之耀的法力消耗:", HOLYLIGHT.cost)
