# Timber Buckling Restrained Brace (T_BRB)
    # Based on Colton Murphy's Paper ---> TBRB-1 (Fatigue Control)
    
from openseespy.opensees import *
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def TBRB (length, lcore, LR_BRB, swidth, sthick, Acore, sFy, wwidth, 
                      wthick, E, R0, cR1, cR2, a1, a2, a3, a4, si, pEnvelopeStress,
                      nEnvelopeStress, pEnvelopeStrain, nEnvelopeStrain, 
                      rDisp, rForce, uForce, loadtype):

    wipe()

    # Model Set Up
    model('basic', '-ndm', 2, '-ndf', 3)

    # Nodes
    node(1, 0.0, 0.0)
    node(2, 0.0, length)

    # Boundary Conditions
    fix(1, 1, 1, 1)
    fix(2, 0, 0, 1)

    # Define Materials
    BRB_Material_1 = 101
    BRB_Material_2 = 102
    BRB_Material_3 = 103
    BRB_Material_4 = 104

    # Steel Material
    Eequ = E/LR_BRB
    params = [R0, cR1, cR2]

    uniaxialMaterial("Steel02", BRB_Material_1, sFy, Eequ, 0.0001, R0, cR1, cR2, a1, a2, a3, a4, si)

    gammaK = [0.5, 0.1, 0.15, 0.1, 0.45]
    gammaD = [0.0, 0.0, 0.0, 0.0, 0.0]
    gammaF = [0.0, 0.0, 0.0, 0.0, 0.0]
    gammaE = 10

    dam = "cycle"

    uniaxialMaterial("Pinching4", BRB_Material_2, pEnvelopeStress[0], pEnvelopeStrain[0], pEnvelopeStress[1], pEnvelopeStrain[1], pEnvelopeStress[2], pEnvelopeStrain[2], pEnvelopeStress[3], pEnvelopeStrain[3], nEnvelopeStress[0], nEnvelopeStrain[0], nEnvelopeStress[1], nEnvelopeStrain[1], nEnvelopeStress[2], nEnvelopeStrain[2], nEnvelopeStress[3], nEnvelopeStrain[3], rDisp[0], rForce[0], uForce[0], rDisp[1], rForce[1], uForce[1], gammaK[0], gammaK[1], gammaK[2], gammaK[3], gammaK[4], gammaD[0], gammaD[1], gammaD[2], gammaD[3], gammaD[4], gammaF[0], gammaF[1], gammaF[2], gammaF[3], gammaF[4], gammaE, dam)

    # Parallel Material
    uniaxialMaterial('Parallel', BRB_Material_3, BRB_Material_1, BRB_Material_2)

    # Fatigue Material
    E0 = 0.084
    m = -0.44
    mini = -0.035
    maxi = 0.035

    uniaxialMaterial("Fatigue", BRB_Material_4, BRB_Material_3, '-E0', E0, '-m', m, '-min', mini, '-max', maxi)

    # Create T-BRB Element
    element("corotTruss", 1, 1, 2, Acore, BRB_Material_4)
    print('The Model is Built')

    # Set up Load and Analysis
    axial = -1.0
    timeSeries("Linear", 1)
    pattern("Plain", 1, 1)
    load(2, 0.0, axial, 0.0)

    system("UmfPack")
    constraints("Transformation")
    numberer("RCM")
    test("EnergyIncr", 1.0e-9, 1000)
    algorithm("KrylovNewton")
    analysis("Static")
    print("Beginning Cyclic Loading")

    # Cyclic Loading Protocal
    ControlNode = 2
    ControlDOF = 2
    Nsteps = 20
    data = np.array([[0,0]])

    if (loadtype == 2):        
        dr_half = [0.5, -1.0, 0.5, 0.5, -1.0, 0.5]
        for Dincr in dr_half:
            incr = 0.05*0.01*Dincr*128.0
            integrator("Displacement Control", ControlNode, ControlDOF, incr)
            for j in range(Nsteps):
                analyze(1)
                disp = nodeDisp(2,2)
                force = -eleForce(1,2)
                data = np.append(data, [[disp, force]], axis=0)
        
        #print("2 Cycles Complete")

        dr_one = [1.0, -2.0, 1.0, 1.0, -2.0, 1.0]
        for Dincr in dr_one:
            incr = 0.05*0.01*Dincr*128.0
            integrator("Displacement Control", ControlNode, ControlDOF, incr)
            for j in range(Nsteps):
                analyze(1)
                data = np.append(data, [[nodeDisp(2,2), -eleForce(1,2)]], axis=0)

        #print("4 Cycles Complete")

        dr_onehalf = [1.5, -3.0, 1.5, 1.5, -3.0, 1.5]
        for Dincr in dr_onehalf:
            incr = 0.05*0.01*Dincr*128.0
            integrator("Displacement Control", ControlNode, ControlDOF, incr)
            for j in range(Nsteps):
                analyze(1)
                data = np.append(data, [[nodeDisp(2,2), -eleForce(1,2)]], axis=0)

        #print("6 Cycles Complete")

        dr_two = [2.0, -4.0, 2.0, 2.0, -4.0, 2.0]
        for Dincr in dr_two:
            incr = 0.05*0.01*Dincr*128.0
            integrator("Displacement Control", ControlNode, ControlDOF, incr)
            for j in range(Nsteps):
                analyze(1)
                data = np.append(data, [[nodeDisp(2,2), -eleForce(1,2)]], axis=0)

        #print("8 Cycles Complete")
        # Fatigue Cycles
        cycle = 9
        while(cycle < 42):
            dr_fatigue = [1.5, -3.0, 1.5]
            for Dincr in dr_one:
                incr = 0.05*0.01*Dincr*128.0
                integrator("Displacement Control", ControlNode, ControlDOF, incr)
                for j in range(Nsteps):
                    analyze(1)
                    data = np.append(data, [[nodeDisp(2,2), -eleForce(1,2)]], axis=0)
                    #print("Cycle ", cycle, "complete")
                    cycle = cycle + 1    
    else:
        dr_half = [0.5, -1.0, 0.5, 0.5, -1.0, 0.5]
        for Dincr in dr_half:
            incr = 0.05*0.01*Dincr*128.0
            integrator("Displacement Control", ControlNode, ControlDOF, incr)
            for j in range(Nsteps):
                analyze(1)
                disp = nodeDisp(2,2)
                force = -eleForce(1,2)
                data = np.append(data, [[disp, force]], axis=0)
                    
                    #print("2 Cycles Complete")

        dr_one = [1.0, -2.0, 1.0, 1.0, -2.0, 1.0]
        for Dincr in dr_one:
            incr = 0.05*0.01*Dincr*128.0
            integrator("Displacement Control", ControlNode, ControlDOF, incr)
            for j in range(Nsteps):
                analyze(1)
                data = np.append(data, [[nodeDisp(2,2), -eleForce(1,2)]], axis=0)

            #print("4 Cycles Complete")

        dr_onehalf = [1.5, -3.0, 1.5, 1.5, -3.0, 1.5]
        for Dincr in dr_onehalf:
            incr = 0.05*0.01*Dincr*128.0
            integrator("Displacement Control", ControlNode, ControlDOF, incr)
            for j in range(Nsteps):
                analyze(1)
                data = np.append(data, [[nodeDisp(2,2), -eleForce(1,2)]], axis=0)

            #print("6 Cycles Complete")

        dr_two = [2.0, -4.0, 2.0, 2.0, -4.0, 2.0]
        for Dincr in dr_two:
            incr = 0.05*0.01*Dincr*128.0
            integrator("Displacement Control", ControlNode, ControlDOF, incr)
            for j in range(Nsteps):
                analyze(1)
                data = np.append(data, [[nodeDisp(2,2), -eleForce(1,2)]], axis=0)

        dr_two = [2.5, -5.0, 2.5, 2.5, -5.0, 2.5]
        for Dincr in dr_two:
            incr = 0.05*0.01*Dincr*128.0
            integrator("Displacement Control", ControlNode, ControlDOF, incr)
            for j in range(Nsteps):
                analyze(1)
                data = np.append(data, [[nodeDisp(2,2), -eleForce(1,2)]], axis=0)                    

        dr_two = [3.0, -6.0, 3.0, 3.0, -6.0, 3.0]
        for Dincr in dr_two:
            incr = 0.05*0.01*Dincr*128.0
            integrator("Displacement Control", ControlNode, ControlDOF, incr)
            for j in range(Nsteps):
                analyze(1)
                data = np.append(data, [[nodeDisp(2,2), -eleForce(1,2)]], axis=0)
 
        dr_two = [3.5, -7.0, 3.5, 3.5, -7.0, 3.5]
        for Dincr in dr_two:
            incr = 0.05*0.01*Dincr*128.0
            integrator("Displacement Control", ControlNode, ControlDOF, incr)
            for j in range(Nsteps):
                analyze(1)
                data = np.append(data, [[nodeDisp(2,2), -eleForce(1,2)]], axis=0)
                    
        dr_two = [4.0, -8.0, 4.0, 4.0, -8.0, 4.0]
        for Dincr in dr_two:
            incr = 0.05*0.01*Dincr*128.0
            integrator("Displacement Control", ControlNode, ControlDOF, incr)
            for j in range(Nsteps):
                analyze(1)
                data = np.append(data, [[nodeDisp(2,2), -eleForce(1,2)]], axis=0)                   
                    
    # Print Model Results to File
    a_file = open('model_results.txt', 'w')
    np.savetxt(a_file, data, delimiter=",")
    
    Force = np.array([data[:,1]])
    Max_Ten = Force.max()
    Max_Comp = Force.min()
    max_min = np.array([Max_Ten, Max_Comp])
    
    return(max_min)
    











































