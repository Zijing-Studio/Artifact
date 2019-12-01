from .Event import Event
from Geometry import calculator

class EventListener:
    def __init__(self):
        self.host = None # where listener is

    def deal_event(self,event):
        pass

class DamageListener(EventListener):
    def deal_event(self,event):
        if event.name == "Damage":
            try:
                if event.parameter_dict["target"] == self.host:
                    self.host.hp -= event.parameter_dict["damage"]
                    print("Deal {} damage on {} (ID: {})".format(
                        event.parameter_dict["damage"],self.host.name,self.host.id
                    ))
            except:
                print("Parameter Dict Error.")

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
                    print("{} (ID: {}) attacks {} (ID: {})".format(
                        event.parameter_dict["source"].name,
                        event.parameter_dict["source"].id,
                        event.parameter_dict["target"].name,
                        event.parameter_dict["target"].id
                    ))
            except:
                print("Parameter Dict Error.")

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
                        print("{} (ID: {}) attacks back on {} (ID: {})".format(
                            event.parameter_dict["target"].name,
                            event.parameter_dict["target"].id,
                            event.parameter_dict["source"].name,
                            event.parameter_dict["source"].id
                        ))
            except:
                print("Parameter Dict Error.")

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
                    print("{} (ID: {}) moves to {}".format(
                        event.parameter_dict["source"].name,
                        event.parameter_dict["source"].id,
                        event.parameter_dict["dest"]
                    ))
            except:
                print("Parameter Dict Error.")
