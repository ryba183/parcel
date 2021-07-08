import sys
sys.path.insert(0, "../")
sys.path.insert(0, "/home/piotr/Piotr/IGF/parcel3/parcel/plots/comparison")
sys.path.insert(0, "./")
sys.path.insert(0, "plots/comparison/")
sys.path.insert(0, "/home/piotr/Piotr/IGF/local_install/parcel/lib/python3/dist-packages")

from parcel import parcel
from libcloudphxx import common
from timestep_plot import timestep_plot
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from scipy.io import netcdf
import numpy as np
import pytest
import os, glob
import subprocess
import pdb
from math import exp, log, sqrt, pi, erf, ceil
plt.rcParams.update({'font.size': 18})



# TEST
n_tot=90e6
mean_r=0.08e-6
gstdev=exp(1.78)

n_tot2=15e6
mean_r2=0.24e-6
gstdev2=exp(1.25)

#TEST2
# n_tot=90e6
# mean_r=0.03e-6
# gstdev=exp(1.58)
#
# n_tot2=15e6
# mean_r2=0.44e-6
# gstdev2=exp(2.25)


def distribution(u, N, std, mean):

    # return (N/pow((2*pi),0.5)*std)*exp(-(pow((u-mean),2))/(2*std*std))
    I = N/(pow((2*pi),0.5)*u*log(std))
    II = pow(log(u)-log(mean),2)
    III = exp(-(II/(2*pow(log(std),2))))
    return I * III

def surface_distribution(u, N, std, mean):

    # return (N/pow((2*pi),0.5)*std)*exp(-(pow((u-mean),2))/(2*std*std))
    I = N*u*u*u*pi/(pow((2*pi),0.5)*log(std)*6)
    II = pow(log(u)-log(mean),2)
    III = exp(-(II/(2*pow(log(std),2))))
    return I * III

x=np.linspace(0.00001, 2000, num=100000)
Rozklad = np.zeros(len(x))
Rozklad2 = np.zeros(len(x))
Rozklad3 = np.zeros(len(x))
for i in range(len(x)):

    Rozklad[i] = surface_distribution(x[i], n_tot, gstdev, mean_r)
    Rozklad2[i] = surface_distribution(x[i], n_tot2, gstdev2, mean_r2)
    # Rozklad3[i] = surface_distribution(x[i], n_tot3, gstdev3, mean_r3)
    Rozklad[i] = Rozklad[i]# + Rozklad2[i]

plt.xscale('log')
plt.plot(x,Rozklad )
# plt.plot(x,Rozklad2 )
# plt.plot(x,Rozklad3 )
plt.savefig("dystrybucja.png")