from exceptions import DummyException


def create_box_menu(game, box):
    from npyscreen import NewMenu

    menu = NewMenu(name="Box Inventory")
    for idx, item in enumerate(box.inv):

        def handle_selection():
            box.inv.remove(item)
            game.inv.append(item)

            raise DummyException()

        menu.addItem(text=item.name, onSelect=handle_selection, shortcut=None, arguments=None, keywords=None)
    return menu

