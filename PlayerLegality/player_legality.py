#!/usr/bin/python
# -*- coding:utf-8 -*-

'''
    player legality check api
'''
from operation import *

def parse(operation):
    '''
        parse operation, check legality and emit responding event
    '''
    #create operation object
    operation_object = to_object(operation)
    if operation_object == None:
        #return error message
        return ""
    if operation_object.check_legality:
        #emit responding event
        print("emit")
    else:
        #return error message
        print("error")

def to_object(operation_json):
    '''
    convert JSON to corresponding operation object
    '''
    try:
        operation_type = operation_json["operation_type"].lower()
        player_id = operation_json["player"]
        params = operation_json["operation_parameters"]
        if operation_type == "forbid":
            operation_object = Forbid(player_id, params)
        return operation_object
    except KeyError as e:
        print(e)

if __name__ == "__main__":
    example = {
            "player": 1,
            "operation_type": "Forbid",
            "operation_parameters":{
                }
            }
    parse(example)
