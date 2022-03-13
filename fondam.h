/** \file fondam.h

This file contains all the information needed to work in a given
system of units.  Contains fundamental constants used thorough the
code.
*/

/* R_MU : ideal gas constant divided by mean molecular weight (R/\mu) */

/* Note: the mean molecular weight assumed below has the fiducial
   value of 2.4 g/mol for protoplanetary disks. */

//Scale free
#define      G_SF  1.0
#define  MSTAR_SF  1.0
#define     R0_SF  1.0
#define   R_MU_SF  1.0
#define    MU0_SF  1.0

#define      G_MKS  6.674e-11
#define  MSTAR_MKS  1.9891e30
#define     R0_MKS  (5.2*1.49597871e11)
#define   R_MU_MKS  3460.0
#define    MU0_MKS  1.25663706143591e-6   //B in Tesla

#define      G_CGS  6.674e-8
//#define  MSTAR_CGS  1.9891e33
//#define     R0_CGS  (5.2*1.49597871e13)
#define   R_MU_CGS  36149835.0
#define    MU0_CGS  12.5663706143591   //B in Gauss

#define  MSTAR_CGS  3.798e30 // 2 jupiter mass
#define     R0_CGS  1.49597871e13 // 1 AU

#if !(defined(MKS) || defined (CGS))
#define		G	(G_SF)
#define     MSTAR       (MSTAR_SF)
#define        R0       (R0_SF)
#define      R_MU       (R_MU_SF)
#define       MU0       (MU0_SF)
#endif

//International System
#ifdef MKS
#define		G	(G_MKS)
#define     MSTAR       (MSTAR_MKS)
#define        R0       (R0_MKS)
#define      R_MU       (R_MU_MKS)
#define       MU0       (MU0_MKS)
#endif

//cgs
#ifdef CGS
#define		G	(G_CGS)
#define     MSTAR       (MSTAR_CGS)
#define        R0       (R0_CGS)
#define      R_MU       (R_MU_CGS)
#define       MU0       (MU0_CGS)
#endif


// Stefan's constant
#define STEFANK (5.6705e-5*pow(R_MU/R_MU_CGS,4.0)*pow(G/G_CGS,-2.5)*pow(MSTAR/MSTAR_CGS,-1.5)*pow(R0/R0_CGS,-0.5))
#define STEFANK_CGS 5.670374e-5

// Speed of light
#define C0      (2.99792458e10*sqrt(G/G_CGS*MSTAR/MSTAR_CGS/R0*R0_CGS))

// Cosmological microwave background's temperature
#define TCMB    (2.73*(G*MSTAR/R0/R_MU)/(G_CGS*MSTAR_CGS/R0_CGS/R_MU_CGS))

//#define TCMB    (30.0*(G*MSTAR/R0/R_MU)/(G_CGS*MSTAR_CGS/R0_CGS/R_MU_CGS))

// Avogadro's constant
#define NA 6.02214076e23

// Boltzmann's constant divided by mean molecular weight
#define KB_MU (1.380649e-16 / 2.4 * (R_MU/R_MU_CGS) * NA)

// Pi
#define PI 3.14159265359

//#define THRESHOLD_STELLAR_MASS 0.05*MSTAR //Our arbitrary threshold to consider an object as stellar.
#define THRESHOLD_STELLAR_MASS 1.0e12*MSTAR // Giant value so that this isn't tripped
