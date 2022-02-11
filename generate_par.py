import os
import argparse

import numpy as np
from pathlib import Path

def generate_par(out_folder):
    
    print('Making cdisk parameter file...')

    parameters = {
                  'Setup':               'cdi',
                  'AspectRatio':         0.05,
                  'Sigma0':              '2.0e-6',
                  'SigmaSlope':          0.8,
                  'FlaringIndex':        0.25,
                  'DampingZone':         1.15,
                  'TauDamp':             0.3,
                  'ThicknessSmoothing':  0.6,
                  'RocheSmoothing':      0.0,
                  'Eccentricity':        0.0,
                  'ExcludeHill':         'no',
                  'IndirectTerm':        'Yes',
                  'AlphaIn':             '1.0e-5',
                  'AlphaOut':            '7.5e-3',
                  'SigmaVisc':           1.0,
                  'Nx':                  32*3,
                  'Ny':                  32,
                  'Xmin':                -3.14159265358979323844,
                  'Xmax':                3.14159265358979323844,
                  'OmegaFrame':          0.0, # sqrt(1/r1)
                  'Frame':               'F',
                  'DT':                  2*np.pi/10,
                  'Ninterm':             100,
                  'Ntot':                1000000,
                  'OutputDir':           out_folder
                  }


    # disk specific parameters
    parameters['PlanetConfig'] = 'planets/cdi.cfg'
    parameters['Epsilon'] = 15.0 # units dimensionless parameter, multiplies R0 factor so R0 can be zero if scale free
    parameters['Rmid'] = 18.0 # middle of disk units of AU
    parameters['Rc'] = 30.0 # disk cutoff units of AU
    parameters['Ymin'] = 10.0
    parameters['Ymax'] = 25.0

    par_filename = './cdi/cdi.par'

    with open(par_filename, 'w') as f:
        for el in parameters.keys():
            f.write('{:32} {:64}'.format(el,str(parameters[el])).rstrip()+'\n')

def main():

    increment=0
    prepath = str(Path.home())
    out_folder_path = prepath+'/landing/data/cdi_'+str(increment).zfill(4)

    while os.path.isdir(out_folder_path):
        increment+=1
        out_folder_path = prepath+'/landing/data/cdi_'+str(increment).zfill(4)

    generate_par(out_folder_path)
    print('Done.')

if __name__=='__main__':
    main()
