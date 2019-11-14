'''
Definition of unit classes
'''

UNIT_ID = 0

class Unit:
    def __init__(self,camp,name,cost,atk,max_hp,atk_range,max_move,cool_down,pos,state_system):
        global UNIT_ID
        self.id = UNIT_ID
        UNIT_ID += 1
        self.camp = camp
        self.name = name
        self.cost = cost
        self.atk = atk
        self.max_hp = max_hp
        self.hp = max_hp
        self.atk_range = atk_range
        self.max_move = max_move
        self.cool_down = cool_down
        self.pos = pos
        self.state_system = state_system
        self.event_listener_list = []

    def __str__(self):
        return '''{}
    ID: {}
    Camp: {}
    Cost: {}
    Atk: {}
    HP: {}/{}
    Atk Range: {}
    Max Move: {}
    Cool Down:{}
    Pos: {}'''.format(
                self.name,
                self.id,
                self.camp,
                self.cost,
                self.atk,
                self.hp,
                self.max_hp,
                self.atk_range,
                self.max_move,
                self.cool_down,
                self.pos
            )

    def add_event_listener(self,listener):
        listener.host = self
        self.event_listener_list.append(listener)

    def deal_event(self,event):
        for listener in self.event_listener_list:
            listener.deal_event(event)

    def emit(self,event):
        self.state_system.emit(event)

class Archer(Unit):
    def __init__(self,camp,level,pos,state_system):
        name = "Archer"
        cost = [2,4,6]
        atk = [1,2,3]
        hp = [1,3,5]
        atk_range = (2,4)
        max_move = 3
        cool_down = 4
        Unit.__init__(
            self,
            camp,
            name + " (Level " + str(level) + ")",
            cost[level-1],
            atk[level-1],
            hp[level-1],
            atk_range,
            max_move,
            cool_down,
            pos,
            state_system
        )