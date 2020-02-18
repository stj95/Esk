from datetime import datetime, timedelta
from obspy.core.utcdatetime import UTCDateTime
from scipy import signal
from functools import reduce
from exception_logging import create_logger
import pandas as pd
import statistics
import numpy as np
import obspy
import os

"""
Low level helper functions

The general structure for processing the data should be:
    * select sample rates (_select_sample_rates)
    * calibrate the streams (this includes decimation and de-trending) (_calibrate)
    * get the 10 minute interval templates (_get_timestamps)
    * split the data stream into the intervals (_stream_to_bins)
    
"""

log_path = r"U:\StephenJ\Python\Seismometer_Status\GCF_Python\Branch\logs\esk.log"
helper_logger = create_logger("main.navigation.helpers", log_path)

def _get_calval(sensor_id):
    """
    Reads the calvals.pkl pickle, and reads the correct calval
    for the sensor id
    """

    filepath = "calvals.pkl"
    try:
        df = pd.read_pickle(filepath)
        calval = df.loc[sensor_id]["calval"]
    except KeyError as e:
        helper_logger.exception("Couldn't read {} calval, set to 1".format(sensor_id), exc_info=e)
        calval = 1

    return calval


def _get_gain(sensor_id):
    """
    Reads the sens_details csv, and reads the correct gain value
    for the sensor stream
    """
    filepath = "calvals.pkl"

    try:
        df = pd.read_pickle(filepath)
        gain = df.loc[sensor_id]["gain"]
    except KeyError as e:
        helper_logger.error("Couldn't read {} gain, set to 1".format(sensor_id), exc_info=e)
        gain = 1

    return gain


def _get_decimation_factor(sensor_id):
    """
    The decimation factor, is the factor by which we reduce the sampling rate (SR), we can afford to drop the sampling
    rate to 20Hz as we are interested only in frequencies below 10Hz (see Nyquist frequency). However since our pass
    filters will have a certain roll off, to be safe we will drop the sampling rate to 50Hz, giving us a 15Hz buffer.

    Fortis or Rad1 & 2 SR: 200Hz -> decimation_factor: 4
    other SR:  100Hz -> decimation_factor: 2

    :param sensor_id:
    :return:
    """

    if sensor_id in ["Fortis1e2", "Fortis1n2", "Fortis1z2",
                     "Rad4z2", "Rad4n2", "Rad4e2",
                     "Rad5z2", "Rad5n2", "Rad5e2",
                     "Rad6z2", "Rad6n2", "Rad6e2"]:

        decimation_factor = 4
    else:
        decimation_factor = 2

    return decimation_factor


def _get_displacement_factor(sensor_id):
    """
    The displacement factor is the exponent of (2*pi*i*f) required to change from the current stream to displacement

    acceleration -> displacement: exponent 4
    velocity     -> displacement: exponent 2

    :param sensor_id:
    :return:
    """

    filepath = "calvals.pkl"

    try:
        df = pd.read_pickle(filepath)
        displacement_factor = df.loc[sensor_id]["displacement_factor"]
    except KeyError as e:
        helper_logger.error("Couldn't read {} displacement factor, set to 1".format(sensor_id), exc_info=e)
        displacement_factor = 1

    return displacement_factor


def _select_channel(input_stream, stream_id):
    """
    selects the traces with the correct channels, depending on the instrument

    :param input_stream:
    :return:
    """
    if stream_id in ["Fortis1e2", "Fortis1n2", "Fortis1z2", "Rad3e2", "Rad3n2", "Rad3z2"]:
        input_stream = input_stream.select(channel="HH*")
    elif stream_id in ["Rad1e2", "Rad1n2", "Rad1z2", "Rad2e2", "Rad2n2", "Rad2z2"]:
        input_stream = input_stream.select(channel="HN{}".format(stream_id[-2].capitalize()))

    return input_stream


def _calibrate(stream, calval, gain, decimation_factor):
    """
    Calibrates the stream given a certain calval

    :param stream:
    :param calval:
    :param gain:
    :return: stream
    """

    for trace in stream:
        # set the calibration value
        trace.data = trace.data * calval/gain
        # de-trend & decimate to avoid spectral leakage,
        # we can afford to lose all frequencies above 50Hz so we decimate to that point (see Nyquist frequency)
        # trace.split()
        trace.detrend('constant')
        # Butterworth low pass
        trace.filter('lowpass', freq=25)
        # Chebyshev II low pass - this gives a massive roll off - after about 17Hz
        # trace.filter('lowpass_cheby_2', freq=25)
        trace.decimate(decimation_factor, no_filter=True)

    return stream


def _stream_to_bins(st, bin_len=600):

    fs = 50
    n_points = fs * bin_len

    # internal round up function to get to the first 10 minute period
    def offset_calc(dt, delta):
        offset = (datetime.min - dt) % delta
        return offset

    ddict = {}
    for tr in st:

        # calculate the offset in seconds
        offset = offset_calc(tr.stats.starttime.datetime, timedelta(seconds=bin_len)).total_seconds()

        # In theory we don't need to have the #microseconds=0 but in practice there is some rounding
        # error in obspy which changes the number of microseconds, hence wrecking later intersections
        trans_dict = {wdw.copy().stats.endtime.datetime.replace(microsecond=0): wdw.copy().data[:n_points] for wdw in
                      tr.slide(window_length=bin_len, step=bin_len, offset=offset) if len(wdw.data) > n_points - 1}

        ddict.update(trans_dict)

    return ddict


def _fft_welchs(data):
    """
    A function which applies the fft, and welches method
    in one function to return the PSD data.
    """

    fs = 50
    n = len(data)
    #assert n == 30000, "Not full 10 minute period: {} instead of 30000".format(n)

    #f, pxx_den = signal.welch(data, fs=fs, nperseg=4096, nfft=4096, detrend=False)
    f, pxx_den = signal.welch(data, fs=fs, nperseg=n//28, nfft=n//28, detrend=False)

    return f, pxx_den


def _iqm(df):
    """
    Take the inter-quartile mean
    """
    data = list(df)
    data.sort()
    q1, q2 = np.nanpercentile(data, [25, 75])
    print(q1, q2)
    iqr_data = [item for item in data if q1 < item < q2]

    if len(data) == 1:
        iqm = data[0]
    elif len(data) == 2:
        iqm = statistics.mean(data)
    else:
        try:
            iqm = statistics.mean(iqr_data)
        except statistics.StatisticsError as e:
            helper_logger.error("couldn't compute the IQM, set to NaN", exc_info=e)
            helper_logger.info(data)
            iqm = np.nan
            pass

    return iqm


def _clean_gcfs(gcf_list):
    """
    removes duplicates and ensures they're all gcf files

    :param gcf_list:
    :return out_list:
    """
    out_list = []

    for gcf in gcf_list:
        try:
            if (gcf.endswith(".gcf")) and ("#" not in gcf):
                out_list.append(gcf)

        except Exception as e:
            helper_logger.error("couldn't append gcf {}".format(gcf), exc_info=e)

    return out_list


def _intersect_dicts(dicts):
    """
    intersect
    :param dicts:
    :return:
    """

    intersected_keys = list(reduce(lambda x, y: x & y.keys(), dicts))

    for index, ddict in enumerate(dicts):
        dicts[index] = {ts: ddict[ts] for ts in ddict if ts in intersected_keys}

    return dicts


def _read_folder(path, stream_id):

    output_ts_data_dict = {}

    # get the calibration values
    calval = _get_calval(stream_id)
    gain = _get_gain(stream_id)
    decimation_factor = _get_decimation_factor(stream_id)

    # read the stream, select the correct channel, and apply the calibration factors
    for file in os.listdir(path + "\\" + stream_id):

        # file_type = os.path.splitext(file)[1]
        print(stream_id + ": " + file)

        try:
            stream = obspy.read(path + "\\" + stream_id + "\\" + file)  # , format=(file_type[1:].upper()))
            stream = _select_channel(stream, stream_id)
            stream = _calibrate(stream, calval, gain, decimation_factor)
            #stream = stream.slice(UTCDateTime(2020, 1, 28, 10, 56, 46, 0), UTCDateTime(2020, 1, 28, 10, 56, 56, 0))

            stream = stream.filter('bandpass', freqmin=0.5, freqmax=10)
            # extract the data & timestamps from the stream
            # timestamps = _get_timestamps(stream)
            ts_data_dict = _stream_to_bins(stream, bin_len=60)

            output_ts_data_dict.update(ts_data_dict)

        except Exception as e:
            helper_logger.error("couldn't read file {}".format(path + "\\ " + stream_id + "\\" + file), exc_info=e)
            output_ts_data_dict.update({})

    return output_ts_data_dict


def _date_filter(df):
    """
    Just filters the TimeStamp column between a load of date ranges

    :param df: The current data frame
    :return: The filtered data frame
    """

    date_ranges = [[datetime(2019, 10, 1, 19, 0, 0), datetime(2019, 10, 10, 0, 0, 0)]]

    mask = 0
    for date_range in date_ranges:
        sub_mask = (df["TimeStamp"] > date_range[0]) & (df["TimeStamp"] < date_range[1])
        mask = (mask | sub_mask)

    df = df.loc[mask]

    return df
