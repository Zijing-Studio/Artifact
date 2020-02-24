from .Event import Event
from Geometry import calculator
from .Buff import PriestAtkBuff

class EventListener:
    def __init__(self):
        self.host = None # where listener is

    def deal_event(self,event):
        pass

class RefreshMoveAtkListener(EventListener):
    def deal_event(self,event):
        if event.name == "Refresh" and event.parameter_dict["camp"] == self.host.camp:
            self.host.can_move = True
            self.host.can_atk = True

class OneMoveListener(EventListener):
    def deal_event(self,event):
        if event.name == "Arrive" and event.parameter_dict["source"] == self.host:
            self.host.can_move = False
            if not self.host.agility:
                self.host.can_atk = False
        if event.name == "Attack" and event.parameter_dict["source"] == self.host:
            self.host.can_atk = False
            if not self.host.agility:
                self.host.can_move = False


class DamageListener(EventListener):
    def deal_event(self,event):
        if event.name == "Damage":
            try:
                if event.parameter_dict["target"] == self.host:
                    if self.host.holy_shield:
                        event.parameter_dict["damage"] = 0
                        self.host.emit(Event("HolyShieldBreak", {"source": self.host}, -1))
                    self.host.hp -= event.parameter_dict["damage"]
                    # print("Deal {} damage on {} (ID: {})".format(
                    #     event.parameter_dict["damage"],self.host.name,self.host.id
                    # ))
            except:
                # print("An Error appears while handling Damage event.")
                pass

class HolyShieldAddListener(EventListener):
    def deal_event(self,event):
        if event.name == "HolyShieldAdd":
            try:
                if event.parameter_dict["source"] == self.host and not self.host.holy_shield:
                    self.host.holy_shield = True
                    # print("{} (ID: {}) gains Holy Shield".format(
                    #     self.host.name,self.host.id
                    # ))
            except:
                # print("An Error appears while handling HolyShieldAdd event.")
                pass


class HolyShieldBreakListener(EventListener):
    def deal_event(self,event):
        if event.name == "HolyShieldBreak":
            try:
                if event.parameter_dict["source"] == self.host:
                    if not self.host.holy_shield:
                        raise BaseException()
                    self.host.holy_shield = False
                    # print("{} (ID: {})'s Holy Shield is broken".format(
                    #     self.host.name,self.host.id
                    # ))
            except:
                # print("An Error appears while handling HolyShieldBreak event.")
                pass

class AttackListener(EventListener):
    def deal_event(self,event):
        if event.name == "Attack":
            try:
                if event.parameter_dict["source"] == self.host:
                    self.host.emit(Event("Attacking",event.parameter_dict))
                    self.host.emit(Event("Damage",{
                        "source": event.parameter_dict["source"],
                        "target": event.parameter_dict["target"],
                        "damage": event.parameter_dict["source"].atk
                    }))
                    self.host.emit(Event("Attacked",event.parameter_dict))
                    self.host.emit(Event("CheckDeath",priority=4))
                    # print("{} (ID: {}) attacks {} (ID: {})".format(
                    #     event.parameter_dict["source"].name,
                    #     event.parameter_dict["source"].id,
                    #     event.parameter_dict["target"].name,
                    #     event.parameter_dict["target"].id
                    # ))
            except:
                # print("An Error appears while handling Attack event..")
                pass

class AttackBackListener(EventListener):
    def deal_event(self,event):
        if event.name == "Attacked":
            try:
                if event.parameter_dict["target"] == self.host:
                    distance = calculator.cube_distance(
                        event.parameter_dict["source"].pos,
                        event.parameter_dict["target"].pos,
                    )
                    if self.host.atk_range[0] <= distance <= self.host.atk_range[1] and \
                        (not event.parameter_dict["source"].flying or self.host.atk_flying):
                        self.host.emit(Event("Damage",{
                            "source": event.parameter_dict["target"],
                            "target": event.parameter_dict["source"],
                            "damage": event.parameter_dict["target"].atk
                        }))
                        # print("{} (ID: {}) attacks back on {} (ID: {})".format(
                        #     event.parameter_dict["target"].name,
                        #     event.parameter_dict["target"].id,
                        #     event.parameter_dict["source"].name,
                        #     event.parameter_dict["source"].id
                        # ))
            except:
                # print("An Error appears while handling Attacked event..")
                pass

class MoveListener(EventListener):
    def deal_event(self,event):
        if event.name == "Move":
            try:
                if event.parameter_dict["source"] == self.host:
                    self.host.emit(Event("Leave",{
                        "source": event.parameter_dict["source"],
                        "pos": event.parameter_dict["source"].pos
                    }))
                    self.host.pos = event.parameter_dict["dest"]
                    self.host.emit(Event("Arrive",{
                        "source": event.parameter_dict["source"],
                        "pos": event.parameter_dict["source"].pos
                    }))
                    self.host.emit(Event("UpdateRingBuff",priority = 3))
                    # print("{} (ID: {}) moves to {}".format(
                    #     event.parameter_dict["source"].name,
                    #     event.parameter_dict["source"].id,
                    #     event.parameter_dict["dest"]
                    # ))
            except:
                # print("An Error appears while handling Move event..")
                pass

class HealListener(EventListener):
    def deal_event(self,event):
        if event.name == "Heal":
            try:
                if event.parameter_dict["target"] == self.host:
                    if self.host.hp < self.host.max_hp:
                        self.host.hp += event.parameter_dict["heal"]
                        self.host.hp = min(self.host.hp, self.host.max_hp)
                        # print("Heal {} HP on {} (ID: {})".format(
                        #     event.parameter_dict["heal"],self.host.name,self.host.id
                        # ))
            except:
                # print("An Error appears while handling Heal event..")
                pass

class PriestHealListener(EventListener):
    def deal_event(self,event):
        if event.name == "TurnEnd":
            try:
                for unit in self.host.state_system.map.unit_list:
                    if calculator.cube_distance(unit.pos,self.host.pos) <= 2 and unit.camp == self.host.camp:
                        self.host.emit(Event("Heal",{
                            "source": self.host,
                            "target": unit,
                            "heal": 1
                        },-3))
            except:
                # print("An Error appears while handling PriestHeal event..")
                pass

class PriestAtkListener(EventListener):
    def deal_event(self,event):
        if event.name == "UpdateRingBuff":
            try:
                # Add buff
                for unit in self.host.state_system.map.unit_list:
                    if calculator.cube_distance(unit.pos,self.host.pos) <= 1 and unit.camp == self.host.camp:
                        if not unit in self.host.priest_buff_list:
                            new_buff = PriestAtkBuff(self.host.state_system)
                            new_buff.add_on(unit)
                            self.host.priest_buff_list.append(new_buff)
                # Delete Buff
                for buff in self.host.priest_buff_list:
                    if calculator.cube_distance(buff.host.pos,self.host.pos) > 1:
                        buff.delete()
                        self.host.priest_buff_list.remove(buff)
            except:
                # print("An Error appears while handling PriestAtk event..")
                pass
        if event.name == "Death":
            try:
                if event.parameter_dict["source"] == self.host:
                    for buff in self.host.priest_buff_list:
                        buff.delete()
            except:
                # print("An Error appears while handling ??? event..")
                pass


class VolcanoDragonAtkListener(EventListener):
    def deal_event(self,event):
        if event.name == "Attacked":
            try:
                if event.parameter_dict["source"] == self.host and\
                    event.parameter_dict["target"].type != "Miracle":
                    for unit in self.host.state_system.map.unit_list:
                        if (calculator.cube_distance(unit.pos,self.host.pos) == 2 or
                            calculator.cube_distance(unit.pos,event.parameter_dict["target"].pos) == 1) and \
                            unit.camp != self.host.camp:
                            self.host.emit(Event("Damage",{
                                "source": self.host,
                                "target": unit,
                                "damage": self.host.level + 2
                            },priority=-1))
            except:
                # print("An Error appears while handling VolcanoDragonAtk event..")
                pass
                