# Mean Motion Resonance

Final class project for PHYS239 Astrophysical Fluid Dynamics at UCSD. Studying mean motion resonance formation in protoplanetary disk systems.

# Requirements
* Python 3+
* numpy
* scipy
* matplotlib
* [REBOUND](https://rebound.readthedocs.io/en/latest/)
* [FARGO3D](https://fargo3d.bitbucket.io/)

# How to Run

## FARGO3D Simulations
Edit  `remake.sh` and `run.sh` to your corresponding directories for FARGO3D.
```
./remake.sh i_j_k
./run.sh
```
Where `i_j_k` is the desired resonance chain of either `1_2` or `1_2_4` or`1_2_4_8`.

`remake.sh` copies over the relevant files and directories and recompiles FARGO3D according to your new inputs.

`run.sh` Just runs the simulation itself. Make sure to change the number of cores to the correct value.

### Changing Parameters
Edit the `generate_par.py` file to change the FARGO3D simulation parameters *not* the actual par file.

## REBOUND MEGNO Simulations
To run the REBOUND MEGNO analysis:
```
python3 mmr_megno.py i_j_k -n n_cores
```
Where `i_j_k` is the desired resonance chain of either `1_2` or `1_2_4` or`1_2_4_8` and `n_cores` is the number of cores to be used.

To make the MEGNO plots:
```
python3 plot_im_megno.py i_j_k
```
Where `i_j_k` is the desired resonance chain of either `1_2` or `1_2_4` or`1_2_4_8`. Should output a PDF file of the plot.

### Changing Parameters
Edit `mmr_megno_parameters_*.txt` files to change the probed parameter space for the MEGNO plots.

# Description
`mmr/` is the "setups" folder required by FARGO3D for the hydrodynamic simulation. Contained should be all the initial conditions and boundary conditions for the simulations. See the FARGO3D docs for more info.
`*.cfg` are the planet configuration files also required by FARGO3D for the N-body component.

# Data Analysis
Some rough notebooks for the data analysis are included in the folder `notebooks` but are not polished.

# Code Modifications
Added an extra flag `-DRVISCOSITY` to add a radially varying viscosity term, as opposed to the default viscosity prescription. `visctensor_cyl.c` is where the radial viscosity term is implemented. This is automatically copied over in the remake step.

Also changed the `./mmr/condinit.c` file to change the initial conditions.
