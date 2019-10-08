import pandas as pd
import numpy as np

"""
############################ 6v71 ################################# 
"""

S_6v71 = pd.DataFrame(columns=["Start", "End", "Quality", "Description"], data=np.array([
    ["2018-12-01 10:00:00", "2018-12-12 00:00:00", "NOT OK", "Not Installed"],
    ["2018-12-19 10:00:00", "2018-12-19 15:00:00", "NOT OK", "Site"],
    ["2019-01-08 11:10:00", "2019-01-08 16:00:00", "NOT OK", "Site"],
    ["2019-01-23 14:50:00", "2019-01-23 16:30:00", "NOT OK", "Site"],
    ["2019-01-24 09:30:00", "2019-01-24 12:30:00", "NOT OK", "Site"],
    ["2019-02-13 11:00:00", "2019-02-13 17:20:00", "NOT OK", "Site"],
    ["2019-02-14 09:30:00", "2019-02-14 17:20:00", "NOT OK", "Site"],
    ["2019-02-19 10:30:00", "2019-02-19 17:30:00", "NOT OK", "Site"],
    ["2019-02-26 12:00:00", "2019-02-26 17:30:00", "NOT OK", "Site"],
    ["2019-02-27 10:00:00", "2019-02-27 17:10:00", "NOT OK", "Site"],
    ["2019-02-28 09:30:00", "2019-02-28 14:00:00", "NOT OK", "Site"],
    ["2019-03-19 11:00:00", "2019-03-19 15:30:00", "NOT OK", "Site"],
    ["2019-03-27 12:30:00", "2019-03-27 19:00:00", "NOT OK", "Site"],
    ["2019-03-28 09:30:00",	"2019-03-28 14:00:00", "NOT OK", "Site"],
    ["2019-04-10 00:00:00",	"2019-04-12 00:00:00", "NOT OK", "Site"], # not refined
    ["2019-04-23 00:00:00",	"2019-04-25 00:00:00", "NOT OK", "Site"], # not refined
    ["2019-05-07 00:00:00",	"2019-05-08 00:00:00", "NOT OK", "Site"], # not refined
    ["2019-05-17 00:00:00",	"2019-05-18 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-05-29 00:00:00", "2019-05-30 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-06-05 00:00:00", "2019-06-07 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-06-19 00:00:00", "2019-06-20 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-06-26 00:00:00", "2019-06-27 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-07-11 00:00:00", "2019-07-12 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-07-19 00:00:00", "2019-07-20 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-07-25 00:00:00", "2019-07-26 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-08-01 00:00:00", "2019-08-02 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-08-08 00:00:00", "2019-08-09 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-08-20 00:00:00", "2019-08-21 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-09-11 00:00:00", "2019-09-12 00:00:00", "NOT OK", "Site"]  # not refined
]))

S_6v71_setup = pd.DataFrame(columns=["Start", "End", "Setup", "Description"], data=np.array([
    ["2018-12-10 00:00:00", "2019-02-14 00:00:00", "Setup 1", "Bucket Installation"],
    ["2019-02-14 00:00:00", "2019-02-28 00:00:00", "setup 2", "2 buckets + 1 bag"],
    ["2019-02-28 00:00:00", "2019-04-24 00:00:00", "Setup 2a", "2 buckets + 1 bag + SP"],
    ["2019-04-24 00:00:00", "2019-06-19 00:00:00", "Setup 3", "2 buckets + 1 bag + sand + SP"],
    ["2019-06-19 00:00:00", "2019-07-29 00:00:00", "Setup 1", "Bucket Installation"]
]))

"""
############################ 6v70 ################################# 
"""

S_6v70 = pd.DataFrame(columns=["Start", "End", "Quality", "Description"], data=np.array([
    ["2018-12-01 10:00:00", "2018-12-12 00:00:00", "NOT OK", "Not Installed"],
    ["2018-12-19 10:00:00", "2018-12-19 15:00:00", "NOT OK", "Site"],
    ["2019-01-08 11:10:00", "2019-01-08 16:00:00", "NOT OK", "Site"],
    ["2019-01-23 14:50:00",	"2019-01-23 16:30:00", "NOT OK", "Site"],
    ["2019-01-24 09:30:00", "2019-01-24 12:30:00", "NOT OK", "Site"],
    ["2019-02-13 11:00:00", "2019-02-13 17:20:00", "NOT OK", "Site"],
    ["2019-02-14 09:30:00", "2019-02-14 17:20:00", "NOT OK", "Site"],
    ["2019-02-19 10:30:00", "2019-02-19 17:30:00", "NOT OK", "Site"],
    ["2019-02-26 12:00:00", "2019-02-26 17:30:00", "NOT OK", "Site"],
    ["2019-02-27 10:00:00", "2019-02-27 17:10:00", "NOT OK", "Site"],
    ["2019-02-28 09:30:00", "2019-02-28 14:00:00", "NOT OK", "Site"],
    ["2019-03-19 11:00:00", "2019-03-19 15:30:00", "NOT OK", "Site"],
    ["2019-03-27 12:30:00", "2019-03-27 19:00:00", "NOT OK", "Site"],
    ["2019-03-28 09:30:00",	"2019-03-28 14:00:00", "NOT OK", "Site"],
    ["2019-04-10 00:00:00",	"2019-04-12 00:00:00", "NOT OK", "Site"], # not refined
    ["2019-04-23 00:00:00",	"2019-04-25 00:00:00", "NOT OK", "Site"], # not refined
    ["2019-05-07 00:00:00", "2019-05-08 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-05-17 00:00:00", "2019-05-18 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-05-29 00:00:00", "2019-05-30 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-06-05 00:00:00", "2019-06-07 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-06-19 00:00:00", "2019-06-20 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-06-26 00:00:00", "2019-06-27 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-07-11 00:00:00", "2019-07-12 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-07-19 00:00:00", "2019-07-20 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-07-25 00:00:00", "2019-07-26 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-08-01 00:00:00", "2019-08-02 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-08-08 00:00:00", "2019-08-09 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-08-20 00:00:00", "2019-08-21 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-09-11 00:00:00", "2019-09-12 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-02-13 11:00:00", "2019-02-27 19:00:00", "PROB OK", "Flooded + poor data"]
]))

S_6v70_setup = pd.DataFrame(columns=["Start", "End", "Setup", "Description"], data=np.array([
    ["2018-12-10 00:00:00", "2019-02-14 00:00:00", "Setup 1", "Bucket Installation"],
    ["2019-02-14 00:00:00", "2019-02-28 00:00:00", "setup 2", "Pipe + 1 bag"],
    ["2019-02-28 00:00:00", "2019-04-24 00:00:00", "Setup 2a", "Pipe + 1 bag + SP"],
    ["2019-04-24 00:00:00", "2019-07-19 00:00:00", "Setup 3", "Pipe + 1 bag + sand + SP"],
    ["2019-07-19 00:00:00", "2019-07-29 00:00:00", "Setup 4", "Short Pipe + 1 bag + sand + SP"]
]))

"""
############################ 6v73 ################################# 
"""

S_6v73 = pd.DataFrame(columns=["Start", "End", "Quality", "Description"], data=np.array([
    ["2018-12-19 10:00:00", "2018-12-19 15:00:00", "NOT OK", "Site"],
    ["2019-01-08 11:10:00", "2019-01-08 16:00:00", "NOT OK", "Site"],
    ["2019-01-23 14:50:00",	"2019-01-23 16:30:00", "NOT OK", "Site"],
    ["2019-01-24 09:30:00", "2019-01-24 12:30:00", "NOT OK", "Site"],
    ["2019-02-12 20:00:00", "2019-02-14 19:00:00", "NOT OK", "Site / Bad Data"],
    ["2019-02-19 10:30:00", "2019-02-19 19:00:00", "NOT OK", "Site"],
    ["2019-02-26 12:00:00", "2019-02-26 17:30:00", "NOT OK", "Site / Bad Data"],
    ["2019-02-27 10:00:00", "2019-02-27 17:10:00", "NOT OK", "Site"],
    ["2019-02-28 09:30:00", "2019-02-28 14:00:00", "NOT OK", "Site"],
    ["2019-04-10 00:00:00",	"2019-04-12 00:00:00", "NOT OK", "Site"], # not refined
    ["2019-04-23 00:00:00",	"2019-04-25 00:00:00", "NOT OK", "Site"], # not refined
    ["2019-05-07 00:00:00", "2019-05-08 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-05-17 00:00:00", "2019-05-18 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-05-29 00:00:00", "2019-05-30 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-06-05 00:00:00", "2019-06-07 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-06-19 00:00:00", "2019-06-20 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-06-26 00:00:00", "2019-06-27 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-07-11 00:00:00", "2019-07-12 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-07-19 00:00:00", "2019-07-20 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-07-25 00:00:00", "2019-07-26 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-08-01 00:00:00", "2019-08-02 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-08-08 00:00:00", "2019-08-09 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-08-20 00:00:00", "2019-08-21 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-09-11 00:00:00", "2019-09-12 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-03-11 18:00:00", "2019-03-28 14:00:00", "NOT OK", "Site / Bad Data (flooded)"]
]))

S_6v73_setup = pd.DataFrame(columns=["Start", "End", "Setup", "Description"], data=np.array([
    ["2018-12-10 00:00:00", "2019-02-14 00:00:00", "Setup 1", "Bucket Installation"],
    ["2019-02-14 00:00:00", "2019-02-19 00:00:00", "Setup 2", "Pipe + 1 bag"],
    ["2019-02-19 00:00:00", "2019-04-11 00:00:00", "Setup 2a", "Pipe + 1 bag + SP"],
    ["2019-04-11 00:00:00", "2019-04-24 00:00:00", "Setup 2b", "Pipe + 4 bags + SP"],
    ["2019-04-11 00:00:00", "2019-07-19 00:00:00", "Setup 3a", "Pipe + 0 bags + Sand + SP"],
    ["2019-07-19 00:00:00", "2019-07-29 00:00:00", "Setup 4", "Short Pipe + 1 bag + sand + SP"]
]))

"""
############################ 6v66 ################################# 
"""

S_6v66 = pd.DataFrame(columns=["Start", "End", "Quality", "Description"], data=np.array([
    ["2018-12-19 10:00:00", "2019-03-19 16:00:00", "NOT OK", "Not Installed / fallen over"],
    ["2019-04-10 00:00:00",	"2019-04-12 00:00:00", "NOT OK", "Site"], # not refined
    ["2019-04-23 00:00:00",	"2019-04-25 00:00:00", "NOT OK", "Site"], # not refined
    ["2019-05-07 00:00:00", "2019-05-08 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-05-17 00:00:00", "2019-05-18 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-05-29 00:00:00", "2019-05-30 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-06-05 00:00:00", "2019-06-07 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-06-19 00:00:00", "2019-06-20 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-06-26 00:00:00", "2019-06-27 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-07-11 00:00:00", "2019-07-12 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-07-19 00:00:00", "2019-07-20 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-07-25 00:00:00", "2019-07-26 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-08-01 00:00:00", "2019-08-02 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-08-08 00:00:00", "2019-08-09 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-08-20 00:00:00", "2019-08-21 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-09-11 00:00:00", "2019-09-12 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-03-19 16:00:00", "2019-03-28 14:00:00", "PROB NOT OK", "PSDs look poor"]
]))

S_6v66_setup = pd.DataFrame(columns=["Start", "End", "Setup", "Description"], data=np.array([
    ["2019-02-28 00:00:00", "2019-04-24 00:00:00", "Setup 2a", "Pipe + 1bag + SP"],
]))

"""
############################ 6v24 ################################# 
"""

S_6v24 = pd.DataFrame(columns=["Start", "End", "Quality", "Description"], data=np.array([
    ["2018-12-19 10:00:00", "2019-04-11 23:30:00", "NOT OK", "Not Installed"],
    ["2019-04-10 00:00:00",	"2019-04-12 00:00:00", "NOT OK", "Site"], # not refined
    ["2019-04-23 00:00:00",	"2019-04-25 00:00:00", "NOT OK", "Site"], # not refined
    ["2019-05-07 00:00:00", "2019-05-08 00:00:00", "NOT OK", "Site"], # not refined
    ["2019-05-17 00:00:00", "2019-05-18 00:00:00", "NOT OK", "Site"], # not refined
    ["2019-05-29 00:00:00", "2019-05-30 00:00:00", "NOT OK", "Site"], # not refined
    ["2019-06-05 00:00:00", "2019-06-07 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-06-19 00:00:00", "2019-06-20 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-06-26 00:00:00", "2019-06-27 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-07-11 00:00:00", "2019-07-12 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-07-19 00:00:00", "2019-07-20 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-07-25 00:00:00", "2019-07-26 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-08-01 00:00:00", "2019-08-02 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-08-08 00:00:00", "2019-08-09 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-08-20 00:00:00", "2019-08-21 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-09-11 00:00:00", "2019-09-12 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-04-11 23:30:00", "2019-04-24 09:00:00", "PROB NOT OK", "Bad Data"],
    ["2019-04-24 18:00:00", "2019-05-07 05:00:00", "PROB OK", "Bad Data"]
]))


S_6v24_setup = pd.DataFrame(columns=["Start", "End", "Setup", "Description"], data=np.array([
    ["2019-04-11 00:00:00", "2019-04-24 00:00:00", "setup 2b", "Pipe + 4 bags + SP + slate"],
    ["2019-04-24 00:00:00", "2019-07-19 00:00:00", "Setup 3", "Pipe + 1 bag + sand + SP"],
    ["2019-07-19 00:00:00", "2019-07-29 00:00:00", "Setup 4", "Short Pipe + 1 bag + sand + SP"]
]))

"""
############################ 6v24 ################################# 
"""

S_6w19 = pd.DataFrame(columns=["Start", "End", "Quality", "Description"], data=np.array([
    ["2019-05-29 00:00:00", "2019-05-30 00:00:00", "NOT OK", "Site"], # not refined
    ["2019-06-05 00:00:00", "2019-06-07 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-06-19 00:00:00", "2019-06-20 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-06-26 00:00:00", "2019-06-27 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-07-11 00:00:00", "2019-07-12 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-07-19 00:00:00", "2019-07-20 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-07-25 00:00:00", "2019-07-26 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-08-01 00:00:00", "2019-08-02 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-08-08 00:00:00", "2019-08-09 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-08-20 00:00:00", "2019-08-21 00:00:00", "NOT OK", "Site"],  # not refined
    ["2019-09-11 00:00:00", "2019-09-12 00:00:00", "NOT OK", "Site"]  # not refined
]))

S_6w19_setup = pd.DataFrame(columns=["Start", "End", "Setup", "Description"], data=np.array([
    ["2019-05-29 00:00:00", "2019-07-19 00:00:00", "Setup 3", "Pipe + 1 bag + sand + SP"],
    ["2019-07-19 00:00:00", "2019-07-29 00:00:00", "Setup 4", "Short Pipe + 1 bag + sand + SP"]
]))

"""
############################ Sensor0 ################################# 
"""

S_Sensor0 = pd.DataFrame(columns = ["Start", "End", "Quality", "Description"])
S_6o35 = pd.DataFrame(columns = ["Start", "End", "Quality", "Description"])

S_Sensor0_setup = pd.DataFrame(columns = ["Start", "End", "Setup", "Description"])
S_6o35_setup = pd.DataFrame(columns = ["Start", "End", "Setup", "Description"])



def read_flags(df):


    # Data Quality DataFrames
    DQFrames = {"6w19": S_6w19, "6v71": S_6v71, "6v70": S_6v70, "6v73": S_6v73,
                "6v66": S_6v66, "6v24": S_6v24, "6o35": S_6o35, "Sensor0_Z": S_Sensor0,
                "Sensor0_N": S_Sensor0, "Sensor0_E": S_Sensor0}
    # setup data frames
    SetUpFrames = {"6w19": S_6w19_setup, "6v24": S_6v24_setup, "6v73": S_6v73_setup,
                   "6v70": S_6v70_setup, "6v71": S_6v71_setup, "6v66": S_6v66_setup, "6o35": S_6o35_setup,
                   "Sensor0_Z": S_Sensor0_setup, "Sensor0_N": S_Sensor0_setup, "Sensor0_E": S_Sensor0_setup}

    """ SPLIT """

    grouped = df.groupby("Sensor", as_index=False)

    """ APPLY """

    output_df = pd.DataFrame()

    for key, group in grouped:

        """ master group df """

        # convert TimeStamps to datetime
        group['TimeStamp'] = pd.to_datetime(group['TimeStamp'])

        """ The DataQuality Dataframe """

        # the data frame we are going to merge into the master group df
        new_df = pd.DataFrame(columns=["TimeStamp", "Quality"])
        new_df_setup = pd.DataFrame(columns=["TimeStamp", "Setup"])

        # the data frame we get the DQ flags
        df = DQFrames[key]
        df_setup = SetUpFrames[key]

        print(df)
        print(df_setup)
        # iterate through the rows and create 10 min time series
        for row in df.iterrows():

            # pad out the times where we are on site etc...
            timeseries = pd.date_range(row[1]["Start"], row[1]["End"], freq='10min', closed='right')
            quality = [row[1]["Quality"]]*len(timeseries)

            data = list(zip(timeseries, quality))
            df_data = pd.DataFrame(data, columns = ['TimeStamp', 'Quality'])

            new_df = new_df.append(df_data)

        for row in df_setup.iterrows():

            # pad out the times where we are on site etc...
            timeseries = pd.date_range(row[1]["Start"], row[1]["End"], freq='10min', closed='right')
            quality = [row[1]["Setup"]] * len(timeseries)

            data = list(zip(timeseries, quality))
            df_data = pd.DataFrame(data, columns=['TimeStamp', 'Setup'])

            new_df_setup = new_df_setup.append(df_data)

        # remove the duplicates (prevents NOT OK data being labeled PROB OK)
        df_nodup = new_df.drop_duplicates(subset = 'TimeStamp')
        df_nodup_setup = new_df_setup.drop_duplicates(subset='TimeStamp')

        group = group.merge(df_nodup, on="TimeStamp", how="left")
        group = group.merge(df_nodup_setup, on="TimeStamp", how="left")

        output_df = output_df.append(group, ignore_index=True)

    return output_df