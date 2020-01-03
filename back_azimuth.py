import numpy as np
import scipy.integrate
import scipy.signal
import _helpers
from itertools import chain

def alpha(z, x, y):
    """
    takes in the three streams, finds the azimuth, alpha, for which rayleigh waves are maximised OR MINIMISED

    !!! Need to implement the second derivative to determine maximum or minimum where

    if alpha = min:
        alpha = alpha + pi

    this returns a maximum for alpha

    :param z:
    :param x:
    :param y:
    :return:
    """

    [z, x, y] = _helpers._intersect_dicts([z, x, y])

    # sort the values so we are "in phase"
    # chain goes from [data_1], [data_2], ... [data_n] to [data_1, data_2, ..., data_n]
    z_values = list(chain(*[z[ts] for ts in sorted(z.keys())]))
    x_values = list(chain(*[x[ts] for ts in sorted(x.keys())]))
    y_values = list(chain(*[y[ts] for ts in sorted(y.keys())]))

    # signal.hilbert doesn't do the hilbert transform, it just returns x + iy analytic signal where y is the hilbert
    # transform of the original signal (such a weird function)
    analytic_func_z = scipy.signal.hilbert(np.array(z_values))
    ht_z = analytic_func_z.imag

    # finding local maxima & minima:
    num = scipy.integrate.trapz(ht_z * np.array(x_values))
    den = scipy.integrate.trapz(ht_z * np.array(y_values))

    alpha = np.arctan(num / den)

    # determining if it's a maximum of a minimum:
    # gpp = integrate(H[z(t)] * [y(t)*cos(alpha) - x(t)*sin(alpha)])
    gpp = scipy.integrate.trapz(ht_z * (np.array(y_values) * np.cos(alpha) - np.array(x_values) * np.sin(alpha)))


    #for index, value in enumerate(alpha):
    #    if gpp[index] > 0:
    #        alpha[index] = value + np.pi

    if gpp > 0:
        print(gpp, "Minimum -> added pi")
        alpha += np.pi

    return alpha



if __name__ == "__main__":

    path = r"Q:\1 Projects\2 Development\381 Eskdalemuir\5 Technical\5.1 Monitoring Campaign\381-190109-4013\2019-10-24"

    # define which sensors you want to look at
    sensor1 = "6v73z2"
    sensor2 = "6v73n2"
    sensor3 = "6v73e2"

    # read in the streams, this returns a dictionary with 10 min timestamps and data
    print("reading z")
    z = _helpers._read_gcf_folder(path, sensor1)
    print("reading y")
    y = _helpers._read_gcf_folder(path, sensor2)
    print("reading x")
    x = _helpers._read_gcf_folder(path, sensor3)

    # conversion to degrees
    print("computing alpha")
    a = alpha(x, y, z)
    a_deg = a * 180 / np.pi

    print(a, " rad")
    print(a_deg, " deg")

