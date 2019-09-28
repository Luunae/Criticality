import curses


def bodge_mouse_event(cls):
    old_event_handler = cls.handle_mouse_event

    def bodged(self, *args, **kwargs):
        if self.editing:
            self.h_select_exit(curses.ascii.NL)
        return old_event_handler(self, *args, **kwargs)

    cls.handle_mouse_event = bodged
