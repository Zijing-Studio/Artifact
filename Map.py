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

    def add_unit(self,unit):
        self.unit_list.append(unit)

    def remove_unit(self,unit):
        self.unit_list.remove(unit)