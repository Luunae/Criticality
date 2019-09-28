from typing import List, Any

from items import *


class Room:
    contents: List[List[Any]]

    def __init__(self):
        self.contents = [[]]
        self.name = "FIXME"

    def empty(self, dims):
        """
        Initialises an empty room of the given dimensions, with walls around the entire space
        """
        self.contents = [[None for _ in range(0, dims[0])] for _ in range(0, dims[1])]

        for x in range(0, dims[0]):
            self.contents[0][x] = Wall()
            self.contents[dims[1] - 1][x] = Wall()

        for y in range(0, dims[1]):
            self.contents[y][0] = Wall()
            self.contents[y][dims[0] - 1] = RightWall()

    def render(self):
        """
        Renders all the items in the room
        """
        result = ""
        for y, row in enumerate(self.contents):
            if y != 0:
                result += "\n"
            for x, thing in enumerate(row):
                if thing:
                    rendered = thing.render([x, y], self)
                    if len(rendered) == 1:
                        result += " "
                    result += rendered
                else:
                    result += "  "
        return result

    def location_of(self, entity):
        for y, row in enumerate(self.contents):
            for x, thing in enumerate(row):
                if thing == entity:
                    return [x, y]
        return None

    def get(self, coords):
        """
        Gets an Entity in the room at the given [x, y] coords

        :param coords: [x, y] coords
        :return: None if out of bounds or empty, else an Entity
        """
        if 0 <= coords[1] < len(self.contents) and 0 <= coords[0] < len(self.contents[0]):
            return self.contents[coords[1]][coords[0]]
        return None
