from StateSystem.Event import Event

class Buff:
    def __init__(self,state_system):
        self.state_system = state_system
        self.event_listener_list = []
        self.host = None
    
    def add_event_listener(self,listener):
        listener.host = self
        self.event_listener_list.append(listener)

    def deal_event(self,event):
        for listener in self.event_listener_list:
            listener.deal_event(event)

    def emit(self,event):
        self.state_system.emit(event)

    def buff(self):
        pass

    def debuff(self):
        pass

    def add_on(self,host):
        # host is a unit
        self.host = host
        host.buff_list.append(self)
        self.state_system.emit(Event("BuffAdd",{
            "source": self.host
        }))
        self.buff()

    def delete(self):
        self.host.buff_list.remove(self)
        self.state_system.emit(Event("BuffRemove",{
            "source": self.host
        }))
        self.debuff()
        self.host = None
        self.event_listener_list = []

class PriestAtkBuff(Buff):
    def buff(self):
        self.host.atk += 1

    def debuff(self):
        self.host.atk -= 1
