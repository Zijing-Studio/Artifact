#!/usr/bin/python
# -*- coding:utf-8 -*-
'''
classes of operations
'''

from . import calculator
from Event import Event

class AbstractOperation:
    '''
    base class of all operations
    '''
    def __init__(self, _id, _map):
        self.player_id = _id
        self.map = _map
        self.player = _map.get_player_by_id(_id)

    def check_legality(self):
        '''
        check legality of this operation
        '''

    def act(self):
        '''
        emit action event after legality check
        '''
    def unit_conflict(self, unit, pos):
        '''
        judge if unit will conflict with another unit
        '''
        target = self.map.get_unit_at(pos)
        result = True
        if target is None or unit.flying != target.flying:
            result = False
        return result

class Forbid(AbstractOperation):
    '''
    operation of forbiding artifact and so on
    '''
    def __init__(self, _id, _map, _params):
        AbstractOperation.__init__(self, _id, _map)
        self.name = "Forbid"
        self.type = _params["type"]
        self.target = _params["target"]

    def check_legality(self):
        return True

    def act(self):
        pass

class Select(AbstractOperation):
    '''
    operation of selecting artifact and so on
    '''
    def __init__(self, _id, _map,  _params):
        AbstractOperation.__init__(self, _id, _map)
        self.name = "Select"
        self.type = _params["type"]
        self.target = _params["target"]

    def check_legality(self):
        return True

    def act(self):
        pass

class Summon(AbstractOperation):
    '''
    summon creature
    '''
    def __init__(self, _id, _map, _params):
        AbstractOperation.__init__(self, _id, _map)
        self.name = "Summon"
        self.type = _params["type"]
        self.star = _params["star"]
        self.position = tuple(_params["position"])

    def check_legality(self):
        result = True
        #if self.position not in self.map.get_barracks(self.player_id):
        #    result = "No barrack at the point"
        if self.unit_conflict(self.type, self.position):
            result = "Unit conflict"
        #elif not self.player.check_unit_cost(self.type, self.star):
        #    result = "Unit cost too high"
        #elif not self.player.check_magic_cost(self.type, self.star):
        #    result = "Magic cost too high"
        return result

    def act(self):
        self.map.emit(
            Event("Summon", {
                "type": self.type,
                "level": self.star,
                "pos": self.position,
                "camp": self.player_id
            }))
        self.map.start_event_processing()

class Move(AbstractOperation):
    '''
    move creature
    '''
    def __init__(self, _id, _map, _params):
        AbstractOperation.__init__(self, _id, _map)
        self.name = "Move"
        self.mover = self.map.get_unit_by_id(_params["mover"])
        self.position = tuple(_params["position"])

    def check_legality(self):
        result = True
        path = calculator.path(self.mover, self.position, self.map)
        if self.unit_conflict(self.mover, self.position):
            result = "Unit conflict: target: {}".format(self.position)
        elif not path:
            result = "No suitable path"
        elif self.mover.max_move < len(path)-1: # path include start point, so len need -1
            result = "Out of reach: max move: {}, shortest path: {}".format(self.mover.max_move, path)
        #elif self.mover.create_round == self.map.round:
        #    result = "Just summoned"
        #elif self.mover.has_acted():
        #    result = "Has acted this round"
        if result is not True:
            result = "start: {}, end: {}\n".format(self.mover.pos, self.position) + result
        return result

    def act(self):
        self.map.emit(
            Event("Move", {
                "source": self.mover,
                "dest": self.position
                }))
        self.map.start_event_processing()

class Attack(AbstractOperation):
    '''
    attack operation
    '''
    def __init__(self, _id, _map, _params):
        AbstractOperation.__init__(self, _id, _map)
        self.name = "Attack"
        self.attacker = self.map.get_unit_by_id(_params["attacker"])
        self.target = self.map.get_unit_by_id(_params["target"])

    def check_legality(self):
        result = True
        dist = calculator.cube_distance(self.attacker.pos, self.target.pos)
        if self.attacker.atk <= 0:
            result = "Attack below zero"
        #elif self.create_round == self.map.round:
        #    result = "Summoned this round"
        #elif self.attacker.has_acted:
        #    result = "Has acted"
        elif not self.attacker.atk_range[0] <= dist <= self.attacker.atk_range[-1]:
            result = "Out of range:\nattack range: {}, target distance: {}"\
                    .format(self.attacker.atk_range, dist)
        elif self.target.pos[-1] == 1 and self.attacker.pos[-1] == 0:
            result = "Cannot reach unit in sky"
        if result is not True:
            result += "\nattacker: {}\n, target: {}"\
                .format(self.attacker, self.target)
        return result

    def act(self):
        self.map.emit(
            Event("Attack", {
                "source": self.attacker,
                "target": self.target
                }))
        self.map.start_event_processing()

class Use(AbstractOperation):
    '''
    use artifact or trap card
    '''
    def __init__(self, _id, _map, _params):
        AbstractOperation.__init__(self, _id, _map)
        self.name = "Use"
        self.type = _params["type"]
        self.card = _params["card"]
        self.target = _params["target"]

    def check_legality(self):
        return True

    def act(self):
        pass
