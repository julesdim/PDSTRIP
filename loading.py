import numpy as np
import matplotlib.pyplot as plt


class Loading:
    def __init__(self):
        self.masses = []

    def plot_loading(self, xb, xe):
        """That function allow the user to print the weightloading, for a list of mass, and with the
            boundaries of the ship"""
        delt_x = 0.1  # value of the strip to calculate the ship loading
        les_x = np.arange(xb, xe + delt_x, delt_x)  # coordinates of each strip
        n = len(les_x)
        mass_per_m = [0]  # we initialize the weight loading for x=0, it's equal to 0
        for i in range(n - 1):
            x_inf = les_x[i]
            x_up = les_x[i + 1]
            # coordinates of the strip i
            el_mass = self.mass_calculation(x_inf, x_up) / delt_x  # element of mass for the strip
            mass_per_m.append(el_mass)  # we add to the list
        plt.plot(les_x, mass_per_m)
        plt.title("weight loading")
        plt.show()
        return

    def __append__(self, mass):
        self.masses.append(mass)

    def mass_calculation(self, xb, xe):
        n = len(self.masses)
        tm = 0
        for i in range(n):
            m = self.masses[i].mass
            xbm = self.masses[i].xb
            xem = self.masses[i].xe
            xgm = self.masses[i].xg
            mb = self.masses[i].mb_per_meter
            me = self.masses[i].me_per_meter
            if xbm < xe and xem > xb:
                rb = np.max([xb, xbm])  # real beginning of the mass for the section
                re = np.min([xe, xem])
                mbr = mb + (rb - xbm) * (me - mb) / (xem - xbm)
                mer = mb + (re - xbm) * (me - mb) / (xem - xbm)
                if xgm != (xbm + xem) / 2:
                    tm += (re - rb) * (mbr + mer) / 2
                if xgm == (xbm + xem) / 2:
                    # real end of the mass for the section, if the end of the mass is after the end of the section
                    if mbr!=mer:
                        print("strange")
                    tm += (re - rb) * mbr
        return tm

    def calcul_center_of_gravity(self, xb, xe):
        tm = self.mass_calculation(xb, xe)
        n = len(self.masses)
        # initialization of the values
        xg = 0
        yg = 0
        zg = 0
        for i in range(n):
            m = self.masses[i].mass
            xbm = self.masses[i].xb  # beginning of the mass
            xem = self.masses[i].xe  # end of the mass
            if xbm < xe and xem > xb:
                rb = np.max([xb, xbm])  # real beginning of the mass, if the mass begins before the frame
                re = np.min([xe, xem])
                mb, me = self.masses[i].calcul_mass2(rb, re)
                rm = (re - rb) * (mb + me) / 2  # proportion of the mass situated between the section
                if mb != 0 and me != 0:
                    xg = self.masses[i].calcul_xg2(rb, re)
                else:
                    xg = 0
                xg += rm * xg
                yg += rm * self.masses[i].yg
                zg += rm * self.masses[i].zg
        return (xg / tm, yg / tm, zg / tm)

    def pdstrip_coordinates(self, midship):
        for mass in self.masses:
            mass.xb = mass.xb - midship
            mass.xe = mass.xe - midship
            mass.xg = mass.xg - midship
            mass.zg = -mass.zg