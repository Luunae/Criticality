class Thing:
    def render(self, coords, room):
        raise Exception("TODO")


class Wall(Thing):
    def render(self, coords, room):
        return "|"
