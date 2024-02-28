import numpy as np
import math

import Parameters as pm
import racm_Parameters as rpm
import racmpm_Parameters as rpmpm
import racmsorg_Parameters as rsm

import Update_Rconst_Func

class Update_Rconst():
  
  f = Update_Rconst_Func.func()
  
  def racm(self, RCONST, fix, jv, TEMP, C_M):
    
    C_H2O = fix[rpm.Param.indf_H2O]
    
    RCONST[ 0] = jv[rpm.Param.Pj_o31d]
    RCONST[ 1] = jv[rpm.Param.Pj_h2o2]
    RCONST[ 2] = jv[rpm.Param.Pj_no2]
    RCONST[ 3] = jv[rpm.Param.Pj_no3o]
    RCONST[ 4] = jv[rpm.Param.Pj_n2o5]
    RCONST[ 5] = jv[rpm.Param.Pj_hno2]
    RCONST[ 6] = jv[rpm.Param.Pj_hno3]
    RCONST[ 7] = jv[rpm.Param.Pj_hno4a]
    RCONST[ 8] = jv[rpm.Param.Pj_hno4b]
    RCONST[ 9] = jv[rpm.Param.Pj_ch2or]
    RCONST[10] = jv[rpm.Param.Pj_ch2om]
    RCONST[11] = jv[rpm.Param.Pj_ch3cho]
    RCONST[12] = jv[rpm.Param.Pj_propanal]
    RCONST[13] = jv[rpm.Param.Pj_acetone]
    RCONST[14] = jv[rpm.Param.Pj_ch3ooh]
    RCONST[15] = jv[rpm.Param.Pj_oclo]
    RCONST[16] = jv[rpm.Param.Pj_cl2]
    RCONST[17] = jv[rpm.Param.Pj_clo]
    RCONST[18] = jv[rpm.Param.Pj_hocl]
    RCONST[19] = jv[rpm.Param.Pj_clno2]
    RCONST[20] = jv[rpm.Param.Pj_clno3a]
    RCONST[21] = jv[rpm.Param.Pj_clno3b]
    RCONST[22] = jv[rpm.Param.Pj_bro]
    RCONST[23] = jv[rpm.Param.Pj_br2]
    RCONST[24] = jv[rpm.Param.Pj_hobr]
    RCONST[25] = jv[rpm.Param.Pj_brno2]
    RCONST[26] = jv[rpm.Param.Pj_brno3a]
    RCONST[27] = jv[rpm.Param.Pj_brno3b]
    RCONST[28] = jv[rpm.Param.Pj_brcl]
    RCONST[29] = (0.21 * Update_Rconst.f.ARR2(3.30e-11, -55.0, TEMP) + 0.78 * 
                           Update_Rconst.f.ARR2(2.15e-11, -110., TEMP))
    RCONST[30] = (7.2e-34 * .78084 * C_M * .20946 * C_M * 
                           (TEMP/300)**(-2.6))
    RCONST[31] = Update_Rconst.f.ARR2(1.63e-11, -60., TEMP)
    RCONST[32] = Update_Rconst.f.ARR2(1.7e-12, 940.0, TEMP)
    RCONST[33] = Update_Rconst.f.ARR2(4.8e-11, -250.0, TEMP)
    RCONST[34] = Update_Rconst.f.ARR2(2.9e-12, 160.0, TEMP)
    RCONST[35] = Update_Rconst.f.ARR2(1.0e-14, 490.0, TEMP)
    RCONST[36] = Update_Rconst.f.k37(TEMP, C_M, C_H2O)
    RCONST[37] = 1.44e-13 * (1 + (C_M / 4.2e+19))
    RCONST[38] = Update_Rconst.f.TROE(7.00e-31,2.6, 3.60e-11,0.1, TEMP, C_M)
    RCONST[39] = Update_Rconst.f.ARR2(3.5e-12, -250.0, TEMP)
    RCONST[40] = Update_Rconst.f.ARR2(3.0e-12, 1500.0, TEMP)
    RCONST[41] = Update_Rconst.f.ARR2(1.5e-11, -170.0, TEMP)
    RCONST[42] = Update_Rconst.f.TROE(1.80e-30, 3.0, 2.80e-11, 0.0, TEMP, C_M)
    RCONST[43] = Update_Rconst.f.TROE(1.90e-31, 3.4, 4.00e-12, 0.3, TEMP, C_M)
    RCONST[44] = Update_Rconst.f.TROEE(4.76e26, 10900.0, 1.90e-31, 3.4, 4.00e-12, 0.3, 
                                TEMP, C_M)
    RCONST[45] = Update_Rconst.f.ARR2(1.3e-12, -380.0, TEMP)
    RCONST[46] = Update_Rconst.f.ARR2(1.2e-13, 2450.0, TEMP)
    RCONST[47] = Update_Rconst.f.TROE(2.40e-30, 3.0, 1.60e-12, -0.1, TEMP, C_M)
    RCONST[48] = Update_Rconst.f.TROEE(1.72e26, 10840.0, 2.40e-30, 3.0, 1.60e-12, -0.1, 
                                TEMP, C_M)
    RCONST[49] = 2.6e-22
    RCONST[50] = Update_Rconst.f.ARR2(1.8e-11, 390.0, TEMP)
    RCONST[51] = Update_Rconst.f.k46(TEMP, C_M)
    RCONST[52] = Update_Rconst.f.ARR2(2.45e-12, 1775.0, TEMP)
    RCONST[53] = Update_Rconst.f.ARR2(2.8e-12, -300.0, TEMP)
    RCONST[54] = Update_Rconst.f.ARR2(4.1e-13, -750.0, TEMP)
    RCONST[55] = Update_Rconst.f.ARR2(9.5e-14, -390.0, TEMP)
    RCONST[56] = Update_Rconst.f.ARR2(2.0e-12, -500.0, TEMP)
    RCONST[57] = Update_Rconst.f.ARR2(7.66e-12, 1020.0, TEMP)
    RCONST[58] = Update_Rconst.f.ARR2(2.6e-12, -365.0, TEMP)
    RCONST[59] = Update_Rconst.f.ARR2(7.5e-13, -700.0, TEMP)
    RCONST[60] = 2.0e-13
    RCONST[61] = 6.8e-14
    RCONST[62] = 1.0e-11
    RCONST[63] = Update_Rconst.f.ARR2(2.0e-12, 585.0, TEMP)
    RCONST[64] = Update_Rconst.f.ARR2(5.6e-12, 585.0, TEMP)
    RCONST[65] = Update_Rconst.f.ARR2(2.9e-12, -350.0, TEMP)
    RCONST[66] = Update_Rconst.f.ARR2(2.7e-12, -360.0, TEMP)
    RCONST[67] = Update_Rconst.f.ARR2(1.5e-13, -1300.0, TEMP)
    RCONST[68] = Update_Rconst.f.ARR2(1.5e-13, -1300.0, TEMP)
    RCONST[69] = 4.8e-13
    RCONST[70] = 1.2e-13
    RCONST[71] = 4.8e-13
    RCONST[72] = 1.2e-13
    RCONST[73] = Update_Rconst.f.ARR2(8.6e-12, 425.0, TEMP)
    RCONST[74] = Update_Rconst.f.ARR2(1.2e-12, 425.0, TEMP)
    RCONST[75] = Update_Rconst.f.THERMAL_T2(9.21e-18, -225.0, TEMP)
    RCONST[76] = Update_Rconst.f.THERMAL_T2(2.39e-18, -225.0, TEMP)
    RCONST[77] = Update_Rconst.f.ARR2(2.7e-12, -360.0, TEMP)
    RCONST[78] = Update_Rconst.f.ARR2(1.8e-13, -1300.0, TEMP)
    RCONST[79] = 2.0e-13
    RCONST[80] = 5.0e-14
    RCONST[81] = Update_Rconst.f.ARR2(2.7e-12, -360.0, TEMP)
    RCONST[82] = Update_Rconst.f.ARR2(1.8e-13, -1300.0, TEMP)
    RCONST[83] = 1.0e-12
    RCONST[84] = 2.6e-13
    RCONST[85] = Update_Rconst.f.ARR2(2.7e-12, -360.0, TEMP)
    RCONST[86] = Update_Rconst.f.ARR2(1.8e-13, -1300.0, TEMP)
    RCONST[87] = 4.7e-15
    RCONST[88] = 2.0e-15
    RCONST[89] = Update_Rconst.f.ARR2(2.7e-12, -360.0, TEMP)
    RCONST[90] = Update_Rconst.f.ARR2(1.8e-13, -1300.0, TEMP)
    RCONST[91] = 1.0e-12
    RCONST[92] = 2.6e-13
    RCONST[93] = Update_Rconst.f.ARR2(2.1e-12, -190.0, TEMP)
    RCONST[94] = Update_Rconst.f.ARR2(3.2e-12, -190.0, TEMP)
    RCONST[95] = Update_Rconst.f.ARR2(5.4e-12, -135.0, TEMP)
    RCONST[96] = Update_Rconst.f.ARR2(4.7e-12, -345.0, TEMP)
    RCONST[97] = Update_Rconst.f.ARR2(1.5e-12, 90.0, TEMP)
    RCONST[98] = (8.8e-12 * math.exp(-1320 / TEMP) + 1.7e-14 * 
                           math.exp(423 / TEMP))
    RCONST[99] = Update_Rconst.f.ARR2(4.9e-12, -405.0, TEMP)
    RCONST[100] = Update_Rconst.f.ARR2(6.0e-12, -410.0, TEMP)
    RCONST[101] = Update_Rconst.f.ARR2(6.8e-12, -410.0, TEMP)
    RCONST[102] = Update_Rconst.f.TROE(9.70e-29, 5.6, 9.30e-12, 1.5, TEMP, C_M)
    RCONST[103] = Update_Rconst.f.ARR2(7.5e-12,-290.0, TEMP)
    RCONST[104] = Update_Rconst.f.TROEE(1.1e28, 14000.0, 9.70e-29, 5.6, 9.30e-12, 1.5, 
                                TEMP, C_M)
    RCONST[105] = Update_Rconst.f.ARR2(2.3e-11, 200.0, TEMP)
    RCONST[106] = Update_Rconst.f.ARR2(1.4e-11, -271.0, TEMP)
    RCONST[107] = Update_Rconst.f.ARR2(3.6e-11, 375.0, TEMP)
    RCONST[108] = Update_Rconst.f.ARR2(1.1e-11, 980.0, TEMP)
    RCONST[109] = 2.4e-11
    RCONST[110] = Update_Rconst.f.ARR2(7.1e-12, 1270.0, TEMP)
    RCONST[111] = Update_Rconst.f.ARR2(7.7e-11, 90.0, TEMP)
    RCONST[112] = Update_Rconst.f.ARR2(8.12e-11, 90.0, TEMP)
    RCONST[113] = Update_Rconst.f.ARR2(6.54e-11, -60.0, TEMP)
    RCONST[114] = Update_Rconst.f.ARR2(1.2e-10, -55.0, TEMP)
    RCONST[115] = Update_Rconst.f.ARR2(9.0e-11, 120.0, TEMP)
    RCONST[116] = 6.2e-11
    RCONST[117] = 8.1e-11
    RCONST[118] = Update_Rconst.f.ARR2(8.1e-11, 30.0, TEMP)
    RCONST[119] = 8.0e-11
    RCONST[120] = Update_Rconst.f.ARR2(1.63e-11, 610.0, TEMP)
    RCONST[121] = 5.7e-11
    RCONST[122] = Update_Rconst.f.ARR2(3.2e-11, -170.0, TEMP)
    RCONST[123] = Update_Rconst.f.ARR2(6.5e-12, -135.0, TEMP)
    RCONST[124] = 1e-14
    RCONST[125] = 1e-16
    RCONST[126] = Update_Rconst.f.TROE(1.80e-31, 2.0, 1.00e-10, 1.0, TEMP, C_M)
    RCONST[127] = Update_Rconst.f.ARR2(7.4e-12, -270.0, TEMP)
    RCONST[128] = Update_Rconst.f.ARR2(3.2e-13, -320.0, TEMP)
    RCONST[129] = Update_Rconst.f.ARR2(2.6e-12, -290.0, TEMP)
    RCONST[130] = Update_Rconst.f.ARR2(1.8e-12, 600.0, TEMP)
    RCONST[131] = 2.0e-12
    RCONST[132] = Update_Rconst.f.ARR2(6.2e-12, -295.0, TEMP)
    RCONST[133] = Update_Rconst.f.TROE(1.80e-31, 3.4, 1.50e-11, 1.9, TEMP, C_M)
    RCONST[134] = Update_Rconst.f.ARR2(1.0e-12, 1590.0, TEMP)
    RCONST[135] = Update_Rconst.f.ARR2(3.0e-11, 2450.0, TEMP)
    RCONST[136] = Update_Rconst.f.ARR2(3.5e-13, 1370.0, TEMP)
    RCONST[137] = Update_Rconst.f.ARR2(4.5e-13, -800.0, TEMP)
    RCONST[138] = Update_Rconst.f.ARR2(2.5e-12, 600.0, TEMP)
    RCONST[139] = Update_Rconst.f.ARR2(3.0e-12, 500.0, TEMP)
    RCONST[140] = Update_Rconst.f.ARR2(1.8e-12, 250.0, TEMP)
    RCONST[141] = Update_Rconst.f.ARR2(1.6e-11, 780.0, TEMP)
    RCONST[142] = Update_Rconst.f.ARR2(2.1e-11, -240.0, TEMP)
    RCONST[143] = Update_Rconst.f.ARR2(4.8e-12, 310.0, TEMP)
    RCONST[144] = Update_Rconst.f.ARR2(7.7e-12, 580.0, TEMP)
    RCONST[145] = Update_Rconst.f.ARR2(1.8e-11, 460.0, TEMP)
    RCONST[146] = Update_Rconst.f.ARR2(5.8e-11, 610.0, TEMP)
    RCONST[147] = Update_Rconst.f.TROE(4.20e-31, 2.4, 2.70e-11, 0.0, TEMP, C_M)
    RCONST[148] = 5.3e-12
    RCONST[149] = 1e-12
    RCONST[150] = 0.02
    RCONST[151] = 0.014
    RCONST[152] = 4.9e-11
    RCONST[153] = 5.0e-11
    RCONST[154] = Update_Rconst.f.ARR2(2.6e-11, 1300.0, TEMP)
    RCONST[155] = Update_Rconst.f.ARR2(1.7e-11, -250.0, TEMP)
    RCONST[156] = Update_Rconst.f.ARR2(4.5e-12, -460.0, TEMP)
    RCONST[157] = 4.1e-12
    RCONST[158] = 1.6e-12
    RCONST[159] = 1.7e-12
    RCONST[160] = Update_Rconst.f.ARR2(8.8e-12, -260.0, TEMP)
    RCONST[161] = Update_Rconst.f.TROE(5.40e-31, 3.1, 6.50e-12, 2.9, TEMP, C_M)
    RCONST[162] = Update_Rconst.f.ARR2(2.4e-12, -40.0, TEMP)
    RCONST[163] = Update_Rconst.f.ARR2(2.8e-14, -860.0, TEMP)
    RCONST[164] = 2.1e-14
    RCONST[165] = Update_Rconst.f.ARR2(5.5e-12, -200.0, TEMP)
    RCONST[166] = 1.5e-11
    RCONST[167] = 1.5e-15
    RCONST[168] = 1.2e-10
    RCONST[169] = 3.3e-15
    RCONST[170] = Update_Rconst.f.ARR2(2.3e-12, -260.0, TEMP)
    RCONST[171] = Update_Rconst.f.ARR2(4.1e-13, -290.0, TEMP)
    RCONST[172] = Update_Rconst.f.ARR2(9.5e-13, -550.0, TEMP)
    
    return RCONST
    
  def racmpm(self, RCONSThet, TEMP, var, Mono_Dis):
    
    Limitor = True
    
    if(Mono_Dis):
      SA_um2_cm3 = 10.
    else:
      SA_um2_cm3 = Update_Rconst.f.SA_um2_cm3_Func() 
    
    if(Limitor):
      
      RCONSThet[0] = (Update_Rconst.f.Het_Coeff(0, TEMP, 108.01, SA_um2_cm3) * 
                               min(var[rpmpm.Param.ind_N2O5], var[rpmpm.Param.ind_Clm_p]) / 
                               max(var[rpmpm.Param.ind_N2O5], 1e-40) /
                               max(var[rpmpm.Param.ind_Clm_p], 1e-40))

      RCONSThet[1] = (Update_Rconst.f.Het_Coeff(1, TEMP, 108.01, SA_um2_cm3)* 
                               min(var[rpmpm.Param.ind_N2O5], var[rpmpm.Param.ind_Brm_p]) / 
                               max(var[rpmpm.Param.ind_N2O5], 1e-40) / 
                               max(var[rpmpm.Param.ind_Brm_p], 1e-40))

      RCONSThet[2] = (Update_Rconst.f.Het_Coeff(2,TEMP,97.4579,SA_um2_cm3))

      RCONSThet[3] = (Update_Rconst.f.Het_Coeff(3,TEMP,97.4579,SA_um2_cm3)* 
                               min(var[rpmpm.Param.ind_ClNO3], var[rpmpm.Param.ind_Clm_p]) / 
                               max(var[rpmpm.Param.ind_ClNO3], 1e-40) / 
                               max(var[rpmpm.Param.ind_Clm_p], 1e-40))

      RCONSThet[4] = (Update_Rconst.f.Het_Coeff(4, TEMP, 97.4579, SA_um2_cm3) * 
                               min(var[rpmpm.Param.ind_ClNO3], var[rpmpm.Param.ind_Brm_p]) / 
                               max(var[rpmpm.Param.ind_ClNO3], 1e-40) / 
                               max(var[rpmpm.Param.ind_Brm_p],1e-40))

      RCONSThet[5] = (Update_Rconst.f.Het_Coeff(5, TEMP, 141.901, SA_um2_cm3))

      RCONSThet[6] = (Update_Rconst.f.Het_Coeff(6, TEMP, 141.901, SA_um2_cm3) * 
                               min(var[rpmpm.Param.ind_BrNO3], var[rpmpm.Param.ind_Clm_p]) / 
                               max(var[rpmpm.Param.ind_BrNO3], 1e-40) / 
                               max(var[rpmpm.Param.ind_Clm_p],1e-40))

      RCONSThet[7] = (Update_Rconst.f.Het_Coeff(7, TEMP, 141.901, SA_um2_cm3) * 
                               min(var[rpmpm.Param.ind_BrNO3], var[rpmpm.Param.ind_Brm_p]) / 
                               max(var[rpmpm.Param.ind_BrNO3], 1e-40) / 
                               max(var[rpmpm.Param.ind_Brm_p], 1e-40))

      RCONSThet[8] = (Update_Rconst.f.Het_Coeff(8, TEMP, 70.906, SA_um2_cm3) * 
                               min(var[rpmpm.Param.ind_Cl2], var[rpmpm.Param.ind_Brm_p]) / 
                               max(var[rpmpm.Param.ind_Cl2], 1e-40) / 
                               max(var[rpmpm.Param.ind_Brm_p], 1e-40))
                               
    return RCONSThet
    
  def racmsorg(self, RCONSTaq, var, TEMP, LWC_Switch, Mono_Dis):
    
    rsm.Param.Mono_Dis = Mono_Dis
    
    if(LWC_Switch):
      rsm.Param.LWC_v_v = 1e-13
    else:
      rsm.Param.LWC_v_v = Update_Rconst.f.kt_p_SizeResolved(TEMP, 1)
      rsm.Param.LWC_v_v = rsm.Param.V_um3_cm3 * rsm.Param.LiquidFraction * 1e-12
    
    RCONSTaq[0] = (Update_Rconst.f.PhaseTransfer_g2p(var[rsm.Param.ind_O3], var[rsm.Param.ind_O3_p], TEMP, 1) / max(var[rsm.Param.ind_O3], 1e-20))
    RCONSTaq[1] = (Update_Rconst.f.PhaseTransfer_p2g(var[rsm.Param.ind_O3], var[rsm.Param.ind_O3_p], TEMP, 1) / max(var[rsm.Param.ind_O3_p], 1e-20)) 
    RCONSTaq[2] = (Update_Rconst.f.PhaseTransfer_g2p(var[rsm.Param.ind_HOCl], var[rsm.Param.ind_HOCl_p], TEMP, 2) / max(var[rsm.Param.ind_HOCl], 1e-20))
    RCONSTaq[3] = (Update_Rconst.f.PhaseTransfer_p2g(var[rsm.Param.ind_HOCl], var[rsm.Param.ind_HOCl_p], TEMP, 2) / max(var[rsm.Param.ind_HOCl_p], 1e-20))
    RCONSTaq[4] = (Update_Rconst.f.PhaseTransfer_g2p(var[rsm.Param.ind_HCl], var[rsm.Param.ind_Clm_p], TEMP, 3) / max(var[rsm.Param.ind_HCl], 1e-20))
    RCONSTaq[5] = (Update_Rconst.f.PhaseTransfer_p2g(var[rsm.Param.ind_HCl], var[rsm.Param.ind_Clm_p], TEMP, 3) / max(var[rsm.Param.ind_Clm_p], 1e-20))
    RCONSTaq[6] = (Update_Rconst.f.PhaseTransfer_g2p(var[rsm.Param.ind_Cl2], var[rsm.Param.ind_Cl2_p], TEMP, 4) / max(var[rsm.Param.ind_Cl2], 1e-20))
    RCONSTaq[7] = (Update_Rconst.f.PhaseTransfer_p2g(var[rsm.Param.ind_Cl2], var[rsm.Param.ind_Cl2_p], TEMP, 4) / max(var[rsm.Param.ind_Cl2_p], 1e-20))
    RCONSTaq[8] = (Update_Rconst.f.PhaseTransfer_g2p(var[rsm.Param.ind_HOBr], var[rsm.Param.ind_HOBr_p], TEMP, 5) / max(var[rsm.Param.ind_HOBr], 1e-20))
    RCONSTaq[9] = (Update_Rconst.f.PhaseTransfer_p2g(var[rsm.Param.ind_HOBr], var[rsm.Param.ind_HOBr_p], TEMP, 5) / max(var[rsm.Param.ind_HOBr_p], 1e-20))
    RCONSTaq[10] = (Update_Rconst.f.PhaseTransfer_g2p(var[rsm.Param.ind_HBr], var[rsm.Param.ind_Brm_p], TEMP, 6) / max(var[rsm.Param.ind_HBr], 1e-20))
    RCONSTaq[11] = (Update_Rconst.f.PhaseTransfer_p2g(var[rsm.Param.ind_HBr], var[rsm.Param.ind_Brm_p], TEMP, 6) / max(var[rsm.Param.ind_Brm_p], 1e-20))
    RCONSTaq[12] = (Update_Rconst.f.PhaseTransfer_g2p(var[rsm.Param.ind_Br2], var[rsm.Param.ind_Br2_p], TEMP, 7) / max(var[rsm.Param.ind_Br2], 1e-20))
    RCONSTaq[13] = (Update_Rconst.f.PhaseTransfer_p2g(var[rsm.Param.ind_Br2], var[rsm.Param.ind_Br2_p], TEMP, 7) / max(var[rsm.Param.ind_Br2_p], 1e-20))
    RCONSTaq[14] = (Update_Rconst.f.PhaseTransfer_g2p(var[rsm.Param.ind_BrCl], var[rsm.Param.ind_BrCl_p], TEMP, 8) / max(var[rsm.Param.ind_BrCl], 1e-20))
    RCONSTaq[15] = (Update_Rconst.f.PhaseTransfer_p2g(var[rsm.Param.ind_BrCl], var[rsm.Param.ind_BrCl_p], TEMP, 8) / max(var[rsm.Param.ind_BrCl_p], 1e-20))
    RCONSTaq[16] = (2.1e2 * math.exp(-4450 / TEMP) / rsm.Param.LWC_v_v / 6.0232e20)
    RCONSTaq[17] = (2.2e4 * (10**(-rsm.Param.pH)) * math.exp(-3580 / TEMP) / rsm.Param.LWC_v_v / 6.0232e20)
    RCONSTaq[18] = (1.3e6 * (10**(-rsm.Param.pH))/ rsm.Param.LWC_v_v / 6.0232e20)
    RCONSTaq[19] = (2.3e10 * (10**(-rsm.Param.pH)) / rsm.Param.LWC_v_v / 6.0232e20)
    RCONSTaq[20] = (1.6e10 * (10**(-rsm.Param.pH)) / rsm.Param.LWC_v_v / 6.0232e20)
    RCONSTaq[21] = (2.2e1 * math.exp(-8012 / TEMP))
    RCONSTaq[22] = (9.7e1 * math.exp(7457 * (1 / TEMP - 1 / 298)))
    RCONSTaq[23] = (3.0e6)
    RCONSTaq[24] = (0.0)
    
    return RCONSTaq
