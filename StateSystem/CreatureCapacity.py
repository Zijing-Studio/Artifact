from .UnitData import UNIT_DATA

class CreatureCapacity:
    def __init__(self,name):
        self.type = name
        self.duplicate = UNIT_DATA[name]["duplicate"]
        self.cool_down_list = []

    def cool_down(self):
        for item in self.cool_down_list:
            item -= 1
        new_list = []
        for item in self.cool_down_list:
            if item != 0:
                new_list.append(item)

    def available_count(self):
        return self.duplicate - len(self.cool_down_list)

    def new_cool_down(self,level):
        self.cool_down_list.append(UNIT_DATA[self.type]["cool_down"][level])

    def parse(self):
        return {
            "type": self.type,
            "available_count": self.available_count(),
            "cool_down_list": self.cool_down_list
        }