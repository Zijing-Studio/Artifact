class Relic:
    def __init__(self,camp,hp,pos):
        self.max_hp = hp
        self.hp = hp
        self.camp = camp
        self.pos = pos
    
    def parse(self):
        return {
            "camp": self.camp,
            "max_hp": self.max_hp,
            "hp": self.hp,
            "pos": self.pos
        }