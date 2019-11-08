#!/usr/bin/python
# -*- coding:utf-8 -*-
'''
classes of operations
'''

class AbstractOperation:
    '''
    base class of all operations
    '''
    def __init__(self, _id):
        self.player_id = _id

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
    def __init__(self, _id, _params):
        AbstractOperation.__init__(self, _id)
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
    def __init__(self, _id, _params):
        AbstractOperation.__init__(self, _id)
        self.type = _params["type"]
        self.target = _params["target"]

    def check_legality(self):
        return True

    def act(self):
        pass
