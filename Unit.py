'''
Definition of unit classes
'''

class Unit:
    def __init__(self,cost,atk,max_hp,atk_range,max_move,cool_down,pos,state_system):
        self.cost = cost
        self.atk = atk
        self.max_hp = max_hp
        self.hp = max_hp
        self.atk_range = atk_range
        self.max_move = max_move
        self.cool_down = cool_down
        self.pos = pos
        self.state_system = state_system
        self.event_listener_list = []

    def add_event_listener(self,listener):
        self.event_listener_list.append(listener)

    def deal_event(self,event):
        for listener in self.event_listener_list:
            listener.deal_event(event)

    def emit(self,event):
        self.state_system.emit(event)
