import os
from glob import glob

import numpy as np

def read_fargo_data(i, run_folder, parameters):

    data_filename = 'gasdens{}.dat'.format(i)
    data_path = os.path.join(run_folder, data_filename)

    domain_x_path = os.path.join(run_folder, 'domain_x.dat')
    domain_y_path = os.path.join(run_folder, 'domain_y.dat')

    phi = np.zeros(parameters['NX'] + 1)
    with open(domain_x_path, 'r') as f:
        count = 0
        for i,line in enumerate(f):
            phi[count] = float(line)
            count+=1

    n_ghost = 3
    r = np.zeros(parameters['NY'] + (n_ghost*2) + 1)
    with open(domain_y_path, 'r') as f:
        count = 0
        for i,line in enumerate(f):
            r[count] = float(line)
            count+=1

    r = r[n_ghost:-n_ghost]
    
    density = np.fromfile(data_path).reshape(parameters['NY'], parameters['NX'])
    
    return phi, r, density

def read_parameters(run_folder):
    variables_filename = 'variables.par'
    variables_path = os.path.join(run_folder, variables_filename)

    parameters = {}
    with open(variables_path, 'r') as f:
        for line in f:
            l = line.split()
            if l[1].isdigit():
                parameters[l[0]] = int(l[1])
            else:
                try:
                    parameters[l[0]] = float(l[1])
                except:
                    parameters[l[0]] = l[1]

    return parameters

def read_planet_orbit_data(planet_data_path, orbit_data_path):

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
