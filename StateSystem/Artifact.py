from Geometry import calculator
from StateSystem.Event import Event
from StateSystem.Buff import Buff
from StateSystem.EventListener import EventListener

class Artifact:
    def __init__(self,camp,cost,cool_down,state_system):
        self.state_system = state_system
        self.event_listener_list = []
        self.cost = cost
        self.max_cool_down = cool_down
        self.cool_down_time = 0
        self.state = "Ready"
        self.camp = camp
        self.name = ""
        self.target_type = None
    
    def add_event_listener(self,listener):
        listener.host = self
        self.event_listener_list.append(listener)

    def deal_event(self,event):
        for listener in self.event_listener_list:
            listener.deal_event(event)

    def emit(self,event):
        self.state_system.emit(event)

    def parse(self):
        return {
            "name": self.name,
            "camp": self.camp,
            "cost": self.cost,
            "max_cool_down": self.max_cool_down,
            "cool_down_time": self.cool_down_time,
            "state": self.state
        }

    def activate(self,target):
        self.state = "In Use"
        self.effect(target)
        
    def effect(self,target):
        pass

    def recycle(self):
        self.state = "Cooling Down"
        self.cool_down_time = self.max_cool_down

    def cool_down(self):
        if self.cool_down_time > 0:
            self.cool_down_time -= 1
        if self.cool_down_time == 0:
            self.state = "Ready"

class HolyLightArtifact(Artifact):
    def __init__(self,camp,state_system):
        Artifact.__init__(self,camp,6,6,state_system)
        self.name = "HolyLight"
        self.target_type = "Pos"

    def effect(self,target):
        for unit in self.state_system.map.unit_list:
            if calculator.cube_distance(unit.pos,target) <= 2 and unit.camp == self.camp:
                self.emit(Event("Heal",{
                    "source": self,
                    "target": unit,
                    "heal": unit.max_hp
                },-1))
                new_buff = HolyLightAtkBuff(self.state_system)
                new_buff.add_on(unit)
        self.recycle()
        
class RemoveOnEndTurnListener(EventListener):
    def deal_event(self,event):
        if event.name == "TurnEnd":
            self.host.delete()

class HolyLightAtkBuff(Buff):
    def __init__(self,state_system):
        Buff.__init__(self,state_system)
        self.add_event_listener(RemoveOnEndTurnListener())

    def buff(self):
        self.host.atk += 2

    def debuff(self):
        self.host.atk -= 2