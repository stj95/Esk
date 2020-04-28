import numpy as np
from datetime import datetime
import sensors
import helpers
from local_factors import compute_rms
import matplotlib.pyplot as plt

"""

Strategy:

find a period of time where the turbines are on & high wind speed

calculate the rms values & plot vs distance

then correct the rms values & plot again vs distance

"""

def calc_distance(sensor):

    fortis = sensors.Sensor("Fortis1z2")
    distance = np.sqrt((sensor.easting - fortis.easting)**2 + (sensor.northing - fortis.northing)**2)

    return distance


if __name__ == "__main__":

    directory = r"Q:\1 Projects\2 Development\381 Eskdalemuir\5 Technical\5.1 Monitoring Campaign\381-190109-4013\2020-03-11"

    sensor_ids = ["6o35z2", "6v71z2", "6v73z2", "Rad1z2", "Rad2z2", "Rad3z2", "Rad4z2"]

    sensors_ = [sensors.Sensor(s) for s in sensor_ids]

    sensor_dicts = [helpers.read_folder(directory, sensor) for sensor in sensors_]

    # # get the date times
    # start = datetime(2020, 2,#  6, 3, 36)
    # end = datetime(2020, 2, 6, 5, 11)

    start = datetime(2020, 3, 9, 0, 0)
    end = datetime(2020, 3, 10, 0, 0)

    # date filter
    sensor_dicts = [{key: dict_[key] for key in list(dict_.keys()) if (key > start and key < end)}
                    for dict_ in sensor_dicts]

    distances = [calc_distance(sensor) for sensor in sensors_]
    rms_values = [compute_rms(dict_) for dict_ in sensor_dicts]
    corrected_rms_values = [rms_values[i] * sensors_[i].local_factor for i in range(len(sensors_))]

    print("len sens: ", len(sensors_))
    print("distances: ", distances)
    print("rms_values: ", rms_values)
    print("corrected_rms_values: ", corrected_rms_values)

    fig, (ax1, ax2) = plt.subplots(1, 2, sharey='all')

    for i, sensor in enumerate(sensors_):
        ax1.plot(distances[i], np.log10(rms_values[i]), label=sensor.id, marker='o')
        ax1.set_title("Original")
        ax1.set_ylabel("RMS velocity, Log10(ms^-1))")
        ax1.set_xlabel("Distance (m)")
        ax2.plot(distances[i], np.log10(corrected_rms_values[i]), label=sensor.id, marker='o')
        ax2.set_title("Corrected")
        ax2.set_xlabel("Distance (m)")

    fig.suptitle("RMS correction")
    plt.legend()
    plt.show()
