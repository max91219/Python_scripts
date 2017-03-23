#!/usr/bin/env python
import os
import glob
import numpy as np

if not os.path.isdir(os.getcwd()+"/mag_files"):
    os.makedirs(os.getcwd()+"/mag_files")

for f in glob.glob(os.getcwd()+"/B_*/MU_*.*/output_*"):
    beta = float(f.split("/")[-1].split("_")[3])
    mu = float(f.split("/")[-1].split("_")[4][:-4])

    #print beta, mu

    if os.path.isfile(os.getcwd()+"/mag_files/mag_"+str(beta)+"_"+str(mu)+".dat"):
        os.remove(os.getcwd()+"/mag_files/mag_"+str(beta)+"_"+str(mu)+".dat")

    #os.system("cat "+f+" | grep Mag | awk '{print $2}' >> mag_files/mag_"+str(beta)+"_"+str(mu)+".dat")
    os.system("cat "+f+" | grep Sz | awk '{print 2.0*$8}' >> mag_files/mag_"+str(beta)+"_"+str(mu)+".dat")
