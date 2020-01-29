'''
Definition of unit classes
'''
from .EventListener import *
from .UnitData import UNIT_DATA

UNIT_ID = 3

class Unit:
    def __init__(self,camp,name,level,pos,state_system):
        global UNIT_ID
        self.id = UNIT_ID
        UNIT_ID += 1
        self.camp = camp
        self.level = level
        self.type = name
        self.name = name + " (Level " + str(level) + ")"
        self.cost = UNIT_DATA[name]["cost"][level-1]
        self.atk = UNIT_DATA[name]["atk"][level-1]
        self.max_hp = UNIT_DATA[name]["hp"][level-1]
        self.hp = self.max_hp
        self.atk_range = UNIT_DATA[name]["atk_range"][level-1]
        self.max_move = UNIT_DATA[name]["max_move"][level-1]
        self.cool_down = UNIT_DATA[name]["cool_down"][level-1]
        self.pos = pos
        self.flying = UNIT_DATA[name]["flying"]
        self.atk_flying = UNIT_DATA[name]["atk_flying"]
        self.agility = UNIT_DATA[name]["agility"]
        self.holy_shield = UNIT_DATA[name]["holy_shield"]

        self.death_flag = False

        self.buff_list = []

        self.state_system = state_system
        self.event_listener_list = []

        self.add_event_listener(DamageListener())
        self.add_event_listener(AttackListener())
        self.add_event_listener(MoveListener())
        self.add_event_listener(AttackBackListener())
        self.add_event_listener(HealListener())
        self.add_event_listener(HolyShieldAddListener())
        self.add_event_listener(HolyShieldBreakListener())

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
    Pos: {}
    Holy Shield: {}'''.format(
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
                self.pos,
                self.holy_shield
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
            "level": self.level,
            "flying": self.flying,
            "atk_flying": self.atk_flying,
            "agility": self.agility,
            "holy_shield": self.holy_shield
        }

    def add_event_listener(self,listener):
        listener.host = self
        self.event_listener_list.append(listener)

    def deal_event(self,event):
        for listener in self.event_listener_list:
            listener.deal_event(event)
        for buff in self.buff_list:
            buff.deal_event(event)

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

class Swordman(Unit):
    def __init__(self,camp,level,pos,state_system):
        name = "Swordman"
        Unit.__init__(
            self,
            camp,
            name,
            level,
            pos,
            state_system
        )

class BlackBat(Unit):
    def __init__(self,camp,level,pos,state_system):
        name = "BlackBat"
        Unit.__init__(
            self,
            camp,
            name,
            level,
            pos,
            state_system
        )

class Priest(Unit):
    def __init__(self,camp,level,pos,state_system):
        name = "Priest"
        Unit.__init__(
            self,
            camp,
            name,
            level,
            pos,
            state_system
        )
        self.priest_buff_list = []

        if level == 1 or level == 3:
            self.add_event_listener(PriestHealListener())

        if level == 2 or level == 3:
            self.add_event_listener(PriestAtkListener())

class VolcanoDragon(Unit):
    def __init__(self,camp,level,pos,state_system):
        name = "VolcanoDragon"
        Unit.__init__(
            self,
            camp,
            name,
            level,
            pos,
            state_system
        )

        self.add_event_listener(VolcanoDragonAtkListener())



