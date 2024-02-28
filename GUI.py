import PySimpleGUI as sg
import os.path
import datetime
import re

import Main
import Plot
import Convert

# ====================================================================================================================================================

sg.theme("default1") # Set GUI Theme

# Species list
specie_list = ["O1D", "O3P", "OH", "HO2", "CO", "O3", "H2O2", "NO", "NO2", 
               "NO3", "HNO3", "HNO4", "N2O5", "HONO", "CH4", "CH3O2", "CH3OOH", "C2H6", 
               "C2H5O2", "C2H5OOH", "C3H8", "nC3H7O2", "iC3H7O2", "nC3H7OH", "iC3H7OH", "nButane", "iButane", 
               "sC4H9O2", "nC4H9O2", "tC4H9O2", "iC4H9O2", "sC4H9OH", "nC4H9OH", "tC4H9OH", "iC4H9OH", "sC4H9OOH", 
               "nC4H9OOH", "HCHO", "CH3CHO", "MEK", "Acetone", "Propanal", "Butanal", "iButanal", "CH3CO3", 
               "PAN", "Cl", "Cl2", "ClO", "OClO", "HOCl", "HCl", "ClNO2", "ClNO3", 
               "Br", "Br2", "BrO", "HOBr", "HBr", "BrCl", "BrONO", "BrNO2", "BrNO3", 
               "H2O", "Clm_p", "Brm_p", "O3_p", "HOCl_p", "Cl2_p", "HOBr_p", "Br2_p", "BrCl_p", "Kh"]

# Height list
z = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 
     1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 
     5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 
     10.0, 10.5, 11.0, 11.5, 12.0, 12.5, 13.0, 13.5, 
     14.0, 14.5, 15.0, 15.5, 16.0, 16.5, 17.0, 17.5, 
     18.0, 18.5, 19.0, 19.5, 20, 21, 22, 23, 24, 25, 
     26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 
     38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 
     50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 
     62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 
     74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 
     86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 
     98, 99, 100, 105, 110, 115, 120, 125, 130, 135, 
     140, 145, 150, 155, 160, 165, 170, 175, 180, 185, 
     190, 195, 200, 205, 210, 215, 220, 225, 230, 235, 
     240, 245, 250, 255, 260, 265, 270, 275, 280, 285, 
     290, 295, 300, 305, 310, 315, 320, 325, 330, 335, 
     340, 345, 350, 355, 360, 365, 370, 375, 380, 385, 
     390, 395, 400, 420, 440, 460, 480, 500, 520, 540, 
     560, 580, 600, 620, 640, 660, 680, 700, 720, 740, 
     760, 780, 800, 820, 840, 860, 880, 900, 920, 940, 
     960, 980, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 
     1700, 1800, 1900, 2000, 2100, 2200, 2300, 2400, 2500, 
     2600, 2700, 2800, 2900, 3000, 3100, 3200, 3300, 3400, 
     3500, 3600, 3700, 3800, 3900, 4000]

# List of initial values for all elements
init_val = [0, 0, 0, 0, 160.0, 34.0, 2.0, 0.02, 0.05,
            0, 0, 0, 0, 0, 1.9, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0.3, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 10, 0, 0, 0, 0, 0, 1e-5,
            0, 20, 0, 0, 0, 0, 0, 0, 1e-5,
            0, 1, 1e-5, 0, 0, 0, 0, 0, 0]


#             e-6     e-9     e-12    e-15   e0      e-6      e-9
unit_list = ['ppmv', 'ppbv', 'pptv', 'ppqv', 'ppv', 'mg/m3', 'µg/m3']

# ====================================================================================================================================================

def confirmation_window(location, name, to_csv, to_txt, box_model, altitude, 
                        vmix, decomp, gas, het, aq, temp, dis_het, dis_aq, 
                        lwc, running_time, pH, rp_um):
    
    # =============================== Confirmation Interface Layout ===============================
    
    layout_msg = [[sg.VPush()],
                  [sg.Text("Confirm your specification:", font = ("Arial", 15))],
                  [sg.Text("Output Location: " + location)],
                  [sg.Text("Name of NetCDF Output File: " + name)],
                  [sg.Text("Generate CSV: " + str(to_csv))],
                  [sg.Text("Generate Text: " + str(to_txt))],
                  [sg.Text("Box Model: " + box_model)],
                  [sg.Text("Altitude Calculations: " + altitude)],
                  [sg.Text("Vertical Mix Calculations: " + vmix)],
                  [sg.Text("Surface Decomposition Calculations: " + decomp)],
                  [sg.Text("Gas Reaction Calculations: " + gas)],
                  [sg.Text("Het Reaction Calculations: " + het)],
                  [sg.Text("Aq Reaction Calculations: " + aq)],
                  [sg.Text("Temperature Calculations: " + temp)],
                  [sg.Text("Mono_Dis_Het Calculations: " + dis_het)],
                  [sg.Text("Mono_Dis_Aq Calculations: " + dis_aq)],
                  [sg.Text("LWC_v_v Calculations: " + lwc)],
                  [sg.Text("Running Time: " + str(running_time) + " day(s)")],
                  [sg.Text("pH Value: " + str(pH))],
                  [sg.Text("rp_um Value: " + str(rp_um))],
                  [sg.Button("Confirm", key = "yes"), sg.Button("Cancel", key = "no")],
                  [sg.VPush()]]
        
    layout = [[sg.VPush()],
              [sg.Column(layout_msg, element_justification = "center", key = "-MSG-")],
              [sg.VPush()],]
    
    window = sg.Window("Confirmation", layout, element_justification = "c")

    # =============================== Run the Event Loop ===============================
    
    while True:
    
        event, values = window.read()
        
        if event == "no" or event == "Exit" or event == sg.WIN_CLOSED:
            # Close Window
            window.close()
            
            return False
            
        if event == "yes":
            # Close Window
            window.close()
        
            return True

# ====================================================================================================================================================
   
def main():
     
    # =============================== Initial value elements ===============================
    
    col1 = [[sg.Text("O1D",      size = (11, 1)), sg.In(size = (8, 1), key = "E1"), sg.Combo(unit_list, size = (5, 1), default_value='ppmv', key = "unit_E1")],
            [sg.Text("O3P",      size = (11, 1)), sg.In(size = (8, 1), key = "E2"), sg.Combo(unit_list, size = (5, 1), default_value='ppmv', key = "unit_E2")],
            [sg.Text("OH",       size = (11, 1)), sg.In(size = (8, 1), key = "E3"), sg.Combo(unit_list, size = (5, 1), default_value='ppmv', key = "unit_E3")],
            [sg.Text("HO2",      size = (11, 1)), sg.In(size = (8, 1), key = "E4"), sg.Combo(unit_list, size = (5, 1), default_value='ppmv', key = "unit_E4")],
            [sg.Text("CO",       size = (11, 1)), sg.In(size = (8, 1), key = "E5"), sg.Combo(unit_list, size = (5, 1), default_value='ppbv', key = "unit_E5")],
            [sg.Text("O3",       size = (11, 1)), sg.In(size = (8, 1), key = "E6"), sg.Combo(unit_list, size = (5, 1), default_value='ppbv', key = "unit_E6")],
            [sg.Text("H2O2",     size = (11, 1)), sg.In(size = (8, 1), key = "E7"), sg.Combo(unit_list, size = (5, 1), default_value='ppbv', key = "unit_E7")],
            [sg.Text("NO",       size = (11, 1)), sg.In(size = (8, 1), key = "E8"), sg.Combo(unit_list, size = (5, 1), default_value='ppbv', key = "unit_E8")],
            [sg.Text("NO2",      size = (11, 1)), sg.In(size = (8, 1), key = "E9"), sg.Combo(unit_list, size = (5, 1), default_value='ppbv', key = "unit_E9")]]
            
    col2 = [[sg.Text("NO3",      size = (11, 1)), sg.In(size = (8, 1), key = "E10"), sg.Combo(unit_list, size = (5, 1), default_value='ppmv', key = "unit_E10")], 
            [sg.Text("HNO3",     size = (11, 1)), sg.In(size = (8, 1), key = "E11"), sg.Combo(unit_list, size = (5, 1), default_value='ppmv', key = "unit_E11")],
            [sg.Text("HNO4",     size = (11, 1)), sg.In(size = (8, 1), key = "E12"), sg.Combo(unit_list, size = (5, 1), default_value='ppmv', key = "unit_E12")],
            [sg.Text("N2O5",     size = (11, 1)), sg.In(size = (8, 1), key = "E13"), sg.Combo(unit_list, size = (5, 1), default_value='ppmv', key = "unit_E13")],
            [sg.Text("HONO",     size = (11, 1)), sg.In(size = (8, 1), key = "E14"), sg.Combo(unit_list, size = (5, 1), default_value='ppmv', key = "unit_E14")],
            [sg.Text("CH4",      size = (11, 1)), sg.In(size = (8, 1), key = "E15"), sg.Combo(unit_list, size = (5, 1), default_value='ppmv', key = "unit_E15")],
            [sg.Text("CH3O2",    size = (11, 1)), sg.In(size = (8, 1), key = "E16"), sg.Combo(unit_list, size = (5, 1), default_value='ppmv', key = "unit_E16")],
            [sg.Text("CH3OOH",   size = (11, 1)), sg.In(size = (8, 1), key = "E17"), sg.Combo(unit_list, size = (5, 1), default_value='ppmv', key = "unit_E17")],
            [sg.Text("C2H6",     size = (11, 1)), sg.In(size = (8, 1), key = "E18"), sg.Combo(unit_list, size = (5, 1), default_value='ppmv', key = "unit_E18")]]
            
    col3 = [[sg.Text("C2H5O2",   size = (11, 1)), sg.In(size = (8, 1), key = "E19"), sg.Combo(unit_list, size = (5, 1), default_value='ppmv', key = "unit_E19")],
            [sg.Text("C2H5OOH",  size = (11, 1)), sg.In(size = (8, 1), key = "E20"), sg.Combo(unit_list, size = (5, 1), default_value='ppmv', key = "unit_E20")],
            [sg.Text("C3H8",     size = (11, 1)), sg.In(size = (8, 1), key = "E21"), sg.Combo(unit_list, size = (5, 1), default_value='ppmv', key = "unit_E21")],
            [sg.Text("nC3H7O2",  size = (11, 1)), sg.In(size = (8, 1), key = "E22"), sg.Combo(unit_list, size = (5, 1), default_value='ppmv', key = "unit_E22")],
            [sg.Text("iC3H7O2",  size = (11, 1)), sg.In(size = (8, 1), key = "E23"), sg.Combo(unit_list, size = (5, 1), default_value='ppmv', key = "unit_E23")],
            [sg.Text("nC3H7OH",  size = (11, 1)), sg.In(size = (8, 1), key = "E24"), sg.Combo(unit_list, size = (5, 1), default_value='ppmv', key = "unit_E24")],
            [sg.Text("iC3H7OH",  size = (11, 1)), sg.In(size = (8, 1), key = "E25"), sg.Combo(unit_list, size = (5, 1), default_value='ppmv', key = "unit_E25")],
            [sg.Text("nButane",  size = (11, 1)), sg.In(size = (8, 1), key = "E26"), sg.Combo(unit_list, size = (5, 1), default_value='ppmv', key = "unit_E26")],
            [sg.Text("iButane",  size = (11, 1)), sg.In(size = (8, 1), key = "E27"), sg.Combo(unit_list, size = (5, 1), default_value='ppmv', key = "unit_E27")]]
            
    col4 = [[sg.Text("sC4H9O2",  size = (11, 1)), sg.In(size = (8, 1), key = "E28"), sg.Combo(unit_list, size = (5, 1), default_value='ppmv', key = "unit_E28")],
            [sg.Text("nC4H9O2",  size = (11, 1)), sg.In(size = (8, 1), key = "E29"), sg.Combo(unit_list, size = (5, 1), default_value='ppmv', key = "unit_E29")],
            [sg.Text("tC4H9O2",  size = (11, 1)), sg.In(size = (8, 1), key = "E30"), sg.Combo(unit_list, size = (5, 1), default_value='ppmv', key = "unit_E30")],
            [sg.Text("iC4H9O2",  size = (11, 1)), sg.In(size = (8, 1), key = "E31"), sg.Combo(unit_list, size = (5, 1), default_value='ppmv', key = "unit_E31")],
            [sg.Text("sC4H9OH",  size = (11, 1)), sg.In(size = (8, 1), key = "E32"), sg.Combo(unit_list, size = (5, 1), default_value='ppmv', key = "unit_E32")],
            [sg.Text("nC4H9OH",  size = (11, 1)), sg.In(size = (8, 1), key = "E33"), sg.Combo(unit_list, size = (5, 1), default_value='ppmv', key = "unit_E33")],
            [sg.Text("tC4H9OH",  size = (11, 1)), sg.In(size = (8, 1), key = "E34"), sg.Combo(unit_list, size = (5, 1), default_value='ppmv', key = "unit_E34")],
            [sg.Text("iC4H9OH",  size = (11, 1)), sg.In(size = (8, 1), key = "E35"), sg.Combo(unit_list, size = (5, 1), default_value='ppmv', key = "unit_E35")],
            [sg.Text("sC4H9OOH", size = (11, 1)), sg.In(size = (8, 1), key = "E36"), sg.Combo(unit_list, size = (5, 1), default_value='ppmv', key = "unit_E36")]]
            
    col5 = [[sg.Text("nC4H9OOH", size = (11, 1)), sg.In(size = (8, 1), key = "E37"), sg.Combo(unit_list, size = (5, 1), default_value='ppmv', key = "unit_E37")],
            [sg.Text("HCHO",     size = (11, 1)), sg.In(size = (8, 1), key = "E38"), sg.Combo(unit_list, size = (5, 1), default_value='ppbv', key = "unit_E38")],
            [sg.Text("CH3CHO",   size = (11, 1)), sg.In(size = (8, 1), key = "E39"), sg.Combo(unit_list, size = (5, 1), default_value='ppmv', key = "unit_E39")],
            [sg.Text("MEK",      size = (11, 1)), sg.In(size = (8, 1), key = "E40"), sg.Combo(unit_list, size = (5, 1), default_value='ppmv', key = "unit_E40")],
            [sg.Text("Acetone",  size = (11, 1)), sg.In(size = (8, 1), key = "E41"), sg.Combo(unit_list, size = (5, 1), default_value='ppmv', key = "unit_E41")],
            [sg.Text("Propanal", size = (11, 1)), sg.In(size = (8, 1), key = "E42"), sg.Combo(unit_list, size = (5, 1), default_value='ppmv', key = "unit_E42")],
            [sg.Text("Butanal",  size = (11, 1)), sg.In(size = (8, 1), key = "E43"), sg.Combo(unit_list, size = (5, 1), default_value='ppmv', key = "unit_E43")],
            [sg.Text("iButanal", size = (11, 1)), sg.In(size = (8, 1), key = "E44"), sg.Combo(unit_list, size = (5, 1), default_value='ppmv', key = "unit_E44")],
            [sg.Text("CH3CO3",   size = (11, 1)), sg.In(size = (8, 1), key = "E45"), sg.Combo(unit_list, size = (5, 1), default_value='ppmv', key = "unit_E45")]]
            
    col6 = [[sg.Text("PAN",      size = (11, 1)), sg.In(size = (8, 1), key = "E46"), sg.Combo(unit_list, size = (5, 1), default_value='ppmv', key = "unit_E46")],
            [sg.Text("Cl",       size = (11, 1)), sg.In(size = (8, 1), key = "E47"), sg.Combo(unit_list, size = (5, 1), default_value='ppmv', key = "unit_E47")],
            [sg.Text("Cl2",      size = (11, 1)), sg.In(size = (8, 1), key = "E48"), sg.Combo(unit_list, size = (5, 1), default_value='pptv', key = "unit_E48")],
            [sg.Text("ClO",      size = (11, 1)), sg.In(size = (8, 1), key = "E49"), sg.Combo(unit_list, size = (5, 1), default_value='ppmv', key = "unit_E49")],
            [sg.Text("OClO",     size = (11, 1)), sg.In(size = (8, 1), key = "E50"), sg.Combo(unit_list, size = (5, 1), default_value='ppmv', key = "unit_E50")],
            [sg.Text("HOCl",     size = (11, 1)), sg.In(size = (8, 1), key = "E51"), sg.Combo(unit_list, size = (5, 1), default_value='ppmv', key = "unit_E51")],
            [sg.Text("HCl",      size = (11, 1)), sg.In(size = (8, 1), key = "E52"), sg.Combo(unit_list, size = (5, 1), default_value='ppmv', key = "unit_E52")],
            [sg.Text("ClNO2",    size = (11, 1)), sg.In(size = (8, 1), key = "E53"), sg.Combo(unit_list, size = (5, 1), default_value='ppmv', key = "unit_E53")],
            [sg.Text("ClNO3",    size = (11, 1)), sg.In(size = (8, 1), key = "E54"), sg.Combo(unit_list, size = (5, 1), default_value='ppqv', key = "unit_E54")]]
            
    col7 = [[sg.Text("Br",       size = (11, 1)), sg.In(size = (8, 1), key = "E55"), sg.Combo(unit_list, size = (5, 1), default_value='ppmv', key = "unit_E55")],
            [sg.Text("Br2",      size = (11, 1)), sg.In(size = (8, 1), key = "E56"), sg.Combo(unit_list, size = (5, 1), default_value='pptv', key = "unit_E56")],
            [sg.Text("BrO",      size = (11, 1)), sg.In(size = (8, 1), key = "E57"), sg.Combo(unit_list, size = (5, 1), default_value='ppmv', key = "unit_E57")],
            [sg.Text("HOBr",     size = (11, 1)), sg.In(size = (8, 1), key = "E58"), sg.Combo(unit_list, size = (5, 1), default_value='ppmv', key = "unit_E58")],
            [sg.Text("HBr",      size = (11, 1)), sg.In(size = (8, 1), key = "E59"), sg.Combo(unit_list, size = (5, 1), default_value='ppmv', key = "unit_E59")],
            [sg.Text("BrCl",     size = (11, 1)), sg.In(size = (8, 1), key = "E60"), sg.Combo(unit_list, size = (5, 1), default_value='ppmv', key = "unit_E60")],
            [sg.Text("BrONO",    size = (11, 1)), sg.In(size = (8, 1), key = "E61"), sg.Combo(unit_list, size = (5, 1), default_value='ppmv', key = "unit_E61")],
            [sg.Text("BrNO2",    size = (11, 1)), sg.In(size = (8, 1), key = "E62"), sg.Combo(unit_list, size = (5, 1), default_value='ppmv', key = "unit_E62")],
            [sg.Text("BrNO3",    size = (11, 1)), sg.In(size = (8, 1), key = "E63"), sg.Combo(unit_list, size = (5, 1), default_value='ppqv', key = "unit_E63")]]
            
#                     H2O initialization is NOT done by assigning a number
    col8 = [[sg.Text("H2O",      size = (11, 1)), sg.In(disabled = True, size = (8, 1), key = "E64"), sg.Combo(unit_list, size = (5, 1), default_value='ppmv', disabled = True, key = "unit_E64")], 
            [sg.Text("Clm_p",    size = (11, 1)), sg.In(size = (8, 1), key = "E65"), sg.Combo(unit_list, size = (5, 1), default_value='ppv', key = "unit_E65")],
            [sg.Text("Brm_p",    size = (11, 1)), sg.In(size = (8, 1), key = "E66"), sg.Combo(unit_list, size = (5, 1), default_value='ppqv', key = "unit_E66")],
            [sg.Text("O3_p",     size = (11, 1)), sg.In(size = (8, 1), key = "E67"), sg.Combo(unit_list, size = (5, 1), default_value='ppmv', key = "unit_E67")],
            [sg.Text("HOCl_p",   size = (11, 1)), sg.In(size = (8, 1), key = "E68"), sg.Combo(unit_list, size = (5, 1), default_value='ppmv', key = "unit_E68")],
            [sg.Text("Cl2_p",    size = (11, 1)), sg.In(size = (8, 1), key = "E69"), sg.Combo(unit_list, size = (5, 1), default_value='ppmv', key = "unit_E69")],
            [sg.Text("HOBr_p",   size = (11, 1)), sg.In(size = (8, 1), key = "E70"), sg.Combo(unit_list, size = (5, 1), default_value='ppmv', key = "unit_E70")],
            [sg.Text("Br2_p",    size = (11, 1)), sg.In(size = (8, 1), key = "E71"), sg.Combo(unit_list, size = (5, 1), default_value='ppmv', key = "unit_E71")],
            [sg.Text("BrCl_p",   size = (11, 1)), sg.In(size = (8, 1), key = "E72"), sg.Combo(unit_list, size = (5, 1), default_value='ppmv', key = "unit_E72")]]
      
    # =============================== Computation Mode Elements ===============================
                         
    binary_switches = [[sg.Text("Box Model Mode", size = (35, 1)), sg.Button('Off', size = (5, 1), button_color = "white on red", key = "box_model")],
                       [sg.Text("Altitude Calculation", size = (35, 1)), 
                        sg.Button('On', size = (5, 1), button_color = "white on green", key = "altitude")],
                       [sg.Text("Vertical Mix", size = (35, 1)), 
                        sg.Button('On', size = (5, 1), button_color = "white on green", key = "vertical_mix")],
                       [sg.Text("Surface Decomposition", size = (35, 1)), 
                        sg.Button('On', size = (5, 1), button_color = "white on green", key = "decomposition")],
                       [sg.Text("Gas Reactions", size = (35, 1)), sg.Button('On', size = (5, 1), button_color = "white on green", key = "gas")],
                       [sg.Text("Het Reactions", size = (35, 1)), sg.Button('On', size = (5, 1), button_color = "white on green", key = "het")],
                       [sg.Text("Aq Reactions", size = (35, 1)), sg.Button('On', size = (5, 1), button_color = "white on green", key = "aq")],
                       [sg.Text("Temperature Calculation", size = (35, 1)), 
                        sg.Button('Off', size = (5, 1), button_color = "white on red", key = "temp"), 
                        sg.Button('?', size = (1, 1), key = "temp_info")],
                       [sg.Text("Mono Dis Het", size = (35, 1)), 
                        sg.Button('Off', size = (5, 1), button_color = "white on red", key = "dis_het"), 
                        sg.Button('?', size = (1, 1), key = "dis_het_info")],
                       [sg.Text("Mono Dis Aq", size = (35, 1)), 
                        sg.Button('Off', size = (5, 1), button_color = "white on red", key = "dis_aq"), 
                        sg.Button('?', size = (1, 1), key = "dis_aq_info")],
                       [sg.Text("LWC_v_v", size = (35, 1)), 
                        sg.Button('Off', size = (5, 1), button_color = "white on red", key = "lwc"), 
                        sg.Button('?', size = (1, 1), key = "lwc_info")]]

    numerical_values = [[sg.Text("Output Folder", size = (25, 1)),
                         sg.In(size = (13, 1), enable_events = True, key = "-FOLDER-"),
                         sg.FolderBrowse(),],
                        [sg.Text("Name of NetCDF Output File", size = (25, 1)), sg.In("Output", size = (13, 1), key = "name")],
                        [sg.Text("Generate Other Formats", size = (25, 1)), 
                         sg.Checkbox('CSV (.csv)', default=False, key = "CSV"), 
                         sg.Checkbox('Text (.txt)', default=False, key = "TXT")],
                        [sg.Text("Running Time", size = (25, 1)), sg.In(size = (5, 1), key = "running_time")],
                        [sg.Text("pH", size = (25, 1)), sg.In("4", size = (3, 1), key = "pH")],
                        [sg.Text("rp_um", size = (25, 1)), sg.In("0.2", size = (3, 1), key = "rp_um")]]
    
    #initial_values = [[sg.Button("Configure Initial Values", key = "init")]]
    initial_values = [[sg.Column(col1, key = "col1"),
                       sg.Column(col2, visible = False, key = "col2"),
                       sg.Column(col3, visible = False, key = "col3"),
                       sg.Column(col4, visible = False, key = "col4"),
                       sg.Column(col5, visible = False, key = "col5"),
                       sg.Column(col6, visible = False, key = "col6"),
                       sg.Column(col7, visible = False, key = "col7"),
                       sg.Column(col8, visible = False, key = "col8")],
                      [sg.Button("<", key = "previous_page"), sg.Button(">", key = "next_page")]]
    
    date_location = [[sg.Text("Year", size = (35, 1)), sg.In("2012", size = (8, 1), key = "DL1")],
                     [sg.Text("Month", size = (35, 1)), sg.In("3", size = (8, 1), key = "DL2")],
                     [sg.Text("Day", size = (35, 1)), sg.In("24", size = (8, 1), key = "DL3")],
                     [sg.Text("Latitude", size = (35, 1)), sg.In("71.2906", size = (8, 1), key = "DL4")],
                     [sg.Text("Longitude", size = (35, 1)), sg.In("156.7886", size = (8, 1), key = "DL5")],
                     [sg.Text("STD Longitude", size = (35, 1)), 
                      sg.In("156.7886", size = (8, 1), key = "DL6"), 
                      sg.Button('?', size = (1, 1), key = "STDLong_info")]]
    
    # =============================== Conversion Mode Elements ===============================
    
    convert_func = [[sg.Text("Input Location"), sg.In(size = (25, 1), enable_events = True, key = "-INNETCDF-"), sg.FolderBrowse(),],
                    [sg.Listbox(values=[], enable_events = True, size = (50, 18), key = "-NETCDF LIST-")],
                    [sg.Text("Output Location"), sg.In(size = (25, 1), key = "-OUTLOCATION-"), sg.FolderBrowse(),],
                    [sg.Text("Select Formats"), 
                     sg.Checkbox('CSV (.csv)', default=False, key = "TOCSV"), 
                     sg.Checkbox('Text (.txt)', default=False, key = "TOTXT")]]
    
    # =============================== Plot Mode Elements ===============================
    
    file_places = [[sg.Text("Input Location"), sg.In(size = (25, 1), enable_events = True, key = "-INFILE-"), sg.FolderBrowse(),],
                   [sg.Listbox(values=[], enable_events = True, size = (50, 18), key = "-FILE LIST-")]]
    
    line_plot = [[sg.Text("Specie", size = (18, 1)), sg.Combo(specie_list, size = (15, 1), default_value='O1D', key = "line_specie")],
                 [sg.Text("Height: 0.1m", size = (18, 1), key = "height_display"), 
                  sg.Slider(range=(1, 248), 
                  resolution = 1, 
                  orientation ='horizontal', 
                  disable_number_display = True, 
                  enable_events = True, 
                  key='line_height')]]
    
    contourf_plot = [[sg.Text("Specie", size = (18, 1)), 
                      sg.Combo(specie_list, size = (15, 1), 
                      default_value='O1D', 
                      key = "contourf_specie")],
                      [sg.Text("Smoothness: 5", size = (18, 1), key = "smooth"), 
                       sg.Slider(range=(5, 100), 
                       resolution = 5, 
                       orientation ='horizontal', 
                       disable_number_display = True, 
                       enable_events = True, 
                       key='contourf_level'),
                       sg.Button('?', size = (1, 1), key = "contourf_info")]]
    
    # =============================== Sub Menu Layouts ===============================
    
    no_task = [[sg.VPush()],
               [sg.Text("No active task", size = (23, 1))],
               [sg.VPush()]]
    
    progression = [[sg.VPush()],
                   [sg.Text("Computation Progress:", size = (23, 1)), sg.Text("0%", key = "progper"), 
                    sg.ProgressBar(50, orientation = 'horizontal', size = (44, 15), border_width = 2, key = "progbar")],
                   [sg.VPush()]]
    
    csv_prog = [[sg.VPush()],
                [sg.Text("CSV conversion progress:", size = (23, 1)), sg.Text("0%", key = "csvper"),
                 sg.ProgressBar(50, orientation = 'horizontal', size = (44, 15), border_width = 2, key = "csvbar")],
                [sg.VPush()]]
                
    txt_prog = [[sg.VPush()],
                [sg.Text("Text conversion progress:", size = (23, 1)), sg.Text("0%", key = "txtper"),
                 sg.ProgressBar(50, orientation = 'horizontal', size = (44, 15), border_width = 2, key = "txtbar")],
                [sg.VPush()]]
    
    plot_button = [[sg.VPush()],
                   [sg.Button("Select File", size = (15, 1), key = "file_in")],
                   [sg.Button("Line Plot", size = (15, 1), disabled = True, key = "Line_Plot")],
                   [sg.Button("Contourf Plot", size = (15, 1), disabled = True, key = "Contourf_Plot")],
                   [sg.Button("Plot", size = (15, 1), disabled = True, key = "show")],
                   [sg.VPush()]]
    
    convert_button = [[sg.VPush()],
                      [sg.Button("Convert", size = (15, 1), disabled = True, key = "convert")],
                      [sg.VPush()]]
    
    compute_button = [[sg.VPush()],
                      [sg.Button("Binary Switch", size = (15, 1), key = "binary_switch")],
                      [sg.Button("Numerical Input", size = (15, 1), key = "numerical_input")],
                      [sg.Button("Initial Value", size = (15, 1), key = "initial_val")],
                      [sg.Button("Date & Location", size = (15, 1), key = "D&L")],
                      [sg.Button("Execute", size = (15, 1), key = "run")],
                      [sg.VPush()]]

    # =============================== Main Layouts ===============================
    
    plot_mode_layout = [[sg.VPush()],
                        [sg.Text("Plot Mode Menu", font = ("Arial", 14))],
                        [sg.HorizontalSeparator(color = "black")],
                        [sg.Column(plot_button, size = (150, 435)),
                         sg.VSeparator(color = "black"),
                         sg.Column(file_places, size = (470, 435), pad = ((0, 0),(10, 0)), visible = True, key = "-FML-"),
                         sg.Column(line_plot, size = (470, 435), pad = ((0, 0),(10, 0)), visible = False, key = "-LS-"),
                         sg.Column(contourf_plot, size = (470, 435), pad = ((0, 0),(10, 0)), visible = False, key = "-CS-")],
                        [sg.VPush()]]
    
    conversion_mode_layout = [[sg.VPush()],
                              [sg.Text("Conversion Mode Menu", font = ("Arial", 14))],
                              [sg.HorizontalSeparator(color = "black")],
                              [sg.Column(convert_button, size = (150, 435)),
                               sg.VSeparator(color = "black"),
                               sg.Column(convert_func, size = (470, 435), pad = ((0, 0),(10, 0)))],
                              [sg.VPush()]]
                                 
    computation_mode_layout = [[sg.VPush()],
                               [sg.Text("Computation Mode Menu", font = ("Arial", 14))],
                               [sg.HorizontalSeparator(color = "black")],
                               [sg.Column(compute_button, size = (150, 435)),
                                sg.VSeparator(color = "black"),
                                sg.Column(binary_switches, size = (470, 435), pad = ((0, 0),(10, 0)), visible = True, key = "binary_face"),
                                sg.Column(numerical_values, size = (470, 435), pad = ((0, 0),(10, 0)), visible = False, key = "numerical_face"),
                                sg.Column(initial_values, size = (470, 435), pad = ((0, 0),(10, 0)), visible = False, key = "initial_face"),
                                sg.Column(date_location, size = (470, 435), pad = ((0, 0),(10, 0)), visible = False, key = "date_loc_face")],
                               [sg.VPush()]]
    
    main_layout = [[sg.Text("Main Menu", font = ("Arial", 15))],
                   [sg.Button("Computation Mode", size = (15, 2), key = "Compute")],
                   [sg.Button("Conversion Mode", size = (15, 2), key = "Convert")],
                   [sg.Button("Plot Mode", size = (15, 2), key = "Plot")],
                   [sg.Exit(size = (15, 2))]]
                   
    layout = [[sg.VPush()],
              [sg.Text("ATmospheric Model - One-dimensional", font = ("Arial", 20))],
              [sg.Text("Version 1.3"),],
              [sg.HorizontalSeparator(color = "black")],
              [sg.Column(main_layout, size = (150, 490), element_justification = "center", key = "-ML-"),
               sg.VSeparator(color = "black"),
               sg.Column(computation_mode_layout, size = (620, 490), visible = True, element_justification = "left", key = "-CML-"),
               sg.Column(plot_mode_layout, size = (620, 490), visible = False, element_justification = "left", key = "-PML-"),
               sg.Column(conversion_mode_layout, size = (620, 490), visible = False, element_justification = "left", key = "-OML-"),],
              [sg.HorizontalSeparator(color = "black")],
              [sg.Column(no_task, size = (770, 40), visible = True, element_justification = "center", key = "no_task"),
               sg.Column(progression, size = (770, 40), visible = False, element_justification = "center", key = "prog_row"),
               sg.Column(csv_prog, size = (770, 40), visible = False, element_justification = "center", key = "-CSV-"), 
               sg.Column(txt_prog, size = (770, 40), visible = False, element_justification = "center", key = "-TEXT-")],
              [sg.VPush()],]
              
    window = sg.Window("ATMO", layout, 
                       size = (770, 665), 
                       resizable = False, 
                       enable_close_attempted_event = True, 
                       element_justification = "center").finalize()
    
    # =============================== Local Variables ===============================
    
    # Values for buttons in Computation Mode 
    box_model = True
    altitude  = True
    vmix      = True
    decomp    = True
    gas       = True
    het       = True
    aq        = True
    height    = True
    temp      = True
    dis_het   = True
    dis_aq    = True
    lwc       = True
        
    # Values for buttons to change plot type
    line     = False
    contourf = False
    
    # Create plot object
    plt = Plot.Plot()
    
    # Input File Name Holder
    filename   = ""
    netcdfname = ""
    file_selected = False
    
    # Initial value page tracker
    page_tracker = 1
    
    # Load initial values
    for i in range(len(specie_list) - 1):
        window[f'E{i + 1}'].update(init_val[i])
        
    # =============================== Run the Event Loop ===============================
    
    while True:
    
        event, values = window.read()
    
        # =============================== Main Menu Functions ===============================
    
        if ((event == "Exit" or event == sg.WINDOW_CLOSE_ATTEMPTED_EVENT) and 
             sg.PopupOKCancel('Are you sure to exit the program?', title = "Exit")) == "OK":
            # Quit program
            break
            
        elif event == "Compute":
            # Switch Layout
            window['-OML-'].update(visible = False)
            window['-FML-'].update(visible = False)
            window['-PML-'].update(visible = False)
            window['-LS-'].update(visible = False)
            window['-CS-'].update(visible = False)
            window['-CML-'].update(visible = True)
        
        elif event == "Convert":
            # Switch Layout
            window['-CML-'].update(visible = False)
            window['-FML-'].update(visible = False)
            window['-PML-'].update(visible = False)
            window['-LS-'].update(visible = False)
            window['-CS-'].update(visible = False)
            window['-OML-'].update(visible = True)
        
        elif event == "Plot":
            # Switch Layout
            window['-OML-'].update(visible = False)
            window['-CML-'].update(visible = False)
            window['-LS-'].update(visible = False)
            window['-CS-'].update(visible = False)
            window['-FML-'].update(visible = True)
            window['-PML-'].update(visible = True)
            
        # =============================== Computation Mode Functions ===============================

        # Switch sub-layouts

        elif event == "binary_switch":
            window["binary_face"].update(visible = True)
            window["numerical_face"].update(visible = False)
            window["initial_face"].update(visible = False)
            window["date_loc_face"].update(visible = False)
        
        elif event == "numerical_input":
            window["binary_face"].update(visible = False)
            window["numerical_face"].update(visible = True)
            window["initial_face"].update(visible = False)
            window["date_loc_face"].update(visible = False)
            
        elif event == "initial_val":
            window["binary_face"].update(visible = False)
            window["numerical_face"].update(visible = False)
            window["initial_face"].update(visible = True)
            window["date_loc_face"].update(visible = False)
        
        elif event == "D&L":
            window["binary_face"].update(visible = False)
            window["numerical_face"].update(visible = False)
            window["initial_face"].update(visible = False)
            window["date_loc_face"].update(visible = True)

        # Run computation
        elif event == "run":
            # Check if no output location is selected
            if values['-FOLDER-'] == "":
                sg.popup("Output location cannot be empty!", title = "Error")
                        
            else:    
                try:
                    # Check if inputs are numbers
                    init_value = []
                    
                    for i in range(len(specie_list) - 1):
                      if init_val[i] != float(values[f'E{i + 1}']):
                        init_val[i] = float(values[f'E{i + 1}']) # Assign configured initial values
                        
                      if values[f'unit_E{i + 1}'] == 'ppmv' or values[f'unit_E{i + 1}'] == 'mg/m3':
                        init_value.append(float(values[f'E{i + 1}']) * 1e-6)
                      
                      elif values[f'unit_E{i + 1}'] == 'ppbv' or values[f'unit_E{i + 1}'] == 'µg/m3':
                        init_value.append(float(values[f'E{i + 1}']) * 1e-9)
                    
                      elif values[f'unit_E{i + 1}'] == 'pptv':
                        init_value.append(float(values[f'E{i + 1}']) * 1e-12)
                        
                      elif values[f'unit_E{i + 1}'] == 'ppqv':
                        init_value.append(float(values[f'E{i + 1}']) * 1e-15)
                        
                      elif values[f'unit_E{i + 1}'] == 'ppv':
                        init_value.append(float(values[f'E{i + 1}']) * 1)
                        
                    v_1 = int(values['running_time'])
                    v_2 = float(values['pH'])
                    v_3 = float(values['rp_um'])
                    
                    # Check if date and location are in correct format   
                    Date = re.split('-', re.split('\s+', str(datetime.datetime(int(values['DL1']), int(values['DL2']), int(values['DL3']))))[0])
                    values['DL1'] = Date[0]
                    values['DL2'] = Date[1]
                    values['DL3'] = Date[2]
                    
                    # Check if inputs are negative
                    if v_1 < 0 or v_2 < 0 or v_3 < 0:
                        sg.popup("Some values cannot be negative!", title = "Error")
                    
                    # Check if latitude is valid
                    elif abs(float(values['DL4'])) > 90:
                        sg.popup("Invalid Latitude!", title = "Error")
                
                    # Check if longitude is valid
                    elif abs(float(values['DL5'])) > 180:
                        sg.popup("Invalid Longitutde!", title = "Error")
             
                    # Check if STD longitude is valid
                    elif abs(float(values['DL6'])) > 180:
                        sg.popup("Invalid STD Longitutde!", title = "Error")
                            
                    else: 
                        DL_value  = [0] * 6
                    
                        for i in range(6):
                            if DL_value[i] != float(values[f'DL{i + 1}']):
                                DL_value[i] = float(values[f'DL{i + 1}']) # Assign configured initial values
                        
                        # Open Confirmation Window
                        if confirmation_window(values['-FOLDER-'],
                                               values['name'],
                                               values['CSV'], values['TXT'],
                                               window.Element("box_model").get_text(),
                                               window.Element("altitude").get_text(),
                                               window.Element("vertical_mix").get_text(),
                                               window.Element("decomposition").get_text(),
                                               window.Element("gas").get_text(),
                                               window.Element("het").get_text(),
                                               window.Element("aq").get_text(),
                                               window.Element("temp").get_text(),
                                               window.Element("dis_het").get_text(),
                                               window.Element("dis_aq").get_text(),
                                               window.Element("lwc").get_text(),
                                               v_1, v_2, v_3):
                                                                          
                            try:
                                max_val = 0 # Reset max value
                                
                                window["progper"].update(str(max_val) + "%") # Reset progress percentage
                                window["progbar"].update(max = max_val, current_count = 0) # Reset progress bar
                                
                                window["no_task"].update(visible = False)
                                window["prog_row"].update(visible = True) # Show progress bar
                                
                                print(init_value)
                                
                                # Run CLI Program
                                for i in (Main.Computation.compute(values['-FOLDER-'],
                                                                   values['name'],
                                                                   window.Element("box_model").get_text(),
                                                                   window.Element("altitude").get_text(),
                                                                   window.Element("vertical_mix").get_text(),
                                                                   window.Element("decomposition").get_text(),
                                                                   window.Element("gas").get_text(),
                                                                   window.Element("het").get_text(),
                                                                   window.Element("aq").get_text(),
                                                                   window.Element("temp").get_text(),
                                                                   window.Element("dis_het").get_text(),
                                                                   window.Element("dis_aq").get_text(),
                                                                   window.Element("lwc").get_text(),
                                                                   v_1, v_2, v_3, init_value, DL_value)):
                
                                    event, values = window.read(10)
                
                                    # Get maximum value
                                    if max_val == 0:
                                        max_val = i
                                        window["progbar"].update(max = max_val, current_count = 0)
                        
                                    # Update Progression Bar
                                    else:
                                        window["progper"].update(str(int(i/max_val*100)) + "%")
                                        window["progbar"].update(max = max_val, current_count = i)
            
                                # Conversion
                                if values['CSV']:
                                    Convert.Convert.To_CSV(os.path.join(values['-FOLDER-'], values['name'] + ".nc"), values['-FOLDER-'], specie_list)
                
                                if values['TXT']:
                                    Convert.Convert.To_Text(os.path.join(values['-FOLDER-'], values['name'] + ".nc"), values['-FOLDER-'], specie_list)
            
                                window["prog_row"].update(visible = False)
                                window["no_task"].update(visible = True) # Hide progress bar
            
                            except Exception as e: 
                                sg.popup(e, title = "Error")
                                                
                except Exception as e: 
                        if "day" in str(e):
                            sg.popup("Day is out of range for month!", title = "Error")
                    
                        elif "month" in str(e):
                            sg.popup("Month is out of range!", title = "Error")
                        
                        elif "year" in str(e):
                            sg.popup("Year is out of range!", title = "Error")
                            
                        else:
                            sg.popup("Values should be numbers!", title = "Error")
        
        # Toggle Binary Switches
        elif event == "box_model":
            box_model = not box_model
            window.Element("box_model").Update(("On", "Off")[box_model], button_color = (("white", ("green", "red")[box_model])))
            
        elif event == "altitude":
            altitude = not altitude
            window.Element("altitude").Update(("Off", "On")[altitude], button_color = (("white", ("red", "green")[altitude])))
            
        elif event == "vertical_mix":
            vmix = not vmix
            window.Element("vertical_mix").Update(("Off", "On")[vmix], button_color = (("white", ("red", "green")[vmix])))
            
        elif event == "decomposition":
            decomp = not decomp
            window.Element("decomposition").Update(("Off", "On")[decomp], button_color = (("white", ("red", "green")[decomp])))

        elif event == "gas":
            gas = not gas
            window.Element("gas").Update(("Off", "On")[gas], button_color = (("white", ("red", "green")[gas])))

        elif event == "het":
            het = not het
            window.Element("het").Update(("Off", "On")[het], button_color = (("white", ("red", "green")[het])))

        elif event == "aq":
            aq = not aq
            window.Element("aq").Update(("Off", "On")[aq], button_color = (("white", ("red", "green")[aq])))
            
        elif event == "temp":
            temp = not temp
            window.Element("temp").Update(("On", "Off")[temp], button_color = (("white", ("green", "red")[temp])))
            
        elif event == "dis_het":
            dis_het = not dis_het
            window.Element("dis_het").Update(("On", "Off")[dis_het], button_color = (("white", ("green", "red")[dis_het])))
            
        elif event == "dis_aq":
            dis_aq = not dis_aq
            window.Element("dis_aq").Update(("On", "Off")[dis_aq], button_color = (("white", ("green", "red")[dis_aq])))
            
        elif event == "lwc":
            lwc = not lwc
            window.Element("lwc").Update(("On", "Off")[lwc], button_color = (("white", ("green", "red")[lwc])))
        
        # Information for some switches
        elif event == "temp_info":
            sg.popup(("Determine if temperature calculation is done by using a function. "
                      "Default (Off) means temperature is the same across all heights."), title = "Temperature Calculation")
            
        elif event == "dis_het_info":
            sg.popup(("Determine if SA_um2_cm3 calculation is done by using a function. "
                      "Default (Off) means calculation is done using a function. "
                      "On means SA_um2_cm3 is set to 10."), title = "Mono Dis Het")
            
        elif event == "dis_aq_info":
            sg.popup("Set to On for monodispersed hypothesized aerosol size distribution. Default is Off.", title = "Mono Dis Aq")
            
        elif event == "lwc_info":
            sg.popup(("Determine if LWC_v_v calculation is done by using a function. "
                      "Default (Off) means calculation is done using a function. "
                      "On means LWC_v_v is set to 1e-13."), title = "LWC_v_v")
                      
        elif event == "STDLong_info":
            sg.popup("STD Longtitude is 75 plus 15 for daylight saving time", title = "STD Longtitude")
        
        # Open initial value configuration window
        #elif event == "init":
        #    initial_value()
        elif event == "previous_page":
           if page_tracker == 1:
             pass
           
           else:
             window[f'col{page_tracker}'].update(visible = False)
             window[f'col{page_tracker - 1}'].update(visible = True)
             page_tracker = page_tracker - 1
              
        elif event == "next_page":
           if page_tracker == 8:
             pass
           
           else:
             window[f'col{page_tracker}'].update(visible = False)
             window[f'col{page_tracker + 1}'].update(visible = True)
             page_tracker = page_tracker + 1 
                
        # =============================== Conversion Mode Functions ===============================
                    
        elif event == "-INNETCDF-":
            # Select folder where input file is located
            folder = values["-INNETCDF-"]
            
            try:
                # Get list of files in folder
                file_list = os.listdir(folder)
            except FileNotFoundError:
                file_list = []
            
            fnames = [f for f in file_list if os.path.isfile(os.path.join(folder, f)) and f.lower().endswith((".nc"))] # Put pathes of all netCDF files in a list
            fnames.sort(key=str.lower) # Sort list alphabetically
            window["-NETCDF LIST-"].update(fnames) # Show avaiable input files
        
        elif event == "-NETCDF LIST-":
            # Select input file
            try:
                netcdfname = os.path.join(values["-INNETCDF-"], values["-NETCDF LIST-"][0]) # Update input file path
                window['convert'].update(disabled = False) # Enable convert button
                            
            except:
                pass 
                
        elif event == "convert":
            # Check if output location is selected
            if values["-OUTLOCATION-"] == "":
                sg.popup("Output location cannot be empty!", title = "Error")
            
            # No formats are selected
            elif not values['TOCSV'] and not values['TOTXT']:
                sg.popup("No formats are selected!", title = "Error")
            
            else:
                max_val = 0 # Reset max value
                
                window["txtper"].update(str(max_val) + "%") # Reset progress percentage
                window["txtbar"].update(max = max_val, current_count = 0) # Reset progress bar
                window["csvper"].update(str(max_val) + "%") # Reset progress percentage
                window["csvbar"].update(max = max_val, current_count = 0) # Reset progress bar
                
                window["no_task"].update(visible = False)
                
                # Switch Layout
                if values['TOTXT'] == True and values['TOCSV'] == False:
                    window['-CSV-'].update(visible = False)
                    window['-TEXT-'].update(visible = True)
            
                else:
                    window['-CSV-'].update(visible = True)
                    window['-TEXT-'].update(visible = False)
             
                # Run Conversion
                if values['TOCSV'] == values['TOTXT']:
                    try:    
                        # Convert to csv
                        for i in (Convert.Convert.To_CSV(netcdfname, values["-OUTLOCATION-"], specie_list)):
                            event, values = window.read(10)
                    
                            # Get maximum value
                            if max_val == 0:
                                max_val = i
                                window["csvbar"].update(max = max_val, current_count = 0)
                        
                            # Update Progression Bar
                            else:
                                window["csvper"].update(str(int(i/max_val*100)) + "%")
                                window["csvbar"].update(max = max_val, current_count = i)
                
                        # Switch layout
                        window['-CSV-'].update(visible = False)
                        window['-TEXT-'].update(visible = True)
                     
                        max_val = 0 # Reset max value
                
                        # Convert to txt
                        for i in (Convert.Convert.To_Text(netcdfname, values["-OUTLOCATION-"], specie_list)):
                            event, values = window.read(10)
                
                            # Get maximum value
                            if max_val == 0:
                                max_val = i
                                window["txtbar"].update(max = max_val, current_count = 0)
                        
                            # Update Progression Bar
                            else:
                                window["txtper"].update(str(int(i/max_val*100)) + "%")
                                window["txtbar"].update(max = max_val, current_count = i)
                        
                    except Exception as e: 
                        print(e)
                    
                    # Hide CSV and Text progress bars
                    window['-CSV-'].update(visible = False)
                    window['-TEXT-'].update(visible = False)
        
                else:
                    # Run Conversion
                    try:
                        if values['TOCSV'] == True:
                            for i in (Convert.Convert.To_CSV(netcdfname, values["-OUTLOCATION-"], specie_list)):
                                event, values = window.read(10)
                    
                                # Get maximum value
                                if max_val == 0:
                                    max_val = i
                                    window["csvbar"].update(max = max_val, current_count = 0)
                        
                                # Update Progression Bar
                                else:
                                    window["csvper"].update(str(int(i/max_val*100)) + "%")
                                    window["csvbar"].update(max = max_val, current_count = i)
                
                        if values['TOTXT'] == True:
                            for i in (Convert.Convert.To_Text(netcdfname, values["-OUTLOCATION-"], specie_list)):
                                event, values = window.read(10)
                
                                # Get maximum value
                                if max_val == 0:
                                    max_val = i
                                    window["txtbar"].update(max = max_val, current_count = 0)
                        
                                # Update Progression Bar
                                else:
                                    window["txtper"].update(str(int(i/max_val*100)) + "%")
                                    window["txtbar"].update(max = max_val, current_count = i)
                            
                    except Exception as e: 
                        print(e)
                    
                    # Hide CSV and Text progress bars
                    window['-CSV-'].update(visible = False)
                    window['-TEXT-'].update(visible = False)
            
                # Hide CSV and Text progress bars
                window["no_task"].update(visible = True)
        
        # =============================== Plot Mode Functions ===============================
        
        elif event == "file_in":
            # Switch Layout
            window['-OML-'].update(visible = False)
            window['-CML-'].update(visible = False)
            window['-LS-'].update(visible = False)
            window['-CS-'].update(visible = False)
            window['-PML-'].update(visible = True)
            window['-FML-'].update(visible = True)
                    
        elif event == "-INFILE-":
            # Select folder where input file is located
            folder = values["-INFILE-"]
            
            try:
                # Get list of files in folder
                file_list = os.listdir(folder)
            except FileNotFoundError:
                file_list = []
            
            fnames = [f for f in file_list if os.path.isfile(os.path.join(folder, f)) and f.lower().endswith((".nc", ".txt", ".csv"))] # Put pathes of all netCDF, text and CSV files in a list
            fnames.sort(key=str.lower) # Sort list alphabetically
            window["-FILE LIST-"].update(fnames) # Show avaiable input files
        
        elif event == "-FILE LIST-":
            # Select input file
            try:
                filename = os.path.join(values["-INFILE-"], values["-FILE LIST-"][0]) # Update input file path
                file_selected = True
                
                # Check filetype and update content
                if os.path.splitext(filename)[1] != ".nc":
                    window['line_specie'].update(disabled = True)
                    window['contourf_specie'].update(disabled = True)
                
                else:
                    window['line_specie'].update(disabled = False)
                    window['contourf_specie'].update(disabled = False)
                            
            except:
                pass
                
            if file_selected:
                # Unlock functions
                window['Line_Plot'].update(disabled = False)
                window['Contourf_Plot'].update(disabled = False)
                window["show"].update(disabled = False)
        
        elif event == 'Line_Plot':
            # Switch Layout
            window['-OML-'].update(visible = False)
            window['-CML-'].update(visible = False)
            window['-FML-'].update(visible = False)
            window['-CS-'].update(visible = False)
            window['-PML-'].update(visible = True)
            window['-LS-'].update(visible = True)
            
            line = True
            contourf = False
        
        elif event == 'Contourf_Plot':
            # Switch Layout
            window['-OML-'].update(visible = False)
            window['-CML-'].update(visible = False)
            window['-FML-'].update(visible = False)
            window['-LS-'].update(visible = False)
            window['-PML-'].update(visible = True)
            window['-CS-'].update(visible = True)
            
            line = False
            contourf = True
        
        elif event == "line_height":
            # Display height
            window['height_display'].update("Height: " + str(z[int(values["line_height"] - 1)]) + "m")
        
        elif event == "contourf_level":
            # Display contourf level
            window["smooth"].update("Smoothness: " + str(int(values["contourf_level"])))
        
        elif event == "show":
            # Display Plots
            
            # Show line plot
            if line == True:
                
                # If input file is an netCDF file
                if os.path.splitext(filename)[1] == ".nc":
                    plt.Line_NC(z, filename, specie_list.index(values['line_specie']), values['line_specie'], values['line_height'] - 1)
                    
                # If input file is not an netCDF file
                else:
                    plt.Line(z, filename, values['line_height'] - 1)
            
            # Show contour plot                    
            elif contourf == True:
                
                # If input file is an netCDF file
                if os.path.splitext(filename)[1] == ".nc":
                    plt.Contourf_NC(filename, specie_list.index(values['contourf_specie']), values['contourf_specie'], int(values["contourf_level"]))
                    
                # If input file is not an netCDF file
                else:
                    plt.Contourf(z, filename, int(values["contourf_level"]))
        
        # Information for some switches
        elif event == "contourf_info":
            sg.popup("Determine how smooth the plot will be.", title = "Smoothness")
    
        # =============================== Mode Functions End ===============================
        
    # Close Window
    window.close()

# ====================================================================================================================================================

if __name__ == "__main__":
    main()

