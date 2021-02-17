# code for calibrating T-BRB Model
from openseespy.opensees import *
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from TBRB import TBRB

def calibration(length, lcore, LR_BRB, swidth, sthick, Acore, sFy, wwidth, 
                      wthick, E, R0, cR1, cR2, a1, a2, a3, a4, si, pEnvelopeStress,
                      nEnvelopeStress, pEnvelopeStrain, nEnvelopeStrain, 
                      rDisp, rForce, uForce, loadtype):
    
    # look at values from experiment results
    data = pd.read_csv('reference_FD.txt', header=None, names=['F_ref', 'd'])
    Force_ref = data['F_ref']
    max_ref = Force_ref.max()
    print("MAX REF = ", max_ref)
    
    min_ref = Force_ref.min()
    print("MIN REF = ", min_ref)

    # calibrate max Tension and Compression By Adjusting a1 and a3
    #a1 = 0.001
    #a3 = 0.001
    step = 0.00005

    #cR2 = 0.05 

    tol = 0.01
    Terror = 0.5
    Cerror = 0.5

    while (Cerror > tol):
        a1 = a1 + step
        #print('\n a1 = ', a1)
        max_min = TBRB(length, lcore, LR_BRB, swidth, sthick, Acore, sFy, wwidth, 
                      wthick, E, R0, cR1, cR2, a1, a2, a3, a4, si, pEnvelopeStress,
                      nEnvelopeStress, pEnvelopeStrain, nEnvelopeStrain, 
                      rDisp, rForce, uForce, loadtype)
        Fmodel_C = max_min[1]
        #print(Fmodel_C)
        Cerror = abs((Fmodel_C-min_ref)/min_ref)
        print('Error = ', Cerror)
        Cerror = -1.0

    while (Terror > tol):
        a3 = a3 + step
        #print('\n a3 = ', a3)
        max_min = TBRB(length, lcore, LR_BRB, swidth, sthick, Acore, sFy, wwidth, 
                      wthick, E, R0, cR1, cR2, a1, a2, a3, a4, si, pEnvelopeStress,
                      nEnvelopeStress, pEnvelopeStrain, nEnvelopeStrain, 
                      rDisp, rForce, uForce, loadtype)
        Fmodel_T = max_min[0]
        #print(Fmodel_T)
        Terror = abs((Fmodel_T-max_ref)/max_ref)
        #print('Error = ', Terror)
        Terror = -1.0

    print('\n Converged a1 =', a1)
    print('\n Converged a3 =', a3)

    # Calibrate Hysteretic Energy By Adjusting R0
    from Hys_Energy_Error import Hys_Energy_Error
    Energy_Error = 0.5
    while (Energy_Error > tol):
        #cR2 = cR2 + 0.05
        print(cR2)
        max_min = TBRB(length, lcore, LR_BRB, swidth, sthick, Acore, sFy, wwidth, 
                      wthick, E, R0, cR1, cR2, a1, a2, a3, a4, si, pEnvelopeStress,
                      nEnvelopeStress, pEnvelopeStrain, nEnvelopeStrain, 
                      rDisp, rForce, uForce, loadtype)
        Energy_Error = Hys_Energy_Error(Energy_Error)
        print("\n", Energy_Error)
        Energy_Error = 0.001 

    #print('\n Converged R0 =', R0)
    
    # Plot the Results
    exper = pd.read_csv('model_results.txt', header=None, names=['d_mod', 'F_mod'])
    Force_mod = exper['F_mod']
    Disp_mod = exper['d_mod']
    plt.plot(Disp_mod, Force_mod, label = 'Model')
    
    # Add Experiment Results to graph
    exper = pd.read_csv('reference_FD.txt', header=None, names=['F_ref', 'd_ref'])
    Force_ref = exper['F_ref']
    Disp_ref = exper['d_ref']
    plt.plot(Disp_ref, Force_ref, label = 'Experiment')

    plt.xlabel("Displacement (in.)")
    plt.ylabel("Axial Force (kip)")
    plt.show()