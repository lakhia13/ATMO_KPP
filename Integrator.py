import numpy as np
import math
import sys

import Integrator_Func

class execute():

  IF = Integrator_Func.Func()

  def init(identifier, RCONST, var, NVAR, NREACT, LU_NONZERO, fix, 
           ATOL, RTOL, VectorTol, FacMax, FacMin, FacSafe, FacRej, 
           TIME_START, TIME_END, Hstart, Hmax, Hmin, Roundoff, DeltaMin, Max_no_steps, Autonomous, 
           Nfun, Njac, Nstp, Nacc, Nrej, Ndec, Nsol, Nsng, 
           ros_A, ros_C, ros_E, ros_ELO, ros_Gamma, ros_M, ros_NewF, ros_S, K):
  
    # Parameters
  
    H = 0
    Hnew = 0
    HC = 0
    HG = 0
    Fac = 0
    Err = 0
    Direction = 0
  
    RejectLastH = False
    RejectMoreH = False
    Singular = False
    
    Ynew  = np.full(NVAR, 0, dtype = object)
    Fcn0  = np.full(NVAR, 0, dtype = object)
    Fcn   = np.full(NVAR, 0, dtype = object)
    K     = np.full(NVAR * ros_S, 0, dtype = object)
    dFdT  = np.full(NVAR, 0, dtype = object)
    Jac0  = np.full(LU_NONZERO, 0, dtype = object)
    Ghimj = np.full(LU_NONZERO, 0, dtype = object)
    Yerr  = np.full(NVAR, 0, dtype = object)
    Pivot = np.full(NVAR, 0, dtype = object)
  
    # Function
  
    Texit = TIME_START
    Hexit = 0
    H = min(Hstart, Hmax)
    
    if(abs(H) <= (10 * Roundoff)):
      H = DeltaMin
    
    if(TIME_END >= TIME_START):
      Direction = 1
    else:
      Direction = -1
    
    while(Direction > 0 and ((Texit - TIME_END) + Roundoff <= 0) or
          Direction < 0 and ((TIMT_END - Texit) + Roundoff <= 0)):
          
      if(Nstp > Max_no_steps):
        execute.IF.ErrorMsg(-6, Texit, H)
      
      if(((Texit + 0.1 * H) == Texit) or (H <= Roundoff)):
        execute.IF.ErrorMsg(-7, Texit, H)
        
      Hexit = H
      H = min(H, abs(TIME_END - Texit))
      
      Fcn0, Nfun = execute.IF.FunTemplate(var, Fcn0, RCONST, fix, Nfun, identifier, NREACT)
      
      if(not Autonomous):
        dFdT, Nfun = execute.IF.FunTimeDeriv(Texit, Roundoff, var, Fcn0, dFdT, RCONST, 
                                                            fix, Nfun, NVAR)
      
      Jac0, Njac = execute.IF.JacTemplate(var, Jac0, fix, Njac, RCONST, identifier)
                                                           
      while(True):
        (Ghimj, Singular, Pivot, H, Ndec, Nsng) = execute.IF.PrepareMatrix(H, Direction, ros_Gamma[0], Jac0, Ghimj, 
                                                                                          Pivot, Singular, Ndec, Nsng, identifier, LU_NONZERO, NVAR)
        
        if(Singular):
          execute.IF.ErrorMsg(-8, Texit, H)
        
        for i in range(ros_S):
        
          ioffset = NVAR * i
          
          if(i == 0):
            Fcn = execute.IF.WCOPY(NVAR, Fcn0, Fcn)
         
          elif(ros_NewF[i]):
            Ynew = execute.IF.WCOPY(NVAR, var, Ynew)
            
            for j in range(i):
            
              Ynew = execute.IF.WAXPY(NVAR, ros_A[int((i) * (i - 1) / 2 + j)],
                                                     K[NVAR * j :], Ynew)
            
            Ynew, Nfun = execute.IF.FunTemplate(Ynew, Fcn, RCONST, fix, Nfun, identifier, NREACT)
                                                                 
          K[ioffset :] = execute.IF.WCOPY(NVAR, Fcn, K[ioffset :])
          
          for j in range(i):
            HC = ros_C[int(i * (i - 1) / 2 + j)] / (Direction * H)
            K[ioffset :] = execute.IF.WAXPY(NVAR, HC, K[NVAR * j :], K[ioffset :])
          
          if((not Autonomous) and (ros_Gamma[i] != 0)):
            HG = Direction * H * ros_Gamma[i]
            K[ioffset :] = execute.IF.WAXPY(NVAR, HG, dFdT, K[ioffset :])
            
          K[ioffset :], Nsol = execute.IF.Ros_Solve(Ghimj, Pivot, K[ioffset :], Nsol, identifier)
        
        Ynew = execute.IF.WCOPY(NVAR, var, Ynew)
        
        for i in range(ros_S):
        
          Ynew = execute.IF.WAXPY(NVAR, ros_M[i], K[NVAR * i :], Ynew)
                                        
        Yerr = execute.IF.WSCAL(NVAR, 0, Yerr)
        
        for i in range(ros_S):
        
          Yerr = execute.IF.WAXPY(NVAR, ros_E[i], K[NVAR * i :], Yerr)
        
        Err = execute.IF.ErrorNorm(var, Ynew, Yerr, ATOL, RTOL, VectorTol, NVAR)
        
        Fac = min(FacMax, max(FacMin, FacSafe / Err**(1 / ros_ELO)))
        
        Hnew = H * Fac
        
        Nstp = Nstp + 1
        
        if((Err <= 1) or (H <= Hmin)):
          Nacc = Nacc + 1
          
          var = execute.IF.WCOPY(NVAR, Ynew, var)
          
          Texit = Texit + Direction * H
          Hnew = max(Hmin, min(Hnew, Hmax))
          
          if(RejectLastH):
            Hnew = min(Hnew, H)
          
          RejectLastH = False
          RejectMoreH = False
          
          H = Hnew
          
          break
          
        else:
          if(RejectMoreH):
            Hnew = H * FacRej
          
          RejectMoreH = RejectLastH
          RejectLastH = True
          
          H = Hnew
          
          if(Nacc >= 1):
            Nrej = Nrej + 1
    
    return var, Nfun, Njac, Nstp, Nacc, Nrej, Ndec, Nsol, Nsng, Texit, Hexit
