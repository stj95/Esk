from datetime import datetime, timedelta
from scipy import signal
from functools import reduce
from logs.exception_logging import create_logger
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


def select_channel(input_stream, sensor):
    """
    selects the traces with the correct channels, depending on the instrument

    :param input_stream:
    :return:
    """
    if sensor.id in ["Fortis1e2", "Fortis1n2", "Fortis1z2", "Rad3e2", "Rad3n2", "Rad3z2"]:
        input_stream = input_stream.select(channel="HH*")
    elif sensor.id in ["Rad1e2", "Rad1n2", "Rad1z2", "Rad2e2", "Rad2n2", "Rad2z2"]:
        input_stream = input_stream.select(channel="HN{}".format(sensor.id[-2].capitalize()))

    return input_stream


def calibrate(stream, sensor):
    """
    Calibrates the stream given a certain calval, detrends and decimates.

    :param stream:
    :param sensor:
    :return: stream
    """

    for trace in stream:
        # set the calibration value
        trace.data = trace.data * sensor.calval / sensor.gain
        # de-trend & decimate to avoid spectral leakage,
        # we can afford to lose all frequencies above 50Hz so we decimate to that point (see Nyquist frequency)
        # trace.split()
        trace.detrend('constant')
        # Butterworth low pass
        trace.filter('lowpass', freq=25)
        # Chebyshev II low pass - this gives a massive roll off - after about 17Hz
        # trace.filter('lowpass_cheby_2', freq=25)
        trace.decimate(int(sensor.decimation_factor), no_filter=True)

    return stream


def stream_to_bins(st, bin_len=600):

    fs = 50
    n_points = fs * bin_len

    # internal round up function to get to the first 10 minute period
    def offset_calc(dt, delta):
        offset_ = (datetime.min - dt) % delta
        return offset_

    def round(dt, roundTo=60):
        if dt == None: dt = datetime.now()
        seconds = (dt.replace(tzinfo=None) - dt.min).seconds
        rounding = (seconds + roundTo/2) // roundTo * roundTo
        return dt + timedelta(0, rounding - seconds, -dt.microsecond)


    ddict = {}
    for tr in st:

        # calculate the offset in seconds
        offset = offset_calc(tr.stats.starttime.datetime, timedelta(seconds=bin_len)).total_seconds()

        # In theory we don't need to have the #microseconds=0 but in practice there is some rounding
        # error in obspy which changes the number of microseconds, hence wrecking later intersections. Since this
        # is well below the precision of the sampling rate it has no effect anyway
        trans_dict = {round(wdw.copy().stats.endtime.datetime): wdw.copy().data[:n_points] for wdw in
                      tr.slide(window_length=bin_len, step=bin_len, offset=offset) if len(wdw.data) > n_points - 1}

        ddict.update(trans_dict)

    return ddict


def fft_welchs(data):
    """
    A function which applies the fft, and welches method
    in one function to return the PSD data.
    """

    fs = 50
    n = len(data)

    # freq, psd = signal.welch(data, fs=fs, nperseg=4096, nfft=4096, detrend=False)
    # freq, psd = signal.welch(data, fs=fs, nperseg=2143, nfft=2143, detrend=False)
    # freq, psd = signal.welch(data, fs=fs, nperseg=n//14, nfft=n//14, detrend=False)
    freq, psd = signal.welch(data, fs=fs, nperseg=n//28, nfft=n//28, detrend=False)

    return freq, psd


def iqm(df):
    """
    Take the inter-quartile mean
    """
    data = list(df)
    data.sort()
    q1, q2 = np.nanpercentile(data, [25, 75])
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
            raise
            pass

    return iqm


def clean_gcfs(gcf_list):
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


def intersect_dicts(dicts):
    """
    This function takes a list of dictionaries and returns the same list but cuts the dictionaries so that only the
    entries corresponding to where the keys intersect are returned.

    In this case the keys are the timestamps of the data and the values are lists of data for the 10 minute period.
    This ensures we are looking only at overlapping data.

    :param dicts:
    :return:
    """

    # give the list of keys which are in all dictionaries
    intersected_keys = list(reduce(lambda x, y: x & y.keys(), dicts))

    # return the set of dictionaries corresponding to intersected keys only
    for index, ddict in enumerate(dicts):
        dicts[index] = {ts: ddict[ts] for ts in ddict if ts in intersected_keys}

    return dicts


def read_folder(path, sensor):

    output_ts_data_dict = {}

    # read the stream, select the correct channel, and apply the calibration factors
    for file in os.listdir(path + "\\" + sensor.id):

        # file_type = os.path.splitext(file)[1]
        print(sensor.id + ": " + file)

        try:
            stream = obspy.read(path + "\\" + sensor.id + "\\" + file)  # , format=(file_type[1:].upper()))
            # stream = select_channel(stream, sensor)
            stream = calibrate(stream, sensor)
            # stream = stream.slice(UTCDateTime(2020, 1, 28, 10, 56, 46, 0), UTCDateTime(2020, 1, 28, 10, 56, 56, 0))
            # if sensor.displacement_factor == 2:
            #     print("velocity")
            # elif sensor.displacement_factor == 4:
            #     print("acceleration")
            #     stream = stream.integrate()
            #     stream = stream.detrend()
            # else:
            #     raise Exception("displacement factor not 2 or 4")

            stream = stream.filter('bandpass', freqmin=0.5, freqmax=8)
            # extract the data & timestamps from the stream
            # timestamps = _get_timestamps(stream)
            ts_data_dict = stream_to_bins(stream, bin_len=60)

            output_ts_data_dict.update(ts_data_dict)

        except Exception as e:
            helper_logger.error("couldn't read file {}".format(path + "\\ " + sensor.id + "\\" + file), exc_info=e)
            output_ts_data_dict.update({})

    return output_ts_data_dict


def date_filter(df):
    """
    Just filters the TimeStamp column between a load of date ranges

    :param df: The current data frame
    :return: The filtered data frame
    """
    df["TimeStamp"] = pd.to_datetime(df["TimeStamp"])
    date_ranges = [[datetime(2020, 2, 6, 3, 41, 0), datetime(2020, 2, 6, 5, 11, 0)]]

    mask = 0
    for date_range in date_ranges:
        sub_mask = (df["TimeStamp"] > date_range[0]) & (df["TimeStamp"] < date_range[1])
        mask = (mask | sub_mask)

    df = df.loc[mask]

    return df
