# Hysteretic Energy Error Calc
from openseespy.opensees import *
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math

def Hys_Energy_Error (Energy_Error):

    energy = np.loadtxt("ref_Energy.txt")
    #print(energy)
    exper_cycles = energy[:,0]
    last_cycle = exper_cycles.max()
    #print(last_cycle)

    model= pd.read_csv('model_results.txt', header=None, names=['d_mod', 'F_mod'])
    Force_mod = model['F_mod']
    Disp_mod = model['d_mod']
    model_results = np.array([Force_mod, Disp_mod])
    #print("\n", model_results)
    
    model_eng = np.array([0])
   # print(model_eng)
    num_rows, num_cols = model_results.shape
    #print(num_rows, num_cols)

    # Find Energy at Each step
    i = 1
    energy_step = 0
    while(i < num_cols):
        force_avg = (model_results[0,i]+model_results[0,i-1])/2
        #print(model_results[0,i])
        #print(model_results[0,i-1])
        #print(force_avg)
        ddisp = model_results[1,i]-model_results[1,i-1]
        #print(model_results[1,i])
        #print(model_results[1,i-1])
        #print(ddisp)
        energy_step = energy_step + force_avg*ddisp
        model_eng = np.append(model_eng, [energy_step], axis=0)
        #print(model_eng)
        i = i + 1
       # print(model_eng)

    # Find Energy at end of each cycle
    cycle = 1 
    i = 39
    cycle_eng = np.array([[0,0]])
    while (cycle <= last_cycle):
        cycle_eng = np.append(cycle_eng, [[cycle, model_eng[i]]], axis = 0)
        cycle = cycle + 1
        i = i + 40

    #print(cycle_eng)

    # calc error in energy calc
    i = 0 
    sum_sqrs = 0.
    while (i< last_cycle):
        error = abs((cycle_eng[i,1]-energy[i,1])/energy[i,1])
        sum_sqrs = sum_sqrs + math.sqrt(error**2)
        i = i+1
    
   # print(sum_sqrs)
    return(sum_sqrs)











