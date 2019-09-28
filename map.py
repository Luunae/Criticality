import curses

import npyscreen


class MapWidget(npyscreen.MultiLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove editing handler, rooms aren't editable
        del self.complex_handlers[-1]
        del self.handlers[curses.ascii.NL]
        del self.handlers[curses.ascii.CR]
        del self.handlers[curses.ascii.DEL]
        del self.handlers[curses.ascii.BS]
        del self.handlers[curses.KEY_DC]
        del self.handlers[curses.KEY_BACKSPACE]
        del self.handlers["^R"]
        self.room = None
        self.cursorx = None
        self.cursory = None

    def get_player_coords(self):
        return [int(self.cursorx / 2), self.cursory]

    def h_line_down(self, input):
        coords = self.get_player_coords()
        block = self.room.get([coords[0], coords[1] + 1])
        if not block or block.traversable:
            super().h_line_down(input)

    def h_line_up(self, input):
        coords = self.get_player_coords()
        block = self.room.get([coords[0], coords[1] - 1])
        if not block or block.traversable:
            super().h_line_up(input)

    def h_cursor_left(self, input):
        coords = self.get_player_coords()
        block = self.room.get([coords[0] - 1, coords[1]])
        if not block or block.traversable:
            super().h_cursor_left(input)

    def h_cursor_right(self, input):
        coords = self.get_player_coords()
        block = self.room.get([coords[0] + 1, coords[1]])
        if not block or block.traversable:
            super().h_cursor_right(input)

    def set_room(self, room):
        self.room = room
        self.value = room.render()

    def update(self, clear=True):
        # force editing to True while rendering so cursor is shown
        old = self.editing
        self.editing = True
        super().update(clear)
        self.editing = old
