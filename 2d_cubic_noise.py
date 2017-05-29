import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy.special import ellipk

args = sys.argv
file_name = args[1]
grid_start = float(args[2])
grid_end = float(args[3])
num_points = int(args[4])
plot_dos = True if str(args[5]) == '1' else False
add_noise = True if str(args[6]) == '1' else False
noise_sd = float(args[7])
dump = True if str(args[8]) == '1' else False

eps_vals, dos = np.loadtxt(file_name,unpack=True)

print "plot_dos: ", plot_dos, "add_noise", add_noise,"dump", dump

grid = np.array(range(-num_points,num_points + 1))
vals = np.zeros(2*num_points+1)
data = np.transpose(np.array([grid,vals]))

print "total points", 2*num_points

for id, x in enumerate(data):
    if data[id][0] == 0: continue
    data[id][0] = (data[id][0]/num_points)*4.0
    data[id][1] = (0.5/(np.pi*np.pi)) * ellipk(1.0 - (data[id][0]*data[id][0])/16.0)

data = np.delete(data,num_points,0)
eps = np.transpose(data)[0]
dos = np.transpose(data)[1]

norm = np.trapz(dos,eps)

dos = dos/norm

if add_noise:
    print "noise_sd", noise_sd
    noise = np.random.normal(0,noise_sd,len(data))
    dos = dos + noise

eps_int = np.trapz(eps*dos,eps)
eps_sq_int = np.trapz(np.square(eps)*dos,eps)

print np.trapz(dos,eps), eps_int, eps_sq_int

if dump:
    data = np.transpose(np.array([eps,dos]))
    pre = "2d_cubic_dos_" + str(2*num_points)
    post = ".txt" if not add_noise else "_" + str(noise_sd) + ".txt"
    np.savetxt(pre+post,data)

if plot_dos:
    plt.plot(eps, dos, '-', label='No Noise')
    plt.show()
