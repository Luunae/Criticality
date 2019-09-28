#!/usr/bin/env python
# encoding: utf-8
import curses
from typing import Union

import awful
from items import *
from map import MapWidget
from rooms import make_rooms
from reactor import Reactor

GAME_NAME: str = "Allonsy"

awful.bodge_mouse_event(npyscreen.FormWithMenus.OKBUTTON_TYPE)


class TimeDisplay:
    def __init__(self):
        # Intent of the following is to provide x,y location for the time portion of the HUD
        # TODO: fill the rest out
        self.locx = 0
        self.locy = 0

    def text(self):
        return f"{game.time:04d}"


class HP:
    def __init__(self):
        self.consequences = ["1"]


def travel_time():
    # Adjust this as necessary for travel time between rooms?
    game.time = game.time + 0.25
    TimeDisplay.label = f"TIME: {game.time:4.0f}"


def minor_action_time():
    # Examine, take something from inventory, small interactions
    game.time = game.time + 1


def major_action_time():
    # Solve a puzzle?
    game.time = game.time + 5


class Game:
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
        self.status = ["fine"]

        self.reactor = Reactor()

        # Variable for end-state
        self.good_end = None

    def show_status(self):
        npyscreen.notify_confirm(game.status)

    def setup_form(self, form):
        self.map = form.add(MapWidget, max_height=10)
        self.time_txt = form.add(npyscreen.TitleFixedText, name="Time:")
        self.inventory_txt = form.add(npyscreen.TitleFixedText, name="Inventory:")
        self.room_txt = form.add(npyscreen.TitleFixedText, name="Room:", value="set this to roomLoc")

    def update(self):
        self.map.value = self.active_room.render()
        if self.map.cursorx and self.map.cursory:
            self.player_coords = [int(self.map.cursorx / 2), self.map.cursory]

        self.time_txt.set_value(f"{self.td.text()}")
        self.inventory_txt.set_value(f"{len(self.inv)} item(s)")

        new_cursor_position = (
            self.player_coords[1] * (len(self.active_room.contents[0]) * 2 + 1) + self.player_coords[0] * 2
        )
        if new_cursor_position != self.map.cursor_position - 1:
            self.map.cursor_position = new_cursor_position
        self.room_txt.set_value(f"{self.active_room.name} ({self.player_coords})")


class MainMenu(npyscreen.FormWithMenus):
    def __init__(self, name=f"Welcome to {GAME_NAME}", minimum_columns=40, minimum_lines=20, *args, **keywords):
        super().__init__(name=name, minimum_columns=minimum_columns, minimum_lines=minimum_lines, *args, **keywords)
        self.m1 = None
        self.m2 = None
        self.m3 = None

    def create(self):
        self.how_exited_handers[npyscreen.wgwidget.EXITED_ESCAPE] = self.exit_application
        # This bit supposedly creates menus
        # Inventory, Status, Notes, Hint(s?), Current Progress
        self.m1 = self.add_menu(name="Inventory", shortcut="i")
        for inv_item in game.inv:

            def use_inv_item():
                inv_item.use_item(game)

                raise DummyException()

            self.m1.addItemsFromList([(inv_item.name, use_inv_item)])

        self.m1.addItem(text="Status", onSelect=game.show_status, shortcut="s", arguments=None, keywords=None)
        # self.m1 = self.add_menu(name="Status", shortcut="s")
        # self.m1 = self.addItemsFromList(
        #     [game.status]
        # )

        # self.m3 = self.m2.addNewSubmenu("A sub menu", "^F")
        # self.m3.addItemsFromList([("Just Beep", self.when_just_beep)])

    def when_display_text(self, argument):
        npyscreen.notify_confirm(argument)

    def when_just_beep(self):
        curses.beep()

    def exit_application(self):
        curses.beep()
        # self.parentApp.setNextForm(None)
        # self.parentApp.switchFormNow()
        self.editing = False
        exit(1)


# def open_menu():
#     # TODO: Draw menu
#
#     pass


def interact():
    # TODO: Door (open, closed, locked), Box (open/close?), puzzle(?), communicator(?)
    # main menu/individual menus?
    pass


game = Game()


def title_card():
    form = MainMenu()
    title_text = r"""
  _____  ______ __  __  ____    _______ ________   _________ 
 |  __ \|  ____|  \/  |/ __ \  |__   __|  ____\ \ / |__   __|
 | |  | | |__  | \  / | |  | |    | |  | |__   \ V /   | |   
 | |  | |  __| | |\/| | |  | |    | |  |  __|   > <    | |   
 | |__| | |____| |  | | |__| |    | |  | |____ / . \   | |   
 |_____/|______|_|  |_|\____/     |_|  |______/_/ \_\  |_|   
"""
    form.add_widget(npyscreen.MultiLineEdit, editable=False, value=title_text)
    form.edit()
    pass


class DummyException(Exception):
    pass


def draw_game_ui():
    npyscreen.Form.FIX_MINIMUM_SIZE_WHEN_CREATED = True
    form = MainMenu()

    game.setup_form(form)

    game.update()
    form.while_editing = lambda x: game.update()

    try:
        form.edit()
    # TODO: less awful way of proceeding to next state?????
    except DummyException:
        pass

    game.update()


class TestApp(npyscreen.NPSApp):
    def main(self):
        title_card()
        while game.good_end == None:
            minor_action_time()
            draw_game_ui()
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
