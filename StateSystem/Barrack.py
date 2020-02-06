class Barrack:
    def __init__(self,pos,camp,summon_pos_list):
        self.pos = pos
        self.camp = camp
        self.summon_pos_list = summon_pos_list

    def parse(self):
        return {
            "pos": self.pos,
            "camp": self.camp,
            "summon_pos_list": self.summon_pos_list
        }

BARRACK_INIT_LIST = [
    ((-6,-6,12), None, [(-7,-5,12), (-5,-7,12), (-5,-6,11)]),
    ((6,6,-12), None, [(7,5,-12), (5,7,-12), (5,6,-11)]),
    ((0,-5,5), None, [(0,-4,4), (-1,-4,5), (-1,-5,6)]),
    ((0,5,-5), None, [(0,4,-4), (1,4,-5), (1,5,-6)])
]