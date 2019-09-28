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
        self.game = None
        self.cursorx = None
        self.cursory = None

    def set_game(self, game):
        self.game = game

    def update(self, clear=True):
        # force editing to True while rendering so cursor is shown
        old = self.editing
        self.editing = True
        super().update(clear)
        self.editing = old
