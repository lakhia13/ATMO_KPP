import numpy as np

class Adriens_class():

  time = None
  z_coordinate = None
  Concentration = None
  RCONST_gas = None
  RCONST_het = None
  RCONST_aq = None
  Kh = None
  Vdep = None
  temperature = None
  potential_temperature = None
  pressure = None

  def define(self, n_level, n_species, n_reactions_gas, n_reactions_het, n_reactions_aq, z_coordinate):

    self.nlev = n_level
    self.nspec = n_species
    self.NREACT_gas = n_reactions_gas
    self.NREACT_het = n_reactions_het
    self.NREACT_aq = n_reactions_aq
    self.z_coordinate = z_coordinate

  def pass_param(self,ncfile,parameter):
    
    self.ncfile = ncfile
    self.parameter = parameter

  def output_netcdf_file(self):

    ncfile = self.ncfile
    
    t = self.parameter[0]

    if t == 0:

      List = ["""O1D,O3P,OH,HO2,CO,O3,H2O2,NO,\
      NO2,NO3,HNO3,HNO4,N2O5,HONO,CH4,CH3O2,\
      CH3OOH,C2H6,C2H5O2,C2H5OOH,\
      C3H8,nC3H7O2,iC3H7O2,nC3H7OH,\
      iC3H7OH,nButane,iButane,sC4H9O2,\
      nC4H9O2,tC4H9O2,iC4H9O2,sC4H9OH,\
      nC4H9OH,tC4H9OH,iC4H9OH,sC4H9OOH, \
      nC4H9OOH,HCHO,CH3CHO,MEK, \
      Acetone,Propanal,Butanal,iButanal,CH3CO3,PAN,Cl, \
      Cl2,\
      ClO,OClO,HOCl,HCl,ClNO2,ClNO3,Br,Br2, \
      BrO,HOBr,HBr,BrCl,BrONO,BrNO2,BrNO3, \
      H2O, Clm_p,Brm_p, \
      O3_p,HOCl_p,Cl2_p,HOBr_p,Br2_p,BrCl_p"""]

      #! Define the dimensions. 

      level_dim = ncfile.createDimension('level', self.nlev)
      species_dim = ncfile.createDimension('species', self.nspec)
      reactions_gas_dim = ncfile.createDimension('reactions_gas', self.NREACT_gas)
      reactions_het_dim = ncfile.createDimension('reactions_het', self.NREACT_het)
      reactions_aq_dim = ncfile.createDimension('reactions_aq', self.NREACT_aq)
      time = ncfile.createDimension('time', None)

      #! Assign create Variables`

      time = ncfile.createVariable('time', np.float32, ('time',))
      z_coordinate = ncfile.createVariable('z_coordinate', np.float32, ('level',))
      Concentration = ncfile.createVariable('Concentration',np.float64,('time','level','species'))
      RCONST_gas = ncfile.createVariable('RCONST_gas',np.float64,('time','level','reactions_gas'))
      RCONST_het = ncfile.createVariable('RCONST_het',np.float64,('time','level','reactions_het'))
      RCONST_aq = ncfile.createVariable('RCONST_aq',np.float64,('time','level','reactions_aq'))
      Kh = ncfile.createVariable('Kh',np.float64,('time','level'))
      Vdep = ncfile.createVariable('Vdep',np.float64,('time','species'))
      temperature = ncfile.createVariable('temperature',np.float64,('time','level'))
      potential_temperature = ncfile.createVariable('potential_temperature',np.float64,('time','level'))
      pressure = ncfile.createVariable('pressure',np.float64,('time','level'))

      #! Assign units attributes to the netCDF variables.

      Kh.units = 'm2/s'
      Vdep.description = 'deposition velocity'
      Vdep.units = 'm/s'
      temperature.units = 'K'
      potential_temperature.units = 'K'
      pressure.units = 'Pa'
      Concentration.units = 'gas (ppbv); aerosol (ended with _p) (µg m-3)'
      Conc_UNITS = "gas (ppbv); aerosol (ended with _p) (µg m-3)"
      RCONST_UNITS = "cm3 molecule-1 s-1 (s-1 for the 1st 29 photolysis reactions)"
      RCONSThet_UNITS = "cm3 molecule-1 s-1"
      RCONSTaq_UNITS = "cm3 molecule-1 s-1"
      Concentration.SpeciesList = List
      RCONST_gas.units = "cm3 molecule-1 s-1 (s-1 for the 1st 29 photolysis reactions)"
      RCONST_gas.Reaction_List = "see http://www.caps.ou.edu/micronet/temp/Jose/Kerri/racm.eqn" 
      RCONST_het.units = "cm3 molecule-1 s-1"
      RCONST_het.Reaction_List  = "see http://www.caps.ou.edu/micronet/temp/Jose/Kerri/racmpm.eqn_xhu"
      RCONST_aq.units = "cm3 molecule-1 s-1"
      RCONST_aq.Reaction_List  = "see http://www.caps.ou.edu/micronet/temp/Jose/Kerri/racmsorg_aqchem.eqn"  
      RCONST_aq.Actual_rates = "check module_kpp_racmsorg_aqchem_Update_Rconst.f90"
      time.units = 'UTC'
      z_coordinate.units = 'm'

      ### DATA CREATION ###

      Adriens_class.time = ncfile.variables['time']
      Adriens_class.z_coordinate = ncfile.variables['z_coordinate']
      Adriens_class.Concentration = ncfile.variables['Concentration']
      Adriens_class.RCONST_gas = ncfile.variables['RCONST_gas']
      Adriens_class.RCONST_het = ncfile.variables['RCONST_het']
      Adriens_class.RCONST_aq = ncfile.variables['RCONST_aq']
      Adriens_class.Kh = ncfile.variables['Kh']
      Adriens_class.Vdep = ncfile.variables['Vdep']
      Adriens_class.temperature = ncfile.variables['temperature']
      Adriens_class.potential_temperature = ncfile.variables['potential_temperature']
      Adriens_class.pressure = ncfile.variables['pressure']
      
      Adriens_class.z_coordinate[:] = self.z_coordinate

    ### DATA WRITING ###

    Adriens_class.time[t] = self.parameter[1]
    Adriens_class.Vdep[t] = self.parameter[2]
    Adriens_class.Kh[t] = self.parameter[3]
    Adriens_class.temperature[t] = self.parameter[4]
    Adriens_class.potential_temperature[t] = self.parameter[5]
    Adriens_class.pressure[t] = self.parameter[6]
    Adriens_class.Concentration[t] = self.parameter[7]
    Adriens_class.RCONST_gas[t] = self.parameter[8]
    Adriens_class.RCONST_het[t] = self.parameter[9]
    Adriens_class.RCONST_aq[t] = self.parameter[10]
