def make_rooms():
    import room
    import items

    rooms = []

    # TODO randomly link rooms together
    reactor_room = room.Room()
    reactor_room.name = "Reactor Room"
    reactor_room.empty([9, 9])
    reactor_room.contents[0][3] = room.Door()
    rooms.append(reactor_room)

    return rooms
