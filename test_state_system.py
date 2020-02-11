from StateSystem.StateSystem import StateSystem
from StateSystem.Event import Event

if __name__ == "__main__":
    sys=StateSystem()
    print(sys.get_summon_pos_list(0))
    sys.emit(Event("GameStart",{
        "camp": 0,
        "cards": {
            "artifacts": ["SalamanderShield", "InfernoFlame"],
            "creatures": ["BlackBat", "Priest", "Archer"]
        }
    }))
    sys.emit(Event("GameStart",{
        "camp": 1,
        "cards": {
            "artifacts": ["SalamanderShield", "HolyLight"],
            "creatures": ["BlackBat", "Priest", "Archer"]
        }
    }))
    sys.start_event_processing()
    sys.emit(Event("Summon",{"type":"BlackBat","level":1,"pos":(0,0,0),"camp":1}))
    sys.start_event_processing()
    sys.emit(Event("Summon",{"type":"BlackBat","level":1,"pos":(0,1,-1),"camp":0}))
    sys.start_event_processing()
    a=sys.map.get_unit_at((0,0,0))
    b=sys.map.get_unit_at((0,1,-1))
    sys.emit(Event("ActivateArtifact",{
        "camp": 0,
        "name": "InfernoFlame",
        "target": (0,1,0)
    }))
    sys.start_event_processing()
    print(a)
    print("----------------")
    sys.emit(Event("TurnEnd"))
    sys.start_event_processing()
    print("----------------")
    # print(b)
    print(sys.parse())
    sys.emit(Event("TurnStart"))
    sys.start_event_processing()
    sys.emit(Event("TurnEnd"))
    sys.start_event_processing()
    # print(sys.parse())
    print("----------------")

