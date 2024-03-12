import numpy as np
import pandas as pd
import netCDF4 as nc
import os

import Parameters as pm
import Secondary_Functions
import Interface
import racmsorg_Parameters as rsm

import Output

class Computation():

  def compute(location, name, box, altitude, vmix, decomp, gas, het, aq, temp, dis_het, dis_aq, lwc, Running_days, pH, rp_um, init_values, DL_values):

    # Control units for turning on/off certain groups
    I_Gas = True if gas == 'On' else False			# Turn on/off gas reactions
    I_Het = True if het == 'On' else False			# Turn on/off heterogeneous reactions
    I_Aq  = True if aq == 'On' else False			# Turn on/off aqueous reactions
    I_mix = True if vmix == 'On' else False			# Turn on/off vertical mix
    I_deposition = True if decomp == 'On' else False		# Turn on/off surface deposition
    I_atk        = True if altitude == 'On' else False	# Turn on/off vertical mixing coefficients
    Mono_Dis_Het = False if dis_het == 'Off' else True	# True to set SA_um2_cm3 to 10, False to set SA_um2_cm3 using a function
    Mono_Dis_Aq  = False if dis_aq == 'Off' else True	# True for monodispersed hypothesized aerosol size distribution
    LWC_Switch   = False if lwc == 'Off' else True      	# True to set LWC_v_v to 1e-13, False to set LWC_v_v using a function
    Box_Model    = False if box == 'Off' else True		# True to run the program as a box model, False to run the complete program
    Temp         = False if temp == 'Off' else True     	# True to compute temperature using a function, False to set temperature as a constant

    # Import input_diurnalVarations
    df = pd.read_csv(r'input_diurnalVarations.csv')
    df1 = pd.read_csv(r'kt_SizeDist.csv')
    pm.Param.dN_dlogDp = df1['dN_dlogDp_avg'].to_dict()
    pm.Param.D_um = df1['Diameter_um'].to_dict()

    # Output file location
    path = os.path.join(location, name + '.nc')

    # Clear old output file
    try:
      os.remove(path)
    except:
      pass

    # Prepare to write netCDF file  
    ncfile = nc.Dataset(path, mode='w', format='NETCDF4')

    # Set level
    if(Box_Model):
      Level = 1
    else:
      Level = pm.Param.nlev
  
    # Set pH and rp_um
    rsm.Param.pH = float(pH)
    rsm.Param.rp_um = float(rp_um)

    # Create obj
    output = Output.Adriens_class()
    Func = Secondary_Functions.Functions()
    IT = Interface.Interface()

    # Configure location & date
    normal = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    abnormal = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    
    iyear = int(DL_values[0]) # Assign year
    
    # Calculate day
    jday = 0
    
    for i in range(int(DL_values[1]) - 1):
    
      if iyear % 4 == 0:
        jday += abnormal[i]
    
      else:
        jday += normal[i]
    
    jday += int(DL_values[2])
    
    xlat = DL_values[3] # Assign Latitude
    xlong = DL_values[4] # Assign Longitude
    stdlng = DL_values[5] # Assign STD Longtitude

    # Create var
    timloc = 0
    rho_phy = 0
    moist   = 0
    deltim = 60 * 5
    ntimes = 60 * 60 / deltim * 24 * Running_days
    x = 0  # For reading input_diurnalVarations
    y = 0  # For output

    dens2con_a = 1e-3 * (1 / 28.97) * 6.022e23
    dens2con_w = 1e-3 * (1 / (2 * 1.0079 + 15.9994)) * 6.022e23
    atols = 1
    rtols = 1e-3

    akh  = np.full(pm.Param.nlev, 0, dtype = object)
    dz   = np.full(pm.Param.nlev, 0, dtype = object)
    dzf  = np.full(pm.Param.nlev, 0, dtype = object)
    Vdep = np.full(pm.Param.nspec_host, 0, dtype = object)
    wind = np.full(pm.Param.nlev, 0, dtype = object)
    relh = np.full(pm.Param.nlev, 0, dtype = object)
    z    = np.full(pm.Param.nlev, 0, dtype = object)
    zf   = np.full(pm.Param.nlev, 0, dtype = object)

    t_prof = np.full(pm.Param.nlev, 0, dtype = object)
    p_prof = np.full(pm.Param.nlev, 0, dtype = object)
    theta  = np.full(pm.Param.nlev, 0, dtype = object)

    vc                  = np.full(pm.Param.nspec_host, 0, dtype = object)
    vcp                 = np.full((pm.Param.nlev, pm.Param.nspec_host), 0, dtype = object)
    RCONST_allLevels    = np.full((pm.Param.nlev, pm.Param.NREACT_gas), 0, dtype = object)
    RCONST              = np.full(pm.Param.NREACT_gas, 0, dtype = object)
    RCONSThet_allLevels = np.full((pm.Param.nlev, pm.Param.NREACT_het), 0, dtype = object)
    RCONSThet           = np.full(pm.Param.NREACT_het, 0, dtype = object)
    RCONSTaq_allLevels  = np.full((pm.Param.nlev, pm.Param.NREACT_aq), 0, dtype = object)
    RCONSTaq            = np.full(pm.Param.NREACT_aq, 0, dtype = object)

    phot1  = np.full((pm.Param.NREACT_J, pm.Param.nlev), 0, dtype = object)
    photoj = np.full(pm.Param.NREACT_J, 0, dtype = object)

    yield ntimes + 1

    # Initiate variables
    (dlong, sinlat, coslat, sindec, cosdec, eqtm, 
     t_prof, theta, p_prof, z, zf, dz, dzf, wind, 
     relh, vcp, phot1) = Func.Init(pm.Param.pid180, jday, stdlng, xlong, xlat, iyear, pm.Param.nlev, 
                                   z, zf, dz, dzf, t_prof, theta, p_prof, vcp, phot1, wind, relh, Temp, init_values)

    # Define output file
    output.define(pm.Param.nlev, pm.Param.nspec_host, pm.Param.NREACT_gas, pm.Param.NREACT_het, pm.Param.NREACT_aq, z)

    # Time loop
    for i in range(1, int(ntimes + 2)):
      t0 = timloc * 3600
      t1 = t0 + deltim
  
      if((i % (600 / int(deltim))) == 1):

        # Assign variables for generating output 
        parameter = [""] * 11
    
        parameter[0] = y
        parameter[1] = timloc + xlong / 15
        parameter[2] = Vdep
        parameter[3] = akh
        parameter[4] = t_prof
        parameter[5] = theta
        parameter[6] = p_prof
        parameter[7] = vcp
        parameter[8] = RCONST_allLevels
        parameter[9] = RCONSThet_allLevels
        parameter[10] = RCONSTaq_allLevels
     
        # Pass values
        output.pass_param(ncfile, parameter)
        # Generate output file
        output.output_netcdf_file()
        
        y = y + 1
        
      if((i % (3600 / int(deltim))) == 1):
        
        # Read input values from input_diurnalVarations
        pm.Param.timin            = df.iat[x,  0]
        pm.Param.averad           = df.iat[x,  1]
        pm.Param.tt               = df.iat[x,  2]
        pm.Param.pp               = df.iat[x,  3]
        pm.Param.Ozone_read       = df.iat[x,  5]
        pm.Param.NO_read          = df.iat[x,  6]
        pm.Param.NO2_read         = df.iat[x,  7]
        pm.Param.CO_read          = df.iat[x,  8]
        pm.Param.HCHO_read        = df.iat[x,  9]
        pm.Param.NOx_obs_read     = df.iat[x, 10]
        pm.Param.averad_obs_read  = df.iat[x, 11]
        pm.Param.averad_obs_Aug26 = df.iat[x, 12]
        
        pm.Param.averad = pm.Param.averad_obs_Aug26
        x = (x + 1) % 24
    
      # Calculate Sun Angle
      coszen, zenang = Func.Zenith(timloc, eqtm, dlong, pm.Param.pid, pm.Param.pid2, sinlat, sindec, coslat, cosdec)
      
      source = np.full((pm.Param.nlev, pm.Param.nspec_host), 0, dtype = object)
      
      # Calculate vertical mixing coefficients
      if(I_atk):
        akh, theta = Func.Atk(akh, pm.Param.LH2O, pm.Param.nlev, theta, t_prof, p_prof, vcp, wind, z)
      
      # Calculate surface deposition
      if(I_deposition):
        Vdep, source = Func.Sinks(akh, pm.Param.f0, pm.Param.henry, pm.Param.LO3, pm.Param.nlev, pm.Param.nspec_host, relh, source, vcp, dz, z)
        
      # Calculate vertical mix
      if(I_mix):
      
        vcp = Func.Newc(pm.Param.nlev, akh, dzf, dz, deltim, pm.Param.nspec_host, vcp, source, pm.Param.LH2O, pm.Param.LO3P)
        
        source = np.full((pm.Param.nlev, pm.Param.nspec_host), 0, dtype = object)
        
        vcp = Func.Newc(pm.Param.nlev, akh, dzf, dz, deltim, pm.Param.nspec_host, vcp, source, pm.Param.LH2O, pm.Param.LO3P) # Need vertical mixing to smooth near surface since extreme high resolution, 0.1m
        
      # Height loop
      for j in range(Level):
        for m in range(pm.Param.nspec_host):
          vc[m] = vcp[j, m]
        
        moist = vc[pm.Param.LH2O] * 18 / 28.8
        pm.Param.tt = t_prof[j]
        pm.Param.pp = p_prof[j]
        rho_phy = pm.Param.pp / (pm.Param.tt * 287.058)
        
        # Assign all photolysis elements
        for m in range(pm.Param.NREACT_J):
          photoj[m] = phot1[m, j]
        
          if(coszen > 0):
            photoj[m] = photoj[m] / 60 * coszen
          else:
            photoj[m] = 0
            
        pm.Param.ph_o31d     = photoj[ 0]   
        pm.Param.ph_h2o2     = photoj[ 1]  
        pm.Param.ph_no2      = photoj[ 2]  
        pm.Param.ph_no3o     = photoj[ 3]  
        pm.Param.ph_n2o5     = photoj[ 4]  
        pm.Param.ph_hno2     = photoj[ 5]  
        pm.Param.ph_hno3     = photoj[ 6]  
        pm.Param.ph_hno4a    = photoj[ 7]  
        pm.Param.ph_hno4b    = photoj[ 8]  
        pm.Param.ph_ch2or    = photoj[ 9]  
        pm.Param.ph_ch2om    = photoj[10]  
        pm.Param.ph_ch3cho   = photoj[11]  
        pm.Param.ph_propanal = photoj[12]  
        pm.Param.ph_acetone  = photoj[13]  
        pm.Param.ph_ch3ooh   = photoj[14]  
        pm.Param.ph_oclo     = photoj[15]  
        pm.Param.ph_cl2      = photoj[16]  
        pm.Param.ph_clo      = photoj[17]  
        pm.Param.ph_hocl     = photoj[18]  
        pm.Param.ph_clno2    = photoj[19]  
        pm.Param.ph_clno3a   = photoj[20]  
        pm.Param.ph_clno3b   = photoj[21]  
        pm.Param.ph_bro      = photoj[22]  
        pm.Param.ph_br2      = photoj[23]  
        pm.Param.ph_hobr     = photoj[24]  
        pm.Param.ph_brno2    = photoj[25]  
        pm.Param.ph_brno3a   = photoj[26]  
        pm.Param.ph_brno3b   = photoj[27]  
        pm.Param.ph_brcl     = photoj[28]
        
        # Gas reactions
        if(I_Gas):
          vc, RCONST = IT.racm(vc, RCONST, atols, rtols, deltim, dens2con_a, rho_phy, dens2con_w, moist)
          
        # Heterogeneous reactions
        if(I_Het):
          vc, RCONSThet = IT.racmpm(vc, RCONSThet, atols, rtols, deltim, dens2con_a, rho_phy, dens2con_w, moist, Mono_Dis_Het)
        
        # Aqueous reactions  
        if(I_Aq):
          vc, RCONSTaq = IT.racmsorg(vc, RCONSTaq, atols, rtols, deltim, dens2con_a, rho_phy, dens2con_w, moist, LWC_Switch, Mono_Dis_Aq)
          
        for m in range(pm.Param.nspec_host):
          vcp[j, m] = max(vc[m], 0)
      
        for m in range(pm.Param.NREACT_gas):
          RCONST_allLevels[j, m] = RCONST[m]
          
        for m in range(pm.Param.NREACT_het):
          RCONSThet_allLevels[j, m] = RCONSThet[m]
        
        for m in range(pm.Param.NREACT_aq):
          RCONSTaq_allLevels[j, m] = RCONSTaq[m]
        
      timloc = t1 / 3600
      
      yield i # Used for GUI progression bar
      
    ncfile.close()
    
if __name__ == "__main__":
#                               directory path,   output file name,   box model, altitude, vmix, decomp, gas,  het,  aq,   temp, dis_het, dis_aq, lwc,   Running_days, pH,  rp_um
  for i in (Computation.compute(os.getcwd(),      "Test Output",      "Off",     "On",     "On", "On",   "On", "On", "On", "On", "Off",   "Off",  "Off", 1,            4.0, 0.2, 
#                   init_values: "O1D", "O3P", "OH", "HO2", "CO",     "O3",    "H2O2", "NO",    "NO2", 
                                [0,     0,     0,    0,     160.0e-9, 34.0e-9, 2e-9,   0.02e-9, 0.05e-9,
#                                "NO3", "HNO3", "HNO4", "N2O5", "HONO", "CH4",  "CH3O2", "CH3OOH", "C2H6", 
                                 0,     0,      0,      0,      0,      1.9e-6, 0,       0,        0,
#                                "C2H5O2", "C2H5OOH", "C3H8", "nC3H7O2", "iC3H7O2", "nC3H7OH", "iC3H7OH", "nButane", "iButane", 
                                 0,        0,         0,      0,         0,         0,         0,         0,         0,
#                                "sC4H9O2", "nC4H9O2", "tC4H9O2", "iC4H9O2", "sC4H9OH", "nC4H9OH", "tC4H9OH", "iC4H9OH", "sC4H9OOH", 
                                 0,         0,         0,         0,         0,         0,         0,         0,         0,
#                                "nC4H9OOH", "HCHO", "CH3CHO", "MEK", "Acetone", "Propanal", "Butanal", "iButanal", "CH3CO3", 
                                 0,          0.3e-9, 0,        0,     0,         0,          0,         0,          0,
#                                "PAN", "Cl", "Cl2",  "ClO", "OClO", "HOCl", "HCl", "ClNO2", "ClNO3", 
                                 0,     0,    10e-12, 0,     0,      0,      0,     0,       1e-20,
#                                "Br", "Br2",  "BrO", "HOBr", "HBr", "BrCl", "BrONO", "BrNO2", "BrNO3", 
                                 0,    20e-12, 0,     0,      0,     0,      0,       0,       1e-20,
#                                "H2O", "Clm_p", "Brm_p", "O3_p", "HOCl_p", "Cl2_p", "HOBr_p", "Br2_p", "BrCl_p"
                                 0,     1,       1e-20,   0,      0,        0,       0,        0,       0],
#                     DL_values: year,  month, day,  latitude, longitutde, STD longitude
                                ['2012', '03',  '24', 72.,      156.,       156.])):
                                     
    _ = i
