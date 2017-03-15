#!/usr/bin/env python
import subprocess
import numpy as np
from tabulate import tabulate

USERNAME = 'bras37867'
JOBNUM_CMD = "qstat -u "+USERNAME+" | tail -n+3 | awk '{print $1}'"

jobnums = subprocess.check_output(JOBNUM_CMD, stderr=subprocess.STDOUT, shell=True).split()

headers = ["job num","mu","beta","state","out file", "current mag"]

jobs = []

for job in jobnums:
    job_name = subprocess.check_output("qstat -j "+job+" | grep job_name | awk '{print $2}'",
                                       stderr=subprocess.STDOUT,
                                       shell=True)
    running = subprocess.check_output("qstat -u bras37867 | grep "+job+" | awk '{print $5}'",
                                      stderr=subprocess.STDOUT,
                                      shell = True)[:-1]

    mu = float(job_name.split("_")[3][:-1])
    beta = float(job_name.split("_")[2])
    out_file = "B_"+str(beta)+"/MU_"+str(mu)+"/output*"

    if running is "r":
        current_mag = subprocess.check_output("cat "+out_file+" | grep Mag | awk '{print $2}' | tail -n 1",
                                              stderr=subprocess.STDOUT,
                                              shell=True)[:-1]
    else:
        current_mag = " "

    jobs.append([job, mu, beta, running, out_file, current_mag])

print tabulate(jobs, headers=headers, tablefmt='orgtbl')
