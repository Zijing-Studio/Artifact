class EventListener:
    def __init__(self,name):
        self.host = None # where listener is
        self.name = name # event name

    def deal_event(self,event):
        if event.name == self.name:
            event.action(self.host)
