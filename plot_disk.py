import os
import pickle
from glob import glob
import argparse
from multiprocessing import Pool

from PIL import Image

import numpy as np

from matplotlib import pyplot as plt
import matplotlib.cm as cm
import matplotlib.animation as animation
from matplotlib import font_manager
from matplotlib.colors import LogNorm

from tqdm import tqdm

from units import *

def read_fargo_data(data_path, parameters):
    phi = np.linspace(parameters['Xmin'], parameters['Xmax'], parameters['Nx']+1)
    r = np.geomspace(parameters['Ymin'],parameters['Ymax'],parameters['Ny']+1)
    
    density = np.fromfile(data_path).reshape(parameters['Ny'], parameters['Nx'])
    
    return phi, r, density

def read_planet_orbit_data(planet_data_path, orbit_data_path, parameters):

    planet = {'i':[],
              'x':[],
              'y':[],
              'z':[],
              'vx':[],
              'vy':[],
              'vz':[],
              'mass':[],
              'time':[],
              'frame_rotation':[]
             }

    orbit = {'time':[],
             'ecc':[],
             'a':[],
             'mean_anomaly':[],
             'true_anomaly':[],
             'arg_periastron':[],
             'rotation':[],
             'inclination':[],
             'lon_asc_node':[],
             'pa_perihelion':[]
            }

    with open(orbit_data_path) as f:
        for line in f:
            l = [float(el) for el in line.split()]
            orbit['time'].append(l[0])
            orbit['ecc'].append(l[1])
            orbit['a'].append(l[2])
            orbit['mean_anomaly'].append(l[3])
            orbit['true_anomaly'].append(l[4])
            orbit['arg_periastron'].append(l[5])
            orbit['rotation'].append(l[6])
            orbit['inclination'].append(l[7])
            orbit['lon_asc_node'].append(l[8])
            orbit['pa_perihelion'].append(l[9]) 

    with open(planet_data_path) as f:
        for line in f:
            l = [float(el) for el in line.split()]
            planet['i'].append(l[0])
            planet['x'].append(l[1])
            planet['y'].append(l[2])
            planet['z'].append(l[3])
            planet['vx'].append(l[4])
            planet['vy'].append(l[5])
            planet['vz'].append(l[6])
            planet['mass'].append(l[7])
            planet['time'].append(l[8])
            planet['frame_rotation'].append(l[9])

    return planet, orbit

def plot_disk(r, phi, density, satellite_coords, host_star_coords, parameters, cmap='gist_heat'):
    font_path =  '/Users/jsn/Library/Fonts/IBMPlexMono-Regular.ttf'  # Your font path goes here
    font_manager.fontManager.addfont(font_path)
    prop = font_manager.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = prop.get_name()
    plt.rcParams['savefig.facecolor'] = (1.0, 1.0, 1.0)
    
    fig,ax = plt.subplots(figsize=(6,6))

    cmap = plt.get_cmap(cmap)
    
    mg_phi, mg_r = np.meshgrid(phi, r)
    mg_x = mg_r*np.cos(mg_phi) / AU_to_cm
    mg_y = mg_r*np.sin(mg_phi) / AU_to_cm

    ymax = parameters['Ymax'] / AU_to_cm
    ymin = parameters['Ymin'] / AU_to_cm

    sc_x = satellite_coords[0]/ AU_to_cm
    sc_y = satellite_coords[1]/ AU_to_cm

    hsc_x = host_star_coords[0]/ AU_to_cm
    hsc_y = host_star_coords[1]/ AU_to_cm

    vmin = 1e-3
    vmax = 1e5
    img = ax.pcolormesh(mg_x, mg_y, density, cmap=cmap, shading='flat', snap=True, norm=LogNorm(vmin=vmin, vmax=vmax))
    ax.plot(sc_x, sc_y, marker='x', linestyle='none', color='#2a52be', markersize=12)
    ax.plot([0,hsc_x], [0,hsc_y], linestyle='--', color='black', markersize=12)

    outer_circle = plt.Circle((0, 0), ymax, ec='black', linewidth=0.8, fc='none', linestyle='-', clip_on=False)
    inner_circle = plt.Circle((0, 0), ymin, ec='black', linewidth=0.8, fc='none', linestyle='-', clip_on=False)
    ax.add_patch(outer_circle)
    ax.add_patch(inner_circle)

    cbar = fig.colorbar(img, ax=ax, shrink=0.8, pad=0.05)
    cbar.set_label('Density [g/cm$^2$]')
    ax.set_aspect("equal")
    ax.set_xlim(-ymax, ymax)
    ax.set_ylim(-ymax, ymax)
    ax.set_xticks(np.linspace(-ymax, ymax, 5))
    ax.set_xlabel('[AU]')
    ax.tick_params(axis="x", direction="inout")
    ax.spines['bottom'].set_position(('outward', 15))

    ax.get_yaxis().set_visible(False)
    ax.spines['left'].set_visible(False)

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    return fig, img

def parallel_plot(params):
    i, r, phi, density, satellite_coords, host_star_coords, parameters = params
    fig, img = plot_disk(r, phi, density, satellite_coords, host_star_coords, parameters)
    oif = './plots/gasdens{0:03d}.jpg'.format(i)
    fig.savefig(oif, bbox_inches='tight')
    plt.close()

def main():
    parser = argparse.ArgumentParser(description='Plot cdisk plots.')
    parser.add_argument('--runfolder', default=None, help='plot a specific run')
    args = parser.parse_args()

    par_pickle_filename = 'cdi.par.pickle'
    with open(par_pickle_filename, 'rb') as f:
        parameters = pickle.load(f)

    data_folder = '/Users/jsn/landing/data/'

    if args.runfolder is not None:
        run_folder = args.runfolder
    else:
        latest_run_folder = sorted(glob(os.path.join(data_folder,'cdi_*')))[-1]
        run_folder = latest_run_folder

    print('Plotting run folder -> {}'.format(run_folder))

    n_frames = len(glob(os.path.join(run_folder,'gasdens*.dat')))-1
    data_files = [os.path.join(run_folder, 'gasdens{}.dat') for i in range(n_frames)]

    satellite_data_path = os.path.join(run_folder,'planet0.dat')
    host_star_data_path = os.path.join(run_folder,'planet1.dat')
    orbit_data_path = os.path.join(run_folder,'orbit0.dat')

    satellite, satellite_orbit = read_planet_orbit_data(satellite_data_path, orbit_data_path, parameters)
    host_star, host_star_orbit = read_planet_orbit_data(host_star_data_path, orbit_data_path, parameters)

    plot_params=[]
    print('Loading in {} data frames...'.format(n_frames))
    for i in tqdm(range(len(data_files))):

        data_filename = 'gasdens{}.dat'.format(i)
        data_path = os.path.join(run_folder, data_filename)
        phi, r, density = read_fargo_data(data_path, parameters)

        plot_params.append((i, r, phi, density, (satellite['x'][i], satellite['y'][i]), (host_star['x'][i], host_star['y'][i]), parameters))

    disk_mass = []
    for params in plot_params:
        r = params[1]
        phi = params[2]
        density = params[3]

        diff = r[1:] - r[:-1]
        dx = 2*np.pi/parameters['Nx']
        mass = np.sum(dx*(density.T * diff).T)
        disk_mass.append(mass)

    fig,ax = plt.subplots(figsize=(6,6))
    ax.plot(disk_mass)
    fig.savefig('./plots/disk_mass.jpg', bbox_inches='tight')

    print('Parallel plotting...')
    with Pool() as pool:
        list(tqdm(pool.imap(parallel_plot, plot_params), total=len(plot_params))) # parallel runs use imap to work with tqdm

if __name__=='__main__':
    main()
