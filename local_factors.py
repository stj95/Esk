import helpers
import pandas as pd
import numpy as np
import sensors
from datetime import datetime
import obspy
from obspy.core.utcdatetime import UTCDateTime
import os

def compute_rms(dict_):

    rolling_sum = 0
    rolling_len = 0

    for item in dict_.values():

        rolling_sum += sum(np.power(list(item), 2))
        rolling_len += len(item)


    rms = np.sqrt(rolling_sum) / rolling_len

    return rms

if __name__ == "__main__":

    directory = (r"U:\StephenJ\HWU\DataTransfer\DT3 noiseless")
    # sensor ids:
    sensor_ids = ["6o35e2", "6v71e2", "6v73e2", "Rad1e2", "Rad2e2", "Rad3e2", "Rad4e2", "Rad5e2", "Rad6e2"]
    # create the sensor objects:
    sensors = [sensors.Sensor(id) for id in sensor_ids]
    # read in the folder, with calibration & band passing included here
    sensor_dicts = [helpers.read_folder(directory, sensor) for sensor in sensors]

    # get the date times
    start = datetime(2020, 2, 6, 3, 30)
    end = datetime(2020, 2, 6, 4, 30)
    # date filter
    sensor_dicts = [{key: dict_[key] for key in list(dict_.keys()) if (key > start and key < end)}
                    for dict_ in sensor_dicts]

    rms_values = [compute_rms(dict_) for dict_ in sensor_dicts]
    mean_rms = sum(rms_values) / len(rms_values)
    alphas = [mean_rms / rms for rms in rms_values]

    alpha_dict = {}
    for i, sensor in enumerate(sensor_ids):
        alpha_dict[sensor] = alphas[i]

    print(alpha_dict)
    df = pd.DataFrame(alpha_dict.items(), columns=["id", "alpha"])
    df.to_csv(directory + "\\" + "alpha_e.csv", index=False)

    calvals = pd.read_excel(r"U:\StephenJ\Python\Seismometer_Status\GCF_Python\Branch\calvals_merged.xlsx")

    merged = pd.merge(df, calvals, how='outer', on='id')
    print(merged)

    merged.to_excel("calvals_merged.xlsx", index=False)
