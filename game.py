#!/usr/bin/env python
# encoding: utf-8

import npyscreen

from items import *

GAME_NAME: str = "Allonsy"
game_time = 0


class Room:
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
        if 0 <= coords[1] < len(self.contents) and 0 <= coords[0] < len(
            self.contents[0]
        ):
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


def interact():
    # Door (open, closed, locked)
    pass


inv = PCInventory()
active_room = make_rooms()[0]


def draw_game_ui():
    npyscreen.Form.FIX_MINIMUM_SIZE_WHEN_CREATED = True
    form = npyscreen.Form(
        name=f"Welcome to {GAME_NAME}", FIX_MINIMUM_SIZE_WHEN_CREATED=True
    )
    time = form.add(
        npyscreen.TitleText, name=f"Time: {td.label}\tLocation: {active_room.name}"
    )

    ml = form.add(npyscreen.MultiLineEdit, value=active_room.render(), max_height=10)

    form.edit()


class TestApp(npyscreen.NPSApp):
    def main(self):
        while True:
            draw_game_ui()
            return


if __name__ == "__main__":
    App = TestApp()
    App.run()
