#!/usr/bin/env python
# encoding: utf-8
import curses
import awful
from items import *
from rooms import make_rooms

GAME_NAME: str = "Allonsy"

awful.bodge_mouse_event(npyscreen.FormWithMenus.OKBUTTON_TYPE)


class TimeDisplay:
    def __init__(self):
        # Intent of the following is to provide x,y location for the time portion of the HUD
        # TODO: fill the rest out
        self.locx = 0
        self.locy = 0

    def text(self):
        return f"TIME: {game.time:4.0f}"


class HP:
    def __init__(self):
        self.consequences = ["1"]


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


class Game:
    def __init__(self):
        # state of various entities/room thingies
        self.inv = [HealthPack()]
        self.rooms = make_rooms()
        self.active_room = self.rooms[0]
        self.hp = HP()
        self.time = 0
        self.td = TimeDisplay()

        self.top_bar = None
        self.map = None
        self.status = ["fine"]

    def show_status(self):
        npyscreen.notify_confirm(game.status)

    def setup_form(self, form):
        self.top_bar = form.add(npyscreen.TitleFixedText)
        self.map = form.add(npyscreen.MultiLineEdit, max_height=10)
        form.add(npyscreen.TitleText, name="Room:", value="set this to roomLoc")

    def update(self):
        self.top_bar.set_value(f"{game.td.text()}\tLOCATION: {game.active_room.name}")
        self.map.value = f"{game.active_room.render()}"


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

    try:
        form.edit()
    # TODO: less awful way of proceeding to next state?????
    except DummyException:
        pass


class TestApp(npyscreen.NPSApp):
    def main(self):
        title_card()
        while True:
            game.time += 1
            draw_game_ui()


if __name__ == "__main__":
    App = TestApp()
    App.run()
