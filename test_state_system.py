from StateSystem.StateSystem import StateSystem
from StateSystem.Event import Event

if __name__ == "__main__":
    sys=StateSystem()
    sys.emit(Event("Refresh",{"camp":0}))
    sys.start_event_processing()
    sys.emit(Event("Summon",{"type":"Archer","level":1,"pos":(0,0,0),"camp":0}))
    sys.start_event_processing()
    sys.emit(Event("Summon",{"type":"Archer","level":1,"pos":(-2,0,2),"camp":1}))
    sys.start_event_processing()
    a=sys.map.get_unit_at((0,0,0))
    b=sys.map.get_unit_at((-2,0,2))
    # sys.emit(Event("Attack",{"source":a,"target":b}))
    sys.emit(Event("CheckDeath",{},4))
    sys.start_event_processing()
    sys.emit(Event("Refresh",{"camp":0}))
    sys.start_event_processing()
    print(sys.parse())
    print("----------------")
    sys.emit(Event("CheckBarrack"))
    sys.start_event_processing()
    print(sys.parse())
    print("----------------")

