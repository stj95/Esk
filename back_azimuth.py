from statistics import mean
from multiprocessing import Pool
import sensors
import matplotlib.pyplot as plt
import numpy as np
import scipy.integrate
import scipy.signal
import helpers
import os
from itertools import chain


def alpha(z, x, y, theta):
    """
    takes in the three streams, finds the azimuth, alpha, for which rayleigh waves are maximised

    :param z:
    :param x:
    :param y:
    :return alpha: Back azimuth, degrees clockwise from north

    (Note in GIS this needs to be converted to degrees anticlockwise from East which is standard form)

    """

    [z, x, y] = helpers.intersect_dicts([z, x, y])

    """
    Chained
    """
    # sort the values so we are "in phase"
    # chain goes from [data_1], [data_2], ... [data_n] to [data_1, data_2, ..., data_n]
    # z_values = list(chain(*[z[ts] for ts in sorted(z.keys())]))
    # x_values = list(chain(*[x[ts] for ts in sorted(x.keys())]))
    # y_values = list(chain(*[y[ts] for ts in sorted(y.keys())]))

    """
    Averaged
    """
    z_values = np.array([z[ts] for ts in sorted(z.keys())])
    x_values = np.array([x[ts] for ts in sorted(x.keys())])
    y_values = np.array([y[ts] for ts in sorted(y.keys())])

    """
    Rotations
    """

    x_values = x_values * np.cos(theta) + y_values * np.sin(theta)
    y_values = x_values * -np.sin(theta) + y_values * np.cos(theta)


    # signal.hilbert doesn't do the hilbert transform, it just returns x + iy analytic signal where y is the hilbert
    # transform of the original signal (such a weird function) This is because its in .signal.hilbert. note that
    # fftpack.hilbert does return the hilbert transform

    ht_z = np.imag(scipy.signal.hilbert(z_values))

    # finding local maxima & minima:
    num = scipy.integrate.trapz(ht_z * x_values)
    den = scipy.integrate.trapz(ht_z * y_values)

    alpha = np.arctan2(num, den)

    # determining if it's a maximum of a minimum:
    integrand = ht_z * (-(np.sin(alpha) * x_values.T).T - (np.cos(alpha) * y_values.T).T)
    gpp = scipy.integrate.trapz(integrand)

    for index, value in enumerate(alpha):
       if gpp[index] > 0:
            alpha[index] = value + np.pi

    return alpha


def compute_azimuths(sensor, inpath, outpath):

    # define which sensors you want to look at
    sensor1 = sensors.Sensor(sensor + "z2")
    sensor2 = sensors.Sensor(sensor + "n2")
    sensor3 = sensors.Sensor(sensor + "e2")

    # read in the streams, this returns a dictionary with 10 min timestamps and data
    print("reading z")
    z = helpers.read_folder(inpath, sensor1)
    print("reading y")
    y = helpers.read_folder(inpath, sensor2)
    print("reading x")
    x = helpers.read_folder(inpath, sensor3)

    print("computing alpha")

    # rotation angle in radians:
    theta = sensor2.theta * np.pi / 180
    # theta = 0
    rad = np.mod(alpha(z, x, y, theta), 2*np.pi)
    deg = rad * 180 / np.pi

    a_rad_mean = mean(rad)
    a_deg_mean = a_rad_mean * 180 / np.pi

    print(a_rad_mean, " rad")
    print(a_deg_mean, " deg")

    """
    Plotting
    """

    fig = plt.figure()
    ax1 = fig.gca()

    n, bins, _ = ax1.hist(deg, bins=np.linspace(0, 360, 50))

    print("most common direction: ", bins[np.argmax(n)])
    plt.show()

    """
    write to file
    """

    import csv
    with open(outpath + "\\" + "{}.csv".format(sensor1.id[:-2]), 'w', newline="") as f:
        writer = csv.writer(f)
        writer.writerows(zip(bins, n))



if __name__ == "__main__":


    path = (r"Q:\1 Projects\2 Development\381 Eskdalemuir\5 Technical"
            r"\5.1 Monitoring Campaign\381-190109-4013\2020-02-04")

    outpath = (r"Q:\1 Projects\2 Development\381 Eskdalemuir\5 Technical"
               r"\5.1 Monitoring Campaign\381-200117-4056\Jan_data")

    sensors = []
    for sensor in os.listdir(path):
        if sensor[:-2] not in sensors:
            sensors.append(sensor[:-2])

    sensors = ["Rad2", "Rad4"]

    args = [(sensor, path, outpath) for sensor in sensors]

    with Pool(processes=4) as p:
        p.starmap(compute_azimuths, args)
