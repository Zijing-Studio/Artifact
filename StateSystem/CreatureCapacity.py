from .UnitData import UNIT_DATA,UNIT_NAME_PARSED

class CreatureCapacity:
    def __init__(self,name):
        self.type = name
        self.duplicate = UNIT_DATA[name]["duplicate"]
        self.cool_down_list = []
        self.available_count = self.duplicate

    def cool_down(self):
        self.cool_down_list = [item - 1 for item in self.cool_down_list]
        new_list = []
        for item in self.cool_down_list:
            if item != 0:
                new_list.append(item)
            else:
                self.available_count += 1
        self.cool_down_list = new_list

    def summon(self):
        self.available_count -= 1

    def new_cool_down(self,level):
        self.cool_down_list.append(UNIT_DATA[self.type]["cool_down"][level-1])

    def parse(self):
        return [
            UNIT_NAME_PARSED[self.type],
            self.available_count,
            self.cool_down_list
        ]