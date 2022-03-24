import os
import argparse
import pickle
import pprint

import numpy as np
from pathlib import Path

from units import *

def generate_par(par_filename, parameters):

    print('Making cdi parameter file -> {}'.format(par_filename))

    # writing to actual par file
    with open(par_filename, 'w') as f:
        f.write('#### THIS FILE IS AUTOGENERATED DO NOT EDIT BY HAND ####\n')
        for el in parameters.keys():
            f.write('{:32} {:64}'.format(el,str(parameters[el])).rstrip()+'\n')

    # pickle file to use parameters elsewhere in analysis code
    par_pickle_filename = 'cdi.par.pickle'
    with open(par_pickle_filename, 'wb') as f:
        pickle.dump(parameters, f)

# technically a satellite not a planet
def generate_satellite(satellite_filename, satellites):

    print('Making cdi planet file -> {}'.format(satellite_filename))

    # write to the planet file
    param_names = ['name', 'a', 'mass', 'accretion', 'feels_disk', 'feels_others']
    with open(satellite_filename, 'w') as f:
        f.write('#### THIS FILE IS AUTOGENERATED DO NOT EDIT BY HAND ####\n')
        for s in satellites:
            for key in param_names:
                f.write(str(s[key])+' ')
            f.write('\n')

# gets the latest output directory
# useful so we don't accidentally overwrite old data
def get_outputdir():
    increment=0
    prepath = str(Path.home())
    outputdir = prepath+'/landing/data/cdisk_data/cdi_'+str(increment).zfill(4)

    while os.path.isdir(outputdir):
        increment+=1
        outputdir = prepath+'/landing/data/cdisk_data/cdi_'+str(increment).zfill(4)

    return outputdir
        
def main():

    planet = {}
    satellite = {}
    parameters = {}

    #####################
    # PLANET DEFINITION #
    #####################

    planet['mass'] = 2.0 * MJ_to_g # make sure MSTAR in fondham.h matches this

    ########################
    # SATELLITE DEFINITION #
    ########################

    satellites = []
    # the star
    # star orbits the planet in the planet reference frame
    star = {}
    star['name'] = 'CDIa'
    star['a'] = 34.3 * AU_to_cm
    star['mass'] = 1047.57 *  MJ_to_g
    star['period'] = None
    star['accretion'] = 0.0
    star['feels_disk'] = 'NO'
    star['feels_others'] = 'NO'
    satellites.append(star)

    ########################
    # PARAMETER DEFINITION #
    ########################

    # disk parameters
    parameters['MassAccretion'] = 1.0e-8 * mass_accretion_conversion # jupiter mass / year to g / sec

    # scaling relationship for truncation distance
    r_trunc = 5*RJ_to_cm * np.power(planet['mass'] / (1.0 * MJ_to_g), -1/7) *  np.power(parameters['MassAccretion'] / (1.0e-7 * mass_accretion_conversion), -2/7)
    r_hill = star['a'] * np.power(planet['mass'] / (3*star['mass']), 1/3) # hill radius
    period_at_radius = 2*np.pi*np.sqrt(np.power( r_hill/3 , 3)/(G_cgs*planet['mass'])) # period at r_hill/2

    '''
    # the orbiting satellite
    s = {}
    s['name'] = 'CDIS'
    s['a'] = r_hill/3.0
    s['mass'] = 1.0e-9 *  MJ_to_g
    s['period'] = None
    s['accretion'] = 0.0
    s['feels_disk'] = 'YES'
    s['feels_others'] = 'YES'
    satellites.append(s)
    '''

    parameters['Rdep'] = r_hill/3.0 # deposit mass at this radius
    parameters['Alpha'] = 0.0001

    # boundaries
    # x should be a full circle in units of radians
    parameters['Xmin'] = -np.pi
    parameters['Xmax'] = np.pi
    # inner/outer annulus distance
    #parameters['Ymin'] = r_trunc
    parameters['Ymin'] = r_hill*0.05
    parameters['Ymax'] = r_hill

    # initial eccentricity of the planets
    parameters['Eccentricity'] = 0.0

    # resolution parameters
    parameters['Spacing'] = 'log'
    grid_power = 8 # number of cells is 2^(n-1) , 2^n
    parameters['Ny'] = int(np.power(2, grid_power-1))
    parameters['Nx'] = int(np.power(2, grid_power))

    # timestep parameters
    total_time = 1e6 * yr_to_sec

    parameters['DT'] = period_at_radius/10
    parameters['Ninterm'] = 1
    parameters['Ntot'] = int(total_time / parameters['DT'])

    #parameters['DT'] = satellites[0]['period']/10
    #parameters['Ninterm'] = 10
    #n_sec = 10 # number of seconds for a 24 fps gif
    #parameters['Ntot'] = 24*parameters['Ninterm']*n_sec

    # simulation files
    #outputdir = get_outputdir()
    prepath = str(os.path.expanduser('~'))
    #outputdir = prepath+'/landing/data/cdisk_data/pds70c'
    outputdir = prepath+'/landing/data/cdisk_data/pds70c_nominal_long_fixed'
    parameters['Setup'] = 'cdi'
    parameters['PlanetConfig'] = 'planets/cdi.cfg'
    parameters['OutputDir'] =  outputdir

    # rotating reference frame
    parameters['OmegaFrame'] = 0.0
    parameters['Frame'] = 'F'

    # smoothing parameters
    parameters['SigmaSlope'] = 0.8
    parameters['FlaringIndex'] = 0.25
    parameters['ThicknessSmoothing'] = 0.6
    parameters['RocheSmoothing'] = 0.0

    # wave damping/killing
    parameters['DampingZone'] = 1.15
    parameters['TauDamp'] = 0.3 # characteristic time for damping, units of inverse local orbital frequency

    # misc
    parameters['ExcludeHill'] = 'No' # hill sphere cutoff for force calculations
    parameters['IndirectTerm'] = 'Yes' # indirect term "ficticious force" due to gravity, usually set to yes

    # generate the par file
    par_filename = './cdi/cdi.par'
    generate_par(par_filename, parameters)

    # generate satellite file
    satellite_filename = 'cdi.cfg'
    generate_satellite(satellite_filename, satellites)

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(parameters)

if __name__=='__main__':
    main()
