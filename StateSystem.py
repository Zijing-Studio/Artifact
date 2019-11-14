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
        self.player_list = [Player(0,self),Player(1,self)]

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

    def get_unit_by_id(self,id):
        return self.map.get_unit_by_id(id)

    def get_player_by_id(self,id):
        for player in self.player_list:
            if player.camp == id:
                return player
        return None

    def get_barracks(self,player_camp):
        return [barrack
            for barrack in self.map.barrack_list
            if barrack.camp == player_camp]

    def get_obstacles(self):
        return self.map.obstacle_list

    def get_relic_by_id(self,player_camp):
        return self.map.get_relic_by_id(player_camp)

if __name__ == "__main__":
    sys=StateSystem()
    a=Archer(1,3,0,sys)
    b=Archer(0,3,1,sys)
    sys.map.add_unit(a)
    sys.map.add_unit(b)
    sys.emit(Event("Attack",{"source":a,"target":b}))
    sys.start_event_processing()
    print(b)