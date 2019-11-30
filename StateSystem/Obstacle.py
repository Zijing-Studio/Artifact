class Obstacle:
    def __init__(self,name,pos):
        self.type = name
        self.pos = pos
        self.allow_flying = name == "Abyss"

    def parse(self):
        return {
            "type": self.type,
            "pos": self.pos,
            "allow_flying": self.allow_flying
        }

ABYSS_INIT_LIST = [
]