#!/usr/bin/python
# -*- coding:utf-8 -*-

'''
    player legality check api
'''
from . import operation
from StateSystem import StateSystem

class Parser:
    '''
    class of parser
    '''
    def __init__(self):
        self.map = StateSystem()
        
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
        if legality == True:
            #emit responding event
            print("emit " + operation_object.name)
            operation_object.act()
        else:
            #return error message
            print("error " + operation_object.name + str(legality))
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
                operation_object = operation.Forbid(player_id, self.map, params)
            elif operation_type == "select":
                operation_object = operation.Select(player_id, self.map, params)
            elif operation_type == "summon":
                operation_object = operation.Summon(player_id, self.map, params)
            elif operation_type == "move":
                operation_object = operation.Move(player_id, self.map, params)
            elif operation_type == "attack":
                operation_object = operation.Attack(player_id, self.map, params)
            elif operation_type == "use":
                operation_object = operation.Use(player_id, self.map, params)
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
    instance = Parser()
    instance.parse(example)
