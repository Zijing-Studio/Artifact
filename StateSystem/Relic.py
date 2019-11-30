from StateSystem.EventListener import DamageListener

class Relic:
    def __init__(self,camp,hp,pos,state_system):
        self.name = "Relic (belongs to Player {})".format(camp)
        self.id = camp
        self.max_hp = hp
        self.hp = hp
        self.camp = camp
        self.pos = pos
        self.state_system = state_system
        self.event_listener_list = []

        self.add_event_listener(DamageListener())

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
            "camp": self.camp,
            "max_hp": self.max_hp,
            "hp": self.hp,
            "pos": self.pos,
            "name": self.name,
            "id": self.id
        }