import navigation
import _helpers
import matplotlib.pyplot as plt
from scipy import integrate
import numpy as np

path = r"Q:\1 Projects\2 Development\381 Eskdalemuir\5 Technical\5.1 Monitoring Campaign\381-190109-4013\2019-10-24"
sensor1 = "Rad2z2"
sensor2 = "6o35z2"

# Calculate power spectrums
psd1 = navigation.psd_sensor_folder(path + "\\" + sensor1, sensor1)
psd2 = navigation.psd_sensor_folder(path + "\\" + sensor2, sensor2)
csd = navigation.correlate_sensor_folder(path, sensor1, sensor2)

# inter-quartile mean the spectral densities
psd1 = psd1[psd1["Frequency"]>0.5].groupby(["Frequency"], as_index=False)["PSD"].agg({"iqm": _helpers._iqm})
psd2 = psd2[psd2["Frequency"]>0.5].groupby(["Frequency"], as_index=False)["PSD"].agg({"iqm": _helpers._iqm})
csd = csd[csd["Frequency"]>0.5].groupby(["Frequency"], as_index=False)["PSD"].agg({"iqm": _helpers._iqm})

# plot
fig = plt.figure()
grid = plt.GridSpec(3, 1)

ax1 = fig.add_subplot(grid[0,0])
ax1.semilogy(psd1["Frequency"], psd1["iqm"], 'r')
ax1.grid()

ax2 = fig.add_subplot(grid[1,0], sharex=ax1)
ax2.semilogy(psd2["Frequency"], psd2["iqm"], 'g')
ax2.grid()

ax3 = fig.add_subplot(grid[2,0], sharex=ax1)
ax3.semilogy(csd["Frequency"], csd["iqm"], 'b')
ax3.grid()

plt.show()