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
        self.flux = self.flux + self.f_change - 5 * 6
        self.d_change -= self.flux / 500
        self.dunk = self.dunk - self.d_change * 5 - self.f_change * 4
        self.v_change += self.dunk / 101
        self.vent += self.dunk / 50 + self.v_change - self.flux / 40
        self.t_change += 1
        self.temp = self.temp + self.t_change + self.flux / 100 - self.dunk / 210 - self.vent / 180
