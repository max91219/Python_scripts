#!/usr/bin/env python
import numpy as np
from shutil import copy, copyfile
import os

#SUBMIT_SCRIPT='/home/dirac/tmcs/bras37867/CTHYB_SEGMENT/executables/runs/FCC_hubbard_t_prime/test/submit_DMFT.sh'
SUBMIT_SCRIPT='/home/dirac/tmcs/bras37867/CTHYB_SEGMENT/executables/runs/FCC_hubbard_t_prime/U_21_restart/long_cycle_length/l_200/submit_DMFT.sh'
SUBMIT_SCRIPT_NAME = 'submit_DMFT.sh'

mu_list = [14.0]
#beta_list = [8.5,9.0]
#beta_list = []
beta_list = np.arange(6.0,7.0,0.1)

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
        #copy(cwd+'/fcc_dos.dat',directory)
        copy(cwd+'/dos.dat',directory)

        # Change to the new directory and submit the job
        os.chdir(directory)
        #print 'qsub ' + SUBMIT_SCRIPT_NAME + ' --U 21.0 --mu ' + str(mu) + ' --beta ' + str(beta) + ' --n_cycles 15000000 --warmup_cycles 1000000 --length_cycle 10 --dmft_loops 30 --n_g_l 40 --do_dmft'
        os.system('qsub ' + SUBMIT_SCRIPT_NAME + ' --U 21.0 --mu ' + str(mu) + ' --beta ' + str(beta) + ' --n_cycles 10000000 --warmup_cycles 1000000 --length_cycle 200 --dmft_loops 50 --n_g_l 35 --do_dmft --no_enforce_spin_symm --n_vertex_cycles 20000000 --legendre_chi --n_g4_l 35 ')
        #os.system('qsub ' + SUBMIT_SCRIPT_NAME + ' --U 21.0 --mu ' + str(mu) + ' --beta ' + str(beta) + ' --n_cycles 40000000 --warmup_cycles 1000000 --length_cycle 10 --dmft_loops 100 --n_g_l 35 --do_dmft --no_enforce_spin_symm --legendre_chi' )

        #change back to cwd
        os.chdir(cwd)
