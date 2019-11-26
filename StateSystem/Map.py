'''
    Definition of map class
'''

class Map:
    def __init__(self):
        self.unit_list = []
        self.obstacle_list = []
        self.barrack_list = []
        self.relic_list = []
        
    def get_unit_at(self,pos):
        for unit in self.unit_list:
            if pos == unit.pos:
                return unit
        return None

    def get_unit_by_id(self,id):
        for unit in self.unit_list:
            if unit.id == id:
                return unit
        return None

    def get_relic_by_id(self,id):
        for relic in self.relic_list:
            if relic.camp == id:
                return relic
        return None

    def add_unit(self,unit):
        self.unit_list.append(unit)

    def remove_unit(self,unit):
        self.unit_list.remove(unit)