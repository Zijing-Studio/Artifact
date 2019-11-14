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
        self.event_listener_list = []

        self.add_event_listener(SummonListener())

    def add_event_listener(self,listener):
        listener.host = self
        self.event_listener_list.append(listener)

    def deal_event(self,event):
        for listener in self.event_listener_list:
            listener.deal_event(event)

    def emit(self,event):
        self.event_heap.append(event)

    def start_event_processing(self):
        while self.event_heap.len():
            current_event = self.event_heap.pop()
            self.deal_event(current_event)
            for player in self.player_list:
                player.deal_event(current_event)
            for unit in self.map.unit_list:
                unit.deal_event(current_event)

    def get_map(self):
        return self.map

    def get_units(self):
        return self.map.unit_list
    
    def get_unit_at(self,pos):
        return self.map.get_unit_at(pos)

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

class SummonListener(EventListener):
    '''
    Only State System register this listener
    '''
    def deal_event(self,event):
        if event.name == "Summon":
            try:
                unit = None
                if event.parameter_dict["type"] == "Archer":
                    unit = Archer(
                        event.parameter_dict["camp"],
                        event.parameter_dict["level"],
                        event.parameter_dict["pos"],
                        self.host
                    )
                if unit:
                    self.host.map.add_unit(unit)
                    self.host.emit(Event("Spawn",{
                        "source": unit,
                        "pos": unit.pos
                    }))
                    print("{} (ID: {}) spawns at {}".format(
                        unit.name,
                        unit.id,
                        unit.pos
                    ))
            except:
                print("Parameter Dict Error.")

if __name__ == "__main__":
    sys=StateSystem()
    sys.emit(Event("Summon",{"type":"Archer","level":3,"pos":0,"camp":0}))
    sys.start_event_processing()
    sys.emit(Event("Summon",{"type":"Archer","level":3,"pos":1,"camp":1}))
    sys.start_event_processing()
    a=sys.map.get_unit_at(0)
    b=sys.map.get_unit_at(1)
    sys.emit(Event("Attack",{"source":a,"target":b}))
    sys.start_event_processing()
    sys.emit(Event("Move",{"source":a,"dest":2}))
    sys.start_event_processing()
    for item in sys.event_heap.record:
        print(item)
    print(b)