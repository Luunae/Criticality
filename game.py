#!/usr/bin/env python
# encoding: utf-8
import curses
from typing import List, Any

import npyscreen

from items import *

GAME_NAME: str = "Allonsy"
game_time = 0


class Room:
    contents: List[List[Any]]

    def __init__(self):
        self.contents = [[]]
        self.name = "FIXME"

    def empty(self, dims):
        self.contents = [[None for _ in range(0, dims[0])] for _ in range(0, dims[1])]
        for y in range(0, dims[1]):
            self.contents[y][0] = Wall()
            self.contents[y][dims[0] - 1] = Wall()

        for x in range(0, dims[0]):
            self.contents[0][x] = Wall()
            self.contents[dims[1] - 1][x] = Wall()

    def render(self):
        result = ""
        for y, row in enumerate(self.contents):
            for x, thing in enumerate(row):
                result += " "
                if thing:
                    rendered = thing.render([x, y], self)
                    if len(rendered) == 1:
                        result += " "
                    result += rendered
                else:
                    result += "  "
            result += "\n"
        return result

    def get(self, coords):
        if 0 <= coords[1] < len(self.contents) and 0 <= coords[0] < len(self.contents[0]):
            return self.contents[coords[1]][coords[0]]
        return None


class TimeDisplay:
    def __init__(self):
        global game_time
        self.time = game_time
        # Intent of the following is to provide x,y location for the time portion of the HUD
        # TODO: fill the rest out
        self.locx = 0
        self.locy = 0
        self.label = f"TIME: {game_time:4.0f}"


td = TimeDisplay()


class HP:
    def __init__(self):
        consequences = []


hp = HP()


def travel_time():
    # Adjust this as necessary for travel time between rooms?
    global game_time
    game_time = game_time + 0.25
    TimeDisplay.label = f"TIME: {game_time:4.0f}"


def minor_action_time():
    # Examine, take something from inventory, small interactions
    global game_time
    game_time = game_time + 1


def major_action_time():
    # Solve a puzzle?
    global game_time
    game_time = game_time + 5


def make_rooms():
    rooms = []

    # TODO randomly link rooms together
    reactor_room = Room()
    reactor_room.name = "Reactor Room"
    reactor_room.empty([9, 9])
    reactor_room.contents[0][3] = Door()
    rooms.append(reactor_room)

    return rooms


class MainMenu(npyscreen.FormWithMenus):
    def __init__(self, *args, **keywords):
        super().__init__(*args, **keywords)
        self.m1 = None
        self.m2 = None
        self.m3 = None

    def create(self):
        self.add(npyscreen.TitleText, name = "Text:", value= "just some text?")
        self.how_exited_handers[npyscreen.wgwidget.EXITED_ESCAPE] = self.exit_application

        # This bit supposedly creates menus
        self.m1 = self.add_menu(name="Main Menu", shortcut="^M")
        self.m1.addItemsFromList([
            ("Display Text", self.when_display_text, None, None, ("Time might go here?",)),
            ("Just Beep", self.when_just_beep, "e"),
            ("Exit Menu", self.exit_application, "exit?"),
        ])

        self.m2 = self.add_menu(name="Another Menu", shortcut="b",)
        self.m2.addItemsFromList([
            ("Just Beep", self.when_just_beep),
        ])

        self.m3 = self.m2.addNewSubmenu("A sub menu", "^F")
        self.m3.addItemsFromList([
            ("Just Beep", self.when_just_beep),
        ])

    def when_display_text(self, argument):
        npyscreen.notify_confirm(argument)

    def when_just_beep(self):
        curses.beep()

    def exit_application(self):
        curses.beep()
        self.parentApp.setNextForm(None)
        self.editing = False
        self.parentApp.switchFormNow()
# def open_menu():
#     # TODO: Draw menu
#     # Inventory, Status, Notes, Hint(s?), Current Progress
#     pass


def interact():
    # TODO: Door (open, closed, locked), Box (open/close?), puzzle(?), communicator(?)
    # main menu/individual menus?
    pass


inv = PCInventory()
active_room = make_rooms()[0]


def draw_game_ui():
    # form = MainMenu()
    npyscreen.Form.FIX_MINIMUM_SIZE_WHEN_CREATED = True
    form = npyscreen.Form(name=f"Welcome to {GAME_NAME}", ok_button=True, DEFAULT_LINES=0, DEFAULT_COLUMNS=0)
    time = form.add(npyscreen.TitleText, name=f"Time: {td.label}\tLocation: {active_room.name}")
    # ml = form.add(npyscreen.MultiLineEdit, value=active_room.render(), max_height=10)
    form.add_handlers({curses.ascii.ESC: lambda x: exit(1), "^N": lambda x: exit(2)})
    form.edit()


class TestApp(npyscreen.NPSApp):
    def main(self):
        while True:
            draw_game_ui()
            return
            # input = getch()

            # if input == b'\x1b':
            #    return

            # import time
            # time.sleep(0.1)


if __name__ == "__main__":
    App = TestApp()
    App.run()
