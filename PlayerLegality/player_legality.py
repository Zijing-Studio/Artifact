#!/usr/bin/python
# -*- coding:utf-8 -*-

'''
    player legality check api
'''

def parse(operation):
    '''
        parse operation, check legality and emit responding event
    '''
    #create operation object
    operation_object = toObject(operation)
    if operation_object.check_legality:
        #emit responding event
        print("emit")
    else:
        #return error message
        print("error")

def toObject(operation):
    print("to")
