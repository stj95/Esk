from os.path import isdir
from os import listdir
from logs.exception_logging import create_logger
from sensors import Sensor
import obspy
import numpy as np
import pandas as pd
import helpers

"""
This is where we have the frame work for the program, it will navigate through the files and process the data
with the use of the _helper functions.

The general structure of this is as follows from low level to high level:

PSD:

    * psd_stream: This is the lowest level PSD function, it takes one gcf file, and does all the calibration and PSD 
                    work and outputs a data frame of the data psd data and corresponding frequency and timestamp.
                    
    * psd_sensor_folder: Now we are just looking for directions to point psd_stream in, so we design a function to
                    read one sensor folder using psd_stream.
                    
    * psd_download_folder: We can now use psd_sensor_folder to deal with an entire download folder.
    
"""

log_path = r"U:\StephenJ\Python\Seismometer_Status\GCF_Python\Branch\logs\esk.log"
navigation_logger = create_logger("navigation", log_path)


def psd_stream(stream, sensor):
    """
    This does all the processing for one stream of any given length, this is the bulk of the work

    :param stream:
    :param sensor:
    :return: ||TimeStamp| |Sensor| |Frequency| |PSD||
    """

    # Select the correct sample rates
    # stream = helpers.select_channel(stream, sensor)
    # calibrate the stream (applies calvals, de-trends, and decimates)
    stream = helpers.calibrate(stream, sensor)

    # stream = stream.filter('bandpass', freqmin=12, freqmax=16)
    # split the stream between those timestamps
    # noting data_per_bin is a dict {timestamp: data for that bin}
    data_per_bin = helpers.stream_to_bins(stream)

    # It can happen that we read a stream with no full 10 minute bins, in this case we should just
    # return an empty data frame
    if len(data_per_bin) == 0:
        return pd.DataFrame()

    # we have the data for each 10 minute time period, and corresponding timestamp
    # now we need to use welchs method on each 10 minute interval to calculate the PSD
    # for each 10 minute bin, psd the data and put it into the array

    # learn the dimension of frequency so as to initialise the array
    freq, _ = helpers.fft_welchs(list(data_per_bin.values())[0])
    array = np.full([len(data_per_bin), len(freq[1:])], np.nan)

    for index, (timestamp, data_bin) in enumerate(data_per_bin.items()):
        freq, psd_data = helpers.fft_welchs(data_bin)
        # conversion to displacement
        # note: np.divide & np.power - point wise operations
        array[index] = np.divide(psd_data[1:], np.power((2*np.pi*freq[1:]), sensor.displacement_factor))

    timestamp_df = pd.DataFrame(sorted(data_per_bin.keys()), columns=["TimeStamp"])
    df = pd.DataFrame(array, columns=freq[1:])

    merged_df = timestamp_df.merge(df, left_index=True, right_index=True, how="outer")
    melted_df = merged_df.melt("TimeStamp")
    melted_df = melted_df.rename(columns={"variable": "Frequency", "value": "PSD"})
    #melted_df = melted_df[(melted_df["Frequency"] <= 10) & (melted_df["Frequency"] > 0)]
    melted_df["Sensor"] = sensor.id

    return melted_df

def psd_sensor_folder(folder_path, sensor):
    """
    Given a folder with GCF files in, this function just PSDs each GCF and concatenates them

    :param folder:
    :return:
    """

    output_df = pd.DataFrame()


    for file in listdir(folder_path):
        if (file.endswith(".gcf") and ("#" not in file)) or (file.endswith(".mseed")):
            print(sensor.id, file)

            # read the stream
            try:
                stream = obspy.read(folder_path + "\\" + file)
            except ValueError as e:
                navigation_logger.error("Couldn't read stream {}".format((folder_path + "\\" + file)), exc_info=e)
                continue
            data_frame = psd_stream(stream, sensor)
            output_df = pd.concat([output_df, data_frame])

    return output_df

def psd_download_folder(download_folder_path, download_folders, sensor_base):
    """
    Given a set of download folders and a set of sensors, this finds the correct sensor folders,
    PSDs the data using "psd_sensor_folder" and returns a concatenated data frame

    :param download_folder_path:
    :param download_folders:
    :return:
    """

    suffixes = ["z2", "n2", "e2"]

    output_df = pd.DataFrame()

    for download_folder in download_folders:

        updated_path = download_folder_path + "\\" +  download_folder

        for suffix in suffixes:
            # initialise the sensor
            sensor = Sensor(sensor_base + suffix)
            sensor_path = updated_path + "\\" + sensor.id
            if isdir(sensor_path):
                sensor_df = psd_sensor_folder(sensor_path, sensor)
                output_df = pd.concat([output_df, sensor_df])

            else:
                navigation_logger.exception("{} is not a correct path".format(sensor_path))
                continue

    # output: ||TimeStamp| |Frequency| |PSD| |Sensor||
    return output_df

