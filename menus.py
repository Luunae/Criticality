import npyscreen

from exceptions import DummyException


def create_box_menu(game, box):
    from npyscreen import NewMenu

    menu = NewMenu(name="Box Inventory")
    for idx, item in enumerate(box.inv):

        def handle_selection(it=item):
            box.inv.remove(it)
            game.inv.append(it)

            raise DummyException()

        menu.addItem(text=item.name, onSelect=handle_selection, shortcut=None, arguments=None, keywords=None)
    return menu


def create_theme_menu(form: npyscreen.Form, button):
    import themes
    from npyscreen import setTheme, NewMenu
    from npyscreen.proto_fm_screen_area import getTheme

    menu = NewMenu(name="Theme Selection")
    for idx, theme in enumerate(themes.themes):

        def select_theme(t=theme):
            setTheme(t)
            form.theme_manager = getTheme()
            button.name = themes.select_theme_text()
            form.display()

        menu.addItem(text=f"{idx:02d} {theme.__name__}", onSelect=select_theme)
    return menu


class SimpleCheckbox(npyscreen.wgcheckbox._ToggleControl):
    False_box = "[ ]"
    True_box = "[X]"

    def __init__(self, screen, value=False, **keywords):
        self.value = value
        super(SimpleCheckbox, self).__init__(screen, **keywords)

        self.show_bold = False
        self.highlight = False
        self.important = False
        self.hide = False

    def update(self, clear=True):
        if clear:
            self.clear()
        if self.hidden:
            self.clear()
            return False
        if self.hide:
            return True

        if self.value:
            cb_display = self.__class__.True_box
        else:
            cb_display = self.__class__.False_box

        color = "CONTROL"
        if self.editing:
            color = "STANDOUT"
        if self.do_colors():
            self.parent.curses_pad.addstr(
                self.rely, self.relx, cb_display, self.parent.theme_manager.findPair(self, color)
            )
        else:
            self.parent.curses_pad.addstr(self.rely, self.relx, cb_display)


def create_key_lock():
    import npyscreen

    form = npyscreen.Popup(name="code lock")
    cbs = []
    for y in range(0, 3):
        for x in range(0, 3):
            cbs.append(
                form.add_widget(SimpleCheckbox, relx=(x + 1) * 3, rely=(y + 1) * 2, width=3, height=2, editable=True)
            )

    def get_results():
        return [cb.value for cb in cbs]

    return form, get_results


def launch_credits():
    import npyscreen

    npyscreen.notify_confirm(
        "Thanks to:\nMink, MMKII, sidereal, and various internet randoms for help with playtesting.", editw=1
    )
    return None


def key_lock(title, expected):
    form, get_results = create_key_lock()
    form.name = title
    form.edit()
    results = get_results()
    return results == expected
