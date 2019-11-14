class Event:
    def __init__(self,name,priority = 0):
        self.name = name
        self.priority = priority

    def action(self,event_target):
        pass

    def __lt__(self,other):
        return self.priority < other.priority

    def __str__(self):
        return '''Event: {}
    Priority: {}'''
    
class DamageEvent(Event):
    def __init__(self,target,damage):
        Event.__init__(self,"Damage")
        self.target = target
        self.damage = damage

    def action(self,event_target):
        if event_target == self.target:
            event_target.hp -= self.damage