'''
Definition of unit classes
'''
from .EventListener import *
from .UnitData import UNIT_DATA

UNIT_ID = 0

class Unit:
    def __init__(self,camp,name,level,pos,state_system):
        global UNIT_ID
        self.id = UNIT_ID
        UNIT_ID += 1
        self.camp = camp
        self.level = level
        self.name = name + " (Level " + str(level) + ")"
        self.cost = UNIT_DATA[name]["cost"][level-1]
        self.atk = UNIT_DATA[name]["atk"][level-1]
        self.max_hp = UNIT_DATA[name]["hp"][level-1]
        self.hp = self.max_hp
        self.atk_range = UNIT_DATA[name]["atk_range"][level-1]
        self.max_move = UNIT_DATA[name]["max_move"][level-1]
        self.cool_down = UNIT_DATA[name]["cool_down"][level-1]
        self.pos = pos
        self.state_system = state_system
        self.event_listener_list = []
        self.death_flag = False

    def __str__(self):
        return '''{}
    ID: {}
    Camp: {}
    Cost: {}
    Atk: {}
    HP: {}/{}
    Atk Range: {}
    Max Move: {}
    Cool Down:{}
    Pos: {}'''.format(
                self.name,
                self.id,
                self.camp,
                self.cost,
                self.atk,
                self.hp,
                self.max_hp,
                self.atk_range,
                self.max_move,
                self.cool_down,
                self.pos
            )
    
    def parse(self):
        return {
            "id": self.id,
            "camp": self.camp,
            "name": self.name,
            "cost": self.cost,
            "atk": self.atk,
            "max_hp": self.max_hp,
            "hp": self.hp,
            "atk_range": self.atk_range,
            "max_move": self.max_move,
            "cool_down": self.cool_down,
            "pos": self.pos,
            "level": self.level
        }

    def add_event_listener(self,listener):
        listener.host = self
        self.event_listener_list.append(listener)

    def deal_event(self,event):
        for listener in self.event_listener_list:
            listener.deal_event(event)

    def emit(self,event):
        self.state_system.emit(event)

class Archer(Unit):
    def __init__(self,camp,level,pos,state_system):
        name = "Archer"
        Unit.__init__(
            self,
            camp,
            name,
            level,
            pos,
            state_system
        )
        self.flying = False

        self.add_event_listener(DamageListener())
        self.add_event_listener(AttackListener())
        self.add_event_listener(MoveListener())
        self.add_event_listener(AttackBackListener())
