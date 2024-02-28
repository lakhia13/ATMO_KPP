import numpy as np
import math

import racm_Jacobian as rj
import racmpm_Jacobian as rpj
import racmsorg_Jacobian as rsj

import Decomp
import Fun
import Jac_SP
import KppSolve

class Func():

  # Parameters

  IERR_NAMES = ['Success',
                'Matrix is repeatedly singular',
                'Step size too small',
                'No of steps exceeds maximum bound',
                'Improper tolerance values',
                'FacMin/FacMax/FacRej must be positive',
                'Hmin/Hmax/Hstart must be positive',
                'Selected Rosenbrock method not implemented',
                'Improper value for maximal no of steps'] 
  
  # Function
  
  def ErrorMsg(self, code, T, H):
    print('Forced exit from Rosenbrock due to the following error: \n')
    
    if(code >= -8 and code <= -1):
      print(Func.IERR_NAMES[code])
    else:
      print('Unknown Error')
      
    print('T =', T, 'and H =', H)
    raise Exception("Rosenbrock Error. Please check your initial value configurations.")
    
  def FunTimeDeriv(self, T, Roundoff, Y, Fcn0, dFdT, RCONST, Fix, Nfun, NVAR):
    
    Delta = math.sqrt(Roundoff) * max(1e-6, abs(T))
    
    dFdT, Nfun = Func.FunTemplate(self, Y, dFdT, RCONST, Fix, Nfun, NVAR)
    
    dFdT = Func.WAXPY(NVAR, -1, Fcn0, dFdT)
    dFdT = Func.WSCAL(NVAR, (1 / Delta), dFdT)
       
    return dFdT, Nfun
  
  def FunTemplate(self, Y, Ydot, RCONST, Fix, Nfun, identifier, NREACT):
    
    F = Fun.Fun()
    
    if(identifier == 'racm'):
      Ydot = F.racm(Y, Fix, RCONST, Ydot, NREACT)
    
    elif(identifier == 'racmpm'):
      Ydot = F.racmpm(Y, Fix, RCONST, Ydot, NREACT)
    
    elif(identifier == 'racmsorg'):
      Ydot = F.racmsorg(Y, Fix, RCONST, Ydot, NREACT)
    
    Nfun = Nfun + 1
    
    return Ydot, Nfun
    
  def WAXPY(self, N, Alpha, X, Y):
    
    if(Alpha == 0):
      return Y
    
    if(N <= 0):
      return Y
      
    M = N % 4
    
    if(M != 0):
      for i in range(M):
        Y[i] = Y[i] + Alpha * X[i]
      
      if(N < 4):
        return Y
    
    for i in range(M, N, 4):
      Y[i] = Y[i] + Alpha * X[i]
      Y[i + 1] = Y[i + 1] + Alpha * X[i + 1]
      Y[i + 2] = Y[i + 2] + Alpha * X[i + 2]
      Y[i + 3] = Y[i + 3] + Alpha * X[i + 3]
      
    return Y
    
  def WCOPY(self, N, X, Y):
  
    if(N <= 0):
      return Y
    
    M = N % 8
    if(M != 0):
      for i in range(M):
        Y[i] = X[i]
      
      if(N < 8):
        return Y
    
    for i in range(M, N, 8):
      Y[i] = X[i]
      Y[i + 1] = X[i + 1]
      Y[i + 2] = X[i + 2]
      Y[i + 3] = X[i + 3]
      Y[i + 4] = X[i + 4]
      Y[i + 5] = X[i + 5]
      Y[i + 6] = X[i + 6]
      Y[i + 7] = X[i + 7]
    
    return Y
    
  def WSCAL(self, N, Alpha, X):
    
    if(Alpha == 1):
      return X
    
    if(N <= 0):
      return X
      
    M = N % 5
    
    if(M != 0):
      if(Alpha == -1):
        for i in range(M):
          X[i] = -X[i]
          
      elif(Alpha == 0):
        for i in range(M):
          X[i] = 0
      
      else:
        for i in range(M):
          X[i] = Alpha * X[i]
      
      if(N < 5):
        return X
    
    if(Alpha == -1):
      for i in range(M, N, 5):
        X[i] = -X[i]
        X[i + 1] = -X[i + 1]
        X[i + 2] = -X[i + 2]
        X[i + 3] = -X[i + 3]
        X[i + 4] = -X[i + 4]
      
    elif(Alpha == 0):
      for i in range(M, N, 5):
        X[i] = 0
        X[i + 1] = 0
        X[i + 2] = 0
        X[i + 3] = 0
        X[i + 4] = 0
        
    else:
      for i in range(M, N, 5):
        X[i] = Alpha * X[i]
        X[i + 1] = Alpha * X[i + 1]
        X[i + 2] = Alpha * X[i + 2]
        X[i + 3] = Alpha * X[i + 3]
        X[i + 4] = Alpha * X[i + 4]
    
    return X
    
  def JacTemplate(self, Y, Jac0, Fix, Njac, RCONST, identifier):
  
    JSP = Jac_SP.Jac_SP()
    
    if(identifier == 'racm'):
      Jac0 = JSP.racm(Y, Fix, RCONST, Jac0)
      
    elif(identifier == 'racmpm'):
      Jac0 = JSP.racmpm(Y, Fix, RCONST, Jac0)
  
    elif(identifier == 'racmsorg'):
      Jac0 = JSP.racmsorg(Y, Fix, RCONST, Jac0)
    
    Njac = Njac + 1
    
    return Jac0, Njac
    
    
  def PrepareMatrix(self, H, Direction, Gamma, Jac0, Ghimj, Pivot, Singular, Ndec, Nsng, identifier, LU_NONZERO, NVAR):
    
    Nconsecutive = 0
    ising = 0
    Singular = True
    
    while(Singular):
      
      Ghimj = Func.WCOPY(self, LU_NONZERO, Jac0, Ghimj)
      
      Ghimj = Func.WSCAL(self, LU_NONZERO, -1, Ghimj)
      
      ghinv = 1 / (Direction * H * Gamma)
      
      if(identifier == 'racm'):
        
        for i in range(NVAR):
          Ghimj[rj.Param.LU_DIAG[i] - 1] = Ghimj[rj.Param.LU_DIAG[i] - 1] + ghinv
        
        Ghimj, Pivot, ising, Ndec = Func.Ros_Decomp(self, Ghimj, Pivot, ising, Ndec, identifier, NVAR)
        
      elif(identifier == 'racmpm'):
       
        for i in range(NVAR):
          Ghimj[rpj.Param.LU_DIAG[i] - 1] = Ghimj[rpj.Param.LU_DIAG[i] - 1] + ghinv
        
        Ghimj, Pivot, ising, Ndec = Func.Ros_Decomp(self, Ghimj, Pivot, ising, Ndec, identifier, NVAR)
      
      elif(identifier == 'racmsorg'):
        
        for i in range(NVAR):
          Ghimj[rsj.Param.LU_DIAG[i] - 1] = Ghimj[rsj.Param.LU_DIAG[i] - 1] + ghinv
        
        Ghimj, Pivot, ising, Ndec = Func.Ros_Decomp(self, Ghimj, Pivot, ising, Ndec, identifier, NVAR)
      
      if(ising == 0):
        Singular = False
        
      else:
        Nsng = Nsng + 1
        Nconsecutive = Nconsecutive + 1
        Singular = True
        
        print("Warning: LU Decomposition returned ising =", ising)
        
        if(Nconsecutive <= 5):
          H = H * 0.5
        else:
          return
    
    return Ghimj, Singular, Pivot, H, Ndec, Nsng
    
  def Ros_Decomp(self, Ghimj, Pivot, ising, Ndec, identifier, NVAR):
  
    D = Decomp.Decomp()
  
    if(identifier == 'racm'):
      Ghimj, ising = D.racm(Ghimj, ising, NVAR)
      
    elif(identifier == 'racmpm'):
      Ghimj, ising = D.racmpm(Ghimj, ising, NVAR)
    
    elif(identifier == 'racmsorg'):
      Ghimj, ising = D.racmsorg(Ghimj, ising, NVAR) 
      
    Pivot[0] = 1
    Ndec = Ndec + 1
    
    return Ghimj, Pivot, ising, Ndec 
    
  def Ros_Solve(self, Ghimj, Pivot, X, Nsol, identifier):
  
    KS = KppSolve.KppSolve()
  
    if(identifier == 'racm'):
      X = KS.racm(Ghimj, X)
    
    elif(identifier == 'racmpm'):
      X = KS.racmpm(Ghimj, X)
    
    elif(identifier == 'racmsorg'):
      X = KS.racmsorg(Ghimj, X)
    
    Nsol = Nsol + 1
    
    return X, Nsol
    
  def ErrorNorm(self, Y, Ynew, Yerr, ATOL, RTOL, VectorTol, NVAR):
    
    Err = 0
    Scale = 0
          
    for i in range(NVAR):
      
      Ymax = max(abs(Y[i]), abs(Ynew[i]))
      
      if(VectorTol):
      
        Scale = ATOL[i] + RTOL[i] * Ymax
      
      else:
        
        Scale = ATOL[0] + RTOL[1] * Ymax
      
      Err = Err + (Yerr[i] / Scale)**2
        
    return math.sqrt(Err/NVAR)
