class Barrack:
    def __init__(self,pos,summon_pos_list):
        self.pos = pos
        self.camp = None
        self.summon_pos_list = summon_pos_list

    def parse(self):
        return {
            "pos": self.pos,
            "camp": self.camp,
            "summon_pos_list": self.summon_pos_list
        }

BARRACK_INIT_LIST = [
    ((0,0,0),[])
]