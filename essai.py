import numpy as np
import matplotlib.pyplot as plt


def calcul_xg(xb, xe, mxb, mxe):
    les_x = np.arange(xb, xe + 0.01, 0.01)
    les_y = (mxe - mxb) / (xe - xb) * (les_x - xb) + mxb
    s = 0
    s_y = 0
    for i in range(len(les_x)):
        s += les_x[i] * les_y[i]
        s_y += les_y[i]
    return s / s_y


def calcul_mass(xb, xe, mb, me):
    return (xe - xb) * (mb + me) / 2


def calcul_mass2(xbm, xem, xb, xe, mb, me):
    coeff = (me - mb) / (xe - xb)
    mbr = mb + coeff * (xb - xbm)
    mer = mb + coeff * (xe - xbm)
    return mbr, mer


def calcul_xg_not_the_mid(m, xb, xe, xg, eps):
    m_per_meter = m / (xe - xb)
    delt = xe - xb
    mb = m_per_meter
    me = m_per_meter
    pourc = 0
    i = 0
    while delt > eps and i < 500000:
        prop = abs(calcul_xg(xb, xe, mb, me) - xg) / (xe - xb)
        if calcul_xg(xb, xe, mb, me) > xg:
            pourc -= prop
        if calcul_xg(xb, xe, mb, me) < xg:
            pourc += prop
        # print(prop)
        mb = (1 - pourc) * m_per_meter
        me = (1 + pourc) * m_per_meter
        delt = abs(calcul_xg(xb, xe, mb, me) - xg)
        i += 1
    return mb, me
