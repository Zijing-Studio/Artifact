from StateSystem.StateSystem import StateSystem
from StateSystem.Event import Event

if __name__ == "__main__":
    sys=StateSystem()
    sys.emit(Event("Refresh",{"camp":0}))
    sys.start_event_processing()
    sys.emit(Event("Summon",{"type":"VolcanoDragon","level":1,"pos":(0,0,0),"camp":1}))
    sys.start_event_processing()
    sys.emit(Event("Summon",{"type":"Priest","level":1,"pos":(0,1,-1),"camp":0}))
    sys.emit(Event("Summon",{"type":"Priest","level":1,"pos":(0,-2,2),"camp":0}))
    sys.emit(Event("Summon",{"type":"Priest","level":1,"pos":(0,0,0),"camp":0}))
    sys.emit(Event("UpdateRingBuff",priority=3))
    sys.start_event_processing()
    a=sys.map.get_unit_at((0,0,0),True)
    b=sys.map.get_unit_at((0,1,-1),False)
    # sys.emit(Event("Attack",{"source":a,"target":b}))
    sys.emit(Event("ActivateArtifact",{
        "camp": 0,
        "name": "HolyLight",
        "target": (0,1,-1)
    }))
    sys.start_event_processing()
    print("----------------")
    print(b)
    sys.emit(Event("TurnEnd",{"camp":0}))
    sys.start_event_processing()
    print("----------------")
    print(b)
    print("----------------")

