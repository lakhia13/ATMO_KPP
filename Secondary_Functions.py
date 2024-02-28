import numpy as np
import math
import Parameters as pm

class Functions():

# ====================================== Altitude ====================================== 

  def Atk(self, akh, LH2O, nlev, theta, t_prof, p_prof, vcp, wind, z):
    
    ak = 0.4
    grav = 9.81
    airmol = 0.1529e-04
    thelam = 30
    brcr = 0.25
    xx0 = 0
    xxh = 0
    kpbl = 0
    
    stable = False
    knov = False
    
    ajnn = np.full(nlev, 0, dtype = object)
    akhst = np.full(nlev, 0, dtype = object)
    akm = np.full(nlev, 0, dtype = object)
    akmst = np.full(nlev, 0, dtype = object)
    akm_ysu = np.full(nlev, 0, dtype = object)
    thvx = np.full(nlev, 0, dtype = object)
    ri_pro = np.full(nlev, 0, dtype = object)
    
    for i in range(nlev):
      theta[i] = t_prof[i] * ((100000 / p_prof[i])**0.286)
      
      im = max(i - 1, 0)
      ip = min(i + 1, nlev - 1)
      
      akhst[i] = 0.05 * akh[i] + 0.9 * akh[im] + 0.05 * akh[ip] + airmol
      akmst[i] = 0.05 * akm[i] + 0.9 * akm[im] + 0.05 * akm[ip] + airmol
      
    for i in range(nlev - 1):
      im = max(i - 1, 0)
      ip = min(i + 1, nlev - 1)
      
      dz_xhu = z[i + 1] - z[i]
      strat = (theta[i + 1] - theta[i]) / dz_xhu
      
      if(strat <= 0):
        xx0 = xx0 + (z[ip] - z[i])
        knov = (theta[i] + 0.1) < theta[0]
        
        if(knov):
          if(xxh <= 0):
            xxh = z[i]
          
      else:
        knov = False
    
    stable_xhu = False
    
    for i in range(nlev):
      thvx[i] = theta[i] * (1 + 0.61 * vcp[i, LH2O] * 0.622)
      
    for i in range(15, nlev - 1):
      if(not stable_xhu):
        spdk2 = max(wind[i]**2, 1)
        brup = (thvx[i] - thvx[14]) * (9.8 * (z[i] - z[14]) / thvx[14]) / spdk2
        kpbl = i
        stable_xhu = brup > brcr
        
    for i in range(nlev - 1):
      dz_xhu = z[i + 1] - z[i]
      strat = (theta[i + 1] - theta[i]) / dz_xhu
      vzbet = (wind[i + 1] - wind[i]) / dz_xhu
      
      zm = 0.5 * (z[i] + z[i + 1])
      tm = 0.5 * (t_prof[i] + t_prof[i + 1])
      
      vzbet2 = vzbet * vzbet
      
      ri = grav * strat / (tm * vzbet2)
      ri_pro[i] = ri
      
      xlam = max(thelam, 0.1 * xx0, 0.1 * xxh)
      
      if(zm > max(xx0, xxh)):
        xlam = thelam
        
      All = ak * zm / (1 + ak * zm / xlam)
      
      ajnn[i] = (All**2) * math.sqrt(vzbet2)
      
      if(ri < 0):
        akm[i] = ajnn[i] * math.sqrt(1 - 11 * ri) + airmol
        akh[i] = akm[i] * 1.35 * (1 - 5.5 * ri) / (1 - 3 * ri) + airmol
      
      else:
        ri = min(ri, 1)
        akm[i] = ajnn[i] / math.sqrt(1 + 6 * ri) + airmol
        
        Ustar = 0.4
        Z_over_L = 0.1
        
        akm_ysu[i] = (0.4 * Ustar / (1 + 5 * Z_over_L) * z[i] * ((1 - z[i] / z[kpbl])**3))
                    
        if(z[kpbl] < 400 and z[i] < z[kpbl]):
          akm[i] = max(akm[i], akm_ysu[i])
        
        if(stable):
          akh[i] = akm[i] * 1.35 / (1 + 6 * ri) + airmol
        
        else:
          akh[i] = akm[i]
        
      akm[i] = 0.1 * akmst[i] + 0.9 * akm[i]
      akh[i] = 0.1 * akhst[i] + 0.9 * akh[i]
    
    return akh, theta

# ====================================== Solar Daclination ====================================== 
        
  def Declin(decmax, icumdy, iyear, pid180):
    
    kday = (iyear - 1977) * 365 + icumdy + 28123
    xm = (-1 + 0.9856 * kday) * pid180
    delnu = 2 * 0.01674 * math.sin(xm) + 1.25 * 0.01674 * 0.01674 * math.sin(2*xm)
    slong = (-79.828 + 0.9856479 * kday) * pid180 + delnu
    decl = math.asin(decmax * math.sin(slong))
    sindec = math.sin(decl)
    cosdec = math.cos(decl)
    eqtm = (9.4564 * math.sin(2 * slong) / cosdec - 4 * delnu / pid180) / 60
    
    return sindec, cosdec, eqtm

# ====================================== Generate Initial Values ====================================== 

  def Init(self, pid180, jday, stdlng, xlong, xlat, iyear, nlev, 
           z, zf, dz, dzf, t_prof, theta, p_prof, vcp, phot1, wind, relh, temp, init_val):
  
    pres = 1013.25*100 # Surface presssure, pascal
  
    decmax = math.sin(23.44 * pid180)
   
    # Hard-coded jday, iyear, xlat, xlong, stdlng
  
    icumdy = jday
  
    dlong = (stdlng - xlong) / 15
    sinlat = math.sin(xlat * pid180)
    coslat = math.cos(xlat * pid180)
    
    sindec, cosdec, eqtm = Functions.Declin(decmax, icumdy, iyear, pid180) # Solar daclination
    
    # Altitude calculation
    
    for i in range(nlev):
      x = i + 1 # Because Python array starts at 0, whereas Fortran array can start at 1
    
      if(i < 9):
        z[i] = x * 0.1
      elif(i < 47):
        z[i] = 1 + (x - 10) * 0.5
      elif(i < 127):
        z[i] = 20 + (x - 48)
      elif(i < 188):
        z[i] = 100 + (x - 128) * 5
      elif(i < 218):
        z[i] = 400 + (x - 188) * 20
      else:
        z[i] = 1000 + (x - 218) * 100
    
    zf[nlev - 1] = (z[nlev - 1] + 0.5 * 
                                      (z[nlev - 1] - z[nlev - 2]))
                                      
    for i in range(nlev - 1):
      zf[i] = 0.5 * (z[i + 1] + z[i])
      
      if(i > 0):
        dzf[i] = zf[i] - zf[i - 1]
      
      dz[i] = z[i + 1] - z[i]
    
    dzf[0] = zf[0]
    dzf[nlev - 1] = dzf[nlev - 2]  
    dz[nlev - 1] = dz[nlev - 2]
  
    # ----------------------------------------------------------
    # ------------ Initialize atmospheric variables ------------
  
    for i in range(nlev):
      p_prof[i] = pres * (((1 - (z[i]) / 44308))**(1 / 0.19023)) # Pressure
      
      if temp: # Calculate temperature using a function
        t_prof[i] = 273 - z[i] * 0.0085 #0.0055
          
        if z[i] > 1500: 
          t_prof[i] = (300 -1500 * 0.005) - (z[i] - 1500) * 0.002
          
        if z[i] < 28:
          t_prof[i] = 290.00 + z[i] * 0.20 
      
      else: # Temperature is a constant
        t_prof[i] = 273
      
      theta[i] = t_prof[i] * ((100000 / p_prof[i])**0.286)
      
      wind = Functions.Wprofil(nlev, wind, z)
      
      # ----------------------------------
      # ------------ Humidity ------------
        
      relh[i] = 0.7
      
      if(z[i] < 500):
        relh[i] = 0.7 - z[i] * 0.2/500
        
      p1 = (relh[i] * 610.7 * math.exp(17.1536 * (t_prof[i] - 273.15) / (t_prof[i] - 38.33)))
      
      # --------------------------------------------
      # ------------ Chemical compounds ------------
      # Volume mixing ratio [ppmv*10**6], corresponding to mole fraction
      
      for k in range(len(init_val)):
      
        vcp[i, k] = init_val[k]
        
      vcp[i, pm.Param.LH2O]   = p1 / p_prof[i]
      '''
      vcp[i, pm.Param.LNO]    = 0.02 * 1e-9    # NO
      vcp[i, pm.Param.LNO2]   = 0.05e-9        # NO2
      vcp[i, pm.Param.LO3]    = 34.0e-9        # O3
      vcp[i, pm.Param.LCO]    = 160.0e-9       # CO
      vcp[i, pm.Param.LCH4]   = 1.9e-6         # CH4
      vcp[i, pm.Param.LHCHO]  = 0.3e-9         # HCHO
      vcp[i, pm.Param.LH2O2]  = 2e-9           # H2O2
      vcp[i, pm.Param.LBR2]   = 20e-12
      vcp[i, pm.Param.LCL2]   = 10e-12
      vcp[i, pm.Param.LCLM_P] = 1		# μg m-3
      vcp[i, pm.Param.LBRM_P] = 1e-20		# μg m-3
      vcp[i, pm.Param.LCLNO3] = 1e-20
      vcp[i, pm.Param.LBRNO3] = 1e-20
      #vcp[i, pm.Param.LC2H6]  = 2.0e-9 
      #vcp[i, pm.Param.LCH3CHO]= 170.0e-12	
      #vcp[i, pm.Param.LHNO3]  = 0.01e-9	# hno3
      #vcp[i, pm.Param.LNO3]   = 0.001e-9
      #vcp[i, pm.Param.LN2O5]  = 1e-9 * 1e-10
      #vcp[i, pm.Param.LCLNO2] = 1e-9
      #vcp[i, pm.Param.LHCL]   = 1e-9    	# μg m-3 
      #vcp[i, pm.Param.LHBR]   = 1e-9    	# μg m-3 
      #vcp[i, pm.Param.LHOBR]  = 10e-9    	# μg m-3 
      #vcp[i, pm.Param.LCLM_P] = 1e-20    	# μg m-3 Alternative, disabled in Fortran
      #vcp[i, pm.Param.LBRM_P] = 0.01     	# μg m-3 Alternative, disabled in Fortran 
      #if(i == 1):
         #vcp[i, pm.Param.LHCL] = 2e-9    	# μg m-3 
      #else: 
         #vcp[i, pm.Param.LHCL] = 1e-9    	# μg m-3  
      #vcp[i, pm.Param.LBRO]   = 0.2e-12
      '''
      # ------------------------------------------------
      # ------------ Photolysis frequencies ------------
      # Constant with height! Will be corrected for current zenith angle and in-cammopy extinction with a very simple paramerization in the main program before calling the chemistry routine.
      # Units for rate constants : 1/min Values for zenith angle=0
      # Calculated by TUV 5.0 by Siyuan

      phot1[0, i]  = 6.24e-05 * 60
      phot1[1, i]  = 1.99e-05 * 60
      phot1[2, i]  = 2.94e-02 * 60
      phot1[3, i]  = 4.62e-01 * 60
      phot1[4, i]  = 1.26e-04 * 60
      phot1[5, i]  = 6.04e-03 * 60  
      phot1[6, i]  = 1.52e-06 * 60
      phot1[7, i]  = 1.12e-05 * 60
      phot1[8, i]  = 0.00e+00 * 60
      phot1[9, i]  = 1.37e-04 * 60
      phot1[10, i] = 8.25e-05 * 60
      phot1[11, i] = 1.15e-05 * 60
      phot1[12, i] = 4.35e-05 * 60
      phot1[13, i] = 7.16e-07 * 60  
      phot1[14, i] = 1.54e-05 * 60
      phot1[15, i] = 0.00e+00 * 60
      phot1[16, i] = 7.31e-03 * 60
      phot1[17, i] = 9.81e-05 * 60
      phot1[18, i] = 4.1787e-04 * 60
      phot1[19, i] = 1.48e-03 * 60
      phot1[20, i] = 1.22e-04 * 60
      phot1[21, i] = 2.23e-05 * 60
      phot1[22, i] = 1.18e-01 * 60
      phot1[23, i] = 9.55e-02 * 60
      phot1[24, i] = 6.87e-03 * 60  
      phot1[25, i] = 3.39286e-02 * 60
      phot1[26, i] = 1.25e-03 * 60
      phot1[27, i] = 3.05e-03 * 60
      phot1[28, i] = 2.73477e-02 * 60
      
      # ------------------------------------------------
      
    return dlong, sinlat, coslat, sindec, cosdec, eqtm, t_prof, theta, p_prof, z, zf, dz, dzf, wind, relh, vcp, phot1

# ====================================== Vertical Mix ====================================== 
      
  def Newc(self, nlev, akh, dzf, dz, deltim, nspec_host, vcp, source, LH2O, LO3P):
  
    nr = 1
    
    a0 = np.full(nlev, 0, dtype = object)
    b0 = np.full(nlev, 0, dtype = object)
    c0 = np.full(nlev, 0, dtype = object)
    cs = np.full(nlev, 0, dtype = object)
    x  = np.full(nlev, 0, dtype = object)
    
    for i in range(1, nlev - 1):
      
      a0[i] = -akh[i - 1] / dzf[i] / dz[i - 1] * deltim
      c0[i] = -akh[i] / dzf[i] / dz[i] * deltim
      b0[i] = 1 + (-a0[i] - c0[i]) 
      
    for i in range(nspec_host):
    
      if i == 51:
        continue
        
      for j in range(nlev):
        cs[j] = vcp[j, i]
      
      for j in range(1, nlev - 1):
        x[j] = cs[j] + source[j, i] * deltim
          
      at = 0
      bt = 1
      dt = cs[nlev - 1]
      ab = 1
      bb = 0
      db = cs[0] + source[0, i] * deltim
      
      if(i == LH2O):
        db = cs[0]
      
      if(i != LO3P):
        cs = Functions.solve(ab, bb, db, at, bt, dt, a0, b0, c0, x, cs, nr, nlev)
      
      for j in range(nlev):
        vcp[j, i] = max(cs[j], 0)
        
      vcp[0, i] = vcp[0, i] * 0.1 + vcp[1, i] * 0.9
    
    return vcp
    
# ====================================== Surface Decomposition ====================================== 

  def Sinks(self, akh, f0, henry, LO3, nlev, nspec_host, relh, source, vcp, dz, z):
    
    rcutref = 3000
    
    rgs = 500
    rgo = 200
    
    f0[LO3] = 1
    
    if(relh[0] > 0.8):
      rgo = 200 + 1800 * (relh[0] - 0.8) / (0.999 - 0.8)
      f0[LO3] = 1 - 0.9 * (relh[0] - 0.8) / (0.999 - 0.8)
      
    Vdep = np.full(nspec_host, 0, dtype = object)
    
    for i in range(nspec_host - 9): # only for gas species
      rgi = 1 / (henry[i] * 1e-5 / rgs + f0[i] / rgo)
      ra0 = z[1] / max(1e-4, akh[0])
      
      sh1 = 1 / (ra0 + rgi)
      Vdep[i] = sh1
      si = -sh1 * vcp[0, i] / dz[0]
      source[0, i] = source[0, i] + si
      
    return Vdep, source

#  ====================================== A function used for vertical mix ====================================== 

  def solve(ab, bb, db, at, bt, dt, a, b, c, d, var, nr, nlev):
  
    alpha = np.full(nlev, 0, dtype = object)
    beta = np.full(nlev, 0, dtype = object)
    xx = np.full(nlev, 0, dtype = object)
  
    alpha[nr - 1] = -bb / ab
    beta[nr - 1] = db / ab
    
    m1 = nlev - 1
    
    for j in range(nr, m1):
      xx[j] = (a[j] * alpha[j-1] + b[j])
      alpha[j] = -c[j] / xx[j]
      beta[j] = -(a[j] * beta[j-1] - d[j]) / xx[j]
      
    var[nlev - 1] = (dt - at * beta[m1 - 1]) / (bt + alpha[m1 - 1] * at)
    
    for jj in range(nr - 1, m1):
      j = nlev - 2 - jj
      var[j] = var[j + 1] * alpha[j] + beta[j]
        
      if(var[j] < 0):
        var[j] = 0.0001 * var[j+1]
        
    return var
    
# ====================================== Wind Profile ====================================== 

  def Wprofil(nlev, wind, z):
  
    vg = 7.0
  
    ustara = vg / 30
    wind[0] = 0
    
    for i in range(1, nlev):
      wind[i] = ustara * math.log((z[i]) / 0.01) / 0.4
      
    return wind

# ====================================== Zenith ====================================== 
        
  def Zenith(self, timloc, eqtm, dlong, pid, pid2, sinlat, sindec, coslat, cosdec):
    
    crtzen = 0
    
    timsun = timloc + eqtm + dlong
    hrang = (timsun - 12) * pid2 / 6
    zenang = math.acos(sinlat * sindec + coslat * cosdec * math.cos(hrang))
    sunazm = math.asin(cosdec * math.sin(hrang) / math.sin(zenang))
    
    if(sindec > sinlat):
      crtzen = math.acos(1)
    else:
      crtzen = math.acos(sindec / sinlat)
      
    if(zenang > crtzen):
      sunazm = (pid - abs(sunazm)) * sunazm / abs(sunazm)
    
    sunazm = sunazm + pid
    coszen = math.cos(zenang)
    
    if(timloc == 4.5):
      print("Check coszen: ", coszen)
      
    return coszen, zenang
