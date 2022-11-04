from django.test import TestCase
import matplotlib.pyplot as plt
import numpy as np

# Create your tests here.
# Plot bar chart
plt.clf()
# switch to AGG to enable the figure display on web
# plt.switch_backend("AGG")
# plt.figure(figsize=(7, 5))
#
# electrolyte = "KCl"
# mem_thickness = 6
# voltage_stage_str = "-1.2, 0"
# voltage_stage = [float(s) for s in voltage_stage_str.split(",")]
# slope_lst = [6, 2]
#
# # calculate the flux value
# electrolyte_lambda_dict = {"KCl": 0.01499, "LiCl": 0.01151}
# electrolyte_lambda = electrolyte_lambda_dict[electrolyte]  # S m2 mol-1
# permeate_volume = 0.000029  # m3
# inner_hole_diameter = 0.004  # m
# A_eff = np.pi * inner_hole_diameter * mem_thickness  # m2
# flux = [slope * 0.000001 * 100 * permeate_volume / (A_eff * electrolyte_lambda) for slope in slope_lst]
#
# plt.bar(voltage_stage_str.split(","), flux, align='center', alpha=0.5)
# x_pos = np.arange(len(voltage_stage))
# plt.xticks(x_pos, voltage_stage)
# plt.xlabel('Applied voltage (V)')
# plt.ylabel('Permeation flux $(mol / m^2 h)$')
# plt.show()