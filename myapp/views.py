import os
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.http import HttpResponse

import base64
import io
import math

# from matplotlib.pylab import *
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# Create your views here.
def index(request):
    context = {}
    global attribute, file_directory, voltage_stage, interval

    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        voltage_stage = request.POST.get('V_stages')
        voltage_stage = [float(s) for s in voltage_stage.split(",")]
        interval = int(request.POST.get('t_interval'))

        # check if this file ends with csv
        if uploaded_file.name.endswith('.txt'):
            savefile = FileSystemStorage()
            name = savefile.save(uploaded_file.name, uploaded_file)  # gets the name of the file
            # print(name)
            # we need to save the file somewhere in the project, MEDIA
            d = os.getcwd()  # how we get the current dorectory
            file_directory = d + '/media/' + name  # saving the file in the media directory

            readfile(file_directory)
            message = f"There are {n_stages} stages detected"
            messages.warning(request, message)

            if n_stages != len(voltage_stage):
                message = "Please check if the given voltage list matches the conductivity file!"
                messages.warning(request, message)
            else:
                return redirect(plot_graph)

        else:
            messages.warning(request, 'File was not uploaded. Please use .csv file extension!')

    return render(request, 'index.html', context)


def readfile(filename):
    # The path of the conductivity data file
    filepath = file_directory
    global index_x, cond_global, cont_arr, cond_unit, interval, n_points_per_stage, n_stages

    # read the missing data - checking if there is a null
    missingvalue = ['?', '0', '--']
    # for windows generated csv txt file, use '\s+' as delimiter
    content = pd.read_csv(filepath, delimiter='\s+', na_values=missingvalue, engine='python')
    cont_arr = content.to_numpy()

    index_x = cont_arr[:, 0]
    cond_global = cont_arr[:, 7]

    # Get the unit of conductivity for unit conversion
    cond_unit = cont_arr[:, 8][0]

    # Get the # of data points in the file
    n_total_points = len(index_x)

    # The time duration for a potential applied on, in the unit of sec
    time_per_stage = 30 * 60

    # The data sampling interval of conductivity meter
    # interval = 1

    # Calculate # of data points per potential stage
    n_points_per_stage = int(time_per_stage / interval)
    n_stages = math.ceil(n_total_points / n_points_per_stage)


# Calculate the slope of every stage and plot a summary graph
def plot_graph(request):
    # Take the "index" and "conductivity" columns for plotting
    index_x = cont_arr[:, 0]
    cond_global = cont_arr[:, 7]
    time = index_x * interval / 3600

    voltage_text_pos = cond_global[0]
    plt.switch_backend("AGG")
    plt.figure(figsize=(7, 5))
    plt.plot(time[:len(voltage_stage) * n_points_per_stage], cond_global[:len(voltage_stage) * n_points_per_stage])

    for i in range(len(voltage_stage)):
        b, k = np.polynomial.polynomial.polyfit(np.array(time[50:n_points_per_stage - 50], dtype=float),
                                                np.array(cond_global[50:n_points_per_stage - 50], dtype=float), 1)
        plt.plot(time[:n_points_per_stage], b + k * time[:n_points_per_stage])
        plt.text(float(time[0]), float(cond_global[n_points_per_stage // 2] + 0.3), s=f"{k:.2}")
        plt.text(float(time[n_points_per_stage // 2]), voltage_text_pos, s=f"{voltage_stage[i]} V")

        time = time[n_points_per_stage:]
        cond_global = cond_global[n_points_per_stage:]

    plt.xlabel("Time (hour)")
    plt.ylabel("Conductivity ($\mu$S / cm)")

    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150)
    buf.seek(0)
    image_png = buf.getvalue()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    buf.close()

    return render(request, 'demo.html', {'graphic': graphic})


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
