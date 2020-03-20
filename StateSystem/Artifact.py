from Geometry import calculator
from StateSystem.Event import Event
from StateSystem.Buff import Buff
from StateSystem.EventListener import EventListener
from StateSystem.Unit import Unit

ARTIFACT_ID = 0

def gen_artifact_by_name(name,camp,state_system):
    if name == "HolyLight":
        return HolyLightArtifact(camp,state_system)
    elif name == "SalamanderShield":
        return SalamanderShieldArtifact(camp,state_system)
    elif name == "InfernoFlame":
        return InfernoFlameArtifact(camp,state_system)
    else:
        return None

class Artifact:
    def __init__(self,camp,cost,cool_down,state_system):
        global ARTIFACT_ID
        self.id = ARTIFACT_ID
        ARTIFACT_ID += 1
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
        return [
            self.id,
            self.name,
            self.cost,
            self.max_cool_down,
            self.cool_down_time,
            self.state,
            self.target_type
        ]

    def activate(self,target):
        self.state = "In Use"
        self.state_system.get_player_by_id(self.camp).mana -= self.cost
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
        self.type = "HolyLightAtkBuff"

    def buff(self):
        self.host.atk += 2

    def debuff(self):
        self.host.atk -= 2

class SalamanderShieldArtifact(Artifact):
    def __init__(self,camp,state_system):
        Artifact.__init__(self,camp,6,6,state_system)
        self.name = "SalamanderShield"
        self.target_type = "Unit"

    def effect(self,target):
        new_buff = SalamanderShieldBuff(self.state_system, self)
        new_buff.add_on(target)

class SalamanderShieldRefreshListener(EventListener):
    def deal_event(self,event):
        if event.name == "TurnStart" and self.host.host.state_system.current_player_id == self.host.host.camp \
            and not self.host.host.holy_shield:
            self.host.emit(Event("BuffAdd",{
                "source": self.host.host,
                "type": "HolyShield"
            },-1))

class SalamanderShieldDeathRecycleListener(EventListener):
    def deal_event(self,event):
        if event.name == "Death" and event.parameter_dict["source"] == self.host.host:
            self.host.artifact_host.recycle()
            self.host.delete()

class SalamanderShieldBuff(Buff):
    def __init__(self,state_system,artifact_host):
        self.artifact_host = artifact_host
        Buff.__init__(self,state_system)
        self.add_event_listener(SalamanderShieldRefreshListener())
        self.add_event_listener(SalamanderShieldDeathRecycleListener())
        self.type = "SalamanderShieldBuff"

    def buff(self):
        self.host.max_hp += 4
        self.host.hp += 4
        if not self.host.holy_shield:
            self.state_system.emit(Event("BuffAdd",{
                    "source": self.host,
                    "type": "HolyShield"
                },1))

    def debuff(self):
        self.host.max_hp -= 4
        self.host.hp = min(self.host.hp, self.host.max_hp)

class InfernoFlameArtifact(Artifact):
    def __init__(self,camp,state_system):
        Artifact.__init__(self,camp,6,6,state_system)
        self.name = "InfernoFlame"
        self.target_type = "Pos"

    def effect(self,target):
        for unit in self.state_system.map.unit_list:
            if calculator.cube_distance(unit.pos,target) <= 2 and unit.camp != self.camp:
                self.emit(Event("Damage",{
                    "source": self,
                    "target": unit,
                    "damage": 2,
                    "type": "InfernoFlameActivate"
                },-3))
        self.emit(Event("Summon",{
            "type": "Inferno",
            "level": 1,
            "pos": target,
            "camp": self.camp,
            "artifact_host": self
        }))
        self.emit(Event("CheckDeath",priority=4))
        
class Inferno(Unit):
    def __init__(self,camp,level,pos,state_system,artifact_host):
        name = "Inferno"
        self.artifact_host = artifact_host
        Unit.__init__(
            self,
            camp,
            name,
            level, # Only a single level
            pos,
            state_system
        )

        self.add_event_listener(InfernoRecycleListener())

class InfernoRecycleListener(EventListener):
    def deal_event(self,event):
        if event.name == "Death" and event.parameter_dict["source"] == self.host:
            self.host.artifact_host.recycle()