from StateSystem.EventListener import DamageListener

class Miracle:
    def __init__(self,camp,hp,pos,summon_pos_list,state_system):
        self.name = "Miracle (belongs to Player {})".format(camp)
        self.id = camp
        self.max_hp = hp
        self.hp = hp
        self.camp = camp
        self.pos = pos
        self.summon_pos_list = summon_pos_list
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
            "summon_pos_list": self.summon_pos_list,
            "name": self.name,
            "id": self.id
        }