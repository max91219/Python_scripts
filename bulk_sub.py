#!/usr/bin/env python
import numpy as np
from shutil import copy, copyfile
import os

SUBMIT_SCRIPT='/home/dirac/tmcs/bras37867/CTHYB_SEGMENT/executables/runs/FCC_hubbard_t_prime/test/submit_DMFT.sh'
SUBMIT_SCRIPT_NAME = 'submit_DMFT.sh'

mu_list = [14.0]
beta_list = np.arange(6.25,7.25,0.25)

print "beta vals: ", beta_list
print "mu vals: ", mu_list

cwd = os.getcwd()

for beta in beta_list:
    for mu in mu_list:
        directory = '/'.join([cwd,"B_"+str(beta),'MU_'+str(mu)])

        # Make the directory if it doesnt exist
        if not os.path.exists(directory):
            os.makedirs(directory)

        # edit and move the submit script
        with open(SUBMIT_SCRIPT) as orig_f:
            with open(directory+'/'+SUBMIT_SCRIPT_NAME, "w") as new_file:
                for line in orig_f:
                    if "#$ -N" in line:
                        line = '#$ -N U_21_' + str(beta) + '_' + str(mu) + '\n'

                    new_file.write(line)

        # Copy what is needed to the new directory
        copy(cwd+'/anderson_FCC',directory)
        copy(cwd+'/fcc_dos.dat',directory)

        # Change to the new directory and submit the job
        os.chdir(directory)
        #print 'qsub ' + SUBMIT_SCRIPT_NAME + ' --U 21.0 --mu ' + str(mu) + ' --beta ' + str(beta) + ' --n_cycles 15000000 --warmup_cycles 1000000 --length_cycle 10 --dmft_loops 30 --n_g_l 40 --do_dmft'
        os.system('qsub ' + SUBMIT_SCRIPT_NAME + ' --U 21.0 --mu ' + str(mu) + ' --beta ' + str(beta) + ' --n_cycles 15000000 --warmup_cycles 1000000 --length_cycle 10 --dmft_loops 100 --n_g_l 35 --do_dmft' )

        #change back to cwd
        os.chdir(cwd)
