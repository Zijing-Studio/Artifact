from StateSystem.EventListener import EventListener
from StateSystem.CreatureCapacity import CreatureCapacity

class Player:
    def __init__(self,camp,mana,state_system):
        self.camp = camp
        self.artifact_list = []
        self.creature_capacity_list = []
        # Debug
        self.creature_capacity_list.append(CreatureCapacity("Archer"))    
        # Debug
        self.max_mana = mana
        self.mana = mana
        self.state_system = state_system
        self.event_listener_list = []

        self.add_event_listener(RefreshListener())
    
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
            "artifact": [artifact.parse() for artifact in self.artifact_list],
            "mana": self.mana,
            "max_mana": self.max_mana,
            "creature_capacity": [capacity.parse() for capacity in self.creature_capacity_list]
        }

class RefreshListener(EventListener):
    def deal_event(self,event):
        if event.name == "Refresh":
            if self.host.max_mana < 12:
                self.host.max_mana += 1
            self.host.mana = self.host.max_mana
            print("Player {} mana refreshed to {}".format(
                self.host.camp,
                self.host.mana
                ))