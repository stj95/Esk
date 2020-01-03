from obspy.core.utcdatetime import UTCDateTime
from datetime import datetime, timedelta
from scipy import signal
from math import ceil, log2
from scipy import integrate
from functools import reduce
from decs import logit
import pandas as pd
import statistics
import numpy as np
import logging
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

#@logit
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
        logging.error("Couldn't read {} calval, set to 1".format(sensor_id), exc_info=e)
        calval = 1

    return calval

#@logit
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
        logging.error("Couldn't read {} gain, set to 1".format(sensor_id), exc_info=e)
        gain = 1

    return gain

#@logit
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

    if sensor_id in ["Fortis1e2", "Fortis1n2", "Fortis1z2", "Rad1e2", "Rad1n2", "Rad1z2", "Rad2e2", "Rad2n2", "Rad2z2"]:
        decimation_factor = 4
    else:
        decimation_factor = 2

    return decimation_factor

#@logit
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
        logging.error("Couldn't read {} displacement factor, set to 1".format(sensor_id), exc_info=e)
        displacement_factor = 1

    return displacement_factor

#@logit
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

#@logit
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
        trace.split()
        trace.detrend('linear')
        trace.decimate(decimation_factor)

    return stream

#@logit
def _get_timestamps(stream):
    """
    Given a sensor this returns timestamps at 10 minute intervals, this is used as a 'template' to slice
    the actual data stream

    :param stream:
    :return: list
    """

    i_start = stream[0].stats.starttime.datetime.replace(microsecond=0)
    i_mins = i_start.minute
    i_hour = i_start.hour

    # Force start at a ten minute interval
    diff = 10 - (i_mins % 10)
    if i_mins % 10 == 0:
        i_start = i_start.replace(minute=i_mins, second=0)
    elif i_mins > 50:
        i_start = i_start.replace(hour=(i_hour+1), minute=0, second=0)
    else:
        i_start = i_start.replace(minute=(i_mins+diff), second=0)

    # Define start and end point (+ 10 mins each because timestamp is at the end of the interval)
    start = i_start + timedelta(minutes=10)
    end = stream[-1].stats.endtime.datetime.replace(microsecond=0) + timedelta(seconds=1)

    # Split into 10 minute intervals & change to UTCDateTime
    t = np.arange(start, end+timedelta(minutes=10), timedelta(minutes=10)).astype(datetime)
    updateTime = lambda x: UTCDateTime(x)
    newt = list(map(updateTime, t))

    return newt

#@logit
def _stream_to_bins(input_stream, dates):
    """
    Cuts the stream between the list of dates, and outputs the data as lists rather than streams

    :param input_stream:
    :param dates:
    :return: dict{time stamp: data}
    """

    # initialise a dictionary to hold a ten minute time stamp and the corresponding set of stream data
    data_per_bin = {}

    for date in dates:

        # because the SCADA timestamp is always at the end of the interval, we should go back 10 minutes
        stream = input_stream.slice(UTCDateTime(date - timedelta(seconds=599.99)), UTCDateTime(date))
        timestamp = UTCDateTime(date).datetime

        # initialise a bin for a specific 10 minute interval
        new_bin = []
        # remove the data from the 10 minute stream and it to the bin
        for trace in stream:
            for data_point in trace.data:
                new_bin.append(data_point)

        # now add the bin to the list of data_bins, and the corresponding timestamp to the list of timestamps
        # but only if it is a full 10 minute bin, it should be fs * 10 * 60 (except the last bin will have 1 less sample
        # so we also lose one sample off the other 10 min periods for consistency)

        if len(new_bin) == 50*10*60 - 1:
            data_per_bin[timestamp] = new_bin
        elif len(new_bin) == 50*10*60:
            data_per_bin[timestamp] = new_bin[:-1]

    return data_per_bin

#@logit
def _fft_welchs(data):
    """
    A function which applies the fft, and welches method
    in one function to return the PSD data.
    """

    fs = 50
    n = len(data)

    assert n == 30000-1, "Not full 10 minute period: {} instead of 29999".format(n)

    f, pxx_den = signal.welch(data, fs=fs, nperseg=n//28, nfft=2**ceil(log2(abs(n/28))), detrend=False)

    return f, pxx_den

#@logit
def _time_integrate(data, displacement_factor):
    """
    Integrates in the time domain, depending on how many times required to get to displacement
    (displacement_factor)

    This is so bad because of drift, look for an integrator or low pass filter first

    :param stream:
    :param displacement_factor:
    :return:
    """

    for _ in range(int(displacement_factor//2)):
        data = integrate.cumtrapz(data, initial=0)

    return data

#@logit
def _csd_welches(data1, data2):
    """
    calculates the cross spectral density using welches method

    :param data1:
    :param data2:
    :return:
    """

    fs = 50
    n1 = len(data1)
    n2 = len(data2)

    assert n1 == n2, "different length streams: {} vs {}".format(n1, n2)
    assert n1 == 30000-1, "Not full 10 minute period: {} instead of 29999".format(n1)

    f, cxy_den = signal.csd(data1, data2, fs=fs, nperseg=n1//28, nfft=2**ceil(log2(abs(n1/28))), detrend=False)

    return f, cxy_den

#@logit
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
            logging.error("couldn't compute the IQM, set to NaN", exc_info=e)
            logging.info(data)
            iqm = np.nan
            pass

    return iqm

#@logit
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
            logging.error("couldn't append gcf {}".format(gcf), exc_info=e)

    return out_list

#@logit
def _intersect_dicts(dicts):
    """
    intersect
    :param dicts:
    :return:
    """

    intersected_keys = list(reduce(lambda x, y: x & y.keys(), dicts))

    for index, dict in enumerate(dicts):
        dicts[index] = {ts: dict[ts] for ts in dict if ts in intersected_keys}

    return dicts

@logit
def _read_gcf_folder(path, stream_id):

    output_ts_data_dict = {}

    # get the calibration values
    calval = _get_calval(stream_id)
    gain = _get_gain(stream_id)
    decimation_factor = _get_decimation_factor(stream_id)

    # read the stream, select the correct channel, and apply the calibration factors
    for gcf in os.listdir(path + "\\" + stream_id):
        print(stream_id + ": " + gcf)
        try:
            stream = obspy.read(path + "\\" + stream_id + "\\" + gcf)
            stream = _select_channel(stream, stream_id)
            stream = _calibrate(stream, calval, gain, decimation_factor)
            #stream = stream.filter('bandpass', freqmin=0.5, freqmax=10)
            # extract the data & timestamps from the stream
            timestamps = _get_timestamps(stream)
            ts_data_dict = _stream_to_bins(stream, timestamps)

            output_ts_data_dict.update(ts_data_dict)
        except Exception as e:
            print(e)
            output_ts_data_dict.update({})

    return output_ts_data_dict
