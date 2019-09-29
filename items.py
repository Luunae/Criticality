from typing import List, TYPE_CHECKING
import npyscreen
import math
import forms
import reactor

if TYPE_CHECKING:
    from game import Game
    from room import Room


class Entity:
    def __init__(self):
        self.traversable = True

    def render(self, coords, room):
        raise Exception("TODO")

    def interact(self, game, coords, room):
        pass

    def get_color(self):
        return "DEFAULT"

    def use_item(self, game):
        npyscreen.notify_confirm("OAK: There's a time and a place for everything! But not now.", editw=1)


class Wall(Entity):
    def __init__(self):
        super().__init__()
        self.traversable = False

    def render(self, coords, room):
        left = isinstance(room.get([coords[0] - 1, coords[1]]), Wall)
        right = isinstance(room.get([coords[0] + 1, coords[1]]), Wall)
        top = isinstance(room.get([coords[0], coords[1] + 1]), Wall)
        bottom = isinstance(room.get([coords[0], coords[1] - 1]), Wall)
        if left and right and top and bottom:
            return "┼"
        if left and right and top:
            return "─┬"
        if left and right and bottom:
            return "─┴"
        if left:
            if bottom and top:
                return "─┤"
            if bottom:
                return "─┘"
            if top:
                return "─┐"
        if right:
            if bottom and top:
                return "├"
            if bottom:
                return "└"
            if top:
                return "┌"
        if left or right:
            return "──"
        return "│"

    def get_color(self):
        return "NO_EDIT"


class RightWall(Wall):
    def render(self, coords, room):
        left = isinstance(room.get([coords[0] - 1, coords[1]]), Wall)
        right = isinstance(room.get([coords[0] + 1, coords[1]]), Wall)
        top = isinstance(room.get([coords[0], coords[1] + 1]), Wall)
        bottom = isinstance(room.get([coords[0], coords[1] - 1]), Wall)
        if left and right and top and bottom:
            return "┼"
        if top and bottom and left:
            return "┤ "
        if left and right and top:
            return "┬─"
        if left and right and bottom:
            return "┴─"
        if left:
            if bottom:
                return "┘ "
            if top:
                return "┐ "
        if right:
            if bottom:
                return "└ "
            if top:
                return "┌─"
        if left or right:
            return "──"
        return "│ "


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


class Note(Entity):
    INSTANCE_COUNT = 0

    def __init__(self):
        super().__init__()
        Note.INSTANCE_COUNT += 1
        self.name = f"Note {Note.INSTANCE_COUNT:02d}"
        self.text = ""
        self.description = ""


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
        form = npyscreen.Popup(name="Dunk Panel", color=self.get_color())
        forms.add_standard_handlers(form)
        temp = form.add_widget(
            npyscreen.Slider,
            out_of=10,
            step=1,
            lowest=1,
            label=True,
            name="Dunk Slider",
            value=int(game.reactor.d_change),
        )
        form.edit()
        game.reactor.d_change = temp.value
        # TODO: Make dunk NOT edit when escaping

    def get_color(self):
        return "CAUTION"


class VentPanel(Entity):
    def render(self, coords, room):
        return "$$"

    def interact(self, game, coords, room):
        def vent_max():
            game.reactor.v_change = 10
            npyscreen.notify_confirm("You hear a loud wind in the ductwork above you.\n"
                                     "(v_change = 10, Venting temporarily increased!)", title="Vent", editw=1)
            form.editing = False

        form = npyscreen.Popup(name="Vent Panel", color=self.get_color())
        forms.add_standard_handlers(form)
        reactor.v_change = form.add_widget(npyscreen.ButtonPress, when_pressed_function=vent_max, name="Vent")
        form.edit()
        # TODO: hook up with game.reactor things? more widgets?
        # TODO: redraw status window after editing Vent Panel.

    def get_color(self):
        return "LABEL"


class FluxPanel(Entity):
    def render(self, coords, room):
        return "$$"

    def interact(self, game, coords, room):
        def on_press():
            game.reactor.f_change = 0
            npyscreen.notify_confirm("TODO flavour text", title="Flux Moderator", editw=1)
            form.editing = False

        form = npyscreen.Popup(name="Flux Panel", color=self.get_color())
        forms.add_standard_handlers(form)
        form.add_widget(
            npyscreen.ButtonPress, when_pressed_function=on_press, name="Dump Boron Moderator (Reduce flux)"
        )
        form.edit()
        # TODO: hook up with game.reactor things? more widgets?
        # TODO: redraw status window after editing Flux Panel.

    def get_color(self):
        return "STANDOUT"


class ReactorPart(Entity):
    def render(self, coords, room):
        return "↑↑"

    def interact(self, game, coords, room):
        if game.reactor.thermal_dump == 0 and game.reactor.temp > 130:
            dump = npyscreen.notify_yes_no(
                f"The reactor glows ominously.\nCurrent temperature: {math.trunc(game.reactor.temp)}\nDo you want to engage the thermal dump?\n(1 use, -100 degrees)",
                editw=1,
            )
            if dump:
                game.reactor.temp -= 100
                game.reactor.thermal_dump = 1
        else:
            npyscreen.notify_confirm(
                f"The reactor glows ominously.\nCurrent temperature: {math.trunc(game.reactor.temp)}", editw=1
            )

    def get_color(self):
        return "STANDOUT"


class Door(Entity):
    target_coords: List[int]
    target_room: "Room"

    def __init__(self):
        super().__init__()
        self.target_coords = []
        self.target_room = None

    def interact(self, game, coords, room):
        game.set_room(self.target_room, self.target_coords)
        game.minor_action_time()

        from exceptions import DummyException

        raise DummyException()

    def render(self, coords, room):
        left = isinstance(room.get([coords[0] - 1, coords[1]]), Wall)
        right = isinstance(room.get([coords[0] + 1, coords[1]]), Wall)
        if left or right:
            return "||"
        if isinstance(room.get([coords[0], coords[1] + 1]), RightWall):
            return "= "
        return "="


class LockedDoor(Door):
    def interact(self, game: "Game", coords, room: "Room"):
        unlocked = False
        if not any([isinstance(x, Crowbar) for x in game.inv]):
            npyscreen.notify_confirm("This door is locked. Enter the key to open it", editw=1)
            import menus

            unlocked = menus.key_lock("Security Door", [True, False, True, False, False, False, True, False, False])
            if not unlocked:
                npyscreen.notify_confirm("You can't open the door, the code is wrong.", editw=1)
                return

        if unlocked:
            npyscreen.notify_confirm("You unlock the door using the code", editw=1)
        else:
            npyscreen.notify_confirm("You pry the blocked door open using the Crowbar.", editw=1)
        idx = room.location_of(self)
        room.contents[idx[1]][idx[0]] = fixed_door = Door()
        fixed_door.target_coords = self.target_coords
        fixed_door.target_room = self.target_room

    def get_color(self):
        return "CAUTIONHL"


class ControlRod(Entity):
    def interact(self, game, coords, room):
        form = npyscreen.Popup(name="Control Rod", color=self.get_color(), lines=7)
        forms.add_standard_handlers(form)
        max_val = 100
        slider: npyscreen.Slider = form.add_widget(
            npyscreen.Slider, lowest=0, out_of=max_val, value=game.reactor.control_rod_depth * max_val, step=0.25, label="Control Rod"
        )
        old_inc = slider.h_increase

        def inc(ch):
            old_inc(ch)
            game.reactor.control_rod_depth = slider.value / max_val
            game.minor_action_time()
            game.update()
            game.current_form.display()

        for key, handler in slider.handlers.items():
            if handler == old_inc:
                slider.handlers[key] = inc
        slider.h_increase = inc

        form.edit()
        game.reactor.control_rod_depth = slider.value / max_val

    def render(self, coords, room):
        return "{}"

    def get_color(self):
        return "CRITICAL"


class HEVSuit(Entity):
    def __init__(self):
        super().__init__()
        self.name = "HEV Suit"

    def use_item(self, game):
        game.rad_mult = 0.02
        game.inv.remove(self)
        game.equipment.append(self)
        game.update()
        game.current_form.display()
        npyscreen.notify_confirm(
            "Equipped the Hazardous EnVironment Suit, which reduces damage and radiation exposure.",
            title="Item Equipped")
