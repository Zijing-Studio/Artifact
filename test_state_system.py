from StateSystem.StateSystem import StateSystem
from StateSystem.Event import Event

if __name__ == "__main__":
    sys=StateSystem()
    print(sys.get_summon_pos_list(0))
    sys.emit(Event("GameStart",{
        "camp": 0,
        "cards": {
            "artifacts": ["SalamanderShield", "InfernoFlame"],
            "creatures": ["BlackBat", "Priest", "VolcanoDragon"]
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
    sys.emit(Event("Summon",{"type":"VolcanoDragon","level":1,"pos":(0,0,0),"camp":0}))
    sys.start_event_processing()
    sys.emit(Event("Summon",{"type":"BlackBat","level":1,"pos":(0,1,-1),"camp":0}))
    sys.start_event_processing()
    a=sys.map.get_unit_at((0,0,0))
    b=sys.map.miracle_list[1]
    sys.emit(Event("TurnEnd"))
    sys.start_event_processing()
    sys.emit(Event("TurnStart"))
    sys.start_event_processing()
    print(sys.current_player_id)
    print(a)
    sys.emit(Event("Attack",{
        "source": a,
        "target": b
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
    print(a)
    sys.emit(Event("TurnEnd"))
    sys.start_event_processing()
    # print(sys.parse())
    print("----------------")

