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