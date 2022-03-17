import os
import pickle
from glob import glob
import argparse
from multiprocessing import Pool

import numpy as np

from tqdm import tqdm

from units import *
from cdisk_analysis import *

def main():
    parser = argparse.ArgumentParser(description='Plot cdisk plots.')
    parser.add_argument('runfolder', default=None, help='plot a specific run')
    args = parser.parse_args()
    run_folder = args.runfolder

    parameters = read_parameters(run_folder)

    mass_file = './data/disk_mass_{}.npy'.format(os.path.basename(os.path.dirname(run_folder)))
    print('Writing mass file -> {}'.format(mass_file))

    n_frames = len(glob(os.path.join(run_folder,'gasdens*.dat')))-1

    print('Loading in {} data frames...'.format(n_frames))
    disk_mass = np.zeros(n_frames)
    for i in tqdm(range(n_frames)):

        phi, r, density = read_fargo_data(i, run_folder, parameters)

        diff = r[1:] - r[:-1]
        dx = (2*np.pi/parameters['NX'])*r[1:]
        mass = np.sum(density.T * diff*dx)
        disk_mass[i] = mass

    with open(mass_file, 'wb') as f:
        np.save(f, disk_mass)

if __name__=='__main__':
    main()
