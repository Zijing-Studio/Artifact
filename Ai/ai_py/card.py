'''标准卡牌
'''


class Creature:
    '''生物
    '''

    def __init__(self, _count, _cost, _atk, _maxhp, _minatk, _maxatk,
                 _maxmove, _cool, _fly,  _atkfly, _agility,
                 _holyshield):
        self.available_count = _count
        self.cost = _cost
        self.atk = _atk
        self.max_hp = _maxhp
        self.min_atk_range = _minatk
        self.max_atk_range = _maxatk
        self.max_move = _maxmove
        self.cool_down = _cool
        self.flying = _fly
        self.atk_flying = _atkfly
        self.agility = _agility
        self.holy_shield = _holyshield


class Artifact:
    '''神器
    '''

    def __init__(self, _cost, _cool, _targettype):
        self.cost = _cost
        self.cool_down = _cool
        self.target_type = _targettype


SWORDMAN = [Creature(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            Creature(4, 2, 2, 2, 1, 1, 3, 3, 0, 0, 0, 0),
            Creature(4, 4, 4, 4, 1, 1, 3, 3, 0, 0, 0, 0),
            Creature(4, 6, 6, 6, 1, 1, 3, 3, 0, 0, 0, 0)]

ARCHER = [Creature(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
          Creature(3, 2, 1, 1, 2, 4, 3, 4, 0, 1, 0, 0),
          Creature(3, 2, 1, 1, 2, 4, 3, 4, 0, 1, 0, 0),
          Creature(3, 2, 1, 1, 2, 4, 3, 4, 0, 1, 0, 0)]

BLACKBAT = [Creature(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            Creature(4, 2, 1, 1, 0, 1, 5, 2, 1, 1, 0, 0),
            Creature(4, 3, 2, 1, 0, 1, 5, 2, 1, 1, 0, 0),
            Creature(4, 5, 3, 2, 0, 1, 5, 2, 1, 1, 0, 0)]

PRIEST = [Creature(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
          Creature(4, 2, 0, 2, 0, 0, 3, 4, 0, 0, 0, 0),
          Creature(4, 3, 0, 2, 0, 0, 3, 4, 0, 0, 0, 0),
          Creature(4, 5, 0, 3, 0, 0, 3, 5, 0, 0, 0, 0)]

VOLCANOGRAGON = [Creature(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                 Creature(3, 5, 3, 5, 1, 2, 3, 5, 0, 0, 0, 0),
                 Creature(3, 7, 4, 7, 1, 2, 3, 5, 0, 0, 0, 0),
                 Creature(3, 9, 5, 9, 1, 2, 3, 5, 0, 0, 0, 0)]

HOLYLIGHT = Artifact(8, 6, "Pos")

SALAMANDERSHIELD = Artifact(6, 6, "Unit")

INFERNOFLAME = Artifact(6, 6, "Pos")


if __name__ == "__main__":
    print("3星弓箭手的攻击力:", ARCHER[3].atk)
    print("圣光之耀的法力消耗:", HOLYLIGHT.cost)