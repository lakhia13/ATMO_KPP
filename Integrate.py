import numpy as np
import math
import sys

import Integrator
import Integrator_Func

class execute():

  IF = Integrator_Func.Func()

  def Integrate(self, identifier, RCONST, NVAR, NREACT, var, LU_NONZERO, fix, TIME_START, TIME_END, ICNTRL, RCNTRL, ATOL, RTOL):
    
    ISTATUS = np.full(20, 0, dtype = object)
    RSTATUS = np.full(20, 0, dtype = object)
    
    return execute.Rosenbrock(identifier, RCONST, NVAR, NREACT, var, LU_NONZERO, fix, TIME_START, TIME_END, ISTATUS, RSTATUS, ICNTRL, RCNTRL, ATOL, RTOL)


  def Rosenbrock(identifier, RCONST, NVAR, NREACT, var, LU_NONZERO, fix, TIME_START, TIME_END, ISTATUS, RSTATUS, ICNTRL, RCNTRL, ATOL, RTOL):
    
    # Parameters
    
    Method = 0
    FacMin = 0
    FacMax = 0
    FacRej = 0
    FacSafe = 0
    Hmin = 0
    Hmax = 0
    Hstart = 0
    UplimTol = 0
    Max_no_steps = 0
    DeltaMin = 1e-5
    
    ifun = 0
    ijac = 1
    istp = 2
    iacc = 3
    irej = 4
    idec = 5
    isol = 6
    isng = 7
    
    itexit = 0
    ihexit = 1
    
    # Function
    
    Nfun = ISTATUS[ifun]
    Njac = ISTATUS[ijac]
    Nstp = ISTATUS[istp]
    Nacc = ISTATUS[iacc]
    Nrej = ISTATUS[irej]
    Ndec = ISTATUS[idec]
    Nsol = ISTATUS[isol]
    Nsng = ISTATUS[isng]
    
    Autonomous = not(ICNTRL[0] == 0)
    VectorTol = False
    
    if(ICNTRL[1] == 0):
      VectorTol = True
      UplimTol = NVAR
    else:
      VectorTol = False
      UplimTol = 1
      
    if(ICNTRL[2] == 0):
      Method = 4
    elif(ICNTRL[2] >= 1 and ICNTRL[2] <= 5):
      Method = ICNTRL[2]
    else:
      print('User-selected Rosenbrock method: ICNTRL[2] =', Method)
      execute.IF.ErrorMsg(-2, TIME_START, 0)
      
    if(ICNTRL[3] == 0):
      Max_no_steps = 100000
    elif(ICNTRL[3] > 0):
      Max_no_steps = ICNTRL[3]
    else:
      print('User-selected max number of steps: ICNTRL[3] =', ICNTRL[3])
      execute.IF.ErrorMsg(-3, TIME_START, 0)
      
    Roundoff = execute.WLAMCH()
    
    if(RCNTRL[0] == 0):
      Hmin = 0
    elif(RCNTRL[0] > 0):
      Hmin = RCNTRL[0]
    else:
      print('User-selected Hmin: RCNTRL[0] =', RCNTRL[0])
      execute.IF.ErrorMsg(-3, TIME_START, 0)
      
    if(RCNTRL[1] == 0):
      Hmax = abs(TIME_END - TIME_START)
    elif(RCNTRL[1] > 0):
      Hmax = min(abs(RCNTRL[1]), abs(TIME_END - TIME_START))
    else:
      print('User-selected Hmax: RCNTRL[1] =', RCNTRL[1])
      execute.IF.ErrorMsg(-3, TIME_START, 0)
      
    if(RCNTRL[2] == 0):
      Hstart = max(Hmin, DeltaMin)
    elif(RCNTRL[2] > 0):
      Hstart = min(abs(RCNTRL[2]), abs(TIME_END - TIME_START))
    else:
      print('User-selected Hstart: RCNTRL[2] =', RCNTRL[2])
      execute.IF.ErrorMsg(-3, TIME_START, 0)
      
    if(RCNTRL[3] == 0):
      FacMin = 0.2
    elif(RCNTRL[3] > 0):
      FacMin = RCNTRL[3]
    else:
      print('User-selected FacMin: RCNTRL[3] =', RCNTRL[3])
      execute.IF.ErrorMsg(-4, TIME_START, 0)
      
    if(RCNTRL[4] == 0):
      FacMax = 6
    elif(RCNTRL[4] > 0):
      FacMax = RCNTRL[4]
    else:
      print('User-selected FacMax: RCNTRL[4] =', RCNTRL[4])
      execute.IF.ErrorMsg(-4, TIME_START, 0)
    
    if(RCNTRL[5] == 0):
      FacRej = 0.1
    elif(RCNTRL[5] > 0):
      FacRej = RCNTRL[5]
    else:
      print('User-selected FacRej: RCNTRL[5] =', RCNTRL[5])
      execute.IF.ErrorMsg(-4, TIME_START, 0)
    
    if(RCNTRL[6] == 0):
      FacSafe = 0.9
    elif(RCNTRL[6] > 0):
      FacSafe = RCNTRL[6]
    else:
      print('User-selected FacSafe: RCNTRL[6] =', RCNTRL[6])
      execute.IF.ErrorMsg(-4, TIME_START, 0)
      
    for i in range(UplimTol):
      if(ATOL[i] <= 0 or 
         RTOL[i] <= (10 * Roundoff) or 
         RTOL[i] >= 1):
        print('ATOL[' + str(i) + '] =', ATOL[i])
        print('RTOL[' + str(i) + '] =', RTOL[i])
        execute.IF.ErrorMsg(-5, TIME_START, 0)
        
    if(Method == 1):
      ros_A, ros_Alpha, ros_C, ros_E, ros_ELO, ros_Gamma, ros_M, ros_NewF, ros_S, K = execute.Ros2(NVAR)
    elif(Method == 2):
      ros_A, ros_Alpha, ros_C, ros_E, ros_ELO, ros_Gamma, ros_M, ros_NewF, ros_S, K = execute.Ros3(NVAR)
    elif(Method == 3):
      ros_A, ros_Alpha, ros_C, ros_E, ros_ELO, ros_Gamma, ros_M, ros_NewF, ros_S, K = execute.Ros4(NVAR)
    elif(Method == 4):
      ros_A, ros_Alpha, ros_C, ros_E, ros_ELO, ros_Gamma, ros_M, ros_NewF, ros_S, K = execute.Rodas3(NVAR)
    elif(Method == 5):
      ros_A, ros_Alpha, ros_C, ros_E, ros_ELO, ros_Gamma, ros_M, ros_NewF, ros_S, K = execute.Rodas4(NVAR)
    else:
      print('Unknown Rosenbrock method: ICNTRL[3] =', Method)
      execute.IF.ErrorMsg(-2, TIME_START, 0)

    (var, Nfun, Njac, Nstp, 
     Nacc, Nrej, Ndec, Nsol, Nsng, 
     Texit, Hexit) = Integrator.execute.init(identifier, RCONST, var, NVAR, NREACT, LU_NONZERO, fix,
                                             ATOL, RTOL, VectorTol, FacMax, FacMin, FacSafe, FacRej, 
                                             TIME_START, TIME_END, Hstart, Hmax, Hmin, Roundoff, DeltaMin, Max_no_steps, Autonomous, 
                                             Nfun, Njac, Nstp, Nacc, Nrej, Ndec, Nsol, Nsng, 
                                             ros_A, ros_C, ros_E, ros_ELO, ros_Gamma, ros_M, ros_NewF, ros_S, K)
    
    ISTATUS[ifun] = Nfun
    ISTATUS[ijac] = Njac
    ISTATUS[istp] = Nstp
    ISTATUS[iacc] = Nacc
    ISTATUS[irej] = Nrej
    ISTATUS[idec] = Ndec
    ISTATUS[isol] = Nsol
    ISTATUS[isng] = Nsng

    RSTATUS[itexit] = Texit
    RSTATUS[ihexit] = Hexit
    
    return var
    
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Supplement Functions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
  def WLAMCH():
    Check = 0
    First = True
    
    if(First):
      First = False
      Eps = (0.5)**(16)
      for i in range(17, 81):
        Eps = Eps * 0.5
        Sum = 1 + Eps
        
        if(Sum <= 1):
          Check = 1
          break
      
    if(Check == 1):
      Eps = Eps * 2
      return Eps
    else:
      print('Error in WLAMCH. EPS <', Eps)
      return 0
      
  def Ros2(NVAR):
    g = 1 + 1 / math.sqrt(2)
  
    ros_S = 2
    
    ros_M = np.full(ros_S, 0, dtype = object)
    ros_E = np.full(ros_S, 0, dtype = object)
    ros_Alpha = np.full(ros_S, 0, dtype = object)
    ros_A = np.full(int(ros_S * (ros_S - 1) / 2), 0, dtype = object)
    ros_Gamma = np.full(ros_S, 0, dtype = object)
    ros_C = np.full(int(ros_S * (ros_S - 1) / 2), 0, dtype = object)
    ros_NewF = np.full(ros_S, 0, dtype = object)
    
    K = np.full(NVAR * ros_S, 0, dtype = object)
    
    ros_A[0] = 1 / g
    ros_C[0] = -2 / g
    
    ros_NewF[0] = True
    ros_NewF[1] = True
    
    ros_M[0] = 3 / (2 * g)
    ros_M[1] = 1 / (2 * g)
    
    ros_E[0] = 1 / (2 * g)
    ros_E[1] = 1 / (2 * g)
    
    ros_ELO = 2
    
    ros_Alpha[0] = 0
    ros_Alpha[1] = 1
    
    ros_Gamma[0] = g
    ros_Gamma[1] = -g
  
    return ros_A, ros_Alpha, ros_C, ros_E, ros_ELO, ros_Gamma, ros_M, ros_NewF, ros_S, K
  
  def Ros3(NVAR):
    ros_S = 3

    ros_M = np.full(ros_S, 0, dtype = object)
    ros_E = np.full(ros_S, 0, dtype = object)
    ros_Alpha = np.full(ros_S, 0, dtype = object)
    ros_A = np.full(int(ros_S * (ros_S - 1) / 2), 0, dtype = object)
    ros_Gamma = np.full(ros_S, 0, dtype = object)
    ros_C = np.full(int(ros_S * (ros_S - 1) / 2), 0, dtype = object)
    ros_NewF = np.full(ros_S, 0, dtype = object)

    K = np.full(NVAR * ros_S, 0, dtype = object)

    ros_A[0]= 1.0
    ros_A[1]= 1.0
    ros_A[2]= 0.0

    ros_C[0] = -0.10156171083877702091975600115545e+01
    ros_C[1] =  0.40759956452537699824805835358067e+01
    ros_C[2] =  0.92076794298330791242156818474003e+01


    ros_NewF[0] = True
    ros_NewF[1] = True
    ros_NewF[2] = False

    ros_M[0] =  0.1e+01
    ros_M[1] =  0.61697947043828245592553615689730e+01
    ros_M[2] = -0.42772256543218573326238373806514e+00

    ros_E[0] =  0.5e+00
    ros_E[1] = -0.29079558716805469821718236208017e+01
    ros_E[2] =  0.22354069897811569627360909276199e+00

    ros_ELO = 3.0

    ros_Alpha[0] = 0.0e+00
    ros_Alpha[1] = 0.43586652150845899941601945119356e+00
    ros_Alpha[2] = 0.43586652150845899941601945119356e+00

    ros_Gamma[0] = 0.43586652150845899941601945119356e+00
    ros_Gamma[1] = 0.24291996454816804366592249683314e+00
    ros_Gamma[2] = 0.21851380027664058511513169485832e+01
    
    return ros_A, ros_Alpha, ros_C, ros_E, ros_ELO, ros_Gamma, ros_M, ros_NewF, ros_S, K
    
  def Ros4(NVAR):
    ros_S = 4
    
    ros_M = np.full(ros_S, 0, dtype = object)
    ros_E = np.full(ros_S, 0, dtype = object)
    ros_Alpha = np.full(ros_S, 0, dtype = object)
    ros_A = np.full(int(ros_S * (ros_S - 1) / 2), 0, dtype = object)
    ros_Gamma = np.full(ros_S, 0, dtype = object)
    ros_C = np.full(int(ros_S * (ros_S - 1) / 2), 0, dtype = object)
    ros_NewF = np.full(ros_S, 0, dtype = object)

    K = np.full(NVAR * ros_S, 0, dtype = object)

    ros_A[0] = 0.2000000000000000e+01
    ros_A[1] = 0.1867943637803922e+01
    ros_A[2] = 0.2344449711399156e+00
    ros_A[3] = ros_A[1]
    ros_A[4] = ros_A[2]
    ros_A[5] = 0.0

    ros_C[0] = -0.7137615036412310e+01
    ros_C[1] = 0.2580708087951457e+01
    ros_C[2] = 0.6515950076447975e+00
    ros_C[3] = -0.2137148994382534e+01
    ros_C[4] = -0.3214669691237626e+00
    ros_C[5] = -0.6949742501781779e+00


    ros_NewF[0]  = True
    ros_NewF[1]  = True
    ros_NewF[2]  = True
    ros_NewF[3]  = False

    ros_M[0] = 0.2255570073418735e+01
    ros_M[1] = 0.2870493262186792e+00
    ros_M[2] = 0.4353179431840180e+00
    ros_M[3] = 0.1093502252409163e+01

    ros_E[0] = -0.2815431932141155e+00
    ros_E[1] = -0.7276199124938920e-01
    ros_E[2] = -0.1082196201495311e+00
    ros_E[3] = -0.1093502252409163e+01

    ros_ELO  = 4.0

    ros_Alpha[0] = 0.0
    ros_Alpha[1] = 0.1145640000000000e+01
    ros_Alpha[2] = 0.6552168638155900e+00
    ros_Alpha[3] = ros_Alpha[2]

    ros_Gamma[0] = 0.5728200000000000e+00
    ros_Gamma[1] = -0.1769193891319233e+01
    ros_Gamma[2] = 0.7592633437920482e+00
    ros_Gamma[3] = -0.1049021087100450e+00
    
    return ros_A, ros_Alpha, ros_C, ros_E, ros_ELO, ros_Gamma, ros_M, ros_NewF, ros_S, K
    
  def Rodas3(NVAR):
    ros_S = 5
    
    ros_M = np.full(ros_S, 0, dtype = object)
    ros_E = np.full(ros_S, 0, dtype = object)
    ros_Alpha = np.full(ros_S, 0, dtype = object)
    ros_A = np.full(int(ros_S * (ros_S - 1) / 2), 0, dtype = object)
    ros_Gamma = np.full(ros_S, 0, dtype = object)
    ros_C = np.full(int(ros_S * (ros_S - 1) / 2), 0, dtype = object)
    ros_NewF = np.full(ros_S, 0, dtype = object)
  
    K = np.full(NVAR * ros_S, 0, dtype = object)
  
    ros_A[0] = 0.0e+00
    ros_A[1] = 2.0e+00
    ros_A[2] = 0.0e+00
    ros_A[3] = 2.0e+00
    ros_A[4] = 0.0e+00
    ros_A[5] = 1.0e+00

    ros_C[0] = 4.0e+00
    ros_C[1] = 1.0e+00
    ros_C[2] =-1.0e+00
    ros_C[3] = 1.0e+00
    ros_C[4] =-1.0e+00
    ros_C[5] =-(8.0e+00/3.0e+00)

    ros_NewF[0]  = True
    ros_NewF[1]  = False
    ros_NewF[2]  = True
    ros_NewF[3]  = True

    ros_M[0] = 2.0e+00
    ros_M[1] = 0.0e+00
    ros_M[2] = 1.0e+00
    ros_M[3] = 1.0e+00

    ros_E[0] = 0.0e+00
    ros_E[1] = 0.0e+00
    ros_E[2] = 0.0e+00
    ros_E[3] = 1.0e+00

    ros_ELO = 3.0e+00

    ros_Alpha[0] = 0.0e+00
    ros_Alpha[1] = 0.0e+00
    ros_Alpha[2] = 1.0e+00
    ros_Alpha[3] = 1.0e+00

    ros_Gamma[0] = 0.5e+00
    ros_Gamma[1] = 1.5e+00
    ros_Gamma[2] = 0.0e+00
    ros_Gamma[3] = 0.0e+00
    
    return ros_A, ros_Alpha, ros_C, ros_E, ros_ELO, ros_Gamma, ros_M, ros_NewF, ros_S, K
  
  def Rodas4(NVAR):
    ros_S = 6
    
    ros_M = np.full(ros_S, 0, dtype = object)
    ros_E = np.full(ros_S, 0, dtype = object)
    ros_Alpha = np.full(ros_S, 0, dtype = object)
    ros_A = np.full(int(ros_S * (ros_S - 1) / 2), 0, dtype = object)
    ros_Gamma = np.full(ros_S, 0, dtype = object)
    ros_C = np.full(int(int(ros_S * (ros_S - 1))) / 2, 0, dtype = object)
    ros_NewF = np.full(ros_S, 0, dtype = object)

    K = np.full(NVAR * ros_S, 0, dtype = object)

    ros_Alpha[0] = 0.000
    ros_Alpha[1] = 0.386
    ros_Alpha[2] = 0.210
    ros_Alpha[3] = 0.630
    ros_Alpha[4] = 1.000
    ros_Alpha[5] = 1.000

    ros_Gamma[0] = 0.2500000000000000e+00
    ros_Gamma[1] = -0.1043000000000000e+00
    ros_Gamma[2] = 0.1035000000000000e+00
    ros_Gamma[3] = -0.3620000000000023e-01
    ros_Gamma[4] = 0.0
    ros_Gamma[5] = 0.0

    ros_A[0] = 0.1544000000000000e+01
    ros_A[1] = 0.9466785280815826e+00
    ros_A[2] = 0.2557011698983284e+00
    ros_A[3] = 0.3314825187068521e+01
    ros_A[4] = 0.2896124015972201e+01
    ros_A[5] = 0.9986419139977817e+00
    ros_A[6] = 0.1221224509226641e+01
    ros_A[7] = 0.6019134481288629e+01
    ros_A[8] = 0.1253708332932087e+02
    ros_A[9] = -0.6878860361058950e+00
    ros_A[10] = ros_A[6]
    ros_A[11] = ros_A[7]
    ros_A[12] = ros_A[8]
    ros_A[13] = ros_A[9]
    ros_A[14] = 1.0e+00

    ros_C[0] = -0.5668800000000000e+01
    ros_C[1] = -0.2430093356833875e+01
    ros_C[2] = -0.2063599157091915e+00
    ros_C[3] = -0.1073529058151375e+00
    ros_C[4] = -0.9594562251023355e+01
    ros_C[5] = -0.2047028614809616e+02
    ros_C[6] = 0.7496443313967647e+01
    ros_C[7] = -0.1024680431464352e+02
    ros_C[8] = -0.3399990352819905e+02
    ros_C[9] = 0.1170890893206160e+02
    ros_C[10] = 0.8083246795921522e+01
    ros_C[11] = -0.7981132988064893e+01
    ros_C[12] = -0.3152159432874371e+02
    ros_C[13] = 0.1631930543123136e+02
    ros_C[14] = -0.6058818238834054e+01

    ros_M[0] = ros_A[6]
    ros_M[1] = ros_A[7]
    ros_M[2] = ros_A[8]
    ros_M[3] = ros_A[9]
    ros_M[4] = 1.0e+00
    ros_M[5] = 1.0e+00

    ros_E[0] = 0.0e+00
    ros_E[1] = 0.0e+00
    ros_E[2] = 0.0e+00
    ros_E[3] = 0.0e+00
    ros_E[4] = 0.0e+00
    ros_E[5] = 1.0e+00

    ros_NewF[0] = True
    ros_NewF[1] = True
    ros_NewF[2] = True
    ros_NewF[3] = True
    ros_NewF[4] = True
    ros_NewF[5] = True

    ros_ELO = 4.0
    
    return ros_A, ros_Alpha, ros_C, ros_E, ros_ELO, ros_Gamma, ros_M, ros_NewF, ros_S, K
