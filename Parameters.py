import numpy as np
import pandas as pd

class Param():
  
  nspec_host = 72
  nlev = 248
  nrect = 237
  NREACT_J = 29
  NREACT_gas = 173
  NREACT_het = 9
  NREACT_aq = 25
  
  Del = 0.23
  zmin1 = 0.33
  zmin2 = 3.927
  pid = 3.1415926535
  pid2 = 3.1415926535/2
  pid180 = 3.1415926535/180
  n_mgn_spc = 20
  n_cat = 5
  ldrog = 17
  sigma = 5.67e-08
  rgas = 8.314
  
  #------------------------------Read From File--------------------------------------
  timin = 0
  tt = 0
  pp = 0
  Ozone_read = 0
  NO_read = 0
  NO2_read = 0
  CO_read = 0
  HCHO_read = 0
  NOx_obs_read = 0
  averad_obs_read = 0
  averad_obs_Aug26 = 0
  
  dN_dlogDp = 0
  D_um = 0
  #---------------------------------------------------------------------------------
  
  imgn_isop  =  0    # isoprene
  imgn_mbo   =  1    # MBO (only (2-methyl-3-ene-2-ol)-methylbutenol) 
  imgn_myrc  =  2    # myrcene
  imgn_sabi  =  3    # sabinene
  imgn_limo  =  4    # limonene
  imgn_3car  =  5    # 3 carene
  imgn_ocim  =  6    # trans-beta-ocimene
  imgn_bpin  =  7    # beta-pinene
  imgn_apin  =  8    # alpha-pinene
  imgn_afarn =  9    # alpha-farnescene
  imgn_bcar  = 10    # beta-caryophyllene
  imgn_meoh  = 11    # methanol
  imgn_acto  = 12    # acetone
  imgn_acta  = 13    # acetaldehyde and ethanol
  imgn_form  = 14    # formic acid, formaldehyde, acetic acid
  imgn_ch4   = 15    # methane
  imgn_no    = 16    # nitric oxide (and NO2 and NH3 )
  imgn_omtp  = 17    # other monoterpenes
  imgn_osqt  = 18    # other sesquiterpenes
  imgn_co    = 19    # CO and other VOC  
  
  LO1D      = 0
  LO3P      = 1
  LOH       = 2
  LHO2      = 3
  LCO       = 4
  LO3       = 5
  LH2O2     = 6
  LNO       = 7
  LNO2      = 8
  LNO3      = 9
  LHNO3     = 10
  LHNO4     = 11
  LN2O5     = 12
  LHONO     = 13
  LCH4      = 14
  LCH3O2    = 15
  LCH3OOH   = 16
  LC2H6     = 17
  LC2H5O2   = 18
  LC2H5OOH  = 19
  LC3H8     = 20
  LNC3H7O2  = 21
  LIC3H7O2  = 22
  LNC3H7OH  = 23
  LIC3H7OH  = 24
  LNBUTANE  = 25
  LIBUTANE  = 26
  LSC4H9O2  = 27
  LNC4H9O2  = 28
  LTC4H9O2  = 29
  LIC4H9O2  = 30
  LSC4H9OH  = 31
  LNC4H9OH  = 32
  LTC4H9OH  = 33
  LIC4H9OH  = 34
  LSC4H9OOH = 35
  LNC4H9OOH = 36
  LHCHO     = 37
  LCH3CHO   = 38
  LMEK      = 39
  LACETONE  = 40
  LPROPANAL = 41
  LBUTANAL  = 42
  LIBUTANAL = 43
  LCH3CO3   = 44
  LPAN      = 45
  LCL       = 46
  LCL2      = 47
  LCLO      = 48
  LOCLO     = 49
  LHOCL     = 50
  LHCL      = 51
  LCLNO2    = 52
  LCLNO3    = 53
  LBR       = 54
  LBR2      = 55
  LBRO      = 56
  LHOBR     = 57
  LHBR      = 58
  LBRCL     = 59
  LBRONO    = 60
  LBRNO2    = 61
  LBRNO3    = 62
  LH2O      = 63
  LCLM_P    = 64
  LBRM_P    = 65
  LO3_P     = 66
  LHOCL_P   = 67
  LCL2_P    = 68
  LHOBR_P   = 69
  LBR2_P    = 70
  LBRCL_P   = 71
  
  ph_o31d = 0.0 
  ph_o33p = 0.0
  ph_no2 = 0.0
  ph_no3o2 = 0.0
  ph_no3o = 0.0
  ph_hno2 = 0.0
  ph_hno3 = 0.0
  ph_hno4 = 0.0
  ph_h2o2 = 0.0
  ph_ch2or = 0.0
  ph_ch2om = 0.0
  ph_ch3cho = 0.0
  ph_ch3coch3 = 0.0
  ph_ch3coc2h5 = 0.0
  ph_hcocho = 0.0
  ph_ch3cocho = 0.0
  ph_hcochest = 0.0
  ph_ch3o2h = 0.0
  ph_ch3coo2h = 0.0
  ph_ch3ono2 = 0.0
  ph_hcochob = 0.0
  ph_macr = 0.0
  ph_n2o5 = 0.0
  ph_o2 = 0.0
  ph_pan = 0.0
  ph_acet = 0.0
  ph_mglo = 0.0
  ph_hno4_2 = 0.0
  ph_n2o = 0.0
  ph_pooh = 0.0
  ph_mpan = 0.0
  ph_mvk = 0.0
  ph_etooh = 0.0
  ph_prooh = 0.0
  ph_onitr = 0.0
  ph_acetol = 0.0
  ph_glyald = 0.0
  ph_hyac = 0.0
  ph_mek = 0.0
  ph_open = 0.0
  ph_gly = 0.0
  ph_acetp = 0.0
  ph_xooh = 0.0
  ph_isooh = 0.0
  ph_alkooh = 0.0
  ph_mekooh = 0.0
  ph_tolooh = 0.0
  ph_terpooh = 0.0
  ph_cl2 = 0.0
  ph_hno4a = 0.0
  ph_hno4b = 0.0
  ph_propanal = 0.0
  ph_acetone = 0.0
  ph_ch3ooh = 0.0
  ph_oclo = 0.0
  ph_clo = 0.0
  ph_clno2 = 0.0
  ph_clno3a = 0.0
  ph_clno3b = 0.0
  ph_bro = 0.0
  ph_br2 = 0.0
  ph_hobr = 0.0
  ph_brno2 = 0.0
  ph_brno3a = 0.0
  ph_brno3b = 0.0
  ph_brcl = 0.0
  ph_hocl = 0.0
  ph_fmcl = 0.0
 
  
  #        LO1D   LO3P   LOH    LHO2   LCO     LO3     LH2O2   LNO
  henry = [1e-22, 1e-22, 1e-22, 1e-22, 8.2e-3, 0.0133, 7.45e4, 1.9e-3,
  #        LNO2    LNO3 LHNO3    LHNO4 LN2O5 LHONO   LCH4    LCH3O2
           0.0064, 15,  2.69e13, 2e13, 1e20, 3.47e5, 1.5e-3, 1e-22,
  #        LCH3OOH LC2H6  LC2H5O2 LC2H5OOH LC3H8  LnC3HO2 LiC3H7O2 LnC3H7OH
           1e-22,  1e-22, 1e-22,  1e-22,   1e-22, 1e-22,  1e-22,   1e-22,
  #        LiC3H7OH LnButane LiButane LsC4H9O2 LnC4H9O2 LtC4H9O2 LiC4H9O2 LsC4H9OH
           1e-22,   1e-22,   1e-22,   1e-22,   1e-22,   1e-22,   1e-22,   1e-22,
  #        LnC4H9OH LtC4H9OH LiC4H9OH LsC4H9OOH LnC4H9OOH LHCHO  LCH3CHO LMEK
           1e-22,   1e-22,   1e-22,   1e-22,    1e-22,    22970, 1e-22,  1e-22,
  #        LAcetone Lpropanal LButanal LiButanal LCH3CO3 LPAN  LCl    LCl2
           1e-22,   1e-22,    1e-22,   1e-22,    1e-22,  2.97, 1e-22, 1e-22,
  #        LClO   LOClO  LHOCl  LHCl   LClNO2 LClNO3 LBr    LBr2
           1e-22, 1e-22, 1e-22, 1e-22, 1e-22, 1e-22, 1e-22, 1e-22,
  #        LBrO   LHOBr  LHBr   LBrCl  LBrONO LBrNO2 LBrNO3 LH2O
           1e-22, 1e-22, 1e-22, 1e-22, 1e-22, 1e-22, 1e-22, 1e-22,
  #        lclm_p lbrm_p lO3_p  lHOCl_p lCl2_p lHOBr_p lBr2_p lBrCl_p
           1e-22, 1e-22, 1e-22, 1e-22,  1e-22, 1e-22,  1e-22, 1e-22] 
           
  #        LO1D LO3P LOH LHO2 LCO LO3 LH2O2 LNO
  f0    = [0,   0,   1,  1,   0,  1,  1,    0,
  #        LNO2 LNO3 LHNO3 LHNO4 LN2O5 LHONO LCH4 LCH3O2
           0.1, 1,   0,    0,    1,    0.1,  0,   0,
  #        LCH3OOH LC2H6 LC2H5O2 LC2H5OOH LC3H8 LnC3HO2 LiC3H7O2 LnC3H7OH
           0,      0,    0,      0,       0,    0,      0,       0,
  #        LiC3H7OH LnButane LiButane LsC4H9O2 LnC4H9O2 LtC4H9O2 LiC4H9O2 LsC4H9OH
           0,       0,       0,       0,       0,       0,       0,       0,
  #        LnC4H9OH LtC4H9OH LiC4H9OH LsC4H9OOH LnC4H9OOH LHCHO  LCH3CHO LMEK
           0,       0,       0,       0,        0,        1,     0,      0,
  #        LAcetone Lpropanal LButanal LiButanal LCH3CO3 LPAN  LCl    LCl2
           0,       0,        0,       0,        0,      0.1,  0,     0,
  #        LClO LOClO LHOCl LHCl LClNO2 LClNO3 LBr LBr2
           0,   0,    0,    0,   0,     0,     0,  0,  
  #        LBrO LHOBr LHBr LBrCl LBrONO LBrNO2 LBrNO3 LH2O
           0,   0,    0,   0,    0,     0,     0,     0,  
  #        lclm_p lbrm_p lO3_p lHOCl_p lCl2_p lHOBr_p lBr2_p lBrCl_p
           0,     0,     0,    0,      0,     0,      0,     0]

  # ----------------------------
  # Belows are probably not used
  # ----------------------------  

  #        ACO3 ADDC ADDT ADDX ALD  API  APIP CH4 
  dfakt = [2,   2.3, 2.2, 2.3, 1.6, 2.6, 2.6, 0.9,
  #        CO   CO2  CSL  CSLP DCB  DIEN ETE  ETEP
           1.2, 1.5, 2.4, 2.4, 2.1, 1.7, 1.9, 1.9,
  #        ETH  ETHP GLY  H2   H2O  H2O2 HC3  HC3P
           1.2, 1.2, 1.7, 0.2, 1,   1.4, 1.5, 1.5,
  #        HC5  HC5P HC8  HC8P HCHO HKET HNO3  HNO4
           1.9, 1,   2.4, 2.5, 1.3, 2,   1.92, 2.14,
  #        HO   HO2  HONO  ISO  ISOP KET KETP  LIM
           1,   1.3, 1.58, 1.9, 1.9, 2,  1.9, 2.6,
  #        LIMP MACR MGLY MO2 N2   N2O5 NO    NO2
           2.6, 1.9, 1.9, 1,  0.9, 2.2, 1.32, 1.646,
  #        NO3  O1D O2 O3   O3P OLI  OLIP OLND
           1.8, 1,  1, 1.4, 1,  1.9, 1.9, 1.5,
  #        OLNN OLT  OLTP ONIT OP1  OP2  ORA1  ORA2
           1.5, 1.5, 1.5, 2.5, 1.6, 1.8, 1.6, 1.8,
  #        PAA PAN   PHO SO2  SULF TCO3 TOL  TOLP
           2,  2.66, 1,  1.9, 0.2, 1.8, 2.3, 2.3]
    
  tdf_prm = [0.09,    # isoprene
             0.09,    # MBO (only (2-methyl-3-ene-2-ol)-methylbutenol) 
             0.1,     # myrcene
             0.1,     # sabinene
             0.1,     # limonene
             0.1,     # 3 carene
             0.1,     # trans-beta-ocimene
             0.1,     # beta-pinene
             0.1,     # alpha-pinene
             0.17,    # alpha-farnescene
             0.17,    # beta-caryophyllene
             0.08,    # methanol
             0.11,    # acetone
             0.13,    # acetaldehyde and ethanol
             0.09,    # formic acid, formaldehyde, acetic acid
             0.05,    # methane
             0.11,    # nitric oxide (and NO2 and NH3 )
             0.1,     # other monoterpenes
             0.17,    # other sesquiterpenes
             0.09]    # CO and other VOC
             
  anew = [1, 2, 0.4, 3, 0.05]
  agro = [1, 1.8, 0.6, 2.6, 0.6]
  amat = [1, 0.95, 1.075, 0.85, 1.125]
  aold = [1, 1, 1, 1, 1]
  
  ldf_fct = [0.9999,  # isoprene
             0.9999,  # MBO (only (2-methyl-3-ene-2-ol)-methylbutenol) 
             0.05,    # myrcene
             0.1,     # sabinene
             0.05,    # limonene
             0.05,    # 3 carene
             0.8,     # trans-beta-ocimene
             0.1,     # beta-pinene
             0.1,     # alpha-pinene
             0.5,     # alpha-farnescene
             0.5,     # beta-caryophyllene
             0.75,    # methanol
             0.25,    # acetone
             0.5,     # acetaldehyde and ethanol
             0.5,     # formic acid, formaldehyde, acetic acid
             0.75,    # methane
             0,       # nitric oxide (and NO2 and NH3 )
             0.1,     # other monoterpenes
             0.5,     # other sesquiterpenes
             0.5]     # CO and other VOC
               
