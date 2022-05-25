import numpy as np
import matplotlib.pyplot as plt

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

    def calcul_xg(self):
        xe=self.xe
        xb=self.xb
        mxb=self.mb_per_meter
        mxe=self.me_per_meter
        les_x = np.arange(xb, xe + 0.01, 0.01)
        les_y = (mxe - mxb) / (xe - xb) * (les_x - xb) + mxb
        s = 0
        s_y = 0
        for i in range(len(les_x)):
            s += les_x[i] * les_y[i]
            s_y += les_y[i]
        return s / s_y

    def calcul_xg2(self,xb,xe):
        mxb = self.mb_per_meter
        mxe = self.me_per_meter
        les_x = np.arange(xb, xe + 0.01, 0.01)
        les_y = (mxe - mxb) / (xe - xb) * (les_x - xb) + mxb
        s = 0
        s_y = 0
        for i in range(len(les_x)):
            s += les_x[i] * les_y[i]
            s_y += les_y[i]
        if s_y==0:
            print(les_x)
            print(les_y)
        return s / s_y

    def calcul_mass(self):
        xe = self.xe
        xb = self.xb
        mb = self.mb_per_meter
        me = self.me_per_meter
        return (xe - xb) * (mb + me) / 2

    def calcul_mass2(self,xb, xe):
        xem = self.xe
        xbm = self.xb
        mb = self.mb_per_meter
        me = self.me_per_meter
        coeff = (me - mb) / (xem - xbm)
        mbr = mb + coeff * (xb - xbm)
        mer = mb + coeff * (xe - xbm)
        return mbr, mer

    def calcul_xg_not_the_mid(self, eps=0.00001):
        m=self.mass
        xg=self.xg
        xe = self.xe
        xb = self.xb
        mxb = self.mb_per_meter
        mxe = self.me_per_meter
        m_per_meter = m / (xe - xb)
        delt = xe - xb
        mb = m_per_meter
        me = m_per_meter
        pourc = 0
        i = 0
        while delt > eps and i < 500000:
            prop = abs(self.calcul_xg(xb, xe, mb, me) - xg) / (xe - xb)
            if self.calcul_xg() > xg:
                pourc -= prop
            if self.calcul_xg() < xg:
                pourc += prop
            self.mb_per_meter = (1 - pourc) * m_per_meter
            self.me_per_meter = (1 + pourc) * m_per_meter
            delt = abs(self.calcul_xg() - xg)
            i += 1
        return mb, me


