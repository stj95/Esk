from multiprocessing import Pool
from logs.exception_logging import create_logger
import pandas as pd
import navigation
import get_scada

log_path = r"U:\StephenJ\Python\Seismometer_Status\GCF_Python\Branch\logs\esk.log"
main_logger = create_logger("main", log_path)

def target(download_folders, sensors, output_path):

    """
    This is the main function, it directs the data flow

    :param download_folders:
    :param sensors:
    :param output_path:
    :return:
    """

    """
    Input variables
    """
    download_folders_path = (r"C:\Users\stephen.jackson\Community Windpower Ltd\Antonios Porpodas - 381 ESK\2. Data")

    scada_path = r"U:\StephenJ\26_6-11_7_Testing\SCADA_20200318.csv"

    arguments = [(download_folders_path, download_folders, sensor) for sensor in sensors]

    """
    Process the data to find the power
    """
    with Pool(processes=4) as p:
        output_df = pd.concat(p.starmap(navigation.psd_download_folder, arguments))

    # output_df = navigation.psd_download_folder(download_folders_path, download_folders, sensors[0])

    """
    Merge additional data
    """
    print("Getting SCADA data")
    scada = get_scada.read_scada(scada_path)
    output_df = output_df.merge(scada, on="TimeStamp", how="left")

    """
    Filter by specific dates
    """
    # print("Date Filtering")
    # output_df = _helpers.date_filter(output_df)

    # output_df = output_df.rename(columns={"Frequency": "Frequency (Hz)"})

    print("writing to file")
    output_df.to_csv(output_path, index=False)

    return 0


if __name__ == "__main__":

    download_folders = ["control data"]
    sensors = ["Fortis1", "Rad1", "Rad2", "Rad3", "Rad4"]
    output_path = r"U:\StephenJ\HWU\DataTransfer\DT3 noiseless\control_my_28.csv"

    target(download_folders, sensors, output_path)
