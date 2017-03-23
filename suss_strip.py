#!/usr/bin/env python
import os
import glob
import subprocess
import numpy as np

FILE_NAME = "beta_t_suss.dat"

points=[]

for f in glob.glob(os.getcwd()+"/B_*/MU_*.*/output_*"):
    beta = float(f.split("/")[-1].split("_")[3])
    mu = float(f.split("/")[-1].split("_")[4][:-4])

    try:
        g_point_entry = float(subprocess.check_output("cat "+f+" | grep chiG | awk '{print $2}' | tr -d '()' | awk -F ',' '{print $1}'", shell=True)[:-1])
    except Exception:
        g_point_entry = 0.0

    try:
        x_point_entry = float(subprocess.check_output("cat "+f+" | grep chiX | awk '{print $2}' | tr -d '()' | awk -F ',' '{print $1}'", shell=True)[:-1])
    except Exception:
        x_point_entry = 0.0

    try:
        l_point_entry = float(subprocess.check_output("cat "+f+" | grep chiL | awk '{print $2}' | tr -d '()' | awk -F ',' '{print $1}'", shell=True)[:-1])
    except Exception:
        l_point_entry = 0.0

    points.append([float(mu),float(beta),g_point_entry,x_point_entry,l_point_entry])


mu_vals = list(set([x[0] for x in points]))
mu_vals.sort()

print mu_vals

if os.path.isfile(FILE_NAME):
    os.remove(FILE_NAME)

with open(FILE_NAME, 'w') as f :
    f.write("#beta T G X L\n\n\n")
    for mu in mu_vals:
        f.write('"Mu = '+str(mu)+'"\n')
        data = [x for x in points if x[0] == mu]
        data.sort(key = lambda x : x[1])

        for p in data:
            f.write("{:10.7f} {:10.7f} {:10.7f} {:10.7f} {:10.7f}\n".format(p[1], 1.0/p[1], p[2], p[3], p[4]))

        f.write("\n\n")

    f.close()
