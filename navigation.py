from os.path import isdir
from os import listdir
import obspy
import numpy as np
import pandas as pd
import _helpers

"""
This is where we have the frame work for the program, it will navigate through the files and process the data
with the use of the _helper functions

The general structure of this is as follows from low level to high level:

    * psd_stream: This is the lowest level function, it takes one gcf file, and does all the calibration and PSD 
                    work and outputs a data frame of the data psd data and corresponding frequency and timestamp
                    
    * psd_sensor_folder: Now we are just looking for directions to point psd_stream in, so we design a function to
                    read one sensor folder using psd_stream.
                    
    * psd_download_folder: We can now use psd_sensor_folder to deal with an entire download folder
    
"""


def psd_stream(stream, stream_id, calval, gain, decimation_factor):
    """
    This does all the processing for one stream of any given length, this is the bulk of the work

    :param stream:
    :param sensor_id:
    :return: ||TimeStamp| |Sensor| |Frequency| |PSD||
    """

    # Select the correct sample rates
    stream = _helpers._select_channel(stream, stream_id)
    # calibrate the stream (applies calvals, de-trends, and decimates)
    stream = _helpers._calibrate(stream, calval, gain, decimation_factor)
    # get the timestamps which we want to split the stream into
    template_timestamps = _helpers._get_timestamps(stream)
    # split the stream between those timestamps
    data_bins, timestamps = _helpers._stream_to_bins(stream, template_timestamps)

    # It can happen that we read a stream with no full 10 minute bins, in this case we should just
    # return an empty data frame
    if data_bins == []:
        return

    # we have the data for each 10 minute time period, and corresponding timestamp
    # now we need to use welchs method on each 10 minute interval to calculate the PSD
    # for each 10 minute bin, psd the data and put it into the array

    # learn the dimension of frequency so as to initialise the array
    freq, _ = _helpers._fft_welchs(data_bins[0])

    array = np.full([len(data_bins), len(freq)], np.nan)
    for index, data_bin in enumerate(data_bins):
        _, psd_data = _helpers._fft_welchs(data_bin)
        array[index] = psd_data

    timestamp_df = pd.DataFrame(timestamps, columns=["TimeStamp"])
    df = pd.DataFrame(array, columns=freq)

    merged_df = timestamp_df.merge(df, left_index=True, right_index=True, how="outer")
    melted_df = merged_df.melt("TimeStamp")
    melted_df = melted_df.rename(columns={"variable": "Frequency", "value": "PSD"})
    melted_df = melted_df[(melted_df["Frequency"] <= 10) & (melted_df["Frequency"] > 0)]
    melted_df["Sensor"] = stream_id

    return melted_df


def psd_sensor_folder(folder_path, sensor_id):
    """
    Given a folder with GCF files in, this function just PSDs each GCF and concatenates them

    :param folder:
    :return:
    """

    output_df = pd.DataFrame()

    # get the calibration factors
    calval = _helpers._get_calval(sensor_id)
    gain = _helpers._get_gain(sensor_id)
    decimation_factor = _helpers._get_decimation_factor(sensor_id)
    displacement_factor = _helpers._get_displacement_factor(sensor_id)

    
    for file in listdir(folder_path):
        if (file.endswith(".gcf") and ("#" not in file)) or (file.endswith(".mseed")):
            print(sensor_id, file)

            # read the stream
            stream = obspy.read(folder_path + "\\" + file)
            data_frame = psd_stream(stream, sensor_id, calval, gain, decimation_factor)
            output_df = pd.concat([output_df, data_frame])

    return output_df


def psd_download_folder(download_folder_path, download_folders, sensor):
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
            sensor_id = sensor + suffix
            sensor_path = updated_path + "\\" + sensor_id
            if isdir(sensor_path):
                sensor_df = psd_sensor_folder(sensor_path, sensor_id)
                output_df = pd.concat([output_df, sensor_df])

            else:
                continue

    # output: ||TimeStamp| |Frequency| |PSD| |Sensor||
    return output_df



