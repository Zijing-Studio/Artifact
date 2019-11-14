#!/usr/bin/python
# -*- coding:utf-8 -*-
'''
classes of operations
'''

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

class Forbid(AbstractOperation):
    '''
    operation of forbiding artifact and so on
    '''
    def __init__(self, _id, _map, _params):
        AbstractOperation.__init__(self, _id, _map)
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
        self.type = _params["type"]
        self.star = _params["star"]
        self.position = calculator.to_xy(_params["position"])

    def check_legality(self):
        result = True
        if self.position not in self.map.getBarracks(self.player_id):
            result = "No barrack at the point"
        elif self.map.unit_conflict(self.type, self.position):
            result = "Unit conflict"
        elif not self.player.check_unit_cost(self.type, self.star):
            result = "Unit cost too high"
        elif not self.player.check_magic_cost(self.type, self.star):
            result = "Magic cost too high"
        return result

    def act(self):
        self.map.emit("summon", self.type, self.star, self.position)

class Move(AbstractOperation):
    '''
    move creature
    '''
    def __init__(self, _id, _map, _params):
        AbstractOperation.__init__(self, _id, _map)
        self.mover = self.map.get_unit_by_id(_params["mover"])
        self.position = calculator.to_xy(_params["position"])

    def check_legality(self):
        result = True
        path = self.map.path(self.mover, self.position)
        if self.map.unit_conflict(self.mover, self.position):
            result = "Unit conflict"
        elif not path:
            result = "No suitable path"
        elif self.mover.max_move <= len(path):
            result = "Out of reach"
        elif self.mover.create_round == self.map.round:
            result = "Just summoned"
        elif 

    def act(self):
        self.map.emit()

class Attack(AbstractOperation):
    '''
    attack operation
    '''
    def __init__(self, _id, _map, _params):
        AbstractOperation.__init__(self, _id, _map)
        self.attacker = _params["attacker"]
        self.target = _params["target"]

    def check_legality(self):
        return True
    
    def act(self):
        pass

class Use(AbstractOperation):
    '''
    use artifact or trap card
    '''
    def __init__(self, _id, _map, _params):
        AbstractOperation.__init__(self, _id, _map)
        self.type = _params["type"]
        self.card = _params["card"]
        self.target = _params["target"]

    def check_legality(self):
        return True

    def act(self):
        pass
