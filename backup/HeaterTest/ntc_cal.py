
import math

def calTPy(data):
    r1 = 100000
    c1 = 4.391855325e-04
    c2 = 2.531872891e-04
    c3 = -6.257262991e-11

    r2 = r1 * ( 1.0/data - 1.0)
    log_r2 = math.log(r2)
    T = (1.0 / (c1 + c2 * log_r2 + c3 * log_r2 * log_r2 * log_r2))
    Tc = T - 273.15
    return Tc


def calTAr2(data):

    _sr = 9900
    _nr = 98000
    _bc = 3950
    _nt = 25.0

    a1 = _sr * ((1024.0 - 1.0)/data - 1.0)
    sh = (math.log(a1/_nr)) / _bc + 1.0 / (_nt + 273.15)
    Tc = 1.0 / sh - 273.15

    return Tc

def calTAr(data):

    _sr = 9900
    _nr = 98000
    _bc = 3950
    _nt = 25.0

    a1 = _sr * ((1024.0 - 1.0)/data - 1.0)
    sh = (math.log(a1/_nr)) / _bc + 1.0 / (_nt + 273.15)
    Tc = 1.0 / sh - 273.15

    return Tc
