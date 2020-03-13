# This Python file uses the following encoding: utf-8
import sys
sys.path.insert(0, "../../")
sys.path.insert(0, "../")
sys.path.insert(0, "./")

from scipy.io import netcdf
import numpy as np
import pytest
import subprocess
from libcloudphxx import common
import ast
import math
from parcel import parcel
import functions as fn

def plot_spectrum(data, data2,  outfolder):
    import Gnuplot

    g = Gnuplot.Gnuplot()# persist=1)
    g('set term svg dynamic enhanced')

    ymax = 1e4
    ymin = 1e-1

    rw = data.variables["wradii_r_wet"][:] * 1e6
    rd = data.variables["dradii_r_dry"][:] * 1e6

    rw2 = data2.variables["wradii_r_wet"][:] * 1e6
    rd2 = data2.variables["dradii_r_dry"][:] * 1e6

    #TODO - add test if it is == to dr in netcdf
    drw = np.empty(rw.shape)
    drw[0] = rw[0] - 0
    drw[1:] = (rw[1:] - rw[0:-1]) * 1e6

    drd = np.empty(rd.shape)
    drd[0] = rd[0] - 0
    drd[1:] = (rd[1:] - rd[0:-1]) * 1e6

    drw2 = np.empty(rw2.shape)
    drw2[0] = rw2[0] - 0
    drw2[1:] = (rw2[1:] - rw2[0:-1]) * 1e6

    drd2 = np.empty(rd2.shape)
    drd2[0] = rd2[0] - 0
    drd2[1:] = (rd2[1:] - rd2[0:-1]) * 1e6

    for t in range(data.variables['t'].shape[0]):

        g('set term svg dynamic enhanced')
        g('reset')
        g('set output "' + outfolder + 'plot_spec_' + str("%03d" % t) + '.svg"')
        # g('set logscale xy')
        # g('set ylabel "[mg^{-1} μm^{-1}]"')
        # g('set yrange [' +  str(ymin) + ':' + str(ymax) + ']')
        g('set yrange [1:200]')
        g('set xrange [0:15]')
        g('set grid')
        # g('set nokey')

        # FSSP range
        g('set arrow from .5,' + str(ymin) + 'to .5,' + str(ymax) + 'nohead')
        g('set arrow from 25,' + str(ymin) + 'to 25,' + str(ymax) + 'nohead')

        g('set xlabel "particle radius [μm]" ')

        nw = data.variables['wradii_m0'][t,:] / drw
        nd = data.variables['dradii_m0'][t,:] / drd

        plot_rw = Gnuplot.PlotItems.Data(rw, nw, with_="fsteps", title="1")
        plot_rd = Gnuplot.PlotItems.Data(rd, nd, with_="fsteps", title="dry radius")

        nw2 = data2.variables['wradii_m0'][t,:] / drw2
        nd2 = data2.variables['dradii_m0'][t,:] / drd2

        plot_rw2 = Gnuplot.PlotItems.Data(rw2, nw2, with_="fsteps", title="1/10")
        plot_rd2 = Gnuplot.PlotItems.Data(rd2, nd2, with_="fsteps", title="dry radius")



        g.plot(plot_rw, plot_rw2 , plot_rd)

def plot_init_spectrum(data, outfolder):
    """
    Plot the initial dry diameter distribution and compare it with the analitycal solution

    """
    import Gnuplot

    # size distribution parameters from Kreidenweis 2003
    # n_tot   = 90e6
    # mean_r  = 0.03e-6
    # gstdev  = 1.28
    # n_tot2   = 15e6
    # mean_r2  = 0.14e-6
    # gstdev2  = 1.75

    n_tot   = 125e6
    mean_r  = 0.011e-6
    gstdev  = 1.2
    n_tot2   = 65e6
    mean_r2  = 0.06e-6
    gstdev2  = 1.7


    # from ncdf file attributes read out_bin parameters as a dictionary ...
    out_bin = ast.literal_eval(getattr(data, "out_bin"))
    # ... and check if the spacing used in the test was logarithmic
    assert out_bin["wradii"]["lnli"] == 'log', "this test should be run with logarithmic spacing of bins"

    # parcel initial condition
    rd = data.variables["wradii_r_wet"][:] # left bin edges

    # for comparison, model solution needs to be divided by log(d2) - log(d2)
    # since the test is run with log spacing of bins log(d2) - log(d1) = const
    d_log_rd = math.log(rd[2], 10) - math.log(rd[1], 10)

    # initial size distribution from the model
    model = data.variables['wradii_m0'][0,:] * data.variables["rhod"][0] / d_log_rd

    # variables for plotting theoretical solution
    radii = np.logspace(-3, 1, 100) * 1e-6
    theor = np.empty(radii.shape)
    theor2 = np.empty(radii.shape)
    for it in range(radii.shape[0]):
        theor[it] = fn.log10_size_of_lnr(n_tot, mean_r, math.log(radii[it], 10), gstdev)
        theor2[it] = fn.log10_size_of_lnr(n_tot2, mean_r2, math.log(radii[it], 10), gstdev2)
    g = Gnuplot.Gnuplot()
    g('set term svg dynamic enhanced')
    g('reset')
    g('set output "' + outfolder + '/init_spectrum.svg" ')
    g('set logscale x')
    g('set xlabel "particle dry diameter [μm]" ')
    g('set ylabel "dN/dlog_{10}(D) [cm^{-3} log_{10}(size interval)]"')
    g('set grid')
    g('set xrange [0.001:10]')
    g('set yrange [0:800]')

    theory_r = Gnuplot.PlotItems.Data(radii * 2 * 1e6,  theor * 1e-6, with_="lines", title="theory")
    theory_r2 = Gnuplot.PlotItems.Data(radii * 2 * 1e6,  theor2 * 1e-6, with_="lines", title="theory2")
    plot     = Gnuplot.PlotItems.Data(rd    * 2 * 1e6,  model * 1e-6, with_="steps", title="model" )

    g.plot(theory_r, theory_r2, plot)

def main():


    RH_init = .98
    T_init  = 298.
    p_init  = 100000.
    r_init  = common.eps * RH_init * common.p_vs(T_init) / (p_init - RH_init * common.p_vs(T_init))
    outfile = "test_spectrum.nc"
    outfile2 = "test_spectrum2.nc"
    out_bin = '{"wradii": {"rght": 1e-4, "left": 1e-9, "drwt": "wet", "lnli": "lin", "nbin": 100, "moms": [0]},\
                "dradii": {"rght": 1e-6, "left": 1e-9, "drwt": "dry", "lnli": "lin", "nbin": 100, "moms": [0]}}'

    # run parcel run!
    parcel(dt = 1, T_0 = T_init, p_0 = p_init, RH_0 = .98, sstp_cond =1, z_max = 200, w=5,  sd_conc = 10000, outfreq = 1, aerosol = '{"ammonium_sulfate": {"kappa": 0.61, "mean_r": [0.03e-6, 0.14e-6], "gstdev": [1.28, 1.75], "n_tot": [90e6, 15e6]}}', outfile = outfile, out_bin = out_bin)
    parcel(dt = 1, T_0 = T_init, p_0 = p_init, RH_0 = .98, sstp_cond =10, z_max = 200, w=5,  sd_conc = 10000, outfreq = 1, aerosol = '{"ammonium_sulfate": {"kappa": 0.61, "mean_r": [0.03e-6, 0.14e-6], "gstdev": [1.28, 1.75], "n_tot": [90e6, 15e6]}}', outfile = outfile2, out_bin = out_bin)

    data = netcdf.netcdf_file(outfile, "r")
    data2 = netcdf.netcdf_file(outfile2, "r")
    # plotting
    plot_spectrum(data, data2, outfolder="../outputs/")
    # doing plotting
    plot_init_spectrum(data, outfolder="../outputs/")

    # cleanup
    subprocess.call(["rm", outfile])

if __name__ == '__main__':
    main()