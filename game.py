#!/usr/bin/env python
# encoding: utf-8
import glob
from math import floor
from pathlib import Path
from typing import Union, List

import awful
import menus
import themes
from exceptions import DummyException
from items import *
from map import MapWidget
from room import Room
from rooms import make_rooms
from reactor import Reactor

GAME_NAME: str = "Criticality"

awful.patch_all()


class TimeDisplay:
    def __init__(self):
        # Intent of the following is to provide x,y location for the time portion of the HUD
        # TODO: fill the rest out
        self.locx = 0
        self.locy = 0

    def text(self):
        h = int(game.time / 100)
        m = int((game.time - (h * 100)) / 10)
        s = int(game.time - (m * 10 + h * 100))

        return f"{h:01d}:{m:01d}:{s:01d}"


class HP:
    def __init__(self):
        self.consequences = ["1"]


class Game:
    rooms: List[Room]
    active_room: Room
    map: Union[None, MapWidget]

    def __init__(self):
        # state of various entities/room thingies
        self.inv = []
        self.rooms = make_rooms()
        self.player_coords = [1, 1]
        self.active_room = self.rooms[0]
        self.hp = HP()
        self.damage_rate = len(self.hp.consequences) * 0.2
        self.time = 0
        self.rads = 0
        self.td = TimeDisplay()

        self.map = None
        self.time_txt = None
        self.room_txt = None
        self.inventory_txt = None
        self.radiation_exposure_txt = None
        self.current_form = None
        self.air_temp = None
        self.set_map_pos = True
        self.get_map_pos = False
        self.last_time = 0

        self.reactor = Reactor()

        # Variable for end-state
        self.good_end = None

    def change_damage_rate(self, dr):
        pass

    def popup_menu(self, menu):
        self.current_form.popup_menu(menu)

    def show_status(self):
        npyscreen.notify_confirm(self.reactor.get_statuses(), editw=1)

    def setup_form(self, form):
        self.current_form = form
        self.map = form.add(MapWidget, max_height=10)
        self.map.game = self
        self.time_txt = form.add(npyscreen.TitleFixedText, name="Time:", editable=False)
        self.inventory_txt = form.add(npyscreen.TitleFixedText, name="Inventory:", editable=False)
        self.room_txt = form.add(npyscreen.TitleFixedText, name="Room:", value="set this to roomLoc", editable=False)
        self.air_temp = form.add(npyscreen.TitleFixedText, name="Air temp:", editable=False)
        self.radiation_exposure_txt = form.add(npyscreen.TitleFixedText, name="Radiation exposure: ", editable=False)
        form.before_display = lambda: self.update()
        forms.add_handlers(form, {"f": self.handle_interact, "e": self.handle_interact})

    def handle_interact(self, _arg):
        x, y = self.map.get_player_coords()
        item: Entity = self.active_room.get([x, y])
        if item:
            item.interact(game, [x, y], self.active_room)

    def set_room(self, room, coords):
        self.active_room = room
        self.player_coords = coords
        self.set_map_pos = True
        self.map.set_room(room)

    def update(self):
        self.update_reactor()

        self.air_temp.value = f"~{int(self.reactor.air_temp / 5) * 5}°C"
        self.map.set_room(self.active_room)

        if self.get_map_pos:
            self.get_map_pos = False
            self.player_coords = self.map.get_player_coords()

        self.time_txt.set_value(f"{self.td.text()}")
        self.inventory_txt.set_value(f"{len(self.inv)} item(s)")
        self.radiation_exposure_txt.value = f"{self.rads:05d} rad"

        new_cursor_position = (
            self.player_coords[1] * (len(self.active_room.contents[0]) * 2 + 1) + self.player_coords[0] * 2
        )
        if new_cursor_position != self.map.cursor_position - 1:
            self.map.cursor_position = new_cursor_position
        self.room_txt.set_value(f"{self.active_room.name} ({self.player_coords})")

    def update_reactor(self):
        time = floor(self.time)
        for i in range(0, time - self.last_time):
            self.reactor.auto_changes(0.5)
            self.rads += self.active_room.rads_per_sec
        self.last_time = time

        if game.reactor.status_percentage() >= 1:
            # TODO flavor text
            npyscreen.notify_confirm("The reactor explodes violently.", title="Meltdown", editw=1)
            exit(0)

    def travel_time(self):
        # Adjust this as necessary for travel time between rooms?
        self.time += 1 * game.damage_rate
        self.get_map_pos = True
        self.update()
        self.current_form.display()

    def tiny_action_time(self):
        self.time += 0.1 * game.damage_rate

    def minor_action_time(self):
        # Examine, take something from inventory, small interactions
        self.time += 1 * game.damage_rate

    def major_action_time(self):
        # Solve a puzzle?
        self.time += 5 * game.damage_rate


class MainMenu(npyscreen.FormBaseNewWithMenus):
    def __init__(self, name=f"{GAME_NAME}", minimum_columns=40, minimum_lines=25, *args, **keywords):
        super().__init__(
            name=name, minimum_columns=minimum_columns, minimum_lines=minimum_lines, ok_button=False, *args, **keywords
        )
        self.m1 = None
        self.m2 = None
        self.m3 = None
        self.before_display = None

    def display(self, clear=False):
        if self.before_display:
            self.before_display()
        super().display(clear=clear)

    def create(self):
        forms.add_standard_handlers(self, quit=True)
        self.m1: npyscreen.NewMenu = self.add_menu(name="Inventory", shortcut="i")
        for idx, inv_item in enumerate(game.inv):

            def use_inv_item(item=inv_item):
                item.use_item(game)
                game.minor_action_time()

                raise DummyException()

            self.m1.addItemsFromList([(inv_item.name, use_inv_item)])

        self.m1.addItem(text="Status", onSelect=game.show_status, shortcut="s", arguments=None, keywords=None)
        datapad: npyscreen.NewMenu = self.m1.addNewSubmenu(name="Datapad", shortcut="d")

        import os

        for file in sorted(glob.glob("story/datapad/*.txt")):
            name = os.path.basename(file)

            def show_file(f=file, n=name):
                old_lines = npyscreen.PopupWide.DEFAULT_LINES
                npyscreen.PopupWide.DEFAULT_LINES = 20
                npyscreen.notify_confirm(Path(f).read_text(), title=n, wide=True, wrap=True)
                npyscreen.PopupWide.DEFAULT_LINES = old_lines

            datapad.addItem(text=name, onSelect=show_file)


game = Game()


def title_card():
    form = MainMenu(minimum_lines=1, name=None)
    title_text = r"""
   _____ _____  _____ _______ _____ _____          _      _____ _________     __ 
  / ____|  __ \|_   _|__   __|_   _/ ____|   /\   | |    |_   _|__   __\ \   / / 
 | |    | |__) | | |    | |    | || |       /  \  | |      | |    | |   \ \_/ /  
 | |    |  _  /  | |    | |    | || |      / /\ \ | |      | |    | |    \   /   
 | |____| | \ \ _| |_   | |   _| || |____ / ____ \| |____ _| |_   | |     | |    
  \_____|_|  \_|_____|  |_|  |_____\_____/_/    \_|______|_____|  |_|     |_|    
""".strip(
        "\n"
    )

    control_text = r"""
 CONTROLS
 F/E        =   INTERACT/USE/OPEN       ↑↓←→/WSAD  =   MOVE
 ESC        =   EXIT                    ENTER/SPACE=   SELECT
 CTRL + X   =   MENU
""".lstrip(
        "\n"
    )
    # TODO: make Q work consistently
    title: npyscreen.MultiLineEdit = form.add_widget(
        npyscreen.MultiLineEdit,
        editable=False,
        value=title_text,
        rely=1,
        max_height=title_text.count("\n") + 2,
        color="WARNING",
        labelColor="WARNING",
    )

    intro = Path("story/intro.txt").read_text()

    intro_pager = form.add_widget(
        npyscreen.Pager, values=[], max_height=form.curses_pad.getmaxyx()[0] - title.height - 3
    )
    intro_pager.values = npyscreen.utilNotify._wrap_message_lines(control_text + "\n" + intro, intro_pager.width - 1)
    for widget in intro_pager._my_widgets[:4]:
        widget.color = "CURSOR"

    button_x_gap = 8
    start_button: npyscreen.ButtonPress = form.add_widget(npyscreen.ButtonPress, name="Start", use_max_space=True)

    def start():
        form.editing = False

    start_button.when_pressed_function = start
    last = start_button

    theme_button = form.add_widget(
        npyscreen.ButtonPress,
        name=themes.select_theme_text(),
        rely=last.rely,
        relx=last.width + last.relx + button_x_gap,
        use_max_space=True,
    )

    last = theme_button
    credits_button = form.add_widget(
        npyscreen.ButtonPress,
        name="Credits",
        rely=last.rely,
        relx=last.width + last.relx + button_x_gap,
        use_max_space=True,
    )
    credits_button.when_pressed_function = menus.launch_credits
    last = theme_button

    theme_button.when_pressed_function = lambda: form.popup_menu(menus.create_theme_menu(form, theme_button))

    form.set_editing(start_button)
    form.edit()


def draw_game_ui():
    form = MainMenu(minimum_lines=10)

    game.setup_form(form)

    try:
        form.edit()
    # TODO: less awful way of proceeding to next state?????
    except DummyException:
        pass

    game.update()


def main_loop():
    while True:
        draw_game_ui()


class TestApp(npyscreen.NPSApp):
    def main(self):
        awful.set_cwd_for_pyinstaller()
        themes.set_startup_theme()
        title_card()

        main_loop()


if __name__ == "__main__":
    App = TestApp()
    App.run()
