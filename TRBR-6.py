#User Input File - TBRB1

from opensees import *
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from calibration import calibration
# Load Protocal, 1-strain, 2-fatigue
loadtype = 1

# Model Dimensions 
length = 181.0
lcore = 98.0
LR_BRB = lcore/length

# steel core properties
swidth = 3.0
sthick = 0.5
Acore = swidth*sthick
sFy = 41.0

# wood casing properties
wwidth = 10.0
wthick = 6.0

# Steel Material
E = 29000.0
R0 = 28.
cR1 = 0.94
cR2 = 0.11
a1 = 0.01
a2 = 1.0
a3 = 0.031
a4 = 1.0
si = 0.1

# Pinching Material 
pEnvelopeStress = [0.0001, 0.0001, 0.0001, 0.0001]
nEnvelopeStress = [-2.272, -8.938, -16.0936, -27.6648]
pEnvelopeStrain = [0.001, 0.0086, 0.0137, 0.0213]
nEnvelopeStrain = [-0.00017, -0.0068, -0.0123, -0.0212]


rDisp = [0.55, 0.62]
rForce = [0.93, 0.69]
uForce = [0.35, 0.06]

results = calibration(length, lcore, LR_BRB, swidth, sthick, Acore, sFy, wwidth, 
                      wthick, E, R0, cR1, cR2, a1, a2, a3, a4, si, pEnvelopeStress,
                      nEnvelopeStress, pEnvelopeStrain, nEnvelopeStrain, 
                      rDisp, rForce, uForce, loadtype)