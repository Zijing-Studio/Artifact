import heapq
import Event
import Unit
import EventListener

class EventHeap:
    def __init__(self):
        self.data = []
        self.record = []

    def append(self,item):
        heapq.heappush(self.data,item)

    def pop(self):
        poper = heapq.heappop(self.data)
        self.record.append(poper)
        return poper

    def len(self):
        return len(self.data)
