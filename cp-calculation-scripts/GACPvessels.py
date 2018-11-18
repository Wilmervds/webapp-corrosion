#!/usr/bin/python3
"""
Collection of calculations for GACP of vessels
-----------------------------------------------
-----------------------------------------------


Calculation of surface areas:
Made generic, things like rudder and propellers can be more than one per vessel
(e.g. from port side and starboard)
-------------------------------------------------------------------------------
To calculate hull surface area:
length of vessel in m (length), breadth of vessel in m (breadth), draft of
vessel in m (draft), block coefficient (ratio volume of displacement to
volume of a rectangular block having same overall length, breadth and depth.) (cb).

Most other parts are either squares or cylinders
rudder = rudder of vessel for steer control
prop_nozz_body = nozzle propeller main body
prop_nozz_ssring = nozzle propeller ss ring
prop_blades = propeller blades (formula: [])
prop_shaft = propeller shaft
thruster = bow or stern thruster tunnel to help giving vessel control
sc = seachest, location inside hull used for cooling purposes


Calculation of coating breakdown factor:
----------------------------------------
Coating breakdown factor (cbf) describes anticipated reduction in cathodic current
density due to coating application. It needs constants a and b (from DNV Table 10-4 An A) and
time, t in years. Factors depend on coating thickness. Both mean and final factors can be
calculated

Calculation of current demand:
------------------------------
Basically, using imput parameters from other sections the current demand is calculated as
I=ixAxcbf

"""

# begin of script

import numpy as np

# Recommended current densities by now in a simple array
# Source for now:
# Corrosion's excel sheet: Calculation galv.anodes Standard sheet.gavl.Anodes CWC 1.xlsx
# Think on implementing from DNV-RP-B401 Annex A!!
# All in mA/m2

# Explanation below: each array element has two elements, first is the part and second is
# recommended current densitity in mA/m2
idens = [['hull', 15], ['rudder', 80], ['propeller', 50], ['ssring', 50],
            ['bowthrust', 25], ['seachests', 600]]
            
# Recommended coating breakdown factors constants in a simple array
# Explanation below: each array element has 4 elements, first is coating category (1-3),
# second is water depth (1 = 0-30m; 2 = >30m), third is constant a and fourth is constant b
cbfc = [[1, 1, 0.10, 0.10], [1, 2, 0.10, 0.05], [2, 1, 0.05, 0.025], [2, 2, 0.05, 0.015],
        [3, 1, 0.02, 0.012], [3, 2, 0.02, 0.008]]


# Temporary test input variables
# ------------------------------
##part for current demand
part = "rudder"
##hull
length = 245.0
breadth = 30.0
draft = 9.75
cb = 0.6

##rudder
rflength = 3.20
rfheight = 4.48

# Example tunnel, nozzle
diam = 2.60
tlength = 1.15

# Example coating breakdown factor
t = 0.5
depth = 40
categ = 1
kind = "final"

# Calculation areas of different parts to be protected
# basic geometries are hull and various cylinders representing nozzles, thrusters, tunnels, etc.

def calc_wet_hull_sa(length, breadth, draft, cb):
    wethullsa = (1.7 * length * draft) + (cb * length * breadth)
    return wethullsa
def calc_rf_sa(rflength, rfheight):
    rfsa = rflength * rfheight * 2
    return rfsa
def calc_tunnels_sa(diam, tlength):
    tun_sa = np.pi * diam * tlength
    return tun_sa
def calc_prop_sa(pdiam):
    propsa = 0.25 * np.pi * pdiam

# Calculation of coating breakdown factor (f)

def cbf(categ, depth, t, kind):
    depth = 1 if depth < 30 else 2
    for i in range(len(cbfc)):
        if cbfc[i][0] == categ and cbfc[i][1] == depth:
            a = cbfc[i][2]
            b = cbfc[i][3]
    cbf = a + b * t / 2 if kind == "mean" else a + b * t
    return cbf

# Calculation of current demand (I)
# depends on part and uses provide cbf above

def idem(part):
    if part == "hull":
        idem = (idens[0][1] / 1000.0) * calc_wet_hull_sa(length, breadth, draft, cb) * cbf(categ, depth, t, kind)
        return idem
    if part == "rudder":
        idem = (idens[1][1] / 1000.0) * calc_rf_sa(rflength, rfheight) * cbf(categ, depth, t, kind)
        return idem

#print(calc_wet_hull_sa(length, breadth, draft, cb))
print(calc_rf_sa(rflength, rfheight))
#print(calc_tunnels_sa(diam, tlength))
print(cbf(categ, depth, t, kind))
print(idem(part))
