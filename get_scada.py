# -*- coding: utf-8 -*-

"""
NAME:        Master_CSV_vX.X.py
DESCRIPTION: Merges and concatenates all given PSD data into a master CSV
CREATED:     02/05/2019
AUTHOR:      Liam Schwartz

VERSION:
    - v0.1 (15/05/2019) - Melt (unpivot) sensor data
    - v0.2 (15/05/2019) - Append sensor data
    - v0.3 (06/06/2019) - Changed location to Q: drive
"""

import pandas as pd

def read_scada(scada_path):


    print('\nReading SCADA data')
    df_scada = pd.read_csv(scada_path)
    df_scada.rename(columns = {'PCTimeStamp': 'TimeStamp'}, inplace = True)
    df_scada['TimeStamp'] = pd.to_datetime(df_scada['TimeStamp'], format = '%d/%m/%Y %H:%M')

    df_scada.columns = df_scada.columns.str.rstrip(' (0123456789)')


    print('Calculating site average wind speed')
    df_scada['WS_SiteAvg'] = df_scada[['WTG01_Ambient WindSpeed Avg.', 'WTG03_Ambient WindSpeed Avg.', 'WTG04_Ambient WindSpeed Avg.', 'WTG05_Ambient WindSpeed Avg.', 'WTG07_Ambient WindSpeed Avg.', 'WTG08_Ambient WindSpeed Avg.', 'WTG09_Ambient WindSpeed Avg.', 'WTG11_Ambient WindSpeed Avg.', 'WTG12_Ambient WindSpeed Avg.']].mean(axis = 1)
    df_scada['WS_T7fillna'] = df_scada['WTG07_Ambient WindSpeed Avg.'].fillna(df_scada['WS_SiteAvg'])

    print('Calculating site average wind direction')
    df_scada['WD_SiteAvg'] = df_scada[['WTG01_Ambient WindDir Absolute Avg.', 'WTG03_Ambient WindDir Absolute Avg.', 'WTG04_Ambient WindDir Absolute Avg.', 'WTG05_Ambient WindDir Absolute Avg.', 'WTG07_Ambient WindDir Absolute Avg.', 'WTG08_Ambient WindDir Absolute Avg.', 'WTG09_Ambient WindDir Absolute Avg.', 'WTG11_Ambient WindDir Absolute Avg.', 'WTG12_Ambient WindDir Absolute Avg.']].mean(axis = 1)
    df_scada['WD_T7fillna'] = df_scada['WTG07_Ambient WindDir Absolute Avg.'].fillna(df_scada['WD_SiteAvg'])

    df_scada['Flag_All'] = pd.np.where(((df_scada['WTG01_HourCounters Average Gen1 Avg.'] == 600) &
             (df_scada['WTG03_HourCounters Average Gen1 Avg.'] == 600) &
             (df_scada['WTG04_HourCounters Average Gen1 Avg.'] == 600) &
             (df_scada['WTG05_HourCounters Average Gen1 Avg.'] == 600) &
             (df_scada['WTG07_HourCounters Average Gen1 Avg.'] == 600) &
             (df_scada['WTG08_HourCounters Average Gen1 Avg.'] == 600) &
             (df_scada['WTG09_HourCounters Average Gen1 Avg.'] == 600) &
             (df_scada['WTG11_HourCounters Average Gen1 Avg.'] == 600) &
             (df_scada['WTG12_HourCounters Average Gen1 Avg.'] == 600)), 'All On',
             pd.np.where(((df_scada['WTG01_HourCounters Average Gen1 Avg.'] == 600) &
             (df_scada['WTG03_HourCounters Average Gen1 Avg.'] == 600) &
             (df_scada['WTG04_HourCounters Average Gen1 Avg.'] == 600) &
             (df_scada['WTG05_HourCounters Average Gen1 Avg.'] == 600) &
             ((df_scada['WTG07_HourCounters Average Gen1 Avg.'] == 0 | df_scada['WTG07_HourCounters Average Gen1 Avg.'].isnull())) &
             (df_scada['WTG08_HourCounters Average Gen1 Avg.'] == 600) &
             (df_scada['WTG09_HourCounters Average Gen1 Avg.'] == 600) &
             (df_scada['WTG11_HourCounters Average Gen1 Avg.'] == 600) &
             (df_scada['WTG12_HourCounters Average Gen1 Avg.'] == 600)), 'All But T7',
             pd.np.where((((df_scada['WTG01_HourCounters Average Gen1 Avg.'] == 0) | (df_scada['WTG01_HourCounters Average Gen1 Avg.'].isnull())) &
             ((df_scada['WTG03_HourCounters Average Gen1 Avg.'] == 0) | (df_scada['WTG03_HourCounters Average Gen1 Avg.'].isnull())) &
             ((df_scada['WTG04_HourCounters Average Gen1 Avg.'] == 0) | (df_scada['WTG04_HourCounters Average Gen1 Avg.'].isnull())) &
             ((df_scada['WTG05_HourCounters Average Gen1 Avg.'] == 0) | (df_scada['WTG05_HourCounters Average Gen1 Avg.'].isnull())) &
             (df_scada['WTG07_HourCounters Average Gen1 Avg.'] == 600) &
             ((df_scada['WTG08_HourCounters Average Gen1 Avg.'] == 0) | (df_scada['WTG08_HourCounters Average Gen1 Avg.'].isnull())) &
             ((df_scada['WTG09_HourCounters Average Gen1 Avg.'] == 0) | (df_scada['WTG09_HourCounters Average Gen1 Avg.'].isnull())) &
             ((df_scada['WTG11_HourCounters Average Gen1 Avg.'] == 0) | (df_scada['WTG11_HourCounters Average Gen1 Avg.'].isnull())) &
             ((df_scada['WTG12_HourCounters Average Gen1 Avg.'] == 0) | (df_scada['WTG12_HourCounters Average Gen1 Avg.'].isnull()))), 'T7 Only',
             pd.np.where((((df_scada['WTG01_HourCounters Average Gen1 Avg.'] == 0) | (df_scada['WTG01_HourCounters Average Gen1 Avg.'].isnull())) &
             ((df_scada['WTG03_HourCounters Average Gen1 Avg.'] == 0) | (df_scada['WTG03_HourCounters Average Gen1 Avg.'].isnull())) &
             ((df_scada['WTG04_HourCounters Average Gen1 Avg.'] == 0) | (df_scada['WTG04_HourCounters Average Gen1 Avg.'].isnull())) &
             ((df_scada['WTG05_HourCounters Average Gen1 Avg.'] == 0) | (df_scada['WTG05_HourCounters Average Gen1 Avg.'].isnull())) &
             ((df_scada['WTG07_HourCounters Average Gen1 Avg.'] == 0) | (df_scada['WTG07_HourCounters Average Gen1 Avg.'].isnull())) &
             ((df_scada['WTG08_HourCounters Average Gen1 Avg.'] == 0) | (df_scada['WTG08_HourCounters Average Gen1 Avg.'].isnull())) &
             ((df_scada['WTG09_HourCounters Average Gen1 Avg.'] == 0) | (df_scada['WTG09_HourCounters Average Gen1 Avg.'].isnull())) &
             ((df_scada['WTG11_HourCounters Average Gen1 Avg.'] == 0) | (df_scada['WTG11_HourCounters Average Gen1 Avg.'].isnull())) &
             ((df_scada['WTG12_HourCounters Average Gen1 Avg.'] == 0) | (df_scada['WTG12_HourCounters Average Gen1 Avg.'].isnull()))), 'All Off', 'Other'))))


    df_scada['Flag_String1'] = pd.np.where(((df_scada['WTG01_HourCounters Average Gen1 Avg.'] == 600) &
             (df_scada['WTG03_HourCounters Average Gen1 Avg.'] == 600) &
             (df_scada['WTG04_HourCounters Average Gen1 Avg.'] == 600) &
             (df_scada['WTG05_HourCounters Average Gen1 Avg.'] == 600) &
             (df_scada['WTG07_HourCounters Average Gen1 Avg.'] == 600)), 'All On',
             pd.np.where(((df_scada['WTG01_HourCounters Average Gen1 Avg.'] == 600) &
             (df_scada['WTG03_HourCounters Average Gen1 Avg.'] == 600) &
             (df_scada['WTG04_HourCounters Average Gen1 Avg.'] == 600) &
             (df_scada['WTG05_HourCounters Average Gen1 Avg.'] == 600) &
             ((df_scada['WTG07_HourCounters Average Gen1 Avg.'] == 0 | df_scada['WTG07_HourCounters Average Gen1 Avg.'].isnull()))), 'All But T7',
             pd.np.where((((df_scada['WTG01_HourCounters Average Gen1 Avg.'] == 0) | (df_scada['WTG01_HourCounters Average Gen1 Avg.'].isnull())) &
             ((df_scada['WTG03_HourCounters Average Gen1 Avg.'] == 0) | (df_scada['WTG03_HourCounters Average Gen1 Avg.'].isnull())) &
             ((df_scada['WTG04_HourCounters Average Gen1 Avg.'] == 0) | (df_scada['WTG04_HourCounters Average Gen1 Avg.'].isnull())) &
             ((df_scada['WTG05_HourCounters Average Gen1 Avg.'] == 0) | (df_scada['WTG05_HourCounters Average Gen1 Avg.'].isnull())) &
             (df_scada['WTG07_HourCounters Average Gen1 Avg.'] == 600)), 'T7 Only',
             pd.np.where((((df_scada['WTG01_HourCounters Average Gen1 Avg.'] == 0) | (df_scada['WTG01_HourCounters Average Gen1 Avg.'].isnull())) &
             ((df_scada['WTG03_HourCounters Average Gen1 Avg.'] == 0) | (df_scada['WTG03_HourCounters Average Gen1 Avg.'].isnull())) &
             ((df_scada['WTG04_HourCounters Average Gen1 Avg.'] == 0) | (df_scada['WTG04_HourCounters Average Gen1 Avg.'].isnull())) &
             ((df_scada['WTG05_HourCounters Average Gen1 Avg.'] == 0) | (df_scada['WTG05_HourCounters Average Gen1 Avg.'].isnull())) &
             ((df_scada['WTG07_HourCounters Average Gen1 Avg.'] == 0) | (df_scada['WTG07_HourCounters Average Gen1 Avg.'].isnull()))), 'All Off', 'Other'))))


    df_scada.drop(columns = ['WTG01_Ambient WindSpeed Avg.', 'WTG03_Ambient WindSpeed Avg.', 'WTG04_Ambient WindSpeed Avg.',
                             'WTG05_Ambient WindSpeed Avg.', 'WTG08_Ambient WindSpeed Avg.',
                             'WTG09_Ambient WindSpeed Avg.', 'WTG11_Ambient WindSpeed Avg.', 'WTG12_Ambient WindSpeed Avg.',
                             'WTG01_Ambient WindDir Absolute Avg.', 'WTG03_Ambient WindDir Absolute Avg.', 'WTG04_Ambient WindDir Absolute Avg.',
                             'WTG05_Ambient WindDir Absolute Avg.', 'WTG08_Ambient WindDir Absolute Avg.',
                             'WTG09_Ambient WindDir Absolute Avg.', 'WTG11_Ambient WindDir Absolute Avg.', 'WTG12_Ambient WindDir Absolute Avg.',
                             'WTG01_HourCounters Average Gen1 Avg.', 'WTG03_HourCounters Average Gen1 Avg.', 'WTG04_HourCounters Average Gen1 Avg.',
                             'WTG05_HourCounters Average Gen1 Avg.', 'WTG08_HourCounters Average Gen1 Avg.',
                             'WTG09_HourCounters Average Gen1 Avg.', 'WTG11_HourCounters Average Gen1 Avg.', 'WTG12_HourCounters Average Gen1 Avg.'], inplace = True)

    print('Removing duplicate rows')
    df_scada.drop_duplicates(inplace = True)

    return(df_scada)