
# ATmopheric Model One-dimentional - KPP Conversion (ATMO\_KPP)

## 1. Introduction

**ATMO_KPP** is a one-dimensional model used to calculate concentrations of chemical species over the atmosphere. 
This model is translated from a Fortran one-dimensional model designed by Toyota, K. et al.

## 2. Features

In addition to all original features, this Python conversion adds a GUI with built-in format conversion and 
plotting functions.

## 3. Required Libraries

ATMO\_KPP requires the following packages

    python3-tk
    numpy
    netcdf4
    pandas
    xarray
    matplotlib

## 4. Guided Example

### Prerequest: 
1. Install Python3.
2. Download and install all required libraries listed under point 3 on this Github page. 
3. Download all .py files on the Github page by clicking Code -> Download ZIP. For Windows 64-bit users, a .zip file containing the .exe version of the program can be found under the Release page. 
4. Unzip all files into the same folder. 

### Running the program in GUI mode:
Open Terminal / Command Prompt and type `python3 GUI.py` / `python GUI.py` for Linux and Windows respectively. The default page will be computation mode - binary switch page.

#### Computation Mode
1. Click the button to the right of "Box Model Mode" to make the program running in one-dimensional space.
2. Click the "Numerical Input" button.
3. Click "Browse" to select a directory / folder for storing the output file.
4. Type "1" into the textbox to the right of "Running Time". This means the program will calculate the concentration changes in species over 1 day / 24 hours.
5. Click "Execute", then click "Confirm" to start calculation.
6. The calculation progress is tracked by a progress bar at the bottom of the GUI. Once the program is done running, the output file will appear in the selected folder.

#### Conversion Mode
1. Click the "Conversion Mode" button.
2. Click the "Browse" to the right of "Input Location" to select a directory / folder where a NetCDF file is stored.
3. Click a file that appeared on the listbox below "Input Location".
4. Click the "Browse" to the right of "Output Location" to select a directory / folder where the converted files will be stored.
5. Click the checkbox next to CSV(.csv) to select CSV format.
6. Click the "Convert" button to start the conversion process.
7. The conversion progress is tracked by a progress bar at the bottom of the GUI. Once the program is done running, the output files will appear in the selected output folder.

#### Plot Mode
1. Click the "Plot Mode" button.
2. Click the "Browse" to the right of "Input Location" to select a directory / folder where a NetCDF file is stored.
3. Click a file that appeared on the listbox below "Input Location".
4. Click "Contourf Plot" button to plot contourf plot.
5. Select a specie using the drop down list.
6. Click "Plot" to generate a plot.

#### Change initial concentration of species (only affects computation)
1. Click the "Computation Mode" button.
2. Click the "Initial Value" button.
3. Find the to-be-changed specie using the arrow buttons.
4. Once the specie is found, type the desired value into the textbox to the right of the specie name.
5. Select the appropriate unit for the new value using the drop down list.

#### Change the location (only affects computation)
1. Click the "Computation Mode" button.
2. Click the "Date & Location" button.
3. Type the desired latitude, longitude, and STD longitude into appropriate textboxes.

#### Change the date (only affects computation)
1. Click the "Computation Mode" button.
2. Click the "Date & Location" button.
3. Type the desired year, month, and day into appropriate textboxes.

### Running the program in CLI mode:
Open Terminal / Command Prompt and type `python3 Main.py` / `python Main.py` for Linux and Windows respectively. The program only performs calculation under CLI mode.

#### Change parameters under CLI model
All parameters can be found in `Main.py` between line line 286 and 305. Under CLI mode, the unit for all initial concentrations is ppv. Therefore, unit conversion rate needs to be applied to each concentration manually (e.g. 1e-12 ppv = 1 ppbv).

## 5. Contributors

Thanks to the contributors, all of them are from Penn State University
    
    Tianjie Chen (tvc5586@psu.edu)
    Adrien Chen (apc6225@psu.edu)
    Abu Asaduzzaman (aua1309@psu.edu)
    Jose D. Fuentes (jul15@psu.edu)

## 6. License

MIT

## 7. Citation

Toyota, K., Dastoor, A. P., & Ryzhkov, A. (2014). Air45snowpack exchange of bromine, ozone and mercury in the springtime Arctic simulated by the 1-D model PHANTAS 45 Part 2: Mercury and its speciation. Atmospheric Chemistry and Physics, 14(8), 4135454167. https://doi.org/10.5194/acp-14-4135-2014
