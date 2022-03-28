#include "fargo3d.h"

void Init() {
  
    OUTPUT(Density);
    OUTPUT(Energy);
    OUTPUT(Vx);
    OUTPUT(Vy);

    int i,j,k;
    real r, omega, h, viscosity, soundspeed, vk;
    real ca, cb, cc;
    real aspect_ratio;

    real *vphi = Vx->field_cpu;
    real *vr   = Vy->field_cpu;
    real *rho  = Density->field_cpu;

    // cs for isothermal
    real *cs   = Energy->field_cpu;

    i = j = k = 0;
    for (j=0; j<Ny+2*NGHY; j++) {
        for (i=0; i<Nx+2*NGHX; i++) {

            r = Ymed(j);

            omega = sqrt(G*MSTAR/r/r/r);

            ca = KB_MU / (G*MSTAR);
            cb = r * (3.0*G*MSTAR*MASSACCRETION)/(8.0*PI*STEFANK_CGS);
            cc = sqrt(YMAX/r) - 1.0;

            // will be NaN for ghost cells since h=0 if r > r_hill
            if (r > YMAX) {
                aspect_ratio = 0.0;
            } else {
                aspect_ratio = sqrt(ca * pow(cb * cc, 0.25));
            }

            h = aspect_ratio*r;
            soundspeed = h*omega;
            viscosity = ALPHA*soundspeed*h;
            rho[l] = (MASSACCRETION / (3.0*PI*viscosity)) * (sqrt(YMAX/r) - 1.0);

            // isothermal
            cs[l] = soundspeed;

            vk = sqrt(G*MSTAR/r);
            vphi[l] = vk * (1.0 - (13.0/8.0) * aspect_ratio*aspect_ratio);
            vphi[l] -= OMEGAFRAME*r;
            vphi[l] *= (1.0+aspect_ratio*NOISE*(drand48()-0.5));

            vr[l]    = MASSACCRETION / (2.0*PI*r*rho[l]);
    }
  } 
}

void DepositMass() {

    INPUT(Density);
    OUTPUT(Density);

    real *rho  = Density->field_cpu;
    real r;
    real cell_area;

    int i,j,k;
    i = j = k = 0;
    for (j=0; j<Ny+2*NGHY; j++) {

        r = Ymed(j);

        if ( r > RDEP ){
            for (i=0; i<Nx+2*NGHX; i++) {
                // NX factor cancels out
                cell_area = (PI*(Ymin(j+1)*Ymin(j+1) - Ymin(j)*Ymin(j)));
                rho[l] += MASSACCRETION*DT / cell_area;
            }
            break;
        }

    }
}

void CondInit() {
    Fluids[0] = CreateFluid("gas",GAS);
    SelectFluid(0);
    Init();
}
