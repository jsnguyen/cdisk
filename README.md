# cdisk

Term project for PHYS239 Disk and their Dynamics at UCSD. This is a study of the the circumplanetary disk around PDS70c.

# Requirements
* Python 3.6+
* numpy
* scipy
* matplotlib
* [FARGO3D](https://fargo3d.bitbucket.io/)

# How to Run

## FARGO3D Simulations
Edit  `remake.sh` and `run.sh` to your corresponding directories for FARGO3D.
```
./remake.sh
./run.sh
```

`remake.sh` copies over the relevant files and directories and recompiles FARGO3D according to your new inputs.

`run.sh` Just runs the simulation itself. Make sure to change the number of cores to the correct value.

### Changing Parameters
Edit the `generate_par.py` file to change the FARGO3D simulation parameters *not* the actual par file.

# Description
`cdi/` is the "setups" folder required by FARGO3D for the hydrodynamic simulation. Contained should be all the initial conditions and boundary conditions for the simulations. See the FARGO3D docs for more info.
`cdi.cfg` is the planet configuration file also required by FARGO3D for the N-body component.

# Data Analysis
Some rough notebooks for the data analysis are included in the folder `notebooks` but are not polished.

# Code Modifications
Added an extra flag `-DRVISCOSITY` to add a radially varying viscosity term, as opposed to the default viscosity prescription. `visctensor_cyl.c` is where the radial viscosity term is implemented. This is automatically copied over in the remake step.

Also changed the `./cdi/condinit.c` file to change the initial conditions.
