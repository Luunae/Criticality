class Reactor:
    CRITICAL_TEMP = 200

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
        self.air_temp = 20
        self.thermal_dump = 0
        self.control_rod_depth = 0  # TODO use in calculations below

    def auto_changes(self, coef):
        self.f_change += (1) * coef
        self.f_change = constrain(self.f_change, 0, 10)
        self.flux += ((self.f_change - 5) * 6) * coef * (1 - self.control_rod_depth)
        self.flux = constrain(self.flux, 0, 1000)
        self.d_change -= (self.flux / 500) * coef
        self.d_change = constrain(self.d_change, 0, 10)
        self.dunk += ((self.d_change - 5) * 4 - self.f_change * 2) * coef
        self.dunk = constrain(self.dunk, 0, 1000)
        self.v_change -= (self.dunk / 200) * coef
        self.v_change = constrain(self.v_change, 0, 10)
        self.vent += (self.dunk / 50 + self.v_change - self.flux / 40) * coef
        self.vent = constrain(self.vent, 0, 1000)
        self.t_change += (
            self.thermal_dump + 1 - (self.v_change / 10) - (self.d_change / 10) + (self.f_change / 10)
        ) * coef
        self.t_change = constrain(self.t_change, 0, 10)
        self.temp += ((self.t_change - 5) + (self.flux / 100) - (self.dunk / 210) - (self.vent / 80)) * coef
        self.air_temp = (self.air_temp * 200 + self.temp - 70) / 201

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

    def status_percentage(self):
        return self.temp / Reactor.CRITICAL_TEMP


def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))
