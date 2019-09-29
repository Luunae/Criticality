# This is the file to change setup environmental items.
def link_doors(r_a, d_a, r_b, d_b):
    d_a.target_room = r_b
    d_a.target_coords = r_b.location_of(d_b)
    d_b.target_room = r_a
    d_b.target_coords = r_a.location_of(d_a)


def contents_from_text(width, text):
    import items

    lines = text.strip("\n").split("\n")
    rows = []
    for line in lines:
        row = []
        idx = -1
        for idx, char in enumerate(line):
            item = None
            if char == "#":
                if idx >= (width / 2):
                    item = items.RightWall()
                else:
                    item = items.Wall()

            row.append(item)
        while idx < width - 1:
            idx += 1
            row.append(None)
        rows.append(row)
    return rows


def make_rooms():
    import room
    import items

    rooms = []

    hallway = room.Room()
    hallway.name = "Hallway"
    hallway.empty([3, 9])
    hallway.contents[0][1] = hallway_north_door = items.Door()
    hallway.contents[8][1] = hallway_south_door = items.Door()
    hallway.contents[4][0] = hallway_west_door = items.BlockedDoor()
    hallway.contents[4][2] = hallway_east_door = items.Door()

    # TODO randomly link rooms together
    reactor_room = room.Room()
    reactor_room.name = "Reactor Room"
    reactor_room.empty([9, 9])
    reactor_room.contents[0][3] = reactor_door = items.Door()
    reactor_room.contents[3][3] = items.ReactorPart()
    reactor_room.contents[4][3] = items.ReactorPart()
    reactor_room.contents[3][4] = items.ReactorPart()
    reactor_room.contents[4][4] = items.ReactorPart()
    reactor_room.contents[4][5] = box = items.Box()
    reactor_room.contents[5][4] = items.VentPanel()
    box.inv.append(items.HealthPack())

    observation_room = room.Room()
    observation_room.name = "Observation Room"
    observation_room.empty([8, 6])
    observation_room.contents[1][1] = box = items.Box()
    observation_room.contents[3][0] = observation_door = items.Door()
    observation_room.contents[3][4] = items.DunkPanel()
    box.inv.append(items.HealthPack())
    box.inv.append(items.Crowbar())

    control_rod_room = room.Room()
    control_rod_room.name = "Control Rod Access"
    control_rod_room.contents = contents_from_text(
        9,
        r"""
#########
#   #   #
#   #   #
#   #   #
#       #
#       #
#       #
##     ##
 ##   ##
  #####
""",
    )
    control_rod_room.contents[2][8] = control_rod_door = items.Door()
    control_rod_room.contents[5][4] = items.FluxPanel()

    sleeping_quarters = room.Room()
    sleeping_quarters.contents = control_rod_room.contents = contents_from_text(
        16,
        r"""
################
#    #    #    #
#    #    #    #
#    #    #    #
### #### #### ##
#              #
#              #
################
""",
    )
    sleeping_quarters.contents[7][14] = sleeping_quarters_door = items.Door()
    sleeping_quarters.name = "Sleeping Quarters"

    # TODO: make more rooms

    link_doors(hallway, hallway_south_door, reactor_room, reactor_door)
    link_doors(hallway, hallway_east_door, observation_room, observation_door)
    link_doors(hallway, hallway_west_door, control_rod_room, control_rod_door)
    link_doors(hallway, hallway_north_door, sleeping_quarters, sleeping_quarters_door)

    rooms.append(sleeping_quarters)
    rooms.append(reactor_room)
    rooms.append(hallway)
    rooms.append(observation_room)
    rooms.append(control_rod_room)

    return rooms
