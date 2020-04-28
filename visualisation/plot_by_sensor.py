import helpers
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

#matplotlib.rcParams['font.serif'] = 'Palatino'
#matplotlib.rcParams['font.family'] = 'serif'

def plot_by_sensor(csv, direction):

    df = pd.read_csv(csv, index_col=False)
    df = df.loc[df["Sensor"].str.endswith("{}2".format(direction))]
    #df = df.loc[(df["WS_T7fillna"] > 4) & (df["WS_T7fillna"] < 8)]
    #df = helpers.date_filter(df)

    df = df.set_index("Sensor")


    grouped = df.groupby(["Sensor", "Frequency"])["PSD"].agg(helpers.iqm)
    grouped = grouped.reset_index().groupby(["Sensor"])


    fig = plt.figure()

    for key, group in grouped:
        if key not in []:

            x = np.array(group["Frequency"])
            y = np.log10(np.array(group["PSD"]))

            plt.plot(x, y, label=key)

    plt.title("Window length = 2143")
    plt.ylabel("log10(m^2/Hz)")
    plt.xlabel("Frequency (Hz)")
    plt.xlim(0, 15)
    plt.legend()
    plt.show()




if __name__ == "__main__":

    csv = (r"U:\StephenJ\HWU\DataTransfer\DT3 noiseless\control.csv")

    plot_by_sensor(csv, "z")

