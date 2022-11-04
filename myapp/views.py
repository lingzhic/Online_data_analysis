import os
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.contrib import messages

import base64
import io
import math

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from .plot_utils import get_graph, get_time_interval

SECONDS_PER_MINUTE = 60
MINUTES_PER_HOUR = 60


# Create your views here.
def index(request):
    context = {}
    # The data sampling interval of conductivity meter
    global file_directory, voltage_stage_str, voltage_stage_interval, mem_thickness, electrolyte

    # get input from the form
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        voltage_stage_str = request.POST.get('V_stages')
        voltage_stage = [float(s) for s in voltage_stage_str.split(",")]
        voltage_stage_interval = int(request.POST.get('t_interval'))
        mem_thickness = float(request.POST.get('mem_thickness')) * 1e-6  # in the unit of um
        electrolyte = request.POST.get('electrolyte')

        # check if this file ends with txt
        if uploaded_file.name.endswith('.txt'):
            savefile = FileSystemStorage()
            name = savefile.save(uploaded_file.name, uploaded_file)  # gets the name of the file
            # save the file somewhere in the project, MEDIA
            d = os.getcwd()  # get the current directory
            file_directory = d + '/media/' + name  # saving the file in the media directory

            readfile(file_directory)
            message = f"There are {n_stages} stages detected"
            messages.warning(request, message)

            if n_stages < len(voltage_stage):
                message = "Please check if the given voltage list matches the conductivity file!"
                messages.warning(request, message)
            else:
                return redirect(plot_graph)

        else:
            messages.warning(request, 'File was not uploaded. Please use .txt file extension!')

    return render(request, 'index.html', context)


def readfile(filename):
    # The path of the conductivity data file
    filepath = file_directory
    global cont_arr, cond_unit, n_points_per_stage, n_stages, time_interval

    # read the missing data - checking if there is a null
    missingvalue = ['?', '0', '--']
    # for windows generated csv txt file, use '\s+' as delimiter
    content = pd.read_csv(filepath, delimiter='\s+', na_values=missingvalue, engine='python')
    cont_arr = content.to_numpy()

    # Get the unit of conductivity for unit conversion
    cond_unit = cont_arr[:, 8][0]

    # Get the # of data points in the file
    n_total_points = len(cont_arr[:, 0])

    # Calculate # of data points per potential stage
    # The time duration for a potential applied on, in the unit of sec
    time_per_stage = voltage_stage_interval * SECONDS_PER_MINUTE
    time_interval = get_time_interval(cont_arr[:, 2])
    n_points_per_stage = int(time_per_stage / time_interval)
    n_stages = math.ceil(n_total_points / n_points_per_stage)


# Calculate the slope of every stage and plot a summary graph
def plot_graph(request):
    # Plot conductivity line chart
    # convert voltage str to num
    voltage_stage = [float(s) for s in voltage_stage_str.split(",")]
    # Take the "index" and "conductivity" columns for plotting
    index_x = cont_arr[:, 0]
    cond = cont_arr[:, 7]
    time = index_x * time_interval / (MINUTES_PER_HOUR * SECONDS_PER_MINUTE)  # in the unit of hour

    voltage_text_pos = cond[0]
    plt.switch_backend("AGG")
    plt.figure(figsize=(7, 5))
    plt.plot(time[:len(voltage_stage) * n_points_per_stage], cond[:len(voltage_stage) * n_points_per_stage])

    slope_lst = []
    for i in range(len(voltage_stage)):
        lower_fitting_range = math.ceil(n_points_per_stage / 2)
        upper_fitting_range = n_points_per_stage
        b, k = np.polynomial.polynomial.polyfit(np.array(time[lower_fitting_range:upper_fitting_range], dtype=float),
                                                np.array(cond[lower_fitting_range:upper_fitting_range], dtype=float), 1)
        plt.plot(time[lower_fitting_range:upper_fitting_range], b + k * time[lower_fitting_range:upper_fitting_range])
        plt.grid(visible=True, which='major', axis='x', color='darkgray', linestyle='-', linewidth=2)
        plt.text(float(time[0]), float(cond[n_points_per_stage // 2] + 0.3), s=f"{k:.2}")
        plt.text(float(time[n_points_per_stage // 2]), voltage_text_pos, s=f"{voltage_stage[i]} V")
        slope_lst.append(k)

        time = time[n_points_per_stage:]
        cond = cond[n_points_per_stage:]

    plt.xlabel("Time (hour)")
    plt.ylabel("Conductivity ($\mu$S / cm)")
    slope_plot = get_graph()

    # Plot bar chart
    plt.clf()
    # switch to AGG to enable the figure display on web
    plt.switch_backend("AGG")
    # calculate the flux value
    electrolyte_lambda_dict = {"KCl": 0.01499, "LiCl": 0.01151}
    electrolyte_lambda = electrolyte_lambda_dict[electrolyte]   # S m2 mol-1
    permeate_volume = 0.000029                                  # m3
    inner_hole_diameter = 0.004                                 # m
    A_eff = np.pi * inner_hole_diameter * mem_thickness         # m2
    flux = [slope * 0.000001 * 100 * permeate_volume / (A_eff * electrolyte_lambda) for slope in slope_lst]

    x_pos = np.arange(len(voltage_stage))
    plt.bar(x_pos, flux, align='center', alpha=0.5)
    plt.xticks(x_pos, voltage_stage)
    plt.xlabel('Applied voltage (V)')
    plt.ylabel('Permeation flux $(mol / m^2 h)$')
    slope_bar = get_graph()

    return render(request, 'diffusion_data_analysed.html', {'slope_plot': slope_plot, 'slope_bar': slope_bar})


def results(request):
    # prepare the visualization
    # message = 'I found ' + str(rows) + ' rows and ' + str(columns) + ' columns. Missing data: ' + str(missing_values)
    message = "hello world"
    messages.warning(request, message)
    #
    # dashboard = []  # ['A11','A11',A'122',]
    # for x in data[attribute]:
    #     dashboard.append(x)
    #
    # my_dashboard = dict(Counter(dashboard))  # {'A121': 282, 'A122': 232, 'A124': 154, 'A123': 332}
    #
    # print(my_dashboard)
    #
    # keys = my_dashboard.keys()  # {'A121', 'A122', 'A124', 'A123'}
    # values = my_dashboard.values()
    #
    # listkeys = []
    # listvalues = []
    #
    # for x in keys:
    #     listkeys.append(x)
    #
    # for y in values:
    #     listvalues.append(y)
    #
    # print(listkeys)
    # print(listvalues)
    #
    context = {
        'listkeys': 1,
        'listvalues': 2,
    }

    return render(request, 'results.html', context)
