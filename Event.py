class Event:
    def __init__(self,name,parameter_dict = {},priority = 0):
        self.name = name
        self.priority = priority
        self.parameter_dict = parameter_dict

    def __lt__(self,other):
        return self.priority < other.priority

    def __str__(self):
        return '''Event: {}
    Priority: {}
    Parameters: {}'''.format(self.name,self.priority,self.parameter_dict)