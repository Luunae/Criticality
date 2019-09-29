# monkey patches for npyscreen to work around bugs/lack of flexibility
import curses

import npyscreen


def patch_all():
    bodge_mouse_event(npyscreen.FormWithMenus.OKBUTTON_TYPE)
    bodge_wrap()
    bodge_notify_confirm()


def bodge_notify_confirm():
    """
    Adds escape handling to notify_confirm
    """

    def notify_confirm(message, title="Message", form_color="STANDOUT", wrap=True, wide=False, editw=0):
        message = npyscreen.utilNotify._prepare_message(message)
        if wide:
            F = npyscreen.PopupWide(name=title, color=form_color)
        else:
            F = npyscreen.Popup(name=title, color=form_color)
        import forms

        forms.add_standard_handlers(F)
        F.preserve_selected_widget = True
        mlw = F.add(npyscreen.Pager)
        mlw_width = mlw.width - 1
        if wrap:
            message = npyscreen.utilNotify._wrap_message_lines(message, mlw_width)
        else:
            message = message.split("\n")
        mlw.values = message
        F.editw = editw
        F.edit()

    npyscreen.notify_confirm = notify_confirm
    pass


def bodge_mouse_event(cls):
    """
    Makes double clicks trigger selection for given button-like class
    """
    old_event_handler = cls.handle_mouse_event

    def bodged(self, *args, **kwargs):
        if self.editing:
            self.h_select_exit(curses.ascii.NL)
        return old_event_handler(self, *args, **kwargs)

    cls.handle_mouse_event = bodged


def bodge_wrap():
    """
    Fixes wrap removing blank lines by adding them back in
    """
    import textwrap

    def _wrap_message_lines(message, line_length):
        lines = []
        for line in message.split("\n"):
            wrapped = textwrap.wrap(line.rstrip(), line_length)
            if len(wrapped) == 0:
                wrapped.append("\n")
            lines.extend(wrapped)
        return lines

    npyscreen.utilNotify._wrap_message_lines = _wrap_message_lines


def set_cwd_for_pyinstaller():
    import sys
    import os

    os.chdir(getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__))))
