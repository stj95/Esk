from os.path import isdir
from os import listdir
from exception_logging import create_logger
import obspy
import numpy as np
import pandas as pd
import _helpers

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

def psd_stream(stream, stream_id, calval, gain, decimation_factor, displacement_factor):
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

    # split the stream between those timestamps
    # noting data_per_bin is a dict {timestamp: data for that bin}
    data_per_bin = _helpers._stream_to_bins(stream)

    # It can happen that we read a stream with no full 10 minute bins, in this case we should just
    # return an empty data frame
    if len(data_per_bin) == 0:
        return pd.DataFrame()

    # we have the data for each 10 minute time period, and corresponding timestamp
    # now we need to use welchs method on each 10 minute interval to calculate the PSD
    # for each 10 minute bin, psd the data and put it into the array

    # learn the dimension of frequency so as to initialise the array
    freq, _ = _helpers._fft_welchs(list(data_per_bin.values())[0])
    array = np.full([len(data_per_bin), len(freq[1:])], np.nan)

    for index, (timestamp, data_bin) in enumerate(data_per_bin.items()):
        freq, psd_data = _helpers._fft_welchs(data_bin)
        # conversion to displacement
        # note: np.divide & np.power - point wise operations
        array[index] = np.divide(psd_data[1:], np.power((2*np.pi*freq[1:]), displacement_factor))

    timestamp_df = pd.DataFrame(sorted(data_per_bin.keys()), columns=["TimeStamp"])
    df = pd.DataFrame(array, columns=freq[1:])

    merged_df = timestamp_df.merge(df, left_index=True, right_index=True, how="outer")
    melted_df = merged_df.melt("TimeStamp")
    melted_df = melted_df.rename(columns={"variable": "Frequency", "value": "PSD"})
    #melted_df = melted_df[(melted_df["Frequency"] <= 10) & (melted_df["Frequency"] > 0)]
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
            try:
                stream = obspy.read(folder_path + "\\" + file)
            except ValueError as e:
                navigation_logger.error("Couldn't read stream {}".format((folder_path + "\\" + file)), exc_info=e)
                continue
            data_frame = psd_stream(stream, sensor_id, calval, gain, decimation_factor, displacement_factor)
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
                navigation_logger.exception("{} is not a correct path".format(sensor_path))
                continue

    # output: ||TimeStamp| |Frequency| |PSD| |Sensor||
    return output_df

