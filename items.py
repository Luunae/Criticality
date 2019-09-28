import curses

import npyscreen


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


class HealthPack(Entity):
    def __init__(self):
        self.name = "Health Pack"

    def use_item(self, game):
        if len(game.hp.consequences) > 0:
            game.hp.consequences.pop(0)
        game.inv.remove(self)
        npyscreen.notify_confirm("Removed a consequence!")


class Crowbar(Entity):
    def __init__(self):
        pass


class Box(Entity):
    def render(self, coords, room):
        return "XX"
    def interact(self):
        curses.beep()


class ReactorPart(Entity):
    def render(self, coords, room):
        return "↑↑"


class Door(Wall):
    def render(self, coords, room):
        left = isinstance(room.get([coords[0] - 1, coords[1]]), Wall)
        right = isinstance(room.get([coords[0] + 1, coords[1]]), Wall)
        if left or right:
            return "||"
        return "="
