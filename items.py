class Entity:
    def render(self, coords, room):
        raise Exception("TODO")


class Wall(Entity):
    def render(self, coords, room):
        left = isinstance(room.get([coords[0] - 1, coords[1]]), Wall)
        right = isinstance(room.get([coords[0] + 1, coords[1]]), Wall)
        top = isinstance(room.get([coords[0], coords[1] + 1]), Wall)
        bottom = isinstance(room.get([coords[0], coords[1] - 1]), Wall)
        if left:
            if bottom:
                return "─┘"
            if top:
                return "─┐"
        if right:
            if bottom:
                return "└"
            if top:
                return "┌"
        if left or right:
            return "──"
        return "|"


class PCInventory(Entity):
    def __init__(self):
        pass


class HealthPack(Entity):
    def __init__(self):
        pass

    def rm_consequence(self, consequence):
        if len(consequence) > 0:
            consequence.pop(0)
            # TODO: remove from inventory


class Crowbar(Entity):
    def __init__(self):
        pass


class Box(Entity):
    def render(self, coords, room):
        return "X"


inventory = []


class Door(Wall):
    def render(self, coords, room):
        left = isinstance(room.get([coords[0] - 1, coords[1]]), Wall)
        right = isinstance(room.get([coords[0] + 1, coords[1]]), Wall)
        if left or right:
            return "||"
        return "="
