def make_rooms():
    import room
    import items

    rooms = []

    # TODO randomly link rooms together
    reactor_room = room.Room()
    reactor_room.name = "Reactor Room"
    reactor_room.empty([9, 9])
    reactor_room.contents[0][3] = room.Door()
    reactor_room.contents[3][3] = items.ReactorPart()
    reactor_room.contents[4][4] = box = items.Box()
    from items import HealthPack

    box.inv.append(HealthPack())
    rooms.append(reactor_room)

    return rooms
