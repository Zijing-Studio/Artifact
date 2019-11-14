from Event import Event

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
                    self.host.emit(Event("Attacked",event.parameter_dict))
                    self.host.emit(Event("Damage",{
                        "target": event.parameter_dict["target"],
                        "damage": event.parameter_dict["source"].atk
                    }))
                    self.host.emit(Event("Damage",{
                        "target": event.parameter_dict["source"],
                        "damage": event.parameter_dict["target"].atk
                    }))
                    print("{} (ID: {}) attacks {} (ID: {})".format(
                        event.parameter_dict["source"].name,
                        event.parameter_dict["source"].id,
                        event.parameter_dict["target"].name,
                        event.parameter_dict["target"].id
                    ))
            except:
                print("Parameter Dict Error.")