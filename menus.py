from npyscreen import Form

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


def create_theme_menu(form: Form, button):
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
