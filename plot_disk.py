import os
import pickle

from glob import glob

import numpy as np

from matplotlib import pyplot as plt
from matplotlib.colors import LogNorm
import matplotlib.cm as cm
import matplotlib.animation as animation

def animate():
    par_pickle_filename = 'cdi.par.pickle'
    with open(par_pickle_filename, 'rb') as f:
        parameters = pickle.load(f)

    sim_units_pickle_filename = 'sim_units.pickle'
    with open(sim_units_pickle_filename, 'rb') as f:
        sim_units = pickle.load(f)

    data_folder = '/Users/jsn/landing/data/'
    latest_run_folder = sorted(glob(os.path.join(data_folder,'cdi_*')))[-1]

    print('Latest run folder -> {}'.format(latest_run_folder))

    data_files = glob(os.path.join(latest_run_folder,'gasdens*.dat'))
 
    for el in data_files:
        if 'gasdens0_2d.dat' in el:
            data_files.remove(el)

    imgs = []

    fig,ax = plt.subplots(figsize=(5,5))
    figure_output_folder = './plots'

    def animate(i):
        data_filename = 'gasdens{}.dat'.format(i)
        data_path = os.path.join(latest_run_folder, data_filename)
        density = np.fromfile(data_path).reshape(parameters['Ny'], parameters['Nx'])

        phi = np.linspace(parameters['Xmin'], parameters['Xmax'], parameters['Nx'])
        r = np.geomspace(np.log10(parameters['Ymin']*sim_units['length']),
                        np.log10(parameters['Ymax']*sim_units['length']),
                        parameters['Ny'])
        PHI, R = np.meshgrid(phi, r)
        X = R*np.cos(PHI)
        Y = R*np.sin(PHI)

        img = ax.pcolormesh(X,Y, density, cmap=cm.Oranges_r)
        ax.set_aspect("equal")

        #fig.savefig(os.path.join(figure_output_folder, 'gasdens{}.png'.format(i)), bbox_inches='tight')
        return img,

    ani = animation.FuncAnimation(fig, animate, frames=50, interval=100, blit=True)
    ani.save('animation.gif', dpi=80, writer='imagemagick')

def main():
    par_pickle_filename = 'cdi.par.pickle'
    with open(par_pickle_filename, 'rb') as f:
        parameters = pickle.load(f)

    sim_units_pickle_filename = 'sim_units.pickle'
    with open(sim_units_pickle_filename, 'rb') as f:
        sim_units = pickle.load(f)

    data_folder = '/Users/jsn/landing/data/'
    latest_run_folder = sorted(glob(os.path.join(data_folder,'cdi_*')))[-1]

    print('Latest run folder -> {}'.format(latest_run_folder))

    data_files = glob(os.path.join(latest_run_folder,'gasdens*.dat'))
 
    for el in data_files:
        if 'gasdens0_2d.dat' in el:
            data_files.remove(el)

    fig,ax = plt.subplots(figsize=(8,8))
    for i in range(len(data_files)):
        data_filename = 'gasdens{}.dat'.format(i)
        data_path = os.path.join(latest_run_folder, data_filename)
        density = np.fromfile(data_path).reshape(parameters['Ny'], parameters['Nx'])

        phi = np.linspace(parameters['Xmin'], parameters['Xmax'], parameters['Nx']+1)
        r = np.geomspace(parameters['Ymin']*sim_units['length'],parameters['Ymax']*sim_units['length'],parameters['Ny']+1)
        PHI, R = np.meshgrid(phi, r)
        X = R*np.cos(PHI)
        Y = R*np.sin(PHI)

        ax.pcolormesh(X,Y, density, cmap=cm.Oranges_r, shading='flat', snap=True, edgecolor=(0,0,0,0.01), linewidth=0.005)
        ax.set_aspect("equal")

        figure_output_folder = './plots'
        #figure_output_folder = '/Users/jsn/landing/code/dynafresh/public/images'
        fig.savefig(os.path.join(figure_output_folder, 'gasdens{0:04d}.pdf'.format(i)), bbox_inches='tight')
        plt.cla()

if __name__=='__main__':
	main()
    #animate()
