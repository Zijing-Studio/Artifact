from EventHeap import *
from Event import *
from EventListener import *
from Unit import *
from Map import *
from Player import *

class StateSystem:
    def __init__(self):
        self.map = Map()
        self.event_heap = EventHeap()
        self.player_list = [Player(0),Player(1)]

    def emit(self,event):
        self.event_heap.append(event)

    def start_event_processing(self):
        while self.event_heap.len():
            current_event = self.event_heap.pop()
            for unit in self.map.unit_list:
                unit.deal_event(current_event)

    def get_map(self):
        return self.map

    def get_units(self):
        return self.map.unit_list

if __name__ == "__main__":
    a=Archer(1,1,0,0)
    b=Archer(0,2,0,0)
    b.add_event_listener(DamageListener())
    sys=StateSystem()
    sys.map.add_unit(a)
    sys.map.add_unit(b)
    sys.emit(Event("Damage",{"target":b,"damage":1}))
    sys.start_event_processing()
    print(b)