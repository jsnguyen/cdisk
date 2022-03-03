#include "fargo3d.h"

#define PI 3.14159265359

void Init() {
  
  OUTPUT(Density);
  OUTPUT(Energy);
  OUTPUT(Vx);
  OUTPUT(Vy);

  int i,j,k;
  real r, omega, h, viscosity, soundspeed, vk;
  
  real *vphi = Vx->field_cpu;
  real *vr   = Vy->field_cpu;
  real *rho  = Density->field_cpu;
  
#ifdef ADIABATIC
  real *e   = Energy->field_cpu;
#endif
#ifdef ISOTHERMAL
  real *cs   = Energy->field_cpu;
#endif

  i = j = k = 0;
  
  for (j=0; j<Ny+2*NGHY; j++) {
    for (i=0; i<Nx+2*NGHX; i++) {

      r = Ymed(j);

      omega = sqrt(G*MSTAR/r/r/r);
      h = ASPECTRATIO*r;

      soundspeed = h/omega;

      viscosity = ALPHA*soundspeed*h;

      //rho[l] = SIGMA0 * pow(REFERENCERADIUS/r, 5.0/4.0);
      
      rho[l] = (MASSACCRETION / (3.0*PI*viscosity)) * (sqrt(HILLRADIUS/r) - 1.0);

#ifdef ISOTHERMAL
      cs[l] = soundspeed;
#endif
#ifdef ADIABATIC
      e[l] = pow(soundspeed,2)*rho[l]/(GAMMA-1.0);
#endif
      
      vk = sqrt(G*MSTAR/r);
      vphi[l] = vk * (1.0 - (13.0/8.0) * ASPECTRATIO*ASPECTRATIO);
      vphi[l] -= OMEGAFRAME*r;
      vphi[l] *= (1.0+ASPECTRATIO*NOISE*(drand48()-0.5));
      
      vr[l]    = MASSACCRETION / (2.0*PI*r*rho[l]);

      /*
      vphi[l] = omega*r*sqrt(1.0+pow(ASPECTRATIO,2)*pow(r/R0,2*FLARINGINDEX)*
			     (2.0*FLARINGINDEX - 1.0 - SIGMASLOPE));
      vphi[l] -= OMEGAFRAME*r;
      vphi[l] *= (1.+ASPECTRATIO*NOISE*(drand48()-.5));
      
      vr[l]    = soundspeed*NOISE*(drand48()-.5);
      */
    }
  } 
}

void CondInit() {
   Fluids[0] = CreateFluid("gas",GAS);
   SelectFluid(0);
   Init();
}
