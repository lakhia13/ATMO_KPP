import numpy as np

import Parameters as pm

class Param():

  # Racmsorg Parameters
  NSPEC = 18
  NVAR = 16
  NVARACT = 16
  NFIX = 2
  NREACT = 26
  NVARST = 1
  NFIXST = 17
  NONZERO = 57
  LU_NONZERO = 59
  CNVAR = 17
  NLOOKAT = 0
  NMONITOR = 0
  NMASS = 1
  
  # Racmsorg Update Rconst
  pH = 4
  V_um_cm3 = 0
  rp_um = 0.2
  LiquidFraction = 1
  LWC_v_v = 0
  
  Mono_Dis = False
  
  # Racmsorg Interface
  ind_O3 = 0 
  ind_HOCl = 1 
  ind_HCl = 2 
  ind_Cl2 = 3 
  ind_HOBr = 4 
  ind_HBr = 5 
  ind_Br2 = 6 
  ind_BrCl = 7 
  ind_O3_p = 8 
  ind_Cl2_p = 9 
  ind_Br2_p = 10 
  ind_HOCl_p = 11 
  ind_Brm_p = 12
  ind_HOBr_p = 13 
  ind_Clm_p = 14
  ind_BrCl_p = 15 
  ind_H2O = 16
  ind_M = 17
  
  indf_H2O = 0
  indf_M = 1
  
  Pj_o31d = 0 
  Pj_o33p = 1 
  Pj_no2 = 2
  Pj_no3o2 = 3 
  Pj_no3o = 4 
  Pj_hno2 = 5 
  Pj_hno3 = 6 
  Pj_hno4 = 7 
  Pj_h2o2 = 8
  Pj_ch2or = 9 
  Pj_ch2om = 10
  Pj_ch3cho = 11
  Pj_ch3coch3 = 12
  Pj_ch3coc2h5 = 13 
  Pj_hcocho = 14
  Pj_ch3cocho = 15 
  Pj_hcochest = 16 
  Pj_ch3o2h = 17
  Pj_ch3coo2h = 18 
  Pj_ch3ono2 = 19 
  Pj_hcochob = 20 
  Pj_macr = 21 
  Pj_n2o5 = 22 
  Pj_o2 = 23
  Pj_pan = 24
  Pj_acet = 25 
  Pj_mglo = 26
  Pj_hno4_2 = 27 
  Pj_n2o = 28
  Pj_pooh = 29 
  Pj_mpan = 30 
  Pj_mvk = 31
  Pj_etooh = 32 
  Pj_prooh = 33 
  Pj_onitr = 34
  Pj_acetol = 35 
  Pj_glyald = 36 
  Pj_hyac = 37 
  Pj_mek = 38
  Pj_open = 39 
  Pj_gly = 40
  Pj_acetp = 41 
  Pj_xooh = 42
  Pj_isooh = 43
  Pj_alkooh = 44 
  Pj_mekooh = 45 
  Pj_tolooh = 46
  Pj_terpooh = 47 
  Pj_cl2 = 48
  Pj_hno4a = 49 
  Pj_hno4b = 50
  Pj_propanal = 51 
  Pj_acetone = 52 
  Pj_ch3ooh = 53 
  Pj_oclo = 54 
  Pj_clo = 55 
  Pj_clno2 = 56
  Pj_clno3a = 57 
  Pj_clno3b = 58 
  Pj_bro = 59 
  Pj_br2 = 60
  Pj_hobr = 61
  Pj_brno2 = 62
  Pj_brno3a = 63 
  Pj_brno3b = 64 
  Pj_brcl = 65 
  Pj_hocl = 66 
  Pj_fmcl = 67
  
