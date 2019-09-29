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
        self.add_handlers(
            {"w": self.h_line_up, "s": self.h_line_down, "a": self.h_cursor_left, "d": self.h_cursor_right}
        )
        self.room = None
        self.cursorx = None
        self.cursory = None

    def translate_coords(self, x, y):
        return [int(x / 2), y]

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
        half_move = self.cursorx % 2 == 1
        if half_move or ((not block or block.traversable) and coords[0] > 0):
            super().h_cursor_left(input)

    def h_cursor_right(self, input):
        coords = self.get_player_coords()
        block = self.room.get([coords[0] + 1, coords[1]])
        half_move = self.cursorx % 2 == 0
        if half_move or ((not block or block.traversable) and (coords[0] + 1) < len(self.room.contents[0])):
            super().h_cursor_right(input)

    def set_room(self, room):
        if room != self.room:
            self.cursorx = self.cursory = None
        self.room = room
        self.value = room.render()

    def update(self, clear=True):
        if clear:
            self.clear()
        display_length = self.maximum_display_height
        display_width = self.maximum_display_width
        xdisplay_offset = 0
        text_to_display = self.get_value_as_list()
        if self.cursor_position < 0:
            self.cursor_position = 0
        if self.cursor_position > len(self.value):
            self.cursor_position = len(self.value)

        self.cursory, self.cursorx = self.translate_cursor(self.cursor_position)

        if self.editing:
            if self.slow_scroll:
                if self.cursory > self.start_display_at + display_length - 1:
                    self.start_display_at = self.cursory - (display_length - 1)

                if self.cursory < self.start_display_at:
                    self.start_display_at = self.cursory

            else:
                if self.cursory > self.start_display_at + (display_length - 1):
                    self.start_display_at = self.cursory

                if self.cursory < self.start_display_at:
                    self.start_display_at = self.cursory - (display_length - 1)

            if self.start_display_at < 0:
                self.start_display_at = 0

            if self.cursorx > display_width:
                xdisplay_offset = self.cursorx - display_width

        max_display = len(text_to_display[self.start_display_at :])

        for line_counter in range(self.height):
            if line_counter >= len(text_to_display) - self.start_display_at:
                break

            line_to_display = text_to_display[self.start_display_at + line_counter][xdisplay_offset:]
            line_to_display = self.safe_string(line_to_display)
            if isinstance(line_to_display, bytes):
                line_to_display = line_to_display.decode(self.encoding, "replace")
            column = 0
            place_in_string = 0
            while column <= (display_width):
                if not line_to_display:
                    break
                if place_in_string >= len(line_to_display):
                    break
                width_of_char_to_print = 1  # self.find_width_of_char(string_to_print[place_in_string])
                # change this when actually have a function to do this
                if column - 1 + width_of_char_to_print > display_width:
                    break

                color = "DEFAULT"
                item = self.room.get(self.translate_coords(column, line_counter))

                if item:
                    color = item.get_color()

                if self.do_colors():
                    color = self.parent.theme_manager.findPair(self, request=color)
                else:
                    color = curses.A_NORMAL

                self.parent.curses_pad.addstr(
                    self.rely + line_counter,
                    self.relx + column,
                    self._print_unicode_char(line_to_display[place_in_string]),
                    color,
                )
                column += width_of_char_to_print
                place_in_string += 1

            _cur_y, _cur_x = self.translate_cursor(self.cursor_position)

            try:
                char_under_cur = self.safe_string(self.value[self.cursor_position])
                if char_under_cur == "\n":
                    char_under_cur = " "
            except:
                char_under_cur = " "

            if self.do_colors():
                self.parent.curses_pad.addstr(
                    self.rely + _cur_y - self.start_display_at,
                    _cur_x - xdisplay_offset + self.relx,
                    char_under_cur,
                    self.parent.theme_manager.findPair(self) | curses.A_STANDOUT,
                )

            else:
                self.parent.curses_pad.addstr(
                    self.rely + _cur_y - self.start_display_at,
                    _cur_x - xdisplay_offset + self.relx,
                    char_under_cur,
                    curses.A_STANDOUT,
                )
