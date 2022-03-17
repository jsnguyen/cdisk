# U units are AU, MJ
# everything else is in cgs
AU_to_cm = 1.495978707e13 # 1 AU in cm
cm_to_AU = 1/AU_to_cm

MJ_to_g  = 1.89813e30 # 1 MJ in g
g_to_MJ = 1/MJ_to_g

yr_to_sec = 60*60*24*365.25 # 1 year in sec
sec_to_yr = 1/yr_to_sec

RJ_to_cm = 7.1492e9 # jupiter radius in cm
cm_to_RJ = 1/RJ_to_cm

G_cgs = 6.67430e-8 # gravitational constant in CGS
G_sim = 3.784e-17 # gravitational constant in au^3/MJ/sec^2

muJ = 2.83e30 # magnetic moment of jupiter
mu_naught_cgs = 0.1256637062 # vaccum permeability in CGS

mass_accretion_conversion  = MJ_to_g/yr_to_sec

kb_cgs = 1.380649e-16
stefan_cgs= 5.670374e-5