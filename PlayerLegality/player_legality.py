#!/usr/bin/python
# -*- coding:utf-8 -*-

'''
    player legality check api
'''
from . import operations

class Parser:
    '''
    class of parser
    '''
    def __init__(self, _map):
        self.map = _map
        self.summoned = []
        self.moved = []
        self.attacked = []
        self.round = 0

    def set_round(self, _round):
        '''
        update round
        '''
        self.summoned = []
        self.moved = []
        self.attacked = []
        self.round = _round

    def parse(self, operation):
        '''
            parse operation, check legality and emit responding event
        '''
        #create operation object
        operation_object = self.to_object(operation)
        if isinstance(operation_object, BaseException):
            #return error message
            print(operation_object)
            return operation_object
        legality = operation_object.check_legality()
        if legality is True:
            #emit responding event
            print("emit " + operation_object.name)
            operation_object.act()
            return "OK"
        else:
            #return error message
            print("emit " + operation_object.name + " error: " + str(legality))
            return legality

    def to_object(self, operation_json):
        '''
        convert JSON to corresponding operation object
        '''
        try:
            operation_type = operation_json["operation_type"].lower()
            player_id = int(operation_json["player"])
            params = operation_json["operation_parameters"]
            if operation_type == "forbid":
                operation_object = operations.Forbid(player_id, self.map, params)
            elif operation_type == "select":
                operation_object = operations.Select(player_id, self.map, params)
            elif operation_type == "summon":
                operation_object = operations.Summon(player_id, self.map, params)
            elif operation_type == "move":
                operation_object = operations.Move(player_id, self.map, params)
            elif operation_type == "attack":
                operation_object = operations.Attack(player_id, self.map, params)
            elif operation_type == "use":
                operation_object = operations.Use(player_id, self.map, params)
            return operation_object
        except KeyError as error:
            return KeyError("KeyError: " + str(error))
        except ValueError as error:
            return ValueError("ValueError: " + str(error).split(':')[-1])

if __name__ == "__main__":
    example = {
        "player": "fuck",
        "operation_type": "Forbid",
        "operation_parameters":{
            }
        }
