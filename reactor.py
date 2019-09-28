class Reactor:
    def __init__(self):
        # Things to keep in certain bounds
        self.temp = 100
        self.t_change = 5
        self.flux = 500
        self.f_change = 5
        self.dunk = 500
        self.d_change = 5
        self.vent = 500
        self.v_change = 5

    def auto_changes(self):
        self.f_change += 1
        self.f_change = constrain(self.f_change, 0, 10)
        self.flux = self.flux + self.f_change - 5 * 6
        self.d_change -= self.flux / 500
        self.d_change = constrain(self.d_change, 0, 10)
        self.dunk = self.dunk - self.d_change * 5 - self.f_change * 4
        self.v_change += self.dunk / 101
        self.v_change = constrain(self.v_change, 0, 10)
        self.vent += self.dunk / 50 + self.v_change - self.flux / 40
        self.t_change += 1
        self.t_change = constrain(self.t_change, 0, 10)
        self.temp = self.temp + self.t_change + self.flux / 100 - self.dunk / 210 - self.vent / 180

    def get_statuses(self):
        return [
            f"flux:\t\t{self.flux:03.3f}",
            f"f_change:\t{self.f_change:03.3f}",
            f"dunk:\t\t{self.dunk:03.3f}",
            f"d_change:\t{self.d_change:03.3f}",
            f"vent:\t\t{self.vent:03.3f}",
            f"v_change:\t{self.v_change:03.3f}",
            f"temp:\t\t{self.temp:03.3f}",
            f"t_change:\t{self.t_change:03.3f}",
        ]

def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))
