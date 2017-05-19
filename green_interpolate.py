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
old_beta = float(args[3])
new_beta = float(args[4])

print "infile: ", file_name, "out_file: ", output_file, "old_beta: ", old_beta, "new_beta: ", new_beta

Archive = HDFArchive(file_name, 'r')
G_orig = Archive["dmft"]["G0_iw"]

orig_data = G_orig['up'].data
first_ind = G_orig['up'].mesh.first_index()
last_ind = G_orig['up'].mesh.last_index()

old_mesh = np.array([iw(n,old_beta) for n in np.arange(first_ind,last_ind+1,1)])
new_mesh = np.array([iw(n,new_beta) for n in np.arange(first_ind,last_ind+1,1)])

orig_data = orig_data.reshape(512)



# x = np.linspace(0, 2*np.pi, 10)
# y = np.sin(x)
# xvals = np.linspace(0, 2*np.pi, 50)

# yinterp = np.interp(xvals, x, y)

# plt.plot(x, y, 'o')
# plt.plot(xvals, yinterp, '-x')

plt.show()
