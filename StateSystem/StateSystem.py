from .EventHeap import EventHeap
from .Event import Event
from .EventListener import EventListener
from .Unit import *
from .Map import *
from .Player import *

class StateSystem:
    def __init__(self):
        self.map = Map()
        self.event_heap = EventHeap()
        self.player_list = [Player(0,1,self),Player(1,2,self)]
        self.event_listener_list = []

        self.add_event_listener(SummonListener())
        self.add_event_listener(CheckDeathListener())

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
        # Check Death
        new_unit_list = []
        for unit in self.map.unit_list:
            if not unit.death_flag:
                new_unit_list.append(unit)
        self.map.unit_list = new_unit_list

    def parse(self):
        return {
            "map": self.map.parse(),
            "players": [player.parse() for player in self.player_list]
        }

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

class CheckDeathListener(EventListener):
    '''
    Only State System register this listener
    '''
    def deal_event(self,event):
        if event.name == "CheckDeath":
            try:
                for unit in self.host.map.unit_list:
                    if unit.hp <= 0 and not unit.death_flag:
                        unit.death_flag = True
                        self.host.emit(Event("Death", {
                            "source": unit
                        }))
                        print("{} (ID: {}) is announced to be dead.".format(
                            unit.name,
                            unit.id
                        ))
            except:
                print("Parameter Dict Error.")
