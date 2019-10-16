import obspy
from os import listdir
#from obspy.signal.cross_correlation import correlate
from scipy.signal import csd
from scipy.signal import correlate # may want to use this version of correlate because obspy
import matplotlib.pyplot as plt
import numpy as np
import _helpers





if __name__ == "__main__":

    path_to_gcfs = (r"Q:\1 Projects\2 Development\381 Eskdalemuir\5 Technical"
                    r"\5.1 Monitoring Campaign\381-190109-4013\2019-10-09")

    # what sensors do we want to correlate?
    sensor1 = "6o35z2"
    sensor2 = "6t93z2"

    # get calibration values
    calib1 = _helpers._get_calval(sensor1)
    calib2 = _helpers._get_calval(sensor2)

    # get the sensor gain
    gain1 = _helpers._get_gain(sensor1)
    gain2 = _helpers._get_gain(sensor2)

    # get the lists of the gcf files for each sensor
    gcfs1 = _helpers._clean_gcfs(listdir(path_to_gcfs + "\\" + sensor1))
    gcfs2 = _helpers._clean_gcfs(listdir(path_to_gcfs + "\\" + sensor2))

    # how displaced are the streams from the original index in ten minute periods
    sens1_disp = 0
    sens2_disp = 0

    # for gcf file
    for i in range(max(len(gcfs1), len(gcfs2))):

        """
        """

        # read in the two gcf files we want to correlate
        st1 = obspy.read(path_to_gcfs + "\\" + sensor1 + "\\" + gcfs1[i+sens1_disp])
        st2 = obspy.read(path_to_gcfs + "\\" + sensor2 + "\\" + gcfs2[i+sens1_disp])

        # apply calibration steps:
        for trace in st1:
            trace.data = trace.data * calib1 / gain1
            #trace.split()
            trace.detrend(type='linear')
            trace.decimate(2)

        for trace in st2:
            trace.data = trace.data * calib2 / gain2
            #trace.split()
            trace.detrend(type='linear')
            trace.decimate(2)

        # correlate with no shift
        cc = correlate(st1, st2)
        print(cc)
        # get the cross spectral density
        f, Pxy = csd(st1[0].data, st2[0].data, fs=50, nperseg=1024)

        """
        Plotting
        """

        print("plotting")

        fig = plt.figure()

        fig.suptitle(gcfs1[i + sens1_disp] + " - " + gcfs2[i+sens2_disp])

        ax1 = plt.subplot(212)
        #ax1.semilogy(f, np.abs(Pxy), 'r')
        ax1.plot(cc[0], 'r')

        ax2 = plt.subplot(221)
        ax2.plot(st1[0], 'g')
        ax2.set_title(sensor1)

        ax3 = plt.subplot(222)
        ax3.plot(st2[0], 'b')
        ax3.set_title(sensor2)

        plt.show(block=True)
