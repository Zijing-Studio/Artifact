'''
    Definition of map class
'''

class Map:
    def __init__(self):
        self.unit_list = []
        self.obstacle_list = []
        self.barrack_list = []
        self.relic_list = []

    def parse(self):
        return {
            "units": [unit.parse() for unit in self.unit_list],
            "barracks": [barrack.parse() for barrack in self.barrack_list],
            "relics": [relic.parse() for relic in self.relic_list],
            "ground_obstacles": [obstacle.parse() for obstacle in self.obstacle_list 
                if not obstacle.allow_ground],
            "flying_obstacles": [obstacle.parse() for obstacle in self.obstacle_list 
                if not obstacle.allow_flying]
        }
        
    def get_unit_at(self,pos,flying = None):
        for unit in self.unit_list:
            if pos == unit.pos:
                if flying == None:
                    return unit
                else:
                    if unit.flying == flying:
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

    def get_obstacles(self):
        return self.obstacle_list

    def get_ground_obstacles(self):
        result = []
        for item in self.obstacle_list:
            if not item.allow_ground:
                result.append(item)
        return result

    def get_flying_obstacles(self):
        result = []
        for item in self.obstacle_list:
            if not item.allow_flying:
                result.append(item)
        return result