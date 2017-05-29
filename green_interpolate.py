import sys
import numpy as np
from math import pi
import matplotlib
import matplotlib.pyplot as plt
from pytriqs.gf.local import *
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
G0_iw_old = Archive["dmft"]["G0_iw"]

old_beta = G0_iw_old['up'].mesh.beta
n_iw = G0_iw_old['up'].mesh.last_index() + 1

print "infile: ", file_name, "out_file: ", output_file, "old_beta: ", old_beta, "new_beta: ", new_beta, "n_iw: ", n_iw

G0_iw = GfImFreq(indices = [0], beta = new_beta, n_points = n_iw)
G0_iw_new = BlockGf(name_list = ('up','down'), block_list = (G0_iw,G0_iw), make_copies = True)

old_data_up = G0_iw_old['up'].data.reshape(2*n_iw)
old_data_down = G0_iw_old['down'].data.reshape(2*n_iw)

# Strip out real and imag parts
old_data_up_im = np.array([x.imag for x in old_data_up])
old_data_up_re = np.array([x.real for x in old_data_up])
old_data_down_im = np.array([x.imag for x in old_data_down])
old_data_down_re = np.array([x.real for x in old_data_down])

old_mesh = np.array([iw(n,old_beta) for n in np.arange(-n_iw,n_iw,1)])
new_mesh = np.array([iw(n,new_beta) for n in np.arange(-n_iw,n_iw,1)])

#Check if the new mesh will extend beyond the old mesh
if (new_beta > old_beta):
    new_data_up_re = np.interp(new_mesh,old_mesh,old_data_up_re)
    new_data_up_im = np.interp(new_mesh,old_mesh,old_data_up_im)
    new_data_down_re = np.interp(new_mesh,old_mesh,old_data_down_re)
    new_data_down_im = np.interp(new_mesh,old_mesh,old_data_down_im)

    for p in range(0, 2*n_iw):
        G0_iw_new['up'].data[p,0,0] = new_data_up_re[p] + 1j * new_data_up_im[p]
        G0_iw_new['down'].data[p,0,0] = new_data_down_re[p] + 1j * new_data_down_im[p]

    # plt.plot(old_mesh, old_data_up_re, 'o')
    # plt.plot(old_mesh, old_data_up_im, 'o')
    # plt.plot(new_mesh, new_data_up_re, 'x')
    # plt.plot(new_mesh, new_data_up_im, 'x')
    # plt.plot(old_mesh, old_data_down_re, 'o')
    # plt.plot(old_mesh, old_data_down_im, 'o')
    # plt.plot(new_mesh, new_data_down_re, 'x')
    # plt.plot(new_mesh, new_data_down_im, 'x')

    # plt.show()
else:

    # transpose the data and mesh together
    grouped_data = np.array([new_mesh, old_mesh, old_data_up_re, old_data_up_im, old_data_down_re, old_data_down_im]).T

    # split the new grid into parts off the old grid and parts in the old grid along with coressponding data
    new_in_old = np.array([x for x in grouped_data if x[0] < old_mesh[-1] and x[0] > old_mesh[0]])
    new_before_old = np.array([x for x in grouped_data if x[0] < old_mesh[0]])
    new_after_old = np.array([x for x in grouped_data if x[0] > old_mesh[-1]])

    # Unpack the data that is in the old grid and interpolate in the same way as above
    new_points = np.transpose(new_in_old)[0]
    old_points = np.transpose(new_in_old)[1]
    old_data_up_re = np.transpose(new_in_old)[2]
    old_data_up_im = np.transpose(new_in_old)[3]
    old_data_down_re = np.transpose(new_in_old)[4]
    old_data_down_im = np.transpose(new_in_old)[5]

    new_data_up_re = np.interp(new_points,old_points,old_data_up_re)
    new_data_up_im = np.interp(new_points,old_points,old_data_up_im)
    new_data_down_re = np.interp(new_points,old_points,old_data_down_re)
    new_data_down_im = np.interp(new_points,old_points,old_data_down_im)

    # Rebuild the data a put it into a greens functions with smaller number of freqs
    new_data_up = new_data_up_re + 1j * new_data_up_im
    new_data_down = new_data_down_re + 1j * new_data_down_im

    G0_iw_red_up = GfImFreq(indices = [0], beta = new_beta, n_points = n_iw - len(new_before_old))
    G0_iw_red_down = GfImFreq(indices = [0], beta = new_beta, n_points = n_iw - len(new_before_old))

    #fill the reduced greens function
    for p in range(0, 2*(n_iw - len(new_before_old))):
        G0_iw_red_up.data[p,0,0] = new_data_up[p]
        G0_iw_red_down.data[p,0,0] = new_data_down[p]

    G0_iw_red_up.tail.zero()
    G0_iw_red_down.tail.zero()

    fixed_coeff = TailGf(1,1,3,-1)
    fixed_coeff[-1] = np.array([[0.]])
    fixed_coeff[0] = np.array([[0.]])
    fixed_coeff[1] = np.array([[1.]])

    fit_max_moment = 4
    fit_stop = n_iw - len(new_before_old)
    fit_start = int(0.8*fit_stop)

    G0_iw_red_up.fit_tail(fixed_coeff, fit_max_moment, fit_start, fit_stop)
    G0_iw_red_down.fit_tail(fixed_coeff, fit_max_moment, fit_start, fit_stop)

    # Now fit the part outside the old grid
    new_points_before = np.transpose(new_before_old)[0]
    new_points_after = np.transpose(new_after_old)[0]

    before_data_up = []
    after_data_up = []
    before_data_down = []
    after_data_down = []

    for p in new_points_before:
        before_data_up.append(G0_iw_red_up.tail(1j*p)[0][0])
        before_data_down.append(G0_iw_red_down.tail(1j*p)[0][0])

    for p in new_points_after:
        after_data_up.append(G0_iw_red_up.tail(1j*p)[0][0])
        after_data_down.append(G0_iw_red_down.tail(1j*p)[0][0])

    before_data_up = np.array(before_data_up)
    before_data_down = np.array(before_data_down)
    after_data_up = np.array(after_data_up)
    after_data_down = np.array(after_data_down)

    # Concatonate the data back together
    new_up_data = np.concatenate([before_data_up,new_data_up,after_data_up])
    new_down_data = np.concatenate([before_data_down,new_data_down,after_data_down])
    new_mesh = np.concatenate([new_points_before,np.transpose(new_in_old)[0],new_points_after])

    for p in range(0, 2*n_iw):
        G0_iw_new['up'].data[p,0,0] = new_up_data[p]
        G0_iw_new['down'].data[p,0,0] = new_down_data[p]

    # oplot(G0_iw_new['up'], 'o')
    # oplot(G0_iw_new['down'], 'o')
    # plt.plot(new_mesh, new_up_data.real, 'x')
    # plt.plot(new_mesh, new_up_data.imag, 'x')
    # plt.plot(new_mesh, new_down_data.real, 'x')
    # plt.plot(new_mesh, new_down_data.imag, 'x')

    # plt.show()


# Now put the results into the output file
out_archive = HDFArchive(output_file, 'w')
out_archive.create_group("dmft")
out_archive['dmft']["G0_iw"] = G0_iw_new
