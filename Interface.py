import numpy as np
import math

import Parameters as pm
import racm_Parameters as rpm
import racmpm_Parameters as rpmpm
import racmsorg_Parameters as rsm

import Update_Rconst
import Integrate

class Interface():

  UPGC = Update_Rconst.Update_Rconst()
  ITGT = Integrate.execute()

  def racm(self, vc, RCONST, atols, rtols, deltim, dens2con_a, rho_phy, dens2con_w, moist):
  
    # Parameters
    
    NJV = 68
    TEMP = 0
    TIME_START = 0
    TIME_END = 0
    IERR = 0
    
    jv  = np.full(NJV, 0, dtype = object)
    var = np.full(rpm.Param.NVAR, 0, dtype = object)
    fix = np.full(rpm.Param.NFIX, 0, dtype = object)
      
    ATOL = np.full(pm.Param.nspec_host, 0, dtype = object)
    RTOL = np.full(pm.Param.nspec_host, 0, dtype = object)
    
    ICNTRL = np.full(20, 0, dtype = object)
    RCNTRL = np.full(20, 0, dtype = object)
    
    # Function
  
    for i in range(pm.Param.nspec_host):
      ATOL[i] = atols
      RTOL[i] = rtols
      
    TIME_END = deltim
    
    ICNTRL[0] = 1
    ICNTRL[2] = 2
    RCNTRL[2] = 0.01 * TIME_END
    
    fix[rpm.Param.indf_M] = dens2con_a * rho_phy
    C_M = fix[rpm.Param.indf_M]
    
    fix[rpm.Param.indf_H2O] = dens2con_w * moist * rho_phy
    
    TEMP = pm.Param.tt
    
    conv = dens2con_a * rho_phy
    oconv = 1e0 / conv
    
    jv[rpm.Param.Pj_o31d] = pm.Param.ph_o31d 
    jv[rpm.Param.Pj_o33p] = pm.Param.ph_o33p 
    jv[rpm.Param.Pj_no2]  = pm.Param.ph_no2 
    jv[rpm.Param.Pj_no3o2] = pm.Param.ph_no3o2 
    jv[rpm.Param.Pj_no3o] = pm.Param.ph_no3o 
    jv[rpm.Param.Pj_hno2] = pm.Param.ph_hno2 
    jv[rpm.Param.Pj_hno3] = pm.Param.ph_hno3 
    jv[rpm.Param.Pj_hno4] = pm.Param.ph_hno4 
    jv[rpm.Param.Pj_h2o2] = pm.Param.ph_h2o2 
    jv[rpm.Param.Pj_ch2or] = pm.Param.ph_ch2or 
    jv[rpm.Param.Pj_ch2om] = pm.Param.ph_ch2om 
    jv[rpm.Param.Pj_ch3cho] = pm.Param.ph_ch3cho 
    jv[rpm.Param.Pj_ch3coch3] = pm.Param.ph_ch3coch3 
    jv[rpm.Param.Pj_ch3coc2h5] = pm.Param.ph_ch3coc2h5 
    jv[rpm.Param.Pj_hcocho] = pm.Param.ph_hcocho 
    jv[rpm.Param.Pj_ch3cocho] = pm.Param.ph_ch3cocho 
    jv[rpm.Param.Pj_hcochest] = pm.Param.ph_hcochest 
    jv[rpm.Param.Pj_ch3o2h] = pm.Param.ph_ch3o2h 
    jv[rpm.Param.Pj_ch3coo2h] = pm.Param.ph_ch3coo2h 
    jv[rpm.Param.Pj_ch3ono2] = pm.Param.ph_ch3ono2 
    jv[rpm.Param.Pj_hcochob] = pm.Param.ph_hcochob 
    jv[rpm.Param.Pj_macr] = pm.Param.ph_macr 
    jv[rpm.Param.Pj_n2o5] = pm.Param.ph_n2o5 
    jv[rpm.Param.Pj_o2] = pm.Param.ph_o2 
    jv[rpm.Param.Pj_pan] = pm.Param.ph_pan 
    jv[rpm.Param.Pj_acet] = pm.Param.ph_acet 
    jv[rpm.Param.Pj_mglo] = pm.Param.ph_mglo 
    jv[rpm.Param.Pj_hno4_2] = pm.Param.ph_hno4_2 
    jv[rpm.Param.Pj_n2o] = pm.Param.ph_n2o 
    jv[rpm.Param.Pj_pooh] = pm.Param.ph_pooh 
    jv[rpm.Param.Pj_mpan] = pm.Param.ph_mpan 
    jv[rpm.Param.Pj_mvk] = pm.Param.ph_mvk 
    jv[rpm.Param.Pj_etooh] = pm.Param.ph_etooh 
    jv[rpm.Param.Pj_prooh] = pm.Param.ph_prooh 
    jv[rpm.Param.Pj_onitr] = pm.Param.ph_onitr 
    jv[rpm.Param.Pj_acetol] = pm.Param.ph_acetol 
    jv[rpm.Param.Pj_glyald] = pm.Param.ph_glyald 
    jv[rpm.Param.Pj_hyac] = pm.Param.ph_hyac 
    jv[rpm.Param.Pj_mek] = pm.Param.ph_mek 
    jv[rpm.Param.Pj_open] = pm.Param.ph_open 
    jv[rpm.Param.Pj_gly] = pm.Param.ph_gly 
    jv[rpm.Param.Pj_acetp] = pm.Param.ph_acetp 
    jv[rpm.Param.Pj_xooh] = pm.Param.ph_xooh 
    jv[rpm.Param.Pj_isooh] = pm.Param.ph_isooh 
    jv[rpm.Param.Pj_alkooh] = pm.Param.ph_alkooh 
    jv[rpm.Param.Pj_mekooh] = pm.Param.ph_mekooh 
    jv[rpm.Param.Pj_tolooh] = pm.Param.ph_tolooh 
    jv[rpm.Param.Pj_terpooh] = pm.Param.ph_terpooh 
    jv[rpm.Param.Pj_cl2] = pm.Param.ph_cl2 
    jv[rpm.Param.Pj_hno4a] = pm.Param.ph_hno4a 
    jv[rpm.Param.Pj_hno4b] = pm.Param.ph_hno4b 
    jv[rpm.Param.Pj_propanal] = pm.Param.ph_propanal 
    jv[rpm.Param.Pj_acetone] = pm.Param.ph_acetone 
    jv[rpm.Param.Pj_ch3ooh] = pm.Param.ph_ch3ooh 
    jv[rpm.Param.Pj_oclo] = pm.Param.ph_oclo 
    jv[rpm.Param.Pj_clo] = pm.Param.ph_clo 
    jv[rpm.Param.Pj_clno2] = pm.Param.ph_clno2 
    jv[rpm.Param.Pj_clno3a] = pm.Param.ph_clno3a 
    jv[rpm.Param.Pj_clno3b] = pm.Param.ph_clno3b 
    jv[rpm.Param.Pj_bro] = pm.Param.ph_bro 
    jv[rpm.Param.Pj_br2] = pm.Param.ph_br2 
    jv[rpm.Param.Pj_hobr] = pm.Param.ph_hobr 
    jv[rpm.Param.Pj_brno2] = pm.Param.ph_brno2 
    jv[rpm.Param.Pj_brno3a] = pm.Param.ph_brno3a 
    jv[rpm.Param.Pj_brno3b] = pm.Param.ph_brno3b 
    jv[rpm.Param.Pj_brcl] = pm.Param.ph_brcl 
    jv[rpm.Param.Pj_hocl] = pm.Param.ph_hocl 
    jv[rpm.Param.Pj_fmcl] = pm.Param.ph_fmcl 
    
    var[rpm.Param.ind_O1D] =  conv * max(vc[pm.Param.LO1D], 0)  
    var[rpm.Param.ind_O3P] =  conv * max(vc[pm.Param.LO3P], 0)  
    var[rpm.Param.ind_OH] = conv  * max(vc[pm.Param.LOH], 0)  
    var[rpm.Param.ind_HO2] = conv  * max(vc[pm.Param.LHO2], 0)  
    var[rpm.Param.ind_CO] = conv  * max(vc[pm.Param.LCO], 0)  
    var[rpm.Param.ind_O3] = conv  * max(vc[pm.Param.LO3], 0)  
    var[rpm.Param.ind_H2O2] = conv  * max(vc[pm.Param.LH2O2], 0)  
    var[rpm.Param.ind_NO] = conv  * max(vc[pm.Param.LNO], 0)  
    var[rpm.Param.ind_NO2] = conv  * max(vc[pm.Param.LNO2], 0)  
    var[rpm.Param.ind_NO3] = conv  * max(vc[pm.Param.LNO3], 0)  
    var[rpm.Param.ind_HNO3] = conv  * max(vc[pm.Param.LHNO3], 0)  
    var[rpm.Param.ind_HNO4] = conv  * max(vc[pm.Param.LHNO4], 0)  
    var[rpm.Param.ind_N2O5] = conv  * max(vc[pm.Param.LN2O5], 0)  
    var[rpm.Param.ind_HONO] = conv  * max(vc[pm.Param.LHONO], 0)  
    var[rpm.Param.ind_CH4] = conv  * max(vc[pm.Param.LCH4], 0)  
    var[rpm.Param.ind_CH3O2] = conv  * max(vc[pm.Param.LCH3O2], 0)  
    var[rpm.Param.ind_CH3OOH] = conv  * max(vc[pm.Param.LCH3OOH], 0)  
    var[rpm.Param.ind_C2H6] = conv  * max(vc[pm.Param.LC2H6], 0)  
    var[rpm.Param.ind_C2H5O2] = conv  * max(vc[pm.Param.LC2H5O2], 0)  
    var[rpm.Param.ind_C2H5OOH] = conv  * max(vc[pm.Param.LC2H5OOH], 0)  
    var[rpm.Param.ind_C3H8] = conv  * max(vc[pm.Param.LC3H8], 0)  
    var[rpm.Param.ind_nC3H7O2] = conv  * max(vc[pm.Param.LNC3H7O2], 0)  
    var[rpm.Param.ind_iC3H7O2] = conv  * max(vc[pm.Param.LIC3H7O2], 0)  
    var[rpm.Param.ind_nC3H7OH] = conv  * max(vc[pm.Param.LNC3H7OH], 0)  
    var[rpm.Param.ind_iC3H7OH] = conv  * max(vc[pm.Param.LIC3H7OH], 0)  
    var[rpm.Param.ind_nButane] = conv  * max(vc[pm.Param.LNBUTANE], 0)  
    var[rpm.Param.ind_iButane] = conv  * max(vc[pm.Param.LIBUTANE], 0)  
    var[rpm.Param.ind_sC4H9O2] = conv  * max(vc[pm.Param.LSC4H9O2], 0)  
    var[rpm.Param.ind_nC4H9O2] = conv  * max(vc[pm.Param.LNC4H9O2], 0)  
    var[rpm.Param.ind_tC4H9O2] = conv  * max(vc[pm.Param.LTC4H9O2], 0)  
    var[rpm.Param.ind_iC4H9O2] = conv  * max(vc[pm.Param.LIC4H9O2], 0)  
    var[rpm.Param.ind_sC4H9OH] = conv  * max(vc[pm.Param.LSC4H9OH], 0)  
    var[rpm.Param.ind_nC4H9OH] = conv  * max(vc[pm.Param.LNC4H9OH], 0)  
    var[rpm.Param.ind_tC4H9OH] = conv  * max(vc[pm.Param.LTC4H9OH], 0)  
    var[rpm.Param.ind_iC4H9OH] = conv  * max(vc[pm.Param.LIC4H9OH], 0)  
    var[rpm.Param.ind_sC4H9OOH] = conv  * max(vc[pm.Param.LSC4H9OOH], 0)  
    var[rpm.Param.ind_nC4H9OOH] = conv  * max(vc[pm.Param.LNC4H9OOH], 0)  
    var[rpm.Param.ind_HCHO] = conv  * max(vc[pm.Param.LHCHO], 0)  
    var[rpm.Param.ind_CH3CHO] = conv  * max(vc[pm.Param.LCH3CHO], 0)  
    var[rpm.Param.ind_MEK] = conv  * max(vc[pm.Param.LMEK], 0)  
    var[rpm.Param.ind_Acetone] = conv  * max(vc[pm.Param.LACETONE], 0)  
    var[rpm.Param.ind_Propanal] = conv  * max(vc[pm.Param.LPROPANAL], 0)  
    var[rpm.Param.ind_Butanal] = conv  * max(vc[pm.Param.LBUTANAL], 0)  
    var[rpm.Param.ind_iButanal] = conv  * max(vc[pm.Param.LIBUTANAL], 0)  
    var[rpm.Param.ind_CH3CO3] = conv  * max(vc[pm.Param.LCH3CO3], 0)  
    var[rpm.Param.ind_PAN] = conv  * max(vc[pm.Param.LPAN], 0)  
    var[rpm.Param.ind_Cl] = conv  * max(vc[pm.Param.LCL], 0)  
    var[rpm.Param.ind_Cl2] = conv  * max(vc[pm.Param.LCL2], 0)  
    var[rpm.Param.ind_ClO] = conv  * max(vc[pm.Param.LCLO], 0)  
    var[rpm.Param.ind_OClO] = conv  * max(vc[pm.Param.LOCLO], 0)  
    var[rpm.Param.ind_HOCl] = conv  * max(vc[pm.Param.LHOCL], 0)  
    var[rpm.Param.ind_HCl] = conv  * max(vc[pm.Param.LHCL], 0)  
    var[rpm.Param.ind_ClNO2] = conv  * max(vc[pm.Param.LCLNO2], 0)  
    var[rpm.Param.ind_ClNO3] = conv  * max(vc[pm.Param.LCLNO3], 0)  
    var[rpm.Param.ind_Br] = conv  * max(vc[pm.Param.LBR], 0)  
    var[rpm.Param.ind_Br2] = conv  * max(vc[pm.Param.LBR2], 0)  
    var[rpm.Param.ind_BrO] = conv  * max(vc[pm.Param.LBRO], 0)  
    var[rpm.Param.ind_HOBr] = conv  * max(vc[pm.Param.LHOBR], 0)  
    var[rpm.Param.ind_HBr] = conv  * max(vc[pm.Param.LHBR], 0)  
    var[rpm.Param.ind_BrCl] = conv  * max(vc[pm.Param.LBRCL], 0)  
    var[rpm.Param.ind_BrONO] = conv  * max(vc[pm.Param.LBRONO], 0)  
    var[rpm.Param.ind_BrNO2] = conv  * max(vc[pm.Param.LBRNO2], 0)  
    var[rpm.Param.ind_BrNO3] = conv  * max(vc[pm.Param.LBRNO3], 0) 
   
    RCONST = Interface.UPGC.racm(RCONST, fix, jv, TEMP, C_M)
    
    var = Interface.ITGT.Integrate('racm', RCONST, rpm.Param.NVAR, rpm.Param.NREACT, var, rpm.Param.LU_NONZERO, fix, TIME_START, TIME_END, ICNTRL, RCNTRL, ATOL, RTOL)
    
    vc[pm.Param.LO1D] = max((oconv * var[rpm.Param.ind_O1D]), 0) 
    vc[pm.Param.LO3P] = max((oconv * var[rpm.Param.ind_O3P]), 0) 
    vc[pm.Param.LOH] = max((oconv * var[rpm.Param.ind_OH]),  0)  
    vc[pm.Param.LHO2] = max((oconv * var[rpm.Param.ind_HO2]),  0)  
    vc[pm.Param.LCO] = max((oconv * var[rpm.Param.ind_CO]),  0)  
    vc[pm.Param.LO3] = max((oconv * var[rpm.Param.ind_O3]),  0)  
    vc[pm.Param.LH2O2] = max((oconv * var[rpm.Param.ind_H2O2]),  0)  
    vc[pm.Param.LNO] = max((oconv * var[rpm.Param.ind_NO]),  0)  
    vc[pm.Param.LNO2] = max((oconv * var[rpm.Param.ind_NO2]),  0)  
    vc[pm.Param.LNO3] = max((oconv * var[rpm.Param.ind_NO3]),  0)  
    vc[pm.Param.LHNO3] = max((oconv * var[rpm.Param.ind_HNO3]),  0)  
    vc[pm.Param.LHNO4] = max((oconv * var[rpm.Param.ind_HNO4]),  0)  
    vc[pm.Param.LN2O5] = max((oconv * var[rpm.Param.ind_N2O5]),  0)  
    vc[pm.Param.LHONO] = max((oconv * var[rpm.Param.ind_HONO]),  0)  
    vc[pm.Param.LCH4] = max((oconv * var[rpm.Param.ind_CH4]),  0)  
    vc[pm.Param.LCH3O2] = max((oconv * var[rpm.Param.ind_CH3O2]),  0)  
    vc[pm.Param.LCH3OOH] = max((oconv * var[rpm.Param.ind_CH3OOH]),  0)  
    vc[pm.Param.LC2H6] = max((oconv * var[rpm.Param.ind_C2H6]),  0)  
    vc[pm.Param.LC2H5O2] = max((oconv * var[rpm.Param.ind_C2H5O2]),  0)  
    vc[pm.Param.LC2H5OOH] = max((oconv * var[rpm.Param.ind_C2H5OOH]),  0)  
    vc[pm.Param.LC3H8] = max((oconv * var[rpm.Param.ind_C3H8]),  0)  
    vc[pm.Param.LNC3H7O2] = max((oconv * var[rpm.Param.ind_nC3H7O2]),  0)  
    vc[pm.Param.LIC3H7O2] = max((oconv * var[rpm.Param.ind_iC3H7O2]),  0)  
    vc[pm.Param.LNC3H7OH] = max((oconv * var[rpm.Param.ind_nC3H7OH]),  0)  
    vc[pm.Param.LIC3H7OH] = max((oconv * var[rpm.Param.ind_iC3H7OH]),  0)  
    vc[pm.Param.LNBUTANE] = max((oconv * var[rpm.Param.ind_nButane]),  0)  
    vc[pm.Param.LIBUTANE] = max((oconv * var[rpm.Param.ind_iButane]),  0)  
    vc[pm.Param.LSC4H9O2] = max((oconv * var[rpm.Param.ind_sC4H9O2]),  0)  
    vc[pm.Param.LNC4H9O2] = max((oconv * var[rpm.Param.ind_nC4H9O2]),  0)  
    vc[pm.Param.LTC4H9O2] = max((oconv * var[rpm.Param.ind_tC4H9O2]),  0)  
    vc[pm.Param.LIC4H9O2] = max((oconv * var[rpm.Param.ind_iC4H9O2]),  0)  
    vc[pm.Param.LSC4H9OH] = max((oconv * var[rpm.Param.ind_sC4H9OH]),  0)  
    vc[pm.Param.LNC4H9OH] = max((oconv * var[rpm.Param.ind_nC4H9OH]),  0)  
    vc[pm.Param.LTC4H9OH] = max((oconv * var[rpm.Param.ind_tC4H9OH]),  0)  
    vc[pm.Param.LIC4H9OH] = max((oconv * var[rpm.Param.ind_iC4H9OH]),  0)  
    vc[pm.Param.LSC4H9OOH] = max((oconv * var[rpm.Param.ind_sC4H9OOH]),  0)  
    vc[pm.Param.LNC4H9OOH] = max((oconv * var[rpm.Param.ind_nC4H9OOH]),  0)  
    vc[pm.Param.LHCHO] = max((oconv * var[rpm.Param.ind_HCHO]),  0)  
    vc[pm.Param.LCH3CHO] = max((oconv * var[rpm.Param.ind_CH3CHO]),  0)  
    vc[pm.Param.LMEK] = max((oconv * var[rpm.Param.ind_MEK]),  0)  
    vc[pm.Param.LACETONE] = max((oconv * var[rpm.Param.ind_Acetone]),  0)  
    vc[pm.Param.LPROPANAL] = max((oconv * var[rpm.Param.ind_Propanal]),  0)  
    vc[pm.Param.LBUTANAL] = max((oconv * var[rpm.Param.ind_Butanal]),  0)  
    vc[pm.Param.LIBUTANAL] = max((oconv * var[rpm.Param.ind_iButanal]),  0)  
    vc[pm.Param.LCH3CO3] = max((oconv * var[rpm.Param.ind_CH3CO3]),  0)  
    vc[pm.Param.LPAN] = max((oconv * var[rpm.Param.ind_PAN]),  0)  
    vc[pm.Param.LCL] = max((oconv * var[rpm.Param.ind_Cl]),  0)  
    vc[pm.Param.LCL2] = max((oconv * var[rpm.Param.ind_Cl2]),  0)  
    vc[pm.Param.LCLO] = max((oconv * var[rpm.Param.ind_ClO]),  0)  
    vc[pm.Param.LOCLO] = max((oconv * var[rpm.Param.ind_OClO]),  0)  
    vc[pm.Param.LHOCL] = max((oconv * var[rpm.Param.ind_HOCl]),  0)  
    vc[pm.Param.LHCL] = max((oconv * var[rpm.Param.ind_HCl]),  0)  
    vc[pm.Param.LCLNO2] = max((oconv * var[rpm.Param.ind_ClNO2]),  0)  
    vc[pm.Param.LCLNO3] = max((oconv * var[rpm.Param.ind_ClNO3]),  0)  
    vc[pm.Param.LBR] = max((oconv * var[rpm.Param.ind_Br]),  0)  
    vc[pm.Param.LBR2] = max((oconv * var[rpm.Param.ind_Br2]),  0)  
    vc[pm.Param.LBRO] = max((oconv * var[rpm.Param.ind_BrO]),  0)  
    vc[pm.Param.LHOBR] = max((oconv * var[rpm.Param.ind_HOBr]),  0)  
    vc[pm.Param.LHBR] = max((oconv * var[rpm.Param.ind_HBr]),  0)  
    vc[pm.Param.LBRCL] = max((oconv * var[rpm.Param.ind_BrCl]),  0)  
    vc[pm.Param.LBRONO] = max((oconv * var[rpm.Param.ind_BrONO]),  0)  
    vc[pm.Param.LBRNO2] = max((oconv * var[rpm.Param.ind_BrNO2]),  0)  
    vc[pm.Param.LBRNO3] = max((oconv * var[rpm.Param.ind_BrNO3]),  0)

    return vc, RCONST
    
    
  def racmpm(self, vc, RCONST, atols, rtols, deltim, dens2con_a, rho_phy, dens2con_w, moist, Mono_Dis_Het):
  
    # Parameters
    
    NJV = 68
    TEMP = 0
    TIME_START = 0
    TIME_END = 0
    IERR = 0
    
    jv  = np.full(NJV, 0, dtype = object)
    var = np.full(rpmpm.Param.NVAR, 0, dtype = object)
    fix = np.full(rpmpm.Param.NFIX, 0, dtype = object)
      
    ATOL = np.full(pm.Param.nspec_host, 0, dtype = object)
    RTOL = np.full(pm.Param.nspec_host, 0, dtype = object)
    
    ICNTRL = np.full(20, 0, dtype = object)
    RCNTRL = np.full(20, 0, dtype = object)
    
    # Function
      
    for i in range(pm.Param.nspec_host):
      ATOL[i] = atols
      RTOL[i] = rtols
      
    TIME_END = deltim
      
    ICNTRL[0] = 1
    ICNTRL[2] = 2
    RCNTRL[2] = 0.01 * TIME_END
    
    fix[rpmpm.Param.indf_M] = dens2con_a * rho_phy
    
    fix[rpmpm.Param.indf_H2O] = dens2con_w * moist * rho_phy
    
    TEMP = pm.Param.tt

    conv = dens2con_a * rho_phy
    oconv = 1e0 / conv
    
    jv[rpmpm.Param.Pj_o31d] = pm.Param.ph_o31d
    jv[rpmpm.Param.Pj_o33p] = pm.Param.ph_o33p
    jv[rpmpm.Param.Pj_no2] = pm.Param.ph_no2
    jv[rpmpm.Param.Pj_no3o2] = pm.Param.ph_no3o2
    jv[rpmpm.Param.Pj_no3o] = pm.Param.ph_no3o
    jv[rpmpm.Param.Pj_hno2] = pm.Param.ph_hno2
    jv[rpmpm.Param.Pj_hno3] = pm.Param.ph_hno3
    jv[rpmpm.Param.Pj_hno4] = pm.Param.ph_hno4
    jv[rpmpm.Param.Pj_h2o2] = pm.Param.ph_h2o2
    jv[rpmpm.Param.Pj_ch2or] = pm.Param.ph_ch2or
    jv[rpmpm.Param.Pj_ch2om] = pm.Param.ph_ch2om
    jv[rpmpm.Param.Pj_ch3cho] = pm.Param.ph_ch3cho
    jv[rpmpm.Param.Pj_ch3coch3] = pm.Param.ph_ch3coch3
    jv[rpmpm.Param.Pj_ch3coc2h5] = pm.Param.ph_ch3coc2h5
    jv[rpmpm.Param.Pj_hcocho] = pm.Param.ph_hcocho
    jv[rpmpm.Param.Pj_ch3cocho] = pm.Param.ph_ch3cocho
    jv[rpmpm.Param.Pj_hcochest] = pm.Param.ph_hcochest
    jv[rpmpm.Param.Pj_ch3o2h] = pm.Param.ph_ch3o2h
    jv[rpmpm.Param.Pj_ch3coo2h] = pm.Param.ph_ch3coo2h
    jv[rpmpm.Param.Pj_ch3ono2] = pm.Param.ph_ch3ono2
    jv[rpmpm.Param.Pj_hcochob] = pm.Param.ph_hcochob
    jv[rpmpm.Param.Pj_macr] = pm.Param.ph_macr
    jv[rpmpm.Param.Pj_n2o5] = pm.Param.ph_n2o5
    jv[rpmpm.Param.Pj_o2] = pm.Param.ph_o2
    jv[rpmpm.Param.Pj_pan] = pm.Param.ph_pan
    jv[rpmpm.Param.Pj_acet] = pm.Param.ph_acet
    jv[rpmpm.Param.Pj_mglo] = pm.Param.ph_mglo
    jv[rpmpm.Param.Pj_hno4_2] = pm.Param.ph_hno4_2
    jv[rpmpm.Param.Pj_n2o] = pm.Param.ph_n2o
    jv[rpmpm.Param.Pj_pooh] = pm.Param.ph_pooh
    jv[rpmpm.Param.Pj_mpan] = pm.Param.ph_mpan
    jv[rpmpm.Param.Pj_mvk] = pm.Param.ph_mvk
    jv[rpmpm.Param.Pj_etooh] = pm.Param.ph_etooh
    jv[rpmpm.Param.Pj_prooh] = pm.Param.ph_prooh
    jv[rpmpm.Param.Pj_onitr] = pm.Param.ph_onitr
    jv[rpmpm.Param.Pj_acetol] = pm.Param.ph_acetol
    jv[rpmpm.Param.Pj_glyald] = pm.Param.ph_glyald
    jv[rpmpm.Param.Pj_hyac] = pm.Param.ph_hyac
    jv[rpmpm.Param.Pj_mek] = pm.Param.ph_mek
    jv[rpmpm.Param.Pj_open] = pm.Param.ph_open
    jv[rpmpm.Param.Pj_gly] = pm.Param.ph_gly
    jv[rpmpm.Param.Pj_acetp] = pm.Param.ph_acetp
    jv[rpmpm.Param.Pj_xooh] = pm.Param.ph_xooh
    jv[rpmpm.Param.Pj_isooh] = pm.Param.ph_isooh
    jv[rpmpm.Param.Pj_alkooh] = pm.Param.ph_alkooh
    jv[rpmpm.Param.Pj_mekooh] = pm.Param.ph_mekooh
    jv[rpmpm.Param.Pj_tolooh] = pm.Param.ph_tolooh
    jv[rpmpm.Param.Pj_terpooh] = pm.Param.ph_terpooh
    jv[rpmpm.Param.Pj_cl2] = pm.Param.ph_cl2
    jv[rpmpm.Param.Pj_hno4a] = pm.Param.ph_hno4a
    jv[rpmpm.Param.Pj_hno4b] = pm.Param.ph_hno4b
    jv[rpmpm.Param.Pj_propanal] = pm.Param.ph_propanal
    jv[rpmpm.Param.Pj_acetone] = pm.Param.ph_acetone
    jv[rpmpm.Param.Pj_ch3ooh] = pm.Param.ph_ch3ooh
    jv[rpmpm.Param.Pj_oclo] = pm.Param.ph_oclo
    jv[rpmpm.Param.Pj_clo] = pm.Param.ph_clo
    jv[rpmpm.Param.Pj_clno2] = pm.Param.ph_clno2
    jv[rpmpm.Param.Pj_clno3a] = pm.Param.ph_clno3a
    jv[rpmpm.Param.Pj_clno3b] = pm.Param.ph_clno3b
    jv[rpmpm.Param.Pj_bro] = pm.Param.ph_bro
    jv[rpmpm.Param.Pj_br2] = pm.Param.ph_br2
    jv[rpmpm.Param.Pj_hobr] = pm.Param.ph_hobr
    jv[rpmpm.Param.Pj_brno2] = pm.Param.ph_brno2
    jv[rpmpm.Param.Pj_brno3a] = pm.Param.ph_brno3a
    jv[rpmpm.Param.Pj_brno3b] = pm.Param.ph_brno3b
    jv[rpmpm.Param.Pj_brcl] = pm.Param.ph_brcl
    jv[rpmpm.Param.Pj_hocl] = pm.Param.ph_hocl
    jv[rpmpm.Param.Pj_fmcl] = pm.Param.ph_fmcl
    
    var[rpmpm.Param.ind_N2O5] = conv * max(vc[pm.Param.LN2O5], 0)
    var[rpmpm.Param.ind_ClNO3] = conv * max(vc[pm.Param.LCLNO3], 0)
    var[rpmpm.Param.ind_HOCl] = conv * max(vc[pm.Param.LHOCL], 0)
    var[rpmpm.Param.ind_Cl2] = conv * max(vc[pm.Param.LCL2], 0)
    var[rpmpm.Param.ind_BrCl] = conv * max(vc[pm.Param.LBRCL], 0)
    var[rpmpm.Param.ind_BrNO3] = conv * max(vc[pm.Param.LBRNO3], 0)
    var[rpmpm.Param.ind_HOBr] = conv * max(vc[pm.Param.LHOBR], 0)
    var[rpmpm.Param.ind_Br2] = conv * max(vc[pm.Param.LBR2], 0)
    var[rpmpm.Param.ind_ClNO2] = conv * max(vc[pm.Param.LCLNO2], 0)
    var[rpmpm.Param.ind_BrNO2] = conv * max(vc[pm.Param.LBRNO2], 0)
    var[rpmpm.Param.ind_Clm_p] = 6.0232e11/35.453 * max(vc[pm.Param.LCLM_P], 0)
    var[rpmpm.Param.ind_Brm_p] = 6.0232e11/79.904 * max(vc[pm.Param.LBRM_P], 0)
    
    RCONST = Interface.UPGC.racmpm(RCONST, TEMP, var, Mono_Dis_Het)
    
    var = Interface.ITGT.Integrate('racmpm', RCONST, rpmpm.Param.NVAR, rpmpm.Param.NREACT, var, rpmpm.Param.LU_NONZERO, fix, TIME_START, TIME_END, ICNTRL, RCNTRL, ATOL, RTOL)
    
    vc[pm.Param.LN2O5] = max((oconv * var[rpmpm.Param.ind_N2O5]), 0)  
    vc[pm.Param.LCLNO3] = max((oconv * var[rpmpm.Param.ind_ClNO3]), 0)  
    vc[pm.Param.LHOCL] = max((oconv * var[rpmpm.Param.ind_HOCl]), 0)  
    vc[pm.Param.LCL2] = max((oconv * var[rpmpm.Param.ind_Cl2]), 0)  
    vc[pm.Param.LBRCL] = max((oconv * var[rpmpm.Param.ind_BrCl]), 0)  
    vc[pm.Param.LBRNO3] = max((oconv * var[rpmpm.Param.ind_BrNO3]), 0)  
    vc[pm.Param.LHOBR] = max((oconv * var[rpmpm.Param.ind_HOBr]), 0)  
    vc[pm.Param.LBR2] = max((oconv * var[rpmpm.Param.ind_Br2]), 0)  
    vc[pm.Param.LCLNO2] = max((oconv * var[rpmpm.Param.ind_ClNO2]), 0)  
    vc[pm.Param.LBRNO2] = max((oconv * var[rpmpm.Param.ind_BrNO2]), 0)  
    vc[pm.Param.LCLM_P] = max((35.453/6.0232e11 * var[rpmpm.Param.ind_Clm_p]), 0)  
    vc[pm.Param.LBRM_P] = max((79.904/6.0232e11 * var[rpmpm.Param.ind_Brm_p]), 0)  
    
    return vc, RCONST
    
    
  def racmsorg(self, vc, RCONST, atols, rtols, deltim, dens2con_a, rho_phy, dens2con_w, moist, LWC_Switch, Mono_Dis_Aq):
  
    # Parameters
    
    NJV = 68
    TEMP = 0
    TIME_START = 0
    TIME_END = 0
    IERR = 0
    
    jv  = np.full(NJV, 0, dtype = object)
    var = np.full(rsm.Param.NVAR, 0, dtype = object)
    fix = np.full(rsm.Param.NFIX, 0, dtype = object)
      
    ATOL = np.full(pm.Param.nspec_host, 0, dtype = object)
    RTOL = np.full(pm.Param.nspec_host, 0, dtype = object)
    
    ICNTRL = np.full(20, 0, dtype = object)
    RCNTRL = np.full(20, 0, dtype = object)
    
    # Function
    
    x = 6.0232e11
  
    for i in range(pm.Param.nspec_host):
      ATOL[i] = atols
      RTOL[i] = rtols
      
    TIME_END = deltim
    
    ICNTRL[0] = 1
    ICNTRL[2] = 2
    RCNTRL[2] = 0.01 * TIME_END
    
    fix[rsm.Param.indf_M] = dens2con_a * rho_phy
    
    fix[rsm.Param.indf_H2O] = dens2con_w * moist * rho_phy
    
    TEMP = pm.Param.tt
    
    conv = dens2con_a * rho_phy
    oconv = 1e0 / conv
    
    jv[rsm.Param.Pj_o31d] = pm.Param.ph_o31d 
    jv[rsm.Param.Pj_o33p] = pm.Param.ph_o33p 
    jv[rsm.Param.Pj_no2]  = pm.Param.ph_no2 
    jv[rsm.Param.Pj_no3o2] = pm.Param.ph_no3o2 
    jv[rsm.Param.Pj_no3o] = pm.Param.ph_no3o 
    jv[rsm.Param.Pj_hno2] = pm.Param.ph_hno2 
    jv[rsm.Param.Pj_hno3] = pm.Param.ph_hno3 
    jv[rsm.Param.Pj_hno4] = pm.Param.ph_hno4 
    jv[rsm.Param.Pj_h2o2] = pm.Param.ph_h2o2 
    jv[rsm.Param.Pj_ch2or] = pm.Param.ph_ch2or 
    jv[rsm.Param.Pj_ch2om] = pm.Param.ph_ch2om 
    jv[rsm.Param.Pj_ch3cho] = pm.Param.ph_ch3cho 
    jv[rsm.Param.Pj_ch3coch3] = pm.Param.ph_ch3coch3 
    jv[rsm.Param.Pj_ch3coc2h5] = pm.Param.ph_ch3coc2h5 
    jv[rsm.Param.Pj_hcocho] = pm.Param.ph_hcocho 
    jv[rsm.Param.Pj_ch3cocho] = pm.Param.ph_ch3cocho 
    jv[rsm.Param.Pj_hcochest] = pm.Param.ph_hcochest 
    jv[rsm.Param.Pj_ch3o2h] = pm.Param.ph_ch3o2h 
    jv[rsm.Param.Pj_ch3coo2h] = pm.Param.ph_ch3coo2h 
    jv[rsm.Param.Pj_ch3ono2] = pm.Param.ph_ch3ono2 
    jv[rsm.Param.Pj_hcochob] = pm.Param.ph_hcochob 
    jv[rsm.Param.Pj_macr] = pm.Param.ph_macr 
    jv[rsm.Param.Pj_n2o5] = pm.Param.ph_n2o5 
    jv[rsm.Param.Pj_o2] = pm.Param.ph_o2 
    jv[rsm.Param.Pj_pan] = pm.Param.ph_pan 
    jv[rsm.Param.Pj_acet] = pm.Param.ph_acet 
    jv[rsm.Param.Pj_mglo] = pm.Param.ph_mglo 
    jv[rsm.Param.Pj_hno4_2] = pm.Param.ph_hno4_2 
    jv[rsm.Param.Pj_n2o] = pm.Param.ph_n2o 
    jv[rsm.Param.Pj_pooh] = pm.Param.ph_pooh 
    jv[rsm.Param.Pj_mpan] = pm.Param.ph_mpan 
    jv[rsm.Param.Pj_mvk] = pm.Param.ph_mvk 
    jv[rsm.Param.Pj_etooh] = pm.Param.ph_etooh 
    jv[rsm.Param.Pj_prooh] = pm.Param.ph_prooh 
    jv[rsm.Param.Pj_onitr] = pm.Param.ph_onitr 
    jv[rsm.Param.Pj_acetol] = pm.Param.ph_acetol 
    jv[rsm.Param.Pj_glyald] = pm.Param.ph_glyald 
    jv[rsm.Param.Pj_hyac] = pm.Param.ph_hyac 
    jv[rsm.Param.Pj_mek] = pm.Param.ph_mek 
    jv[rsm.Param.Pj_open] = pm.Param.ph_open 
    jv[rsm.Param.Pj_gly] = pm.Param.ph_gly 
    jv[rsm.Param.Pj_acetp] = pm.Param.ph_acetp 
    jv[rsm.Param.Pj_xooh] = pm.Param.ph_xooh 
    jv[rsm.Param.Pj_isooh] = pm.Param.ph_isooh 
    jv[rsm.Param.Pj_alkooh] = pm.Param.ph_alkooh 
    jv[rsm.Param.Pj_mekooh] = pm.Param.ph_mekooh 
    jv[rsm.Param.Pj_tolooh] = pm.Param.ph_tolooh 
    jv[rsm.Param.Pj_terpooh] = pm.Param.ph_terpooh 
    jv[rsm.Param.Pj_cl2] = pm.Param.ph_cl2 
    jv[rsm.Param.Pj_hno4a] = pm.Param.ph_hno4a 
    jv[rsm.Param.Pj_hno4b] = pm.Param.ph_hno4b 
    jv[rsm.Param.Pj_propanal] = pm.Param.ph_propanal 
    jv[rsm.Param.Pj_acetone] = pm.Param.ph_acetone 
    jv[rsm.Param.Pj_ch3ooh] = pm.Param.ph_ch3ooh 
    jv[rsm.Param.Pj_oclo] = pm.Param.ph_oclo 
    jv[rsm.Param.Pj_clo] = pm.Param.ph_clo 
    jv[rsm.Param.Pj_clno2] = pm.Param.ph_clno2 
    jv[rsm.Param.Pj_clno3a] = pm.Param.ph_clno3a 
    jv[rsm.Param.Pj_clno3b] = pm.Param.ph_clno3b 
    jv[rsm.Param.Pj_bro] = pm.Param.ph_bro 
    jv[rsm.Param.Pj_br2] = pm.Param.ph_br2 
    jv[rsm.Param.Pj_hobr] = pm.Param.ph_hobr 
    jv[rsm.Param.Pj_brno2] = pm.Param.ph_brno2 
    jv[rsm.Param.Pj_brno3a] = pm.Param.ph_brno3a 
    jv[rsm.Param.Pj_brno3b] = pm.Param.ph_brno3b 
    jv[rsm.Param.Pj_brcl] = pm.Param.ph_brcl 
    jv[rsm.Param.Pj_hocl] = pm.Param.ph_hocl 
    jv[rsm.Param.Pj_fmcl] = pm.Param.ph_fmcl 
    
    var[rsm.Param.ind_O3]   = conv * max(vc[pm.Param.LO3], 0)
    var[rsm.Param.ind_HOCl] = conv * max(vc[pm.Param.LHOCL], 0)
    var[rsm.Param.ind_HCl]  = conv * max(vc[pm.Param.LHCL], 0)
    var[rsm.Param.ind_Cl2]  = conv * max(vc[pm.Param.LCL2], 0)
    var[rsm.Param.ind_HOBr] = conv * max(vc[pm.Param.LHOBR], 0)
    var[rsm.Param.ind_HBr]  = conv * max(vc[pm.Param.LHBR], 0)
    var[rsm.Param.ind_Br2]  = conv * max(vc[pm.Param.LBR2], 0)
    var[rsm.Param.ind_BrCl] = conv * max(vc[pm.Param.LBRCL], 0)
    
    var[rsm.Param.ind_Clm_p]  = x / 35.453  * max(vc[pm.Param.LCLM_P], 0)
    var[rsm.Param.ind_Brm_p]  = x / 79.904  * max(vc[pm.Param.LBRM_P], 0)
    var[rsm.Param.ind_O3_p]   = x / 48      * max(vc[pm.Param.LO3_P], 0)
    var[rsm.Param.ind_HOCl_p] = x / 52.46   * max(vc[pm.Param.LHOCL_P], 0)
    var[rsm.Param.ind_Cl2_p]  = x / 70.906  * max(vc[pm.Param.LCL2_P], 0)
    var[rsm.Param.ind_HOBr_p] = x / 96.9113 * max(vc[pm.Param.LHOBR_P], 0)
    var[rsm.Param.ind_Br2_p]  = x / 159.808 * max(vc[pm.Param.LBR2_P], 0)
    var[rsm.Param.ind_BrCl_p] = x / 115.357 * max(vc[pm.Param.LBRCL_P], 0)
   
    RCONST = Interface.UPGC.racmsorg(RCONST, var, TEMP, LWC_Switch, Mono_Dis_Aq)
    
    var = Interface.ITGT.Integrate('racmsorg', RCONST, rsm.Param.NVAR, rsm.Param.NREACT, var, rsm.Param.LU_NONZERO, fix, TIME_START, TIME_END, ICNTRL, RCNTRL, ATOL, RTOL)
    
    vc[pm.Param.LO3]   = max((oconv * var[rsm.Param.ind_O3]), 0)
    vc[pm.Param.LHOCL] = max((oconv * var[rsm.Param.ind_HOCl]), 0)
    vc[pm.Param.LHCL]  = max((oconv * var[rsm.Param.ind_HCl]), 0)
    vc[pm.Param.LCL2]  = max((oconv * var[rsm.Param.ind_Cl2]), 0)
    vc[pm.Param.LHOBR] = max((oconv * var[rsm.Param.ind_HOBr]), 0)
    vc[pm.Param.LHBR]  = max((oconv * var[rsm.Param.ind_HBr]), 0)
    vc[pm.Param.LBR2]  = max((oconv * var[rsm.Param.ind_Br2]), 0)
    vc[pm.Param.LBRCL] = max((oconv * var[rsm.Param.ind_BrCl]), 0)
    
    vc[pm.Param.LCLM_P]  = max((35.453  / x * var[rsm.Param.ind_Clm_p]), 0)
    vc[pm.Param.LBRM_P]  = max((79.904  / x * var[rsm.Param.ind_Brm_p]), 0)
    vc[pm.Param.LO3_P]   = max((48      / x * var[rsm.Param.ind_O3_p]), 0)
    vc[pm.Param.LHOCL_P] = max((52.46   / x * var[rsm.Param.ind_HOCl_p]), 0)
    vc[pm.Param.LCL2_P]  = max((70.906  / x * var[rsm.Param.ind_Cl2_p]), 0)
    vc[pm.Param.LHOBR_P] = max((96.9113 / x * var[rsm.Param.ind_HOBr_p]), 0)
    vc[pm.Param.LBR2_P]  = max((159.808 / x * var[rsm.Param.ind_Br2_p]), 0)
    vc[pm.Param.LBRCL_P] = max((115.357 / x * var[rsm.Param.ind_BrCl_p]), 0)
    
    return vc, RCONST
