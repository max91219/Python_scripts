#!/usr/bin/env python
import os
import glob
import numpy as np
import subprocess

FILE_NAME = "beta_t_mag.dat"

files = glob.glob("mag_files/*.dat")

datapoints = []

for f in files:
    beta = float(f.split("/")[1].split("_")[1])
    mu = float(f.split("/")[1].split("_")[2][:-4])
    T = 1.0/beta
    mag = float(subprocess.check_output(['tail', '-1', f])[:-1])
    datapoints.append([beta,T,mu,mag])

mu_vals = list(set([x[2] for x in datapoints]))
mu_vals.sort()

print mu_vals

if os.path.isfile(FILE_NAME):
    os.remove(FILE_NAME)

with open(FILE_NAME, 'w') as f :
    f.write("#beta T mag\n\n\n")
    for mu in mu_vals:
        f.write('"Mu = '+str(mu)+'"\n')
        points = [x for x in datapoints if x[2] == mu]
        points.sort(key = lambda x : x[0])

        for p in points:
            f.write("{:10.7f} {:10.7f} {:10.7f}\n".format(p[0],p[1],p[3]))

        f.write("\n\n")

    f.close()
