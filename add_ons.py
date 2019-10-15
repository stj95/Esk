from datetime import datetime



def date_filter(df):
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
