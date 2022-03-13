import numpy as np


def read_fargo_data(data_path, parameters):
    phi = np.linspace(parameters['Xmin'], parameters['Xmax'], parameters['Nx']+1)
    r = np.geomspace(parameters['Ymin'],parameters['Ymax'],parameters['Ny']+1)
    
    density = np.fromfile(data_path).reshape(parameters['Ny'], parameters['Nx'])
    
    return phi, r, density

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
