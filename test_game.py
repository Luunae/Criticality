from game import *


def test_room():
    rooms = make_rooms()
    print(f"{rooms}")

    for room in rooms:
        print(f"{room.render()}")
