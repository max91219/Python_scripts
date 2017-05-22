import sys
import numpy as np
from math import pi
import matplotlib
import matplotlib.pyplot as plt
from pytriqs.gf.local import GfImFreq, GfReFreq
from pytriqs.archive import HDFArchive
from pytriqs.gf.local.descriptors import SemiCircular
from pytriqs.plot.mpl_interface import oplot, plt

def iw(n,b):
    return (2.0*n+1)*np.pi/b

args = sys.argv
file_name = args[1]
output_file = args[2]
new_beta = float(args[3])

Archive = HDFArchive(file_name, 'r')
G_orig = Archive["dmft"]["G0_iw"]

old_beta = G_orig['up'].mesh.beta

print "infile: ", file_name, "out_file: ", output_file, "old_beta: ", old_beta, "new_beta: ", new_beta

old_data = G_orig['up'].data
first_ind = G_orig['up'].mesh.first_index()
last_ind = G_orig['up'].mesh.last_index()

old_mesh = np.array([iw(n,old_beta) for n in np.arange(first_ind,last_ind+1,1)])
new_mesh = np.array([iw(n,new_beta) for n in np.arange(first_ind,last_ind+1,1)])

old_data = old_data.reshape(old_data.shape[0])
old_data_im = np.array([x.imag for x in old_data])
old_data_re = np.array([x.real for x in old_data])

if (new_beta > old_beta):
    new_data_re = np.interp(new_mesh,old_mesh,old_data_re)
    new_data_im = np.interp(new_mesh,old_mesh,old_data_im)

    plt.plot(old_mesh, old_data_re, 'o')
    plt.plot(old_mesh, old_data_im, 'o')
    plt.plot(new_mesh, new_data_re, 'x')
    plt.plot(new_mesh, new_data_im, 'x')

    plt.show()

else :
    print "Not implemented yet for smaller beta"
    exit()
