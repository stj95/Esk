from scipy.integrate import trapz
from matplotlib.lines import Line2D
from datetime import datetime
from helpers import iqm
import matplotlib.pyplot as plt
import numpy as np
import navigation
import sensors

def amplitude(folder_path, sensor, dt1, dt2, style='-'):
    """
    The MOD model works out a speculative 'worst case' power spectrum of a turbine, with this it combines a frequency-
    distance weighting function to give you the power spectrum that you should see at some distance r from the turbine.
    In order for this to be a general model used view the effect of multiple turbines, you cannot
    combine power spectrums, so instead they look a cumulative amplitude which they just define to be the square root
    of the power between frequencies 0.5 - 8. The equation looks like this:

    amp = sqrt( int^8_0.5 ('power spectrum' (k)) dk )

    :param stream:
    :return:
    """

    # psd stream
    df = navigation.psd_sensor_folder(folder_path, sensor)
    mask = ((df["Frequency"] >= 0.5) &
            (df["Frequency"] <= 10) &
            (df["TimeStamp"] >= dt1) &
            (df["TimeStamp"] <= dt2))

    df = df.loc[mask]

    # integrate between 0.5 & 8
    grouped = df.groupby("TimeStamp")

    amps = []
    for key, group in grouped:
        psd = group["PSD"]
        freq = group["Frequency"]
        plt.plot(freq, np.log10(psd), style)
        amp = np.trapz(psd, x=freq)

        amps.append(amp)

    #[plt.axvline(x=a) for a in [0.276*k for k in range(1, 100)]]

    # legend
    custom_lines = [Line2D([0], [0], color='k', linestyle='-', label="Sanquhar On" ),
                    Line2D([0], [0], color='k', linestyle='--', label="Sanquhar Off" )]

    plt.legend(handles=custom_lines)
    plt.xlim(.5, 10)
    plt.ylabel("Displacement PSD (m^2 / Hz)")
    plt.xlabel("Frequency (Hz)")
    plt.show()
    # sqrt
    amps = np.sqrt(amps)
    print(amps)
    avg_amp = iqm(amps)

    return avg_amp


if __name__ == "__main__":

    sensor = sensors.Sensor("Rad2z2")
    folder_path = (r"U:\StephenJ\HWU\mod compare\Rad2z2")

    quiet_dt1 = datetime(2020, 4, 13, 0, 10, 0)
    quiet_dt2 = datetime(2020, 4, 13, 5, 0, 0)

    noisy_dt1 = datetime(2020, 4, 12, 18, 10, 0)
    noisy_dt2 = datetime(2020, 4, 12, 23, 0, 0)

    quiet_amp = amplitude(folder_path, sensor, quiet_dt1, quiet_dt2, style='--')
    noisy_amp = amplitude(folder_path, sensor, noisy_dt1, noisy_dt2)

    print(quiet_amp, noisy_amp)

    print("Difference = {}".format(noisy_amp - quiet_amp))
