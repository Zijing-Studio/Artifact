from StateSystem.StateSystem import StateSystem
from StateSystem.Event import Event

if __name__ == "__main__":
    sys=StateSystem()
    sys.emit(Event("Refresh",{"camp":0}))
    sys.start_event_processing()
    sys.emit(Event("Summon",{"type":"BlackBat","level":3,"pos":(0,0,0),"camp":0}))
    sys.start_event_processing()
    sys.emit(Event("Summon",{"type":"Swordman","level":1,"pos":(0,0,0),"camp":1}))
    sys.start_event_processing()
    a=sys.map.get_unit_at((0,0,0),True)
    b=sys.map.get_unit_at((0,0,0),False)
    sys.emit(Event("Attack",{"source":a,"target":b}))
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

