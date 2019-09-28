from typing import List
import npyscreen

import forms
import reactor


class Entity:
    def __init__(self):
        self.traversable = True

    def render(self, coords, room):
        raise Exception("TODO")

    def interact(self, game, coords, room):
        pass


class Wall(Entity):
    def __init__(self):
        super().__init__()
        self.traversable = False

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


class RightWall(Wall):
    def render(self, coords, room):
        left = isinstance(room.get([coords[0] - 1, coords[1]]), Wall)
        right = isinstance(room.get([coords[0] + 1, coords[1]]), Wall)
        top = isinstance(room.get([coords[0], coords[1] + 1]), Wall)
        bottom = isinstance(room.get([coords[0], coords[1] - 1]), Wall)
        if left:
            if bottom:
                return "┘ "
            if top:
                return "┐ "
        if right:
            if bottom:
                return "└"
            if top:
                return "┌"
        if left or right:
            return "──"
        return "| "


class HealthPack(Entity):
    def __init__(self):
        super().__init__()
        self.name = "Health Pack"

    def use_item(self, game):
        if len(game.hp.consequences) > 0:
            game.hp.consequences.pop(0)
        game.inv.remove(self)
        npyscreen.notify_confirm("Removed a consequence!", editw=1)


class Crowbar(Entity):
    def __init__(self):
        super().__init__()
        self.name = "Crowbar"


class Box(Entity):
    def __init__(self):
        super().__init__()
        self.inv = []

    def render(self, coords, room):
        return "[]"

    def interact(self, game, coords, room):
        from menus import create_box_menu

        game.popup_menu(create_box_menu(game, self))


class DunkPanel(Entity):
    def render(self, coords, room):
        return "$$"

    def interact(self, game, coords, room):
        form = npyscreen.Form(name="Dunk Panel")
        forms.add_standard_handlers(form)
        temp = form.add_widget(
            npyscreen.Slider, out_of=10, step=1, lowest=1, label=True, name="Dunk Slider",
            value=int(game.reactor.d_change)
        )
        form.edit()
        game.reactor.d_change = temp.value
        # TODO: hook up with game.reactor things? more widgets?
        # TODO: redraw status window after editing Dunk Panel.


class VentPanel(Entity):
    def render(self, coords, room):
        return "$$"

    def interact(self, game, coords, room):
        def vent_max():
            game.reactor.v_change = 10
            npyscreen.notify_confirm("You hear a loud wind in the ductwork above you.", title="Vent", editw=1)
            form.editing = False

        form = npyscreen.Form(name="Vent Panel")
        forms.add_standard_handlers(form)
        reactor.v_change = form.add_widget(npyscreen.ButtonPress, when_pressed_function=vent_max, name="Vent")
        form.edit()
        # TODO: hook up with game.reactor things? more widgets?
        # TODO: redraw status window after editing Vent Panel.


class ReactorPart(Entity):
    def render(self, coords, room):
        return "↑↑"

    def interact(self, game, coords, room):
        npyscreen.notify_confirm(f"The reactor glows ominously.\nCurrent temperature: {game.reactor.temp}", editw=1)


class Door(Entity):
    target_coords: List[int]
    target_room: "Room"

    def __init__(self):
        super().__init__()
        self.target_coords = []
        self.target_room = None

    def interact(self, game, coords, room):
        game.active_room = self.target_room
        game.player_coords = self.target_coords

        from exceptions import DummyException

        raise DummyException()

    def render(self, coords, room):
        left = isinstance(room.get([coords[0] - 1, coords[1]]), Wall)
        right = isinstance(room.get([coords[0] + 1, coords[1]]), Wall)
        if left or right:
            return "||"
        return "="
