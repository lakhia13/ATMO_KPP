import os
import re
import datetime
from flask import Flask, render_template, request, jsonify, send_from_directory, url_for, redirect, flash
from werkzeug.utils import secure_filename
import threading
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
from flask_bootstrap import Bootstrap

import Main
import Plot
import Convert

app = Flask(__name__)
app.secret_key = 'atmokpp_secret_key'
Bootstrap(app)

# Create required directories if they don't exist
os.makedirs(os.path.join(app.root_path, 'static'), exist_ok=True)
os.makedirs(os.path.join(app.root_path, 'static', 'plots'), exist_ok=True)
os.makedirs(os.path.join(app.root_path, 'uploads'), exist_ok=True)

# Constants and global variables
specie_list = ["O1D", "O3P", "OH", "HO2", "CO", "O3", "H2O2", "NO", "NO2", 
               "NO3", "HNO3", "HNO4", "N2O5", "HONO", "CH4", "CH3O2", "CH3OOH", "C2H6", 
               "C2H5O2", "C2H5OOH", "C3H8", "nC3H7O2", "iC3H7O2", "nC3H7OH", "iC3H7OH", "nButane", "iButane", 
               "sC4H9O2", "nC4H9O2", "tC4H9O2", "iC4H9O2", "sC4H9OH", "nC4H9OH", "tC4H9OH", "iC4H9OH", "sC4H9OOH", 
               "nC4H9OOH", "HCHO", "CH3CHO", "MEK", "Acetone", "Propanal", "Butanal", "iButanal", "CH3CO3", 
               "PAN", "Cl", "Cl2", "ClO", "OClO", "HOCl", "HCl", "ClNO2", "ClNO3", 
               "Br", "Br2", "BrO", "HOBr", "HBr", "BrCl", "BrONO", "BrNO2", "BrNO3", 
               "H2O", "Clm_p", "Brm_p", "O3_p", "HOCl_p", "Cl2_p", "HOBr_p", "Br2_p", "BrCl_p", "Kh"]

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

init_val = [0, 0, 0, 0, 160.0, 34.0, 2.0, 0.02, 0.05,
            0, 0, 0, 0, 0, 1.9, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0.3, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 10, 0, 0, 0, 0, 0, 1e-5,
            0, 20, 0, 0, 0, 0, 0, 0, 1e-5,
            0, 1, 1e-5, 0, 0, 0, 0, 0, 0]

unit_list = ['ppmv', 'ppbv', 'pptv', 'ppqv', 'ppv', 'mg/m3', 'µg/m3']

# Global variables for computation status
computation_status = {
    'running': False,
    'progress': 0,
    'total_steps': 0,
    'message': 'Ready'
}

conversion_status = {
    'running': False,
    'csv_progress': 0,
    'txt_progress': 0,
    'csv_total': 0,
    'txt_total': 0,
    'message': 'Ready'
}

# Store the selected file for plotting
selected_file = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compute')
def compute():
    return render_template('compute.html', 
                          specie_list=specie_list,
                          init_val=init_val, 
                          unit_list=unit_list)

@app.route('/convert')
def convert():
    return render_template('convert.html')

@app.route('/plot')
def plot():
    return render_template('plot.html', 
                          specie_list=specie_list, 
                          z=z)

@app.route('/api/compute_status')
def compute_status():
    return jsonify(computation_status)

@app.route('/api/conversion_status')
def conversion_status():
    return jsonify(conversion_status)

@app.route('/api/netcdf_files')
def get_netcdf_files():
    uploads_folder = os.path.join(app.root_path, 'uploads')
    files = [f for f in os.listdir(uploads_folder) if f.endswith('.nc')]
    return jsonify({'files': files})

@app.route('/api/get_specie_list')
def get_specie_list():
    return jsonify({'specie_list': specie_list})

@app.route('/api/get_height_list')
def get_height_list():
    return jsonify({'height_list': z})

def async_computation(data):
    global computation_status
    try:
        # Extract data from the request
        output_path = os.path.join(app.root_path, 'uploads')
        name = data['name']
        to_csv = data['to_csv']
        to_txt = data['to_txt']
        box_model = data['box_model']
        altitude = data['altitude']
        vmix = data['vmix']
        decomp = data['decomp']
        gas = data['gas']
        het = data['het']
        aq = data['aq']
        temp = data['temp']
        dis_het = data['dis_het']
        dis_aq = data['dis_aq']
        lwc = data['lwc']
        running_time = int(data['running_time'])
        pH = float(data['pH'])
        rp_um = float(data['rp_um'])
        
        # Parse initial values
        init_value = []
        for i in range(len(specie_list) - 1):
            species_key = f'E{i+1}'
            unit_key = f'unit_E{i+1}'
            
            if species_key in data and unit_key in data:
                value = float(data[species_key]) if data[species_key] else 0
                unit = data[unit_key]
                
                # Convert based on unit
                if unit == 'ppmv' or unit == 'mg/m3':
                    init_value.append(value * 1e-6)
                elif unit == 'ppbv' or unit == 'µg/m3':
                    init_value.append(value * 1e-9)
                elif unit == 'pptv':
                    init_value.append(value * 1e-12)
                elif unit == 'ppqv':
                    init_value.append(value * 1e-15)
                elif unit == 'ppv':
                    init_value.append(value * 1)
                else:
                    init_value.append(0)
            else:
                init_value.append(0)
        
        # Parse date and location
        year = data['DL1']
        month = data['DL2']
        day = data['DL3']
        latitude = float(data['DL4'])
        longitude = float(data['DL5'])
        std_longitude = float(data['DL6'])
        
        dl_values = [year, month, day, latitude, longitude, std_longitude]
        
        # Start computation
        computation_status['running'] = True
        computation_status['progress'] = 0
        computation_status['message'] = 'Computing...'
        
        # Run the computation
        for i in Main.Computation.compute(output_path, name, 
                                      box_model, altitude, vmix, decomp, 
                                      gas, het, aq, temp, dis_het, dis_aq, 
                                      lwc, running_time, pH, rp_um, 
                                      init_value, dl_values):
            if i == 1:
                # First iteration returns the total steps
                computation_status['total_steps'] = i
            else:
                computation_status['progress'] = i
                computation_status['message'] = f'Computing... {i}/{computation_status["total_steps"]}'
        
        # Handle conversion if requested
        if to_csv or to_txt:
            output_file = os.path.join(output_path, f"{name}.nc")
            
            if to_csv:
                threading.Thread(target=async_convert_csv, 
                               args=(output_file, output_path)).start()
            
            if to_txt:
                threading.Thread(target=async_convert_txt, 
                               args=(output_file, output_path)).start()
        
        computation_status['running'] = False
        computation_status['message'] = 'Computation completed successfully.'
        
    except Exception as e:
        computation_status['running'] = False
        computation_status['message'] = f'Error: {str(e)}'

def async_convert_csv(input_file, output_path):
    global conversion_status
    try:
        conversion_status['running'] = True
        conversion_status['csv_progress'] = 0
        conversion_status['message'] = 'Converting to CSV...'
        
        for i in Convert.Convert.To_CSV(input_file, output_path, specie_list):
            conversion_status['csv_total'] = len(specie_list) + 1
            conversion_status['csv_progress'] = i
        
        conversion_status['message'] = 'CSV conversion completed.'
        
    except Exception as e:
        conversion_status['message'] = f'CSV Conversion Error: {str(e)}'
    finally:
        conversion_status['running'] = False

def async_convert_txt(input_file, output_path):
    global conversion_status
    try:
        conversion_status['running'] = True
        conversion_status['txt_progress'] = 0
        conversion_status['message'] = 'Converting to TXT...'
        
        for i in Convert.Convert.To_Text(input_file, output_path, specie_list):
            conversion_status['txt_total'] = len(specie_list) + 1
            conversion_status['txt_progress'] = i
        
        conversion_status['message'] = 'TXT conversion completed.'
        
    except Exception as e:
        conversion_status['message'] = f'TXT Conversion Error: {str(e)}'
    finally:
        conversion_status['running'] = False

@app.route('/api/run_computation', methods=['POST'])
def run_computation():
    global computation_status
    
    if computation_status['running']:
        return jsonify({'success': False, 'message': 'Computation already running'})
    
    data = request.json
    threading.Thread(target=async_computation, args=(data,)).start()
    
    return jsonify({'success': True, 'message': 'Computation started'})

@app.route('/api/convert_file', methods=['POST'])
def convert_file():
    data = request.json
    input_file = os.path.join(app.root_path, 'uploads', data['input_file'])
    output_path = os.path.join(app.root_path, 'uploads')
    to_csv = data['to_csv']
    to_txt = data['to_txt']
    
    if to_csv:
        threading.Thread(target=async_convert_csv, args=(input_file, output_path)).start()
    
    if to_txt:
        threading.Thread(target=async_convert_txt, args=(input_file, output_path)).start()
    
    return jsonify({'success': True, 'message': 'Conversion started'})

@app.route('/api/select_file', methods=['POST'])
def select_file():
    global selected_file
    data = request.json
    selected_file = os.path.join(app.root_path, 'uploads', data['file'])
    return jsonify({'success': True, 'message': 'File selected'})

@app.route('/uploads/<path:filename>')
def download_file(filename):
    return send_from_directory(os.path.join(app.root_path, 'uploads'), filename, as_attachment=True)

def generate_plot(plot_type, specie_idx=None, specie_name=None, height=None, smoothness=None):
    global selected_file
    
    if not selected_file or not os.path.exists(selected_file):
        return None
    
    plt_obj = Plot.Plot()
    plt.figure(figsize=(10, 6))
    
    # Generate unique filename for the plot
    plot_filename = f"{plot_type}_{specie_name}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.png"
    plot_path = os.path.join(app.root_path, 'static', 'plots', plot_filename)
    
    try:
        if plot_type == 'line':
            if specie_name == 'Kh':
                plt_obj.Line_NC(z, selected_file, None, specie_name, int(height))
            else:
                plt_obj.Line_NC(z, selected_file, specie_idx, specie_name, int(height))
        elif plot_type == 'contourf':
            if specie_name == 'Kh':
                plt_obj.Contourf_NC(selected_file, None, specie_name, int(smoothness))
            else:
                plt_obj.Contourf_NC(selected_file, specie_idx, specie_name, int(smoothness))
        
        # Save the plot to a file instead of showing it
        plt.savefig(plot_path)
        plt.close()
        
        return url_for('static', filename=f'plots/{plot_filename}')
    except Exception as e:
        print(f"Error generating plot: {str(e)}")
        plt.close()
        return None

@app.route('/api/line_plot', methods=['POST'])
def line_plot():
    data = request.json
    specie = data['specie']
    height = data['height']
    
    # Get the index of the specie
    specie_idx = specie_list.index(specie) if specie != 'Kh' else None
    
    plot_url = generate_plot('line', specie_idx, specie, height)
    if plot_url:
        return jsonify({'success': True, 'plot_url': plot_url})
    else:
        return jsonify({'success': False, 'message': 'Error generating plot'})

@app.route('/api/contourf_plot', methods=['POST'])
def contourf_plot():
    data = request.json
    specie = data['specie']
    smoothness = data['smoothness']
    
    # Get the index of the specie
    specie_idx = specie_list.index(specie) if specie != 'Kh' else None
    
    plot_url = generate_plot('contourf', specie_idx, specie, None, smoothness)
    if plot_url:
        return jsonify({'success': True, 'plot_url': plot_url})
    else:
        return jsonify({'success': False, 'message': 'Error generating plot'})

@app.route('/upload_file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file and file.filename.endswith('.nc'):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.root_path, 'uploads', filename))
        flash(f'File {filename} uploaded successfully')
        return redirect(url_for('plot'))
    
    flash('Please upload a valid NetCDF file (.nc)')
    return redirect(request.url)

if __name__ == '__main__':
    # Create templates directory and subdirectories
    os.makedirs(os.path.join(app.root_path, 'templates'), exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)
