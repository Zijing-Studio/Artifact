class Player:
    def __init__(self,camp,state_system):
        self.camp = camp
        self.artifact_list = []
        self.creature_list = []
        self.max_mana = 0
        self.mana = 0
        self.state_system = state_system
        self.event_listener_list = []
    
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
            "max_mana": self.max_mana
        }