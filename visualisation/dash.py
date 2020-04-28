import pandas as pd
import numpy as np
from helpers import iqm

from bokeh.io import output_file, output_notebook
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource
from bokeh.layouts import row, column, gridplot
from bokeh.models.widgets import Tabs, Panel


def bok_csv(csv):

    """
    Arranging data
    """

    df = pd.read_csv(csv)

    # bin the wind speed data & wind direction data
    ws_bins = [i + 0.5 for i in range(0, 21)]
    ws_labels = [i for i in range(1, 21)]

    wd_bins = [30*i for i in range(0, 13)]
    wd_labels = [(30 * i - 15) for i in range(1, 13)]

    df["WS_T7fillna"] = pd.cut(df["WS_T7fillna"], bins=ws_bins, labels=ws_labels)
    df["WD_T7fillna"] = pd.cut(df["WD_T7fillna"], bins=wd_bins, labels=wd_labels)

    aggregated = df.groupby(["Sensor", "WS_T7fillna", "WD_T7fillna", "Frequency"])["PSD"].agg(iqm=iqm)

    grouped = aggregated.groupby(["Sensor", "WS_T7fillna", "WD_T7fillna"], as_index=False)

    for key, group in grouped:
        print(group)

    #print(df)

    output_file('testing.html')

    fig = figure(background_fill_color='gray',
                 background_fill_alpha=0.5,
                 border_fill_color='blue',
                 border_fill_alpha=0.25,
                 plot_height=300,
                 plot_width=500,
                 x_axis_label='Frequency',
                 x_axis_type='linear',
                 x_axis_location='below',
                 x_range=(0.5, 25),
                 y_axis_label='Power',
                 y_axis_type='linear',
                 y_axis_location='left',
                 y_range=(0, 10000),
                 title='Power Spectral Density',
                 title_location='right',
                 toolbar_location='above',
                 tools=['save', 'pan', 'zoom_in', 'zoom_out'])


    for key, group in grouped:
        print(group)

    # remove logo
    fig.toolbar.logo = None

    # show(fig)


if __name__ == "__main__":

    csv = r"U:\StephenJ\26_6-11_7_Testing\19_11_08.csv"

    bok_csv(csv)