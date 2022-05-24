class Mass:
    def __init__(self, mass, xb, xe, xg, yg, zg, mb_per_meter, me_per_meter):
        self.mass = mass
        self.xb = xb
        self.xe = xe
        self.xg = xg
        self.yg = yg
        self.zg = zg
        self.mb_per_meter = mb_per_meter
        self.me_per_meter = me_per_meter

    def __get_mass__(self):
        return self.mass


masse = Mass(1, 2, 3, 4, 5, 6, 7, 8)
print(masse.mass)
