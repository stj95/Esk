import matplotlib.pyplot as plt
import os
import sensors
import helpers
from scipy import signal
import numpy as np

def calculate_velocity(sensor1, sensor2, data1, data2):

    # sampling rate:
    sr = 50

    # Distance
    distance = np.sqrt((sensor1.easting - sensor2.easting)**2 + (sensor1.northing - sensor2.northing)**2)

    # Time
    assert len(data1) == len(data2)

    corr = signal.correlate(data1, data2)

    sample_delay = abs(np.argmax(corr) - len(corr)/2)
    print(sample_delay)
    time = sample_delay / sr

    #plt.plot(np.log(abs(corr)))
    #plt.show()


    print(distance, time)

    velocity = distance / time

    return velocity

def get_v(path, sensor1, sensor2):

    dict1 = helpers.read_folder(path, sensor1)
    dict2 = helpers.read_folder(path, sensor2)

    dict1, dict2 = helpers.intersect_dicts([dict1, dict2])

    velocities = []
    for key in dict1:
        velocity = calculate_velocity(sensor1, sensor2, dict1[key], dict2[key])
        velocities.append(velocity)

    print(velocities)
    plt.hist(velocities)
    plt.show()

    v = helpers.iqm(velocities)

    print(v)

if __name__ == "__main__":

    path = (r"U:\StephenJ\HWU\DataTransfer\DT1\15-21 January 2020")

    sensors = [sensors.Sensor(file) for file in os.listdir(path) if file.endswith("z2")]

    arr = np.full([len(sensors), len(sensors)], np.nan)

    for i, sensor_i in enumerate(sensors):
        for j, sensor_j in enumerate(sensors[:len(sensors)-i]):

            if  i!=j:
                try:
                    arr[i, j] = get_v(path, sensor_i, sensor_j)
                except Exception as e:
                    print(e)
                    arr[i, j] = np.nan
            else:
                arr[i, j] = np.nan
    print(arr)


    plt.matshow(arr)



