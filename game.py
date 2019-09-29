#!/usr/bin/env python
# encoding: utf-8
from typing import Union, List

import awful
import menus
import curses

import forms
from exceptions import DummyException
from items import *
from map import MapWidget
from room import Room
from rooms import make_rooms
from reactor import Reactor

GAME_NAME: str = "Criticality"

awful.bodge_mouse_event(npyscreen.FormWithMenus.OKBUTTON_TYPE)


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


def travel_time():
    # Adjust this as necessary for travel time between rooms?
    game.time = game.time + 0.25


def minor_action_time():
    # Examine, take something from inventory, small interactions
    game.time = game.time + 1


def major_action_time():
    # Solve a puzzle?
    game.time = game.time + 5


class Game:
    rooms: List[Room]
    active_room: Room
    map: Union[None, MapWidget]

    def __init__(self):
        # state of various entities/room thingies
        self.inv = [HealthPack()]
        self.rooms = make_rooms()
        self.player_coords = [4, 4]
        self.active_room = self.rooms[0]
        self.hp = HP()
        self.time = 0
        self.td = TimeDisplay()

        self.map = None
        self.time_txt = None
        self.room_txt = None
        self.inventory_txt = None
        self.current_form = None

        self.reactor = Reactor()

        # Variable for end-state
        self.good_end = None

    def popup_menu(self, menu):
        self.current_form.popup_menu(menu)

    def show_status(self):
        npyscreen.notify_confirm(self.reactor.get_statuses(), editw=1)

    def setup_form(self, form):
        self.current_form = form
        self.map = form.add(MapWidget, max_height=10)
        self.time_txt = form.add(npyscreen.TitleFixedText, name="Time:", editable=False)
        self.inventory_txt = form.add(npyscreen.TitleFixedText, name="Inventory:", editable=False)
        self.room_txt = form.add(npyscreen.TitleFixedText, name="Room:", value="set this to roomLoc", editable=False)
        form.before_display = lambda: self.update()
        form.add_handlers({"f": self.handle_interact})
        form.add_handlers({"e": self.handle_interact})

    def handle_interact(self, _arg):
        x, y = self.map.get_player_coords()
        item: Entity = self.active_room.get([x, y])
        if item:
            item.interact(game, [x, y], self.active_room)

    def update(self):
        self.map.set_room(self.active_room)
        if self.map.cursorx and self.map.cursory:
            self.player_coords = self.map.get_player_coords()

        self.time_txt.set_value(f"{self.td.text()}")
        self.inventory_txt.set_value(f"{len(self.inv)} item(s)")

        new_cursor_position = (
            self.player_coords[1] * (len(self.active_room.contents[0]) * 2 + 1) + self.player_coords[0] * 2
        )
        if new_cursor_position != self.map.cursor_position - 1:
            self.map.cursor_position = new_cursor_position
        self.room_txt.set_value(f"{self.active_room.name} ({self.player_coords})")


class MainMenu(npyscreen.FormWithMenus):
    def __init__(self, name=f"Welcome to {GAME_NAME}", minimum_columns=40, minimum_lines=30, *args, **keywords):
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
        self.m1 = self.add_menu(name="Inventory", shortcut="i")
        for idx, inv_item in enumerate(game.inv):
            def use_inv_item(item=inv_item):
                item.use_item(game)

                raise DummyException()

            self.m1.addItemsFromList([(inv_item.name, use_inv_item)])

        self.m1.addItem(text="Status", onSelect=game.show_status, shortcut="s", arguments=None, keywords=None)


game = Game()


def title_card():
    form = MainMenu(minimum_lines=1)
    title_text = r"""
   _____ _____  _____ _______ _____ _____          _      _____ _________     __ 
  / ____|  __ \|_   _|__   __|_   _/ ____|   /\   | |    |_   _|__   __\ \   / / 
 | |    | |__) | | |    | |    | || |       /  \  | |      | |    | |   \ \_/ /  
 | |    |  _  /  | |    | |    | || |      / /\ \ | |      | |    | |    \   /   
 | |____| | \ \ _| |_   | |   _| || |____ / ____ \| |____ _| |_   | |     | |    
  \_____|_|  \_|_____|  |_|  |_____\_____/_/    \_|______|_____|  |_|     |_|    
                                                                                 """
    title_text.strip("\n")

    control_text = r"""
 CONTROLS
 F          =   INTERACT/USE/ENTER
 ESC        =   EXIT
 WSAD/↑↓←→  =   MOVE
 
 you wake up and everything's gone to frick
 todo fix this text
"""
    # TODO: make Q work consistently
    title: npyscreen.MultiLineEdit = form.add_widget(
        npyscreen.MultiLineEdit,
        editable=False,
        value=title_text,
        max_height=title_text.count("\n") + 2,
        color="WARNING",
        labelColor="WARNING",
    )
    form.add_widget(
        npyscreen.MultiLineEdit, value=control_text, editable=False, max_height=control_text.count("\n") + 2
    )

    # TODO main menu button positions?
    form.add_widget(
        npyscreen.ButtonPress,
        name="Select Theme",
        when_pressed_function=lambda: form.popup_menu(menus.create_theme_menu(form)),
    )
    form.edit()


def draw_game_ui():
    form = MainMenu()

    game.setup_form(form)

    try:
        form.edit()
    # TODO: less awful way of proceeding to next state?????
    except DummyException:
        pass

    game.update()


class TestApp(npyscreen.NPSApp):
    def main(self):
        title_card()
        last_time = 0
        while True:
            minor_action_time()
            draw_game_ui()

            for i in range(0, game.time - last_time):
                game.reactor.auto_changes()
            last_time = game.time

            if game.reactor.temp > 200:
                game.good_end = 0

            if game.time > 99:
                if game.reactor.temp < 151:
                    game.good_end = 1

                else:
                    game.good_end = 0.5

        if game.good_end == 0:
            # Bad End
            pass

        elif game.good_end == 1:
            # Good End
            pass
        else:
            # sudden death, reinforcements?
            pass


if __name__ == "__main__":
    App = TestApp()
    App.run()
