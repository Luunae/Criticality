class Thing:
    def render(self, coords, room):
        raise Exception("TODO")


class Wall(Thing):
    def render(self, coords, room):
        return "|"


class PCInventory(Thing):
    def __init__(self):
        pass


class HealthPack(Thing):
    def rm_consequence(self, consequence):
        if len(consequence) > 0:
            consequence.pop(0)
            # TODO: remove from inventory


class Box(Thing):
    def render(self, coords, room):
        return "X"
    inventory = []
