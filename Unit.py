'''
Definition of unit classes
'''

class Unit:
    def __init__(self,cost,atk,hp,atk_range,max_move,cool_down):
        self.cost = cost
        self.atk = atk
        self.hp = hp
        self.atk_range = atk_range
        self.max_move = max_move
        self.cool_down = cool_down
        self.event_listener_list = []

    def add_event_listener(self,listener):
        self.event_listener_list.append(listener)

    def deal_event(self,event):
        for listener in self.event_listener_list:
            listener.deal_event(event)