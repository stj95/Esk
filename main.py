from multiprocessing import Pool
import pandas as pd
import navigation
import get_scada
import add_flags
import add_ons


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
    download_folders_path = (r"Q:\1 Projects\2 Development\381 Eskdalemuir"
                             r"\5 Technical\5.1 Monitoring Campaign\381-190109-4013")

    scada_path = r"U:\StephenJ\26_6-11_7_Testing\SCADA_20191009.csv"

    arguments = [(download_folders_path, download_folders, sensor) for sensor in sensors]

    """
    Process the data to find the power
    """
    with Pool(processes=4) as p:
        output_df = pd.concat(p.starmap(navigation.psd_download_folder, arguments))


    """
    Merge additional data
    """
    print("Getting SCADA data")
    scada = get_scada.read_scada(scada_path)
    output_df = output_df.merge(scada, on="TimeStamp", how="left")

    print("Adding Flags")
    output_df = add_flags.read_flags(output_df)

    """
    Filter by specific dates
    """
    print("Date Filtering")
    output_df = add_ons.date_filter(output_df)

    output_df = output_df.rename(columns={"Frequency": "Frequency (Hz)"})

    print("writing to file")
    output_df.to_csv(output_path, index=False)

    return 0
