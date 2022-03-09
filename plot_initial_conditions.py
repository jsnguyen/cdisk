import os
import pickle
from glob import glob
from multiprocessing import Pool

from PIL import Image

import numpy as np

from matplotlib import pyplot as plt
import matplotlib.cm as cm
import matplotlib.animation as animation
from matplotlib import font_manager
from matplotlib.colors import LogNorm

from tqdm import tqdm

def scale_height(r, params):
    return r*params['AspectRatio']

def soundspeed(r, params, sim_units):
    omega = np.sqrt(sim_units['G']*sim_units['mass']/r/r/r)
    h = scale_height(r, params)
    cs = h/omega
    return cs

def initial_density(r, params, sim_units):
    h = scale_height(r, params)
    cs = soundspeed(r, params, sim_units)
    viscosity = params['Alpha']*cs*h

    g_per_MJ = 1.899e+30
    cm_per_AU = 1.496e+13

    rho = (params['MassAccretion']*sim_units['mass']/sim_units['time'] / (3*np.pi*viscosity)) * (np.sqrt(params['Ymax']*sim_units['length']/r) - 1) * g_per_MJ/(cm_per_AU*cm_per_AU)

    return rho

def initial_vphi(r, params, sim_units):
    vk = np.sqrt(sim_units['G']*sim_units['mass']/r)
    vphi = vk * (1 - (13/8)*params['AspectRatio']*params['AspectRatio']) - params['OmegaFrame']*r

    return vphi

def initial_vr(r, params, sim_units):
    rho = initial_density(r, params, sim_units)
    vr = params['MassAccretion']*sim_units['mass']/sim_units['time'] / (2*np.pi*r*rho)

    return vr

def main():

    par_pickle_filename = 'cdi.par.pickle'
    with open(par_pickle_filename, 'rb') as f:
        params = pickle.load(f)

    sim_units_pickle_filename = 'sim_units.pickle'
    with open(sim_units_pickle_filename, 'rb') as f:
        sim_units = pickle.load(f)

    fig, ax = plt.subplots(figsize=(4,4))
    r = np.linspace(params['Ymin']*sim_units['length'], params['Ymax']*sim_units['length'], 100)
    rho = initial_density(r, params, sim_units)

    ax.plot(r, rho)
    ax.set_xscale('log')
    ax.set_yscale('log')
    plt.show()



if __name__=='__main__':
    main()
