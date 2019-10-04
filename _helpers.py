from obspy.core.utcdatetime import UTCDateTime
from datetime import datetime, timedelta
import numpy as np

"""
Helper functions

The general structure for processing the data should be:
    * select sample rates (_select_sample_rates)
    * calibrate the streams (this includes decimation and de-trending) (_calibrate)
    * get the 10 minute interval templates (_get_timestamps)
    * split the data stream into the intervals (_stream_to_bins)
     
"""


def _select_sample_rates(input_stream):
    """
    If there is a 200Hz trace, select it as it must be a radian, otherwise select the 100Hz traces

    :param input_stream:
    :return:
    """

    # make a copy of the stream because obspy
    stream = input_stream.copy()

    # get a list of the sample rates
    sample_rates = [trace.stats.sample_rate for trace in stream]

    # perform logic
    if 200 in sample_rates:
        stream.select(sample_rate=200)
    elif 100 in sample_rates:
        stream.select(sample_rate=100)
    else:
        raise Exception("The stream {} has no traces with sample rate 100, or 200Hz".format(stream))

    return stream


def _calibrate(stream, calval, gain):
    """
    Calibrates the stream given a certain calval

    :param stream:
    :param calval:
    :param gain:
    :return:
    """


    return 0


def _get_timestamps(stream):
    """
    Given a sensor this returns timestamps at 10 minute intervals, this is used as a 'template' to slice
    the actual data stream

    :param stream:
    :return:
    """

    i_start = stream[0].stats.starttime.datetime
    i_mins = i_start.minute
    i_hour = i_start.hour

    # Force start at a ten minute interval
    diff = 10 - (i_mins % 10)
    if i_mins % 10 == 0:
        i_start = i_start.replace(minute=(i_mins+1), second=0)
    elif i_mins > 50:
        i_start = i_start.replace(hour=(i_hour+1), minute=0, second=0)
    else:
        i_start = i_start.replace(minute=(i_mins+diff), second=0)

    # Define start and end point
    start = i_start
    end = stream[-1].stats.endtime.datetime + timedelta(minutes=10)

    # Split into 10 minute intervals & change to UTCDateTime
    t = np.arange(start, end, timedelta(minutes=10)).astype(datetime)
    updateTime = lambda x: UTCDateTime(x)
    newt = list(map(updateTime, t))

    return newt


def _stream_to_bins(input_stream, dates):
    """
    Cuts the stream between the list of dates, and outputs the data as lists rather than streams

    :param input_stream:
    :param dates:
    :return:
    """

    # initialise lists to hold the 10 minute data lists and the corresponding timestamps
    data_bins = []
    timestamps = []

    for date in dates:

        # copy the stream because obspy (unbelievably slow but I cant think of a better way)
        stream = input_stream.copy()

        # because the SCADA timestamp is always at the end of the interval, we should go back 10 minutes
        stream.trim(UTCDateTime(date - timedelta(seconds=599.99)), UTCDateTime(date))
        timestamp = UTCDateTime(date).datetime

        # initialise a bin for a specific 10 minute interval
        bin = []
        # remove the data from the 10 minute stream and it to the bin
        for trace in stream:
            for data_point in trace.data:
                bin.append(data_point)

        # now add the bin to the list of data_bins, and the corresponding timestamp to the list of timestamps
        data_bins.append(bin)
        timestamps.append(timestamp)

        # make sure data_bins isn't empty for debugging purposes
        assert not data_bins == []

    return data_bins, timestamps
