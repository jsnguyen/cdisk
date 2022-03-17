import os
import pickle
from glob import glob
import argparse
from multiprocessing import Pool

import numpy as np

from matplotlib import pyplot as plt
import matplotlib.cm as cm
import matplotlib.animation as animation
from matplotlib import font_manager
from matplotlib.colors import LogNorm

from tqdm import tqdm

from units import *
from cdisk_analysis import *

def main():
    parser = argparse.ArgumentParser(description='Plot cdisk plots.')
    parser.add_argument('--runfolder', default=None, help='plot a specific run')
    args = parser.parse_args()

    par_pickle_filename = 'cdi.par.pickle'
    with open(par_pickle_filename, 'rb') as f:
        parameters = pickle.load(f)

    prepath = str(os.path.expanduser('~'))
    data_folder = prepath+'/landing/data/'

    if args.runfolder is not None:
        run_folder = args.runfolder
    else:
        latest_run_folder = sorted(glob(os.path.join(data_folder,'cdi_*')))[-1]
        run_folder = latest_run_folder

    print('Plotting run folder -> {}'.format(run_folder))

    n_frames = len(glob(os.path.join(run_folder,'gasdens*.dat')))-1
    data_files = [os.path.join(run_folder, 'gasdens{}.dat') for i in range(n_frames)]

    host_star_data_path = os.path.join(run_folder,'planet0.dat')
    satellite_data_path = os.path.join(run_folder,'planet1.dat')
    orbit_data_path = os.path.join(run_folder,'orbit0.dat')

    host_star, host_star_orbit = read_planet_orbit_data(host_star_data_path, orbit_data_path)
    if os.path.exists(satellite_data_path):
        satellite, satellite_orbit = read_planet_orbit_data(satellite_data_path, orbit_data_path)
    else:
        satellite = None

    plot_params=[]
    print('Loading in {} data frames...'.format(n_frames))
    for i in tqdm(range(len(data_files))):

        data_filename = 'gasdens{}.dat'.format(i)
        data_path = os.path.join(run_folder, data_filename)
        phi, r, density = read_fargo_data(data_path, parameters)

        if satellite is not None:
            plot_params.append((i, r, phi, density, parameters, (host_star['x'][i], host_star['y'][i]), (satellite['x'][i], satellite['y'][i])))
        else:
            plot_params.append((i, r, phi, density, parameters, (host_star['x'][i], host_star['y'][i]), None))

    disk_mass = []
    for params in plot_params:
        r = params[1]
        phi = params[2]
        density = params[3]

        diff = r[1:] - r[:-1]
        dx = 2*np.pi/parameters['Nx']
        mass = np.sum(dx*(density.T * diff).T)
        disk_mass.append(mass)

    dt = parameters['DT']
    sec_to_year = 60*60*24*365.25
    times = dt * np.arange(0, len(data_files), 1) / sec_to_year
    fig,ax = plt.subplots(figsize=(6,6))
    ax.plot(times, disk_mass)
    ax.set_yscale('log')
    fig.savefig('./plots/disk_mass.jpg', bbox_inches='tight')

if __name__=='__main__':
    main()
