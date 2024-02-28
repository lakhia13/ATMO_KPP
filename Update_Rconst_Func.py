import math
import pandas as pd
import sys

import Parameters as pm
import racmsorg_Parameters as rsm

class func():
  
  def ARR2(self, A0, B0, TEMP):
    return A0 * math.exp(-B0 / TEMP)
    
  def TROE(self, k0_300K, n, kinf_300K, m, temp, cair):
    zt_help = 300 / temp
    k0_T = k0_300K * zt_help**(n) * cair
    kinf_T = kinf_300K * zt_help**(m)
    k_ratio = k0_T / kinf_T
    
    return k0_T / (1 + k_ratio) * 0.6**(1 / (1 + math.log10(k_ratio)**2))
    
  def TROEE(self, A, B, k0_300K, n, kinf_300K, m, temp, cair):
    zt_help = 300 / temp
    k0_T = k0_300K * zt_help**(n) * cair
    kinf_T = kinf_300K * zt_help**(m)
    k_ratio = k0_T / kinf_T
    troe = k0_T / (1 + k_ratio) * 0.6**(1 / (1 + math.log10(k_ratio)**2))
    
    return A * math.exp(-B / temp) * troe
    
  def THERMAL_T2(self, c, d, temp):
    return temp**2 * c * math.exp(-d / temp)
    
  def k37(self, TEMP, C_M, C_H2O):
    KMT06 = 1 + (1.4e-21 * math.exp(2200 / TEMP) * C_H2O)
    k2 = 2.2e-13 * math.exp(600 / TEMP)
    k3 = 1.9e-33 * C_M * math.exp(980 / TEMP)
    
    return KMT06 * (k2 + k3)
    
  def k46(self, TEMP, C_M):
    k0=2.4e-14 * math.exp(460 / TEMP)
    k2=2.7e-17 * math.exp(2199 / TEMP)
    k3=6.5e-34 * math.exp(1335 / TEMP) * C_M
    
    return k0 + k3 / (1 + k3 / k2)
    
  def SA_um2_cm3_Func(self):
    x = 0
  
    for i in range(69):
      x = (x + (pm.Param.dN_dlogDp[i] * 4 * pm.Param.pid * ((pm.Param.D_um[i] / 2)**2) +
              pm.Param.dN_dlogDp[i + 1] * 4 * pm.Param.pid * ((pm.Param.D_um[i + 1] /2)**2.)) *
              (math.log10(pm.Param.D_um[i + 1]) - math.log10(pm.Param.D_um[i])) / 2)
              
    return x
    
  def Het_Coeff(self, N_eqn, TEMP, MW_g_mol, SA_um2_cm3):
    gamma = [0.02, 0.005, 0, 0.024, 0.041, 0, 0, 0.02, 0.16]
    
    return (25 * gamma[N_eqn] * (SA_um2_cm3 * 1.E-8) * math.sqrt(21171.4 * TEMP / MW_g_mol))
    
  def kt_p_SizeResolved(self, TEMP, AqCmpID):
    Dg_cm2_s = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1] 
    alpha    = [0.04, 0.6, 0.01, 0.001, 0.6, 0.1, 0.1, 0.15] 
    MW_g_mol = [48., 52.46, 36.461, 70.906, 96.9113, 80.91, 159.808, 115.357] 
    
    A_int = 0
    V_temp = 0
    pi = pm.Param.pid
    
    for i in range(69): # n_bin = 70
      A_int = (A_int + (pm.Param.dN_dlogDp[i] * 4 / 3 * pi * ((pm.Param.D_um[i] / 2)**3) / 
                        (((1e-4 * (pm.Param.D_um[i] / 2))**2 / 3 / Dg_cm2_s[AqCmpID - 1]) +
                        (4e-4 * (pm.Param.D_um[i] / 2) / 3 / (100 * math.sqrt(21171.4 * TEMP / MW_g_mol[AqCmpID - 1])) /
                        alpha[AqCmpID - 1])) + 
                        pm.Param.dN_dlogDp[i + 1] * 4 / 3 * pi * ((pm.Param.D_um[i + 1] / 2)**3) /
                        (((1e-4 * (pm.Param.D_um[i + 1] / 2))**2 / 3 / Dg_cm2_s[AqCmpID - 1]) +
                        (4e-4 * (pm.Param.D_um[i + 1] / 2) / 3 / (100 * math.sqrt(21171.4 * TEMP / MW_g_mol[AqCmpID - 1])) /
                        alpha[AqCmpID - 1]))) * 
                       (math.log10(pm.Param.D_um[i + 1]) - math.log10(pm.Param.D_um[i])) / 2)
      
      V_temp = V_temp + ((pm.Param.dN_dlogDp[i] * 4 / 3 * pi * ((pm.Param.D_um[i] / 2)**3) + pm.Param.dN_dlogDp[i + 1] *
                          4 / 3 * pi * ((pm.Param.D_um[i + 1] / 2)**3)) * 
                         (math.log10(pm.Param.D_um[i + 1]) - math.log10(pm.Param.D_um[i])) / 2)
    
    rsm.Param.V_um3_cm3 = V_temp
    
    return (A_int/rsm.Param.V_um3_cm3/rsm.Param.LiquidFraction)
    
  def kt_p(self, rp_um, TEMP, AqCmpID):
    Dg_cm2_s = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1] 
    alpha    = [0.04, 0.6, 0.01, 0.001, 0.6, 0.1, 0.1, 0.15] 
    MW_g_mol = [48., 52.46, 36.461, 70.906, 96.9113, 80.91, 159.808, 115.357] 
    
    return (1 / (((1e-4 * rp_um)**2 / 3 / Dg_cm2_s[AqCmpID - 1]) + (4e-4 * rp_um / 3 / (100 * 
                math.sqrt(21171.4 * TEMP / MW_g_mol[AqCmpID - 1]))) / alpha[AqCmpID - 1]))
                         
  def PhaseTransfer_g2p(self, C_gas, C_aq, TEMP, AqCmpID):
    Switch = rsm.Param.Mono_Dis
    rp_um = rsm.Param.rp_um
    x = rsm.Param.LWC_v_v
    
    if(Switch):
      return (func.kt_p(self, rp_um, TEMP, AqCmpID) * (C_gas * x))
    
    else:
      return (func.kt_p_SizeResolved(self, TEMP, AqCmpID) * (C_gas * x))
      
  def PhaseTransfer_p2g(self, C_gas, C_aq, TEMP, AqCmpID):
    Switch = rsm.Param.Mono_Dis
    rp_um = rsm.Param.rp_um
    pH = rsm.Param.pH
    
    if(Switch):
      return (func.kt_p(self, rp_um, TEMP, AqCmpID) * (C_aq / 0.082 / TEMP / func.Heff(self, TEMP, pH, AqCmpID)))
    
    else:
      return (func.kt_p_SizeResolved(self, TEMP, AqCmpID) * (C_aq / 0.082 / TEMP / func.Heff(self, TEMP, pH, AqCmpID)))
      
  def Heff(self, TEMP, pH, AqCmpID):
    if(AqCmpID == 1):
      return (9.4 * 1.E-3 * math.exp(2400 * (1 / TEMP - 1 / 298)))
    
    elif(AqCmpID == 2):
      return (6.6 * 1E2 * math.exp(5900 * (1 / TEMP - 1 / 298)) * (1 + 3.2 * 1e-8 / (10**(-pH))))
      
    elif(AqCmpID == 3):
      return (2 * 1E6 * math.exp(9000 * (1 / TEMP - 1 / 298)) * (1 + 1.7 * 1E6 / (10**(-pH))))
      
    elif(AqCmpID == 4):
      return (math.exp(-134.4 + 7590 / TEMP + 18.702 * math.log(TEMP)))
      
    elif(AqCmpID == 5):
      return (6.1 * 1E3 * (1 + (2.3 * 1E-9 * math.exp(-3091 * (1 / TEMP - 1 / 298))) / (10**(-pH))))
      
    elif(AqCmpID == 6):
      return (7.2 * 1E8 * math.exp(10000 * (1 / TEMP - 1 / 298)) * (1 + 1E9 / (10**(-pH))))
    
    elif(AqCmpID == 7):
      return (math.exp(-15.05 + 4390 / TEMP))
      
    elif(AqCmpID == 8):
      return (9.4 * 1E-1 * math.exp(5600 * (1 / TEMP - 1 / 298)))
    
    else:
      sys.exit('racmsorg_Update_Rconst Heff function out of bound.')
      return None
