def link_doors(r_a, d_a, r_b, d_b):
    d_a.target_room = r_b
    d_a.target_coords = r_b.location_of(d_b)
    d_b.target_room = r_a
    d_b.target_coords = r_a.location_of(d_a)


def make_rooms():
    import room
    import items

    rooms = []

    hallway = room.Room()
    hallway.name = "Hallway"
    hallway.empty([3, 9])
    hallway.contents[0][1] = hallway_north_door = items.Door()
    hallway.contents[8][1] = hallway_south_door = items.Door()

    # TODO randomly link rooms together
    reactor_room = room.Room()
    reactor_room.name = "Reactor Room"
    reactor_room.empty([9, 9])
    reactor_room.contents[0][3] = reactor_door = items.Door()
    reactor_room.contents[3][3] = items.ReactorPart()
    reactor_room.contents[4][4] = box = items.Box()
    box.inv.append(items.HealthPack())

    observation_room = room.Room()
    observation_room.name = "Observation Room"
    observation_room.empty([8, 6])
    observation_room.contents[1][1] = box = items.Box()
    observation_room.contents[3][1] = items.TestPanel()
    observation_room.contents[5][4] = observation_door = items.Door()
    box.inv.append(items.HealthPack())

    # TODO: make more rooms

    link_doors(hallway, hallway_south_door, reactor_room, reactor_door)
    link_doors(hallway, hallway_north_door, observation_room, observation_door)

    rooms.append(reactor_room)
    rooms.append(hallway)
    rooms.append(observation_room)

    return rooms
